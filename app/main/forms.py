from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, IntegerField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired

import wtforms
import flask_wtf
from app import db
from app.models.info import Part_Course


class InfoForm(FlaskForm):
    name = wtforms.fields.StringField("Name")
    country = wtforms.fields.StringField("Country")
    date_of_birth = wtforms.fields.DateField('Date of birth')
    phone_number = wtforms.fields.StringField('Phone')
    speed = wtforms.fields.SelectField('Speed', choices=['Slow', 'Fast', 'Super fast'])
    source = wtforms.fields.StringField('Sourse')
    prize = wtforms.fields.IntegerField('Prize')
    submit = wtforms.fields.SubmitField('Submit')

    
class MoreInfo(InfoForm):
    pass


class GraphForm(FlaskForm):
    weekday = wtforms.fields.SelectField('day', choices=['Monday', 'Tuesday', 'Wednessday', 'Thirthday', 'Friday', 'Sartuday', 'Sunday'])
    houer = wtforms.fields.SelectField('hour', choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    minute = wtforms.fields.SelectField('minute', choices=[0, 15, 30, 45])
    submit = wtforms.fields.SubmitField('Submit')


class PartyForm(wtforms.Form):
    ids = wtforms.fields.HiddenField('ids')
    rypma = wtforms.fields.BooleanField('rypma', default=False)
    sympfany = wtforms.fields.BooleanField('sympfany', default=False)
    repeated = wtforms.fields.BooleanField('repeated', default=False)
    proninciation = wtforms.fields.BooleanField('proninciation', default=False)
    reading = wtforms.fields.BooleanField('reading', default=False)


class ProcessForm(FlaskForm):
    parts = wtforms.fields.FieldList(wtforms.fields.FormField(PartyForm))

    submit = wtforms.fields.SubmitField('SUBMIT')

    # def fullfill(self, id):
    #     party = db.session.query(Part_Course).filter(Part_Course.id_course == id).all()
    #
    #     for i in range(80):
    #         self.rypma =