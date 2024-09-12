from app.main import bp
from app import db
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, flash
from datetime import datetime, timedelta

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

    student = db.session.query(Info).filter(Info.id.in_(liste)).filter(Info.activa).all()

    return render_template('teachers_panel/teachers_panel_main.html', student=student)


@bp.route('/create_lesson/<int:graphid>', methods=['POST'])
def create_lesson_post(graphid):
    form = ProcessForm()
    graph = db.session.query(Graficks).filter(Graficks.id == graphid).first()
    course = db.session.query(Cource).filter(Cource.to_student == graph.id_user).first()
    party = db.session.query(Part_Course).filter(Part_Course.id_course == course.id).order_by(Part_Course.number).all()

    if db.session.query(Info).filter(graph.id_user == Info.id).first().activa == False:
        flash('This student not active')
        return redirect(url_for("main.index"))

    if form.validate_on_submit():


        get_parts = form.parts.data
        today = datetime.utcnow()
        delta = timedelta(days=today.weekday() - graph.weekday,
                          hours=today.hour - graph.hour,
                          minutes=today.minute - graph.minute,
                          seconds=today.second,
                          microseconds=today.microsecond)

        if db.session.query(Lesson).filter(Lesson.teacher == current_user.id).filter(Lesson.student == graph.id_user).filter(Lesson.datetimes == today - delta).first():
            flash('this lesson is alredy exist')
            return redirect(url_for('main.information'))

        parts = []
        for j in range(80):
            number = j
            if party[j].rypma != party[80].rypma:
                rypma = (True)
            else:
                rypma = (False)

            if party[j].repetition != party[80].repetition:
                repetition = (True)
            else:
                repetition = (False)

            if party[j].reading != party[80].reading:
                reading = (True)
            else:
                reading = (False)

            if party[j].speaking != party[80].speaking:
                speaking = (True)
            else:
                speaking = (False)

            if party[j].qetion != party[80].qetion:
                qetion = (True)
            else:
                qetion = (False)

            if party[j].topics != party[80].topics:
                topics = (True)
            else:
                topics = (False)

            if party[j].associations != party[80].associations:
                associations = (True)
            else:
                associations = (False)

            if party[j].grammar != party[80].grammar:
                grammar = (True)
            else:
                grammar = (False)

            parts.append({'rypma': rypma, 'repetition': repetition, 'reading': reading, 'speaking': speaking,
                          'qetion': qetion, 'topics': topics, 'associations': associations, 'grammar': grammar,
                          'number': number})



        for i in range(80):

            if get_parts[i]['rypma'] != parts[i]['rypma']:
                if get_parts[i]['rypma']:
                    party[i].rypma = today - delta
                else:
                    party[i].rypma = party[80].rypma

            if get_parts[i]['repetition'] != parts[i]['repetition']:
                if get_parts[i]['repetition']:
                    party[i].repetition = today - delta
                else:
                    party[i].repetition = party[80].repetition

            if get_parts[i]['reading'] != parts[i]['reading']:
                if get_parts[i]['reading']:
                    party[i].reading = today - delta
                else:
                    party[i].reading = party[80].reading

            if get_parts[i]['speaking'] != parts[i]['speaking']:
                if get_parts[i]['speaking']:
                    party[i].speaking = today - delta
                else:
                    party[i].speaking = party[80].speaking

            if get_parts[i]['qetion'] != parts[i]['qetion']:
                if get_parts[i]['qetion']:
                    party[i].qetion = today - delta
                else:
                    party[i].qetion = party[80].qetion

            if get_parts[i]['topics'] != parts[i]['topics']:
                if get_parts[i]['topics']:
                    party[i].topics = today - delta
                else:
                    party[i].topics = party[80].topics

            if get_parts[i]['associations'] != parts[i]['associations']:
                if get_parts[i]['associations']:
                    party[i].associations = today - delta
                else:
                    party[i].associations = party[80].associations

            if get_parts[i]['grammar'] != parts[i]['grammar']:
                if get_parts[i]['grammar']:
                    party[i].grammar = today - delta
                else:
                    party[i].grammar = party[80].grammar


        db.session.add_all(party)
        t_prize = db.session.query(Info.value).filter(Info.id_user == current_user.id).first().value or 0
        lesson = Lesson(student=graph.id_user,
                        teacher=current_user.id,
                        datetimes=today - delta,
                        prize=db.session.query(Info).filter(Info.id == graph.id_user).first().value,
                        teacher_prize=t_prize)
        stud = db.session.query(Info).filter(Info.id == graph.id_user).first()
        stud.pay_already = stud.pay_already - stud.value
        stud.pass_lesson += 1
        db.session.add(stud)

        db.session.add(lesson)
        db.session.commit()

        return redirect(url_for('main.information'))
    else:
        pass
    return redirect(url_for('main.information',))


@bp.route('/create_lesson/<int:graphid>',
#          methods=['GET', 'POST']
          )
def create_lesson_get(graphid):
    if current_user.role < 2:
        redirect(url_for('main.index'))

    graph = db.session.query(Graficks).filter(Graficks.id == graphid).first()
    if db.session.query(Info).filter(graph.id_user == Info.id).first().activa == False:
        flash('This student not active')
        return redirect(url_for("main.index"))
    course = db.session.query(Cource).filter(Cource.to_student == graph.id_user).first()
    party = db.session.query(Part_Course).filter(Part_Course.id_course == course.id).order_by(Part_Course.number).all()
    form = ProcessForm()
    parts = []
    for j in range(80):
        number = str(j+1)

        if party[j].rypma != party[80].rypma:
            rypma = (True)
        else:
            rypma = (False)

        if party[j].repetition == party[80].repetition:
            repetition = (False)
        else:
            repetition = (True)

        if party[j].reading == party[80].reading:
            reading = (False)
        else:
            reading = (True)

        if party[j].speaking == party[80].speaking:
            speaking = (False)
        else:
            speaking = (True)

        if party[j].qetion == party[80].qetion:
            qetion = (False)
        else:
            qetion = (True)

        if party[j].topics == party[80].topics:
            topics = (False)
        else:
            topics = (True)

        if party[j].associations == party[80].associations:
            associations = (False)
        else:
            associations = (True)

        if party[j].grammar == party[80].grammar:
            grammar = (False)
        else:
            grammar = (True)


        parts.append({'ids': j+1,  'rypma': rypma, 'repetition': repetition, 'reading': reading, 'speaking': speaking,
                      'qetion': qetion, 'topics': topics, 'associations': associations, 'grammar': grammar})

    form.process(data={'parts': parts})

    return render_template('teachers_panel/add_lesson.html', form=form)


@bp.route('/del_teach/<int:stud>/<int:teach>', methods=['GET', 'POST', 'PUT'])
def del_teacher(stud, teach):
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    i = db.session.query(Teacher_To_Student).filter(Teacher_To_Student.id_Student == stud, Teacher_To_Student.id_Teacher == teach).first()
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