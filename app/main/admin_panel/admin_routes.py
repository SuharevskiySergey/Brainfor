from app.main import bp
from app import db, login
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from app.models.info import Info
from app.models.user import User
from app.main.forms import InfoForm
from app.models.info import Cource
from app.models.info import Graficks
from app.models.info import Cashflows
from app.main.admin_panel.forms import ChoiseTimeForm
from datetime import datetime, timedelta
from app.models.info import Lesson, Cashflows
from app.main.admin_panel.forms import GetPaidForm



@bp.route('/admin_panel_teachers')
@login_required
def admin_panel_teachers():
    if current_user.role < 2:
        return redirect(url_for('main.index'))
    teach = db.session.query(User.id).filter(User.role == 2).all()
    teach_id = []
    for i in teach:
        teach_id.append(i.id)
    infos = db.session.query(Info).filter(Info.id_user.in_(teach_id)).order_by(Info.id_user).all()

    return render_template('admin_panel/admin_teachers.html', infos=infos)


@bp.route('/admin_panel_main')
@login_required
def admin_panel_main():
    if current_user.role < 2:
        return redirect(url_for('main.index'))

    infose = db.session.query(Info).filter(Info.id_user == None).filter(Info.activa == True).order_by(Info.id).all()
    infos = []
    s = 0
    for info in infose:
        graph = db.session.query(Graficks).filter(Graficks.id_user== info.id).all()
        s += 1
        infos.append([info, graph, s])


    return render_template('admin_panel/admin_panel_main.html', infos=infos)


@bp.route('/add_new', methods=['GET', 'POST'])
@login_required
def add_new():
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    id = request.args.get('id', 0, type=int)

    form = InfoForm()
    if id != 0:
        info = db.session.query(Info).filter(Info.id == id)
        # teacer info + admin info

        form.name.data = info.name
        form.country.data = info.country
        form.date_of_birth.data = info.date_of_birth
        form.phone_number.data = info.phone_number

    if form.validate_on_submit():
        info = Info(name=form.name.data, date_of_birth=form.date_of_birth.data, country=form.country.data,
                    phone_number=form.phone_number.data, speed=form.speed.data, source=form.source.data,
                    value=form.prize.data, occupation=form.occupation.data, city=form.city.data)


        db.session.add(info)
        db.session.commit()
        course = Cource(to_student=info.id)
        db.session.add(course)
        db.session.commit()
        course.initialization()
        db.session.commit()
        return redirect(url_for('main.admin_panel_main'))

    return render_template('admin_panel/student_page.html', form=form)


@bp.route('/admin_users')
@login_required
def admin_users():
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    users_info = db.session.query(User, Info).join(Info).all()
        #(Info).filter(User.role < current_user.role).all()

    return render_template('admin_panel/admin_users.html', users_info=users_info)


@bp.route("/make_teacher<int:id>")
@login_required
def make_teacher(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    teach = db.session.query(User).filter(User.id == id).first()
    teach.role = 2
    db.session.add(teach)
    db.session.commit()
    return redirect(url_for('main.admin_users'))

@bp.route("/make_admin<int:id>")
@login_required
def make_admin(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    admin = db.session.query(User).filter(User.id == id).first()
    admin.role = 3
    db.session.add(admin)
    db.session.commit()
    return redirect(url_for('main.admin_users'))


@bp.route('/admin_user/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_user(id):
    user = db.session.query(User, Info).join(Info).filter_by(User.id == id).first()
    form = user

@bp.route('/temp')
@login_required
def temp():
    s = [2, 5, 6, 9]
    for i in s:
        course = Cource(to_student=i)
        db.session.add(course)
        db.session.commit()
        course = db.session.query(Cource).filter(Cource.to_student == i).first()
        course.initialization()
        db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/sudo_graph')
@login_required
def sudo_graph():
    role = request.args.get('role', 'student', type=str)
    graph = db.session.query(Graficks, Info)\
        .order_by(Graficks.weekday)\
        .order_by(Graficks.hour)\
        .order_by(Graficks.minute).join(Info).all()

    teacher_id = [i.id for i in db.session.query(User.id).filter(User.role >= 2).all()]
    teacher_info = db.session.query(Info).filter(Info.id_user.in_(teacher_id)).all()

    to_total = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, 6: {}, 7: {}}
    day = graph[0].Graficks.weekday
    to_total[0] = {i.name: 0 for i in teacher_info}
    to_total[0]['Total '] = 0
    for g in graph:
        if day < g.Graficks.weekday:
            day = g.Graficks.weekday
            to_total[day] = {i.name: 0 for i in teacher_info}
            to_total[day]['Total '] = 0

        if role == 'student':
            if not g.Info.id_user:
                for teac in g.Info.get_teacher():
                    to_total[day][teac] += 1
                    to_total[day]['Total '] += 1
            else:
                continue

        if role == 'teacher':
            if g.Info.id_user:
                to_total[day][g.Info.name] += 1

    return render_template('admin_panel/sudo_graph.html', graph=graph, les=len(graph), rolee=role, to_total=to_total)


@bp.route('/finansal', methods=['POST'])
@login_required
def finansal_post():
    if current_user.role < 4:
        return redirect('main.index')

    form = ChoiseTimeForm()
    if form.validate_on_submit():

        start = form.from_field.data
        finish = form.till_field.data
        if finish <= start:
            flash('incorrect data')
            return redirect(url_for('main.finansal_get'))

        delta = timedelta(days=1)

        to_output = []
        days = []
        totaly = {i.name: {'get': 0, 'paid': 0, 'count': 0} for i in db.session.query(Info).filter(
            Info.id_user.in_([j.id for j in db.session.query(User).filter(User.role >= 2).all()])).all()}
        totaly['Total'] = {'get': 0, 'paid': 0, 'count': 0}
        while start < finish:
            days.append(start)
            to_output.append({i.name: {'get': 0, 'paid': 0, 'count': 0} for i in db.session.query(Info)
                             .filter(Info.id_user.in_([j.id for j in db.session.query(User)
                                                      .filter(User.role >= 2).all()])).all()})
            to_output[-1]['Total'] = {'get': 0, 'paid': 0, 'count': 0}
            lessons_day = db.session.query(Lesson).filter(Lesson.datetimes > start, Lesson.datetimes < start+delta).all()

            for lesson in lessons_day:
                geting = lesson.prize
                paying = lesson.teacher_prize
                to_output[-1][db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name]['get'] += geting
                to_output[-1][db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name]['paid'] += paying
                to_output[-1][db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name]['count'] +=1
                to_output[-1]['Total']['get'] += geting
                to_output[-1]['Total']['paid'] += paying
                to_output[-1]['Total']['count'] += 1
                totaly['Total']['get'] += geting
                totaly['Total']['paid'] += paying
                totaly['Total']['count'] += 1
                totaly[db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name][
                    'get'] += geting
                totaly[db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name][
                    'paid'] += paying
                totaly[db.session.query(Info).filter(Info.id_user == lesson.teacher).first().name]['count'] += 1

            start = start+delta

            teachers = [i.name for i in db.session.query(Info).filter(
                Info.id_user.in_([s.id for s in db.session.query(User).filter(User.role > 2).all()])).all()]

        return render_template('admin_panel/fin_exe.html',
                               form=form, days=days,
                               to_output=to_output, teachers=teachers,
                               totaly = totaly)
    else:
        pass

    return redirect(url_for('main.finansal_get'))


@bp.route('/finansal')
@login_required
def finansal_get():
    if current_user.role<4:
        return redirect(url_for('main.index'))

    form = ChoiseTimeForm()
    now = datetime.utcnow()
    starttime = now - timedelta(days=now.weekday(),
                                hours=now.hour,
                                minutes=now.minute,
                                seconds=now.second,
                                microseconds=now.microsecond)
    finishtime = now - timedelta(days=now.weekday() - 7,
                                 hours=now.hour,
                                 minutes=now.minute,
                                 seconds=now.second,
                                 microseconds=now.microsecond)
    lessons = db.session.query(Lesson).filter(Lesson.datetimes > starttime).filter(Lesson.datetimes < finishtime).all()
    return render_template('admin_panel/fin_exe.html', form=form)


@bp.route('/finpersson/<int:id>', methods=['GET', 'POST'])
@login_required
def get_paid(id):
    if current_user.role<3:
        return redirect(url_for('main.index'))
    form = GetPaidForm()

    info = db.session.query(Info).filter(Info.id == id).first()


    if form.validate_on_submit():
        if form.money.data < 0:
            if current_user.role < 4:
                flash('incorrect data sum can be less then zero')
                return redirect(url_for('main.get_paid', id=id))

        c = Cashflows(date=datetime.today(), id_info=id, sum=form.money.data, coment=form.coment.data)
        info.pay_already += form.money.data
        db.session.add(info)
        db.session.add(c)
        db.session.commit()

    cah_flows = db.session.query(Cashflows).filter(Cashflows.id_info == id).order_by(Cashflows.date).all()

    return render_template('admin_panel/finperson.html', form=form, info=info, cah_flows=cah_flows)


@bp.route('/deactivate/<int:id>')
@login_required
def deactivate(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    i = db.session.query(Info).filter(Info.id == id).first()
    i.activa = False
    db.session.add(i)
    db.session.commit()
    return redirect(url_for("main.admin_panel_main", id=id))


@bp.route('/activate/<int:id>')
@login_required
def activate(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    i = db.session.query(Info).filter(Info.id == id).first()
    i.activa = True
    db.session.add(i)
    db.session.commit()
    return redirect(url_for("main.admin_panel_main", id=id))

@bp.route('/deactivated_stud')
@login_required
def deac_info():
    if current_user.role < 2:
        return redirect(url_for('main.index'))

    d_info = db.session.query(Info).filter(Info.id_user == None).filter(Info.activa != True).order_by(Info.id).all()
    infos = []
    s = 0
    for info in d_info:
        graph = db.session.query(Graficks).filter(Graficks.id_user == info.id).all()
        s += 1
        infos.append([info, graph, s])

    return render_template('admin_panel/admin_panel_main.html', infos=infos)