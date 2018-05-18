from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class CheckIn(FlaskForm):
    name = StringField('hmis', validators=[Length(
        min=4, max=10, message='ID must be between 4 and 10')])
