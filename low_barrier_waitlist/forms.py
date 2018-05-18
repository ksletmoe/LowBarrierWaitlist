from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import Length


class CheckIn(FlaskForm):
    hmis = StringField('HMIS ID', validators=[Length(
        min=4, max=10, message='ID must be between 4 and 10')])


class Import(FlaskForm):
    participant_list = FileField(validators=[FileRequired()])
