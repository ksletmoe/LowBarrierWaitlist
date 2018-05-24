import flask
import json
from . import app
from . import forms
from . import persistence
from . import mongo
from .importer.data_importer import DataImporter
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=('POST', 'GET'))
def root():
    form = forms.CheckIn()
    if form.validate_on_submit():
        participant = persistence.get_participant(mongo.db, form.hmis.data)
        if participant:
            participant.assigned_bed = False
            participant.check_in()

            if persistence.update_participant(mongo.db, participant, persistence.get_checkin_attributes()):
                return flask.redirect('/confirmed/{}'.format(participant.hmis))
            else:
                flask.abort(500)
        else:
            return flask.redirect('/registration_required')

    return flask.render_template('index.html', form=form)


@app.route('/confirmed/<hmis_id>')
def confirm(hmis_id):
    return flask.render_template('confirmed.html', hmis_id=hmis_id)


@app.route('/registration_required')
def registration_required():
    return flask.render_template('registration_required.html')


@app.route('/admin')
def admin():
    ranked_participants = persistence.get_recent_participants(mongo.db)
    return flask.render_template('admin.html', ranked_participants=ranked_participants)


@app.route('/admin/login', methods=('GET', 'POST'))
def login():
    return 'login'


@app.route('/admin/logout', methods=['POST'])
def logout():
    # TODO: actually do this
    flask.redirect('/')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/admin/import', methods=('GET', 'POST'))
def import_participants():
    form = forms.Import()
    if form.validate_on_submit():
        f = form.participant_list.data
        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(local_path)
            importer = DataImporter()
            importer.parse_input_file(local_path)
            participants = importer.get_participants()
            for p in participants:
                persistence.update_participant(mongo.db, p, persistence.get_import_attributes())
            return flask.render_template('/import_successful.html', participant_count=len(participants))
        else:
            flask.abort(422)
    return flask.render_template('/admin_import.html', form=form)


@app.route('/admin/assign_bed/<hmis_id>', methods=['POST'])
def assign_bed(hmis_id):
    participant = persistence.get_participant(hmis_id)
    if participant:
        participant.go_to_bed()
        if persistence.update_participant(mongo.db, participant, ['has_bed']):
            return json.dumps({'success': True}), 200, {'Content-Type': 'application/json'}
        else:
            flask.abort(500)
    else:
        flask.abort(400)


@app.route('/about', methods=['GET'])
def about_page():
    return flask.render_template('about.html')


@app.route('/contact', methods=['GET'])
def contact_page():
    return flask.render_template('contact.html')
