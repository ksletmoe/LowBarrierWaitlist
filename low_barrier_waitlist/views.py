from . import app


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/confirm', methods=['GET'])
def confirm_get():
    return 'Confirm'


@app.route('/confirm', methods=['POST'])
def confirm_post():
    pass


@app.route('/deny', methods=['GET'])
def deny():
    return 'deny'


@app.route('/admin', methods=['GET'])
def admin_get():
    return 'admin'


@app.route('/admin', methods=['POST'])
def admin_post():
    pass
