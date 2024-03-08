from app import db
from datetime import datetime, date
from app.models.user import User
from datetime import timedelta

class Info(db.Model):
    __tablename__ = 'info'
    #student
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    country = db.Column(db.String(150))
    date_of_birth = db.Column(db.Date())
    phone_number = db.Column(db.String(20))

    speed = db.Column(db.String(120))
    value = db.Column(db.Integer)
    source = db.Column(db.String(100))
    pay_already = db.Column(db.Integer, default=0)
    pass_lesson = db.Column(db.Integer, default=0)

    finish_lesson = db.Column(db.Integer)
    lesson = db.relationship('Lesson', backref='lessons', lazy='dynamic')
    teacher = db.relationship('Teacher_To_Student', backref='teacher', lazy='dynamic')
    graphiks = db.relationship('Graficks', backref='graphiks', lazy='dynamic')
    coursess = db.relationship('Cource', backref='cource', lazy='dynamic')

    was_pay_for_lesson = db.Column(db.Integer)

    def role(self):
        temp = db.session.query(User).filter(User.id == self.id_user).first()

        if self.id_user:
            temp = temp.role
        else:
            temp = 1

        return temp

    def has_teacher(self):
        if db.session.query(Teacher_To_Student).filter(Teacher_To_Student.id_Student == self.id).first():
            return True
        else:
            return False


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, index=True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.Column(db.Integer, db.ForeignKey('info.id'))
    prize = db.Column(db.Integer)
    datetime = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, student, teacher):
        self.student = student
        self.teacher = teacher
        self.prize = db.session.query(Info).filter(Info.id == student).first().value
        self.datetime = datetime.utcnow()

    def teacher_name(self):
        return db.session.query(Info).filter(Info.id_user == self.teacher).first().name

    def student_name(self):
        return db.session.query(Info).filter(Info.id == self.student).first().name

    def daytime_output(self):
        return self.datetime.strftime("%d.%m.%Y %H:%M")


class Teacher_To_Student(db.Model):
    __tablename__ = 'teacher_to_student'
    id_Teacher = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    id_Student = db.Column(db.Integer, db.ForeignKey('info.id'), primary_key=True)


    def linst_student(self, id_teach):

        return self.query(self.id_Student).filter(Teacher_To_Student.id_Teacher == id_teach).all()


class Graficks(db.Model):
    __tablename__ = 'graficks'
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_user = db.Column(db.Integer, db.ForeignKey('info.id'))
    weekday = db.Column(db.Integer)
    hour = db.Column(db.Integer)
    minute = db.Column(db.Integer)
    key = {'Monday': 0, 'Tuesday': 1, 'Wednessday': 2, 'Thirthday': 3, 'Friday': 4, 'Sartuday': 5, 'Sunday': 6}
    alt_key = {0: 'Monday', 1: 'Tuesday', 2: 'Wednessday', 3: 'Thirthday', 4: 'Friday', 5: 'Sartuday', 6: 'Sunday'}


class Part_Course(db.Model):
    __tablename__ = 'partcourses'
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_course = db.Column(db.Integer, db.ForeignKey('cource.id'))
    number = db.Column(db.Integer)

    rypma = db.Column(db.DateTime, default=datetime.utcnow())
    sympfany = db.Column(db.DateTime, default=datetime.utcnow())
    repeated = db.Column(db.DateTime, default=datetime.utcnow())
    proninciation = db.Column(db.DateTime, default=datetime.utcnow())
    speacking = db.Column(db.DateTime, default=datetime.utcnow())


class Cource(db.Model):
    __tablename__ = "cource"
    id = db.Column(db.Integer, primary_key=True, index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    to_student = db.Column(db.Integer, db.ForeignKey('info.id'))
    party_course = db.relationship('Part_Course', backref='party', lazy='dynamic')

    def initialization(self):
        set = []
        for i in range(81):
            s = Part_Course(rypma=self.created, sympfany=self.created, repeated=self.created,
                            proninciation=self.created, speacking=self.created)
            set.append(Part_Course(number=i, id_course=self.id))

        db.session.add_all(set)
