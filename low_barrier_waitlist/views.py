from flask import redirect, abort
from . import app
from . import forms
from . import persistence


@app.route('/', methods=('POST', 'GET'))
def hello_world():
    form = forms.CheckIn()
    if form.validate_on_submit():
        participant = persistence.getParticipant(form.id)
        if participant:
            participant.check_in()

            if persistence.updateParticipant(participant):
                return redirect('/confirm')
            else:
                abort(500)
        else:
            return redirect('/deny')


@app.route('/confirm', methods=('GET', 'POST'))
def confirm():
    return 'Confirm'


@app.route('/deny')
def deny():
    return 'deny'


@app.route('/admin', methods=('GET', 'POST'))
def admin():
    return 'admin'


@app.route('/admin/login', methods=('GET', 'POST'))
def login():
    return 'login'


@app.route('/admin/logout', methods=['POST'])
def logout():
    # TODO: actually do this
    redirect('/')


@app.route('/admin/import', methods=('GET', 'POST'))
def import_participants():
    return 'add client'


@app.route('/admin/assign_bed/<hmis_id>', methods=['POST'])
def assign_bed(hmis_id):
    pass
