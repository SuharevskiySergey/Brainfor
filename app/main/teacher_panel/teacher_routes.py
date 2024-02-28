from app.main import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for
#models
from app.models.info import Info
from app.models.user import User
from app.models.info import Lesson, Teacher_To_Student


@bp.route('/teacher_panel')
@login_required
def teacher_panel():

    temp = db.session.query(Teacher_To_Student.id_Student).filter(Teacher_To_Student.id_Teacher == current_user.id).all()

    liste = []
    for i in temp:
        liste.append(i[0])

    student = db.session.query(Info).filter(Info.id.in_(liste)).all()

    return render_template('teachers_panel/teachers_panel_main.html', student=student)


@bp.route('/create_lesson/<int:stud>')
def create_lesson(stud):
    if current_user.role < 2:
        redirect(url_for('main.index'))

    les = Lesson(student=stud, teacher=current_user.id)
    db.session.add(les)
    db.session.commit()
    return redirect(url_for('main.teacher_panel'))


@bp.route('/del_teach/<int:stud>/<int:teach>', methods=['GET', 'POST', 'PUT'])
def del_teacher(stud, teach):
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    i = db.session.query(Teacher_To_Student).filter(Teacher_To_Student.id_Student == stud, Teacher_To_Student.id_Teacher == teach).first()
    print(i)
    db.session.delete(i)

    db.session.commit()
    return redirect(url_for('main.information', id=stud))


@bp.route('/add_teacher/<int:teach>/<int:id>')
def add_teach_to_student(teach, id):

    if current_user.role < 3:
        return redirect(url_for('main.index'))

    toadd = Teacher_To_Student(id_Teacher=teach, id_Student=id)
    db.session.add(toadd)
    db.session.commit()

    return redirect(url_for('main.information', id=id))


@bp.route('/chouse_teacher/<int:id>')
@login_required
def chouse_teacher(id):
    if current_user.role < 2:
        return redirect(url_for('main.index'))

    teachers = db.session.query(User, Info).filter(User.role > 1).join(Info).all()

    return render_template('teachers_panel/chouse_teacher.html', teachers=teachers, id=id)


@bp.route('/setup_lesson/')
@login_required
def setup_lesson():
    return render_template('main/setap_lesson.html')