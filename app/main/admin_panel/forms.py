from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField, IntegerField, StringField


class ChoiseTimeForm(FlaskForm):
    from_field = DateField('From')
    till_field = DateField('Till')

    submit = SubmitField('Execute')

    # def __init__(self, teacher_name):
    #     teacher_name


class GetPaidForm(FlaskForm):
    money = IntegerField('How mutch')
    coment = StringField('Comment')
    date = DateField('Date')
    submit = SubmitField('Submit')
