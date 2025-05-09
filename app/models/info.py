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

    speed = db.Column(db.String(120), default="Slow")
    value = db.Column(db.Integer, default=0)
    source = db.Column(db.String(100), default="")
    pay_already = db.Column(db.Float, default=0)
    pass_lesson = db.Column(db.Integer, default=0)
    lessons = db.Column(db.Integer, default=0)

    city = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    activa = db.Column(db.Boolean, default=True)

    lesson = db.relationship('Lesson', backref='lessons', lazy='dynamic')
    teacher = db.relationship('Teacher_To_Student', backref='teacher', lazy='dynamic')
    graphiks = db.relationship('Graficks', backref='graphiks', lazy='dynamic')
    coursess = db.relationship('Cource', backref='cource', lazy='dynamic')
    cash_flow = db.relationship('Cashflows', backref='cashflow', lazy='dynamic')


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

    def get_teacher(self):
        conection = db.session.query(Teacher_To_Student.id_Teacher).filter(Teacher_To_Student.id_Student == self.id).all()
        teacher = []
        for con in conection:
            teacher.append(db.session.query(Info.name).filter(Info.id_user == con.id_Teacher).first().name)
        return teacher

    def to_dick(self):
        data = {
            "id": self.id,
            "name": self.name,
            "lessons": self.lessons,
            "activa": self.activa
        }
        return data


class Lesson(db.Model):
    __tablename__ = 'lessons'
    id = db.Column(db.Integer, primary_key=True, index=True)
    teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    student = db.Column(db.Integer, db.ForeignKey('info.id'))
    prize = db.Column(db.Integer)
    teacher_prize = db.Column(db.Integer)
    datetimes = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, student, teacher, datetimes, prize, teacher_prize):
        self.student = student
        self.teacher = teacher
        self.prize = db.session.query(Info).filter(Info.id == student).first().value
        self.datetimes = datetimes
        self.prize=prize
        self.teacher_prize = teacher_prize

    def teacher_name(self):
        return db.session.query(Info).filter(Info.id_user == self.teacher).first().name

    def student_name(self):
        return db.session.query(Info).filter(Info.id == self.student).first().name

    def daytime_output(self):
        return self.datetimes.strftime("%d.%m.%Y %H:%M")


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
    id_Teacher = db.Column(db.Integer, db.ForeignKey('user.id'))
    key = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    alt_key = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}



class Part_Course(db.Model):
    __tablename__ = 'partcourses'
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_course = db.Column(db.Integer, db.ForeignKey('cource.id'))
    number = db.Column(db.Integer)

    rypma = db.Column(db.DateTime, default=datetime.utcnow())
    repetition = db.Column(db.DateTime, default=datetime.utcnow())
    reading = db.Column(db.DateTime, default=datetime.utcnow())
    speaking = db.Column(db.DateTime, default=datetime.utcnow())
    qetion = db.Column(db.DateTime, default=datetime.utcnow())
    topics = db.Column(db.DateTime, default=datetime.utcnow())
    associations = db.Column(db.DateTime, default=datetime.utcnow())
    assrep = db.Column(db.DateTime, default=datetime.utcnow())
    grammar = db.Column(db.DateTime, default=datetime.utcnow())


class Cource(db.Model):
    __tablename__ = "cource"
    id = db.Column(db.Integer, primary_key=True, index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    to_student = db.Column(db.Integer, db.ForeignKey('info.id'))
    party_course = db.relationship('Part_Course', backref='party', lazy='dynamic')

    def initialization(self):
        set = []
        for i in range(81):
            s = Part_Course(rypma=self.created, repetition=self.created, reading=self.created, speaking=self.created,
                            qetion=self.created, topics=self.created, associations=self.created, grammar=self.created,)
            set.append(Part_Course(number=i, id_course=self.id))

        db.session.add_all(set)


class Cashflows(db.Model):
    __tablename__ = "cashflows"
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_info = db.Column(db.Integer, db.ForeignKey('info.id'))
    sum = db.Column(db.Float)
    lessons = db.Column(db.Integer)
    date = db.Column(db.Date(), default=date.today())
    coment = db.Column(db.String(150))


class BankInfo(db.Model):
    __tablename__ = "bankcarty"
    id = db.Column(db.Integer, primary_key=True, index=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    number = db.Column(db.String(20))
    name_bank = db.Column(db.String(20))