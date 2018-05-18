from . import app
from flask import redirect
from . import forms


@app.route('/', methods=('POST', 'GET'))
def hello_world():
    form = forms.CheckIn()
    if form.validate_on_submit():
        form.id
        return redirect('confirm')
    else:
        return redirect('deny')


@app.route('/confirm')
def confirm_get():
    return 'Confirm'


@app.route('/confirm', methods=['POST'])
def confirm_post():
    pass


@app.route('/deny')
def deny():
    return 'deny'


@app.route('/admin')
def admin_get():
    return 'admin'


@app.route('/admin', methods=['POST'])
def admin_post():
    pass


@app.route('/login')
def login_get():
    return 'login'


@app.route('/login', methods=['POST'])
def login_post():
    pass


@app.route('/logout', methods=['POST'])
def logout():
    pass


@app.route('/add_client')
def add_client_get():
    return 'add client'


@app.route('/add_client', methods=['POST'])
def add_client_post():
    pass


@app.route('/assign_bed', methods=['POST'])
def assign_bed():
    pass
