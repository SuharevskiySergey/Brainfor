from app.main import bp
from app import db, login
from flask import render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from app.models.info import Info
from app.models.user import User
from app.main.forms import InfoForm
from app.models.info import Cource
from app.models.info import Graficks
from app.models.info import Teacher_To_Student
from app.models.info import Cashflows
from app.main.admin_panel.forms import ChoiseTimeForm
from datetime import datetime, timedelta, date
from app.models.info import Lesson, Cashflows
from app.main.admin_panel.forms import GetPaidForm
from sqlalchemy import desc
from app.email import teach_create_stud


@bp.route('/admin_panel_teachers')
@login_required
def admin_panel_teachers():
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    teach = db.session.query(User.id).filter(User.role == 2).all()
    teach_id = []
    for i in teach:
        teach_id.append(i.id)
    infos = db.session.query(Info).filter(Info.id_user.in_(teach_id)).order_by(Info.id_user).all()

    money = {}
    for i in infos:
        Cashflows.sum
        Lesson.teacher_prize
        paid = sum([j.sum for j in db.session.query(Cashflows).filter(Cashflows.id_info == i.id).all()])
        earn = sum([j.teacher_prize for j in db.session.query(Lesson).filter(Lesson.teacher == i.id_user).all()])
        money[i.id] = [paid, earn]
    #print(money)
    return render_template('admin_panel/admin_teachers.html', infos=infos, money=money)


@bp.route('/admin_panel_main')
@login_required
def admin_panel_main():
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    act = request.args.get('act', 'tru', type=str)
    if act == "all":
        infose = db.session.query(Info).filter(Info.id_user == None).order_by(Info.id).all()
    elif act == 'tru':
        infose = db.session.query(Info).filter(Info.id_user == None).filter(Info.activa == True).order_by(Info.id).all()
    elif act == 'fals':
        infose = db.session.query(Info).filter(Info.id_user == None).filter(Info.activa == False).order_by(Info.id).all()

    infos = []
    s = 0
    for info in infose:
        graph = db.session.query(Graficks).filter(Graficks.id_user== info.id).all()
        s += 1
        infos.append([info, graph, s])

    return render_template('admin_panel/admin_panel_main.html', infos=infos, act=act)


@bp.route('/add_new', methods=['GET', 'POST'])
@login_required
def add_new():
    if current_user.role < 2:
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

    if current_user.role == 2:
        form.prize.data = 300

    if form.validate_on_submit():
        info = Info(name=form.name.data, date_of_birth=form.date_of_birth.data, country=form.country.data,
                    phone_number=form.phone_number.data, speed=form.speed.data, source=form.source.data,
                    value=form.prize.data, occupation=form.occupation.data, city=form.city.data, activa=False)
        if current_user.role == 2:
            db.session.add(info)
            db.session.commit()
            course = Cource(to_student=info.id)
            db.session.add(course)
            db.session.commit()
            course.initialization()
            db.session.commit()
            t_st = Teacher_To_Student(id_Teacher=current_user.id, id_Student = info.id)
            db.session.add(t_st)
            db.session.commit()

            #rozcilka
            admins = db.session.query(User).filter(User.role>2).all()
            teach = db.session.query(Info).filter(Info.id_user == current_user.id).first()
            admins += teach
            for adms in admins:
                teach_create_stud(teach=teach, stud=info, adminemail = adms.email)
            return redirect(url_for('main.teacher_panel'))

        db.session.add(info)
        db.session.commit()
        course = Cource(to_student=info.id)
        db.session.add(course)
        db.session.commit()
        course.initialization()
        db.session.commit()
        return redirect(url_for('main.admin_panel_main'))

    form.name.data = '-'
    form.country.data = '-'
    form.city.data = '-'
    form.occupation.data = '-'
    form.phone_number.data = '-'
    form.source.data = '-'

    return render_template('admin_panel/student_page.html', form=form)


@bp.route('/admin_users')
@login_required
def admin_users():
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    users_info = db.session.query(User, Info).join(Info).all()
        #(Info).filter(User.role < current_user.role).all()
    return render_template('admin_panel/admin_users.html', users_info=users_info)

    # if current_user.role >2:
    #     return redirect(url_for('main.admin_panel_main'))
    # else:
    #     return redirect(url_for('main.admin_panel_teachers'))


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


@bp.route("/make_noone<int:id>")
@login_required
def make_noone(id):
    if current_user.role < 4:
        return redirect(url_for('main.index'))
    us = db.session.query(User).filter(User.id == id).first()
    us.role = 1
    db.session.add(us)
    db.session.commit()
    return redirect(url_for('main.admin_users'))


@bp.route('/sudo_graph')
@login_required
def sudo_graph():
    if current_user.role < 3:
        return redirect(url_for('main.index'))

    role = request.args.get('role', 'student', type=str)

    #orgenaize data to output
    to_total = {0: {"Total": 0, "list": []}, 1: {"Total": 0, "list": []}, 2: {"Total": 0, "list": []},
                3: {"Total": 0, "list": []}, 4: {"Total": 0, "list": []}, 5: {"Total": 0, "list": []},
                6: {"Total": 0, "list": []}, 7: {"Total": 0}, "list": []}
    less = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    tot_pass = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    if role == "student":
        graph = db.session.query(Graficks, Info) \
            .order_by(Graficks.weekday) \
            .order_by(Graficks.hour) \
            .order_by(Graficks.minute) \
            .join(Info)\
            .filter(Info.id_user == None)\
            .filter(Info.activa).all()


        les_all = db.session.query(Lesson).filter(Lesson.datetimes >= date.today()-timedelta(days=date.today().weekday())).order_by(Lesson.datetimes).all()
        less = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        tot_pass ={0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for les in les_all:
            less[les.datetimes.weekday()].append(les)
            tot_pass[les.datetimes.weekday()] += 1

        # generete key of Student to teacher
        teacher_key = {temp.id_user : temp
                       for temp in [db.session.query(Info).filter(Info.id_user == i.id).first()
                                    for i in db.session.query(User).filter(User.role > 1).all()]}

        # counting total
        for g in graph:
            # main day counter
            to_total[g.Graficks.weekday]["Total"] += 1

            # count by teacher
            # teacher_key[g.Graficks.id_Teacher].name
            if teacher_key[g.Graficks.id_Teacher].name in to_total[g.Graficks.weekday]["list"]:
                to_total[g.Graficks.weekday][teacher_key[g.Graficks.id_Teacher].name] += 1
            else:
                to_total[g.Graficks.weekday]["list"].append(teacher_key[g.Graficks.id_Teacher].name)
                to_total[g.Graficks.weekday][teacher_key[g.Graficks.id_Teacher].name] = 1

        lenss = len(graph)

        return render_template('admin_panel/sudo_graph.html', graph=graph, rolee=role, teacher_key=teacher_key,
                               lenss=lenss, to_total=to_total, less=less, tot_pass=tot_pass)

    else:
        graph = db.session.query(Graficks, Info) \
            .order_by(Graficks.weekday) \
            .order_by(Graficks.hour) \
            .order_by(Graficks.minute) \
            .join(Info) \
            .filter(Info.id_user != None).all()

        for g in graph:
            to_total[g.Graficks.weekday]["Total"] += 1
            if g.Info.name in to_total[g.Graficks.weekday]["list"]:
                to_total[g.Graficks.weekday][g.Info.name] += 1
            else:
                to_total[g.Graficks.weekday][g.Info.name] = 1
                to_total[g.Graficks.weekday]["list"].append(g.Info.name)
        lenss = len(graph)
        return render_template('admin_panel/sudo_graph.html', graph=graph, rolee=role, lenss=lenss, to_total=to_total, less=less)



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
            Info.id_user.in_([j.id for j in db.session.query(User).filter(User.role > 1).all()])).all()}
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
                Info.id_user.in_([s.id for s in db.session.query(User).filter(User.role >= 2).all()])).all()]
        # print(totaly)
        # print(to_output)
        return render_template('admin_panel/fin_exe.html',
                               form=form, days=days,
                               to_output=to_output, teachers=teachers,
                               totaly=totaly)
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
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    form = GetPaidForm()

    info = db.session.query(Info).filter(Info.id == id).first()


    if form.validate_on_submit():
        if form.money.data < 0:
            if current_user.role < 4:
                flash('incorrect data sum can be less then zero')
                return redirect(url_for('main.get_paid', id=id))
        c = Cashflows(date=form.date.data, id_info=id, sum=form.money.data, lessons=form.lessons.data, coment=form.coment.data)
        info.lessons += form.lessons.data
        info.pay_already += form.money.data
        db.session.add(info)
        db.session.add(c)
        db.session.commit()
    form.money.data = 0
    form.lessons.data = 0
    form.date.data = date.today()

    cah_flows = db.session.query(Cashflows).filter(Cashflows.id_info == id).order_by(Cashflows.date.desc()).all()
    paid = sum([i.sum for i in cah_flows])
    if info.id_user:
        sume = sum([i.teacher_prize for i in db.session.query(Lesson).filter(Lesson.teacher == info.id_user).all()])
        num_less = len(db.session.query(Lesson).filter(Lesson.teacher == info.id_user).all())
    else:
        sume = sum([i.prize for i in db.session.query(Lesson).filter(Lesson.student == info.id).all()])
        num_less = len(db.session.query(Lesson).filter(Lesson.student == info.id).all())
    paid_lessons = sum([i.lessons for i in cah_flows])

    return render_template('admin_panel/finperson.html', form=form, info=info, cah_flows=cah_flows,
                           sume=sume, paid=paid, num_less=num_less, paid_lessons=paid_lessons)


@bp.route('/deactivate/<int:id>')
@login_required
def deactivate(id):
    if current_user.role < 2:
        return redirect(url_for('main.index'))
    act = request.args.get('act', 'tru', type=str)
    i = db.session.query(Info).filter(Info.id == id).first()
    i.activa = False
    db.session.add(i)
    db.session.commit()

    # return redirect(url_for("main.admin_panel_main"))
    if current_user.role > 2:
        return redirect(url_for("main.admin_panel_main"))
    else:
        return redirect(url_for('main.teacher_panel'))



@bp.route('/activate/<int:id>')
@login_required
def activate(id):
    if current_user.role < 2:
        return redirect(url_for('main.index'))
    act = request.args.get('act', 'tru', type=str)
    i = db.session.query(Info).filter(Info.id == id).first()
    i.activa = True
    db.session.add(i)
    db.session.commit()
    # return redirect(url_for("main.admin_panel_main"))
    if current_user.role > 2:
        return redirect(url_for("main.admin_panel_main"))
    else:
        return redirect(url_for('main.teacher_panel'))


@bp.route("/total_finance")
@login_required
def total_finance():
    if current_user.role < 4:
        return redirect(url_for('main.index'))

    yeare = request.args.get('year', date.today().year, type=int)
    # to shown
    key = {1: 'Jan', 2: 'Feb', 3: 'March', 4: 'Apr', 5: 'May', 6: 'June',
           7: 'July', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    to_output_income = {}
    to_output_outcome = {}
    for mon in range(1, 13):
        income = 0
        outcome = 0
        if mon != 12:
            inc = db.session.query(Cashflows.sum, Info).\
                filter(Cashflows.date >= date(day=1, month=mon, year=yeare)).\
                filter(Cashflows.date < date(day=1, month=mon+1, year=yeare)).\
                join(Info).filter(Info.id_user == None).all()
            out = db.session.query(Cashflows.sum, Info). \
                filter(Cashflows.date >= date(day=1, month=mon, year=yeare)). \
                filter(Cashflows.date < date(day=1, month=mon + 1, year=yeare)). \
                join(Info).filter(Info.id_user != None).all()
        else:
            inc = db.session.query(Cashflows.sum, Info).\
                filter(Cashflows.date >= date(day=1, month=mon, year=yeare)) \
                .filter(Cashflows.date < date(day=1, month=1, year=yeare+1)).\
                join(Info).filter(Info.id_user == None).all()
            out = db.session.query(Cashflows.sum, Info). \
                filter(Cashflows.date >= date(day=1, month=mon, year=yeare)) \
                .filter(Cashflows.date < date(day=1, month=1, year=yeare+1)).\
                join(Info).filter(Info.id_user != None).all()
        to_output_income[key[mon]] = sum([i.sum for i in inc])

        # calculating output
        to_output_outcome[key[mon]] = sum([i.sum for i in out])

    years = [y for y in range(2023, date.today().year+1)]

    return render_template("admin_panel/tot_finance.html", to_output_income=to_output_income,
                           to_output_outcome=to_output_outcome, key=key, years=years)


@bp.route("/finmonce_income")
@login_required
def fim_month_inc():
    if current_user.role < 4:
        return redirect(url_for('main.index'))
    yeare = request.args.get('year', date.today().year, type=int)
    monthe = request.args.get('month', date.today().month, type=int)

    if monthe != 12:
        fin_get = db.session.query(Cashflows, Info).filter(Cashflows.date >= date(day=1, month=monthe, year=yeare))\
            .filter(Cashflows.date < date(day=1, month=monthe+1, year=yeare))\
            .join(Info).all()
    else:
        fin_get = db.session.query(Cashflows, Info).filter(Cashflows.date >= date(day=1, month=monthe, year=yeare)) \
            .filter(Cashflows.date < date(day=1, month=1, year=yeare+1))\
            .join(Info).all()
    to_output = {"list": []}
    #calculate paing bu student
    to_sent = {}
    for fin in fin_get:

        if fin.Info.name in to_output["list"]:
            to_output[fin.Info.name] += fin.Cashflows.sum
        else:
            to_output[fin.Info.name] = fin.Cashflows.sum
            to_output["list"].append(fin.Info.name)
            to_sent[fin.Info.name] = fin.Info.id

    return render_template("admin_panel/finance_month_income.html", to_output=to_output, to_sent=to_sent)


@bp.route("/finmonce_outcone")
@login_required
def fim_month_out():
    if current_user.role < 4:
        return redirect(url_for('main.index'))

    yeare = request.args.get('year', date.today().year, type=int)
    monthe = request.args.get('month', date.today().month, type=int)

    if monthe != 12:
        fin_out = db.session.query(Lesson, Info).filter(Lesson.datetimes >= date(day=1, month=monthe, year=yeare))\
            .filter(Lesson.datetimes < date(day=1, month=monthe+1, year=yeare))\
            .join(Info, Info.id_user == Lesson.teacher).all()
    else:
        fin_out = db.session.query(Lesson, Info).filter(Lesson.datetimes >= date(day=1, month=monthe, year=yeare)) \
            .filter(Lesson.datetimes < date(day=1, month=1, year=yeare+1))\
            .join(Info, Info.id_user == Lesson.teacher).all()
    to_output = {"list": []}
    to_sent = {}
    # calculate paing bu student
    for fin in fin_out:

        if fin.Info.name in to_output["list"]:
            to_output[fin.Info.name] += fin.Lesson.teacher_prize
        else:
            to_output[fin.Info.name] = fin.Lesson.teacher_prize
            to_output["list"].append(fin.Info.name)
            to_sent[fin.Info.name] = fin.Info.id

    return render_template("admin_panel/finance_month_income.html", to_output=to_output, to_sent=to_sent)


@bp.route('/fixing_lesson/<int:id>')
@login_required
def check_lesson(id):
    if current_user.role < 4:
        if id != db.session.query(Info).filter(Info.id_user == current_user.id).first().id:
            return redirect(url_for('main.index'))
    info = db.session.query(Info).filter(Info.id == id).first()
    lesw = db.session.query(Lesson, Info).filter(Lesson.teacher == info.id_user).order_by(desc(Lesson.datetimes))\
        .join(Info).all()
    keys = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3 :'Thursday', 4: 'Friday', 5: 'Saturday', 6:'Sunday'}
    return render_template("admin_panel/check_lesson.html", info=info, lesw=lesw, keys=keys)


@bp.route('/deletes_lesson/<int:id>')
@login_required
def del_lesson(id):
    if current_user.role < 4:
        return redirect(url_for('main.index'))
    l = db.session.query(Lesson).filter(Lesson.id == id).first()
    id_t = db.session.query(Info).filter(Info.id_user == l.teacher).first().id
    db.session.delete(l)
    db.session.commit()

    return redirect(url_for('main.check_lesson', id=id_t))
