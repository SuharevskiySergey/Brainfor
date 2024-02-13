from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired


class InfoForm(FlaskForm):
    name = StringField("Name")
    country = StringField("Country")
    date_of_birth = DateField('Date of birth')
    phone_number = StringField('Phone')
    speed = StringField('Speed')
    source = StringField('Sourse')
    prize = IntegerField('Prize')
    submit = SubmitField('Submit')

    
class MoreInfo(InfoForm):
    pass


class GraphForm(FlaskForm):
    weekday = SelectField('day', choices=['Monday', 'Tuesday', 'Wednessday', 'Thirthday', 'Friday', 'Sartuday', 'Sunday'])
    houer = SelectField('hour', choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    minute = SelectField('minute', choices=[0, 15, 30, 45])
    submit = SubmitField('Submit')
