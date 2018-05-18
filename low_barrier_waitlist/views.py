import flask
from . import app
from . import forms
from . import persistence
from . import mongo


@app.route('/', methods=('POST', 'GET'))
def hello_world():
    form = forms.CheckIn()
    if form.validate_on_submit():
        participant = persistence.get_participant(mongo.db, form.hmis)
        if participant:
            participant.check_in()

            if persistence.update_participant(mongo.db, participant):
                return flask.redirect('/confirm')
            else:
                flask.abort(500)
        else:
            return flask.redirect('/registration_required')

    return flask.render_template('index.html', form=form)


@app.route('/confirm', methods=('GET', 'POST'))
def confirm():
    return 'Confirm'


@app.route('/registration_required')
def registration_required():
    return flask.render_template('registration_required.html')


@app.route('/admin', methods=('GET', 'POST'))
def admin():
    return 'admin'


@app.route('/admin/login', methods=('GET', 'POST'))
def login():
    return 'login'


@app.route('/admin/logout', methods=['POST'])
def logout():
    # TODO: actually do this
    flask.redirect('/')


@app.route('/admin/import', methods=('GET', 'POST'))
def import_participants():
    pass


@app.route('/admin/assign_bed/<hmis_id>', methods=['POST'])
def assign_bed(hmis_id):
    pass

@app.route('/about', methods=['GET'])
def about_page():
    return flask.render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact_page():
    return flask.render_template('contact.html')
