from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_login import current_user
from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField('Stay in system?')
    submit = SubmitField("Authoraze")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat_Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField("Register")

    def validate_email(self, mail):
        user = User.query.filter_by(email=mail.data).first()
        if user is not None:
            raise ValidationError("This Email is alredy okupase. Please, chose another mail.")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')
