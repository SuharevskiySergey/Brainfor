from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app
from time import time


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    __tablenamme__ = 'user'
    id = db.Column(db.Integer, primary_key=True, index =True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=1)  # 1 - Student, 2 - teacher, 3-admin, 4 sudou
    info = db.relationship('Info', backref='info', lazy='dynamic')
    lesson = db.relationship('Lesson', backref='lesson', lazy='dynamic')
    student = db.relationship('Teacher_To_Student', backref='student', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        s = jwt.encode(
            {'reset_password': self.id, 'exp': time()+expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        print(s)
        return s

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)