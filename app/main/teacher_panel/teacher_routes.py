from app.main import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request
#models
from app.models.info import Info
from app.models.user import User
from app.models.info import Lesson, Teacher_To_Student
from app.models.info import Cource, Part_Course, Graficks
from app.main.forms import ProcessForm

@bp.route('/teacher_panel')
@login_required
def teacher_panel():

    temp = db.session.query(Teacher_To_Student.id_Student).filter(Teacher_To_Student.id_Teacher == current_user.id).all()

    liste = []
    for i in temp:
        liste.append(i[0])

    student = db.session.query(Info).filter(Info.id.in_(liste)).all()

    return render_template('teachers_panel/teachers_panel_main.html', student=student)


@bp.route('/create_lesson/<int:graphid>', methods=['POST'])
def create_lesson_post(graphid):
    form = ProcessForm()
    graph = db.session.query(Graficks).filter(Graficks.id == graphid).first()
    course = db.session.query(Cource).filter(Cource.to_student == graph.id_user).first()
    party = db.session.query(Part_Course).filter(Part_Course.id_course == course.id).order_by(Part_Course.number).all()

    parts =[]
    for j in range(80):
        number = j+1
        if party[j].rypma != party[80].rypma:
            rypma = (True)
        else:
            rypma = (False)

        if party[j].sympfany == party[80].sympfany:
            sympfany = (False)
        else:
            sympfany = (True)

        if party[j].repeated == party[80].repeated:
            repeated = (False)
        else:
            repeated = (True)
        if party[j].proninciation == party[80].proninciation:
            proninciation = (False)
        else:
            proninciation = (True)
        if party[j].speacking == party[80].speacking:
            reading = (False)
        else:
            reading = (True)

        parts.append({'rypma': rypma, 'sympfany': sympfany, 'repeated': repeated, 'proninciation': proninciation,
                            'reading': reading, 'number': number})

    if form.validate_on_submit():
        print('#')
        return redirect(url_for('main.information'))
    print('!')
    return redirect(url_for('main.information',))


@bp.route('/create_lesson/<int:graphid>',
#          methods=['GET', 'POST']
          )
def create_lesson_get(graphid):
    if current_user.role < 2:
        redirect(url_for('main.index'))


    graph = db.session.query(Graficks).filter(Graficks.id == graphid).first()
    course = db.session.query(Cource).filter(Cource.to_student == graph.id_user).first()
    party = db.session.query(Part_Course).filter(Part_Course.id_course == course.id).order_by(Part_Course.number).all()
    form = ProcessForm()
    # les = Lesson(student=stud, teacher=current_user.id)
    # db.session.add(les)
    # db.session.commit()

    # if form.validate_on_submit():
    #
    #     print('#')
    #     return redirect(url_for('main.create_lesson_get', graphid=graphid))

    parts = []
    for j in range(80):
        number = j+1
        if party[j].rypma != party[80].rypma:
            rypma = (True)
        else:
            rypma = (False)

        if party[j].sympfany == party[80].sympfany:
            sympfany = (False)
        else:
            sympfany = (True)

        if party[j].repeated == party[80].repeated:
            repeated = (False)
        else:
            repeated = (True)
        if party[j].proninciation == party[80].proninciation:
            proninciation = (False)
        else:
            proninciation = (True)
        if party[j].speacking == party[80].speacking:
            reading = (False)
        else:
            reading = (True)

        parts.append({'rypma': rypma, 'sympfany': sympfany, 'repeated': repeated, 'proninciation': proninciation,
                            'reading': reading, 'number': number})

    form.process(data={'parts': parts})
    # for i in range(5):
    #     form.rypma.append_entry(True)
    #     form.sympfany.append_entry()
    #     form.repeated.append_entry()
    #     form.proninciation.append_entry()
    #     form.reading.append_entry()

    return render_template('teachers_panel/add_lesson.html', form=form)



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
