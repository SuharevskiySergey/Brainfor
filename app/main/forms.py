from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, IntegerField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired
import wtforms
from app import db
from app.models.info import Part_Course


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

class PartyForm(FlaskForm):
    rypma = wtforms.fields.BooleanField('rypma')
    sympfany = wtforms.fields.BooleanField('sympfany')
    repeated = wtforms.fields.BooleanField('repeated')
    proninciation = wtforms.fields.BooleanField('proninciation')
    reading = wtforms.fields.BooleanField('reading')


class ProcessForm(FlaskForm):
    parts = wtforms.fields.FieldList(wtforms.fields.FormField(PartyForm))

    submit = wtforms.fields.SubmitField('Submit')

    # def fullfill(self, id):
    #     party = db.session.query(Part_Course).filter(Part_Course.id_course == id).all()
    #
    #     for i in range(80):
    #         self.rypma =