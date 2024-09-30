from app.main import bp
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.info import Info, Lesson
from app.models.user import User
from app.models.info import Teacher_To_Student
from app.main.forms import InfoForm
from app.models.info import Info, Cashflows
from app.models.info import Graficks
from app.main.forms import GraphForm
from app.models.info import Cource, Part_Course
from app.main.forms import Change_progress_data
from datetime import datetime, timedelta, date
from app.models.info import BankInfo

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return redirect(url_for("main.information"))
    return render_template('index.html')


@bp.route('/profile/')
@login_required
def information():
    user_id = request.args.get('id', db.session.query(Info).filter(Info.id_user == current_user.id).first().id, type=int)

    info = db.session.query(Info).filter(Info.id == user_id).first()

    if current_user.role == 1 and info.id_user != current_user.id:
        return redirect(url_for('main.index'))

    if not info.id_user:
        i = db.session.query(Teacher_To_Student.id_Teacher).filter(Teacher_To_Student.id_Student == user_id).all()
        liste =[]
        for i in i:
            liste.append(i[0])

        teachers = db.session.query(Info).filter(Info.id_user.in_(liste)).all()

    else:
        teachers = []

    if info.role() == 1:
        lessons = db.session.query(Lesson).filter(Lesson.student == user_id).all()
    else:
        pass
    graph = db.session.query(Graficks).filter(Graficks.id_user == user_id).order_by(Graficks.weekday).all()

    paids = db.session.query(Cashflows).filter(Cashflows.id_info == user_id).all()
    summe = 0
    for paid in paids:
        summe += paid.sum
    salar = 0
    w_l_c = 0
    if info.id_user != None:
        st = date.today() - timedelta(days=date.today().weekday())

        week_less = db.session.query(Lesson).filter(Lesson.teacher == info.id_user)\
            .filter(Lesson.datetimes >= st).all()
        for les in week_less:
            salar += les.teacher_prize
            w_l_c += 1
    if info.id_user != None:
        tot_les = len(db.session.query(Lesson).filter(Lesson.teacher == info.id).all())

    else:
        tot_les = -1

    bank_inf = db.session.query(BankInfo).filter(BankInfo.id_user == info.id_user).first()
    return render_template('main/information.html', info=info,  role=current_user.role, teachers=teachers,
                           day=0, graph=graph, summe=summe, salar=salar, w_l_c=w_l_c, tot_les=tot_les, bank_inf=bank_inf)


@bp.route('/lesons_past/<int:id>')
@login_required
def lessons_past(id):
    # права доступу
    if current_user.role < 3:
        if id != db.session.query(Info).filter(Info.id_user == current_user.id).first().id:
            return redirect(url_for('main.index'))

    info = db.session.query(Info).filter(Info.id == id).first()
    if info.id_user == None :
        lessons = db.session.query(Lesson, Info).filter(Lesson.student == id).join(Info, Info.id_user == Lesson.teacher).all()
        tot_les = len(lessons)
    else:
        lessons_all = db.session.query(Lesson).filter(Lesson.teacher == info.id_user).order_by(
            Lesson.datetimes.desc()).all()
        tot_les = len(lessons_all)
        j = 0
        lessons = []
        # 7 total
        lessons.append({0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: 0})

        for i in range(len(lessons_all) - 1):

            lessons[j][lessons_all[i].datetimes.weekday()].append(lessons_all[i])
            lessons[j][7] += 1

            if lessons_all[i].datetimes.weekday() < lessons_all[i + 1].datetimes.weekday() or \
                    (lessons_all[i].datetimes - lessons_all[i + 1].datetimes).days > 6:
                # lessons.append(week[j])
                j += 1
                # 7 total
                lessons.append({0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: 0})
        # addinglast
        if len(lessons_all) > 1:
            if lessons_all[-2].datetimes.weekday() < lessons_all[-1].datetimes.weekday() or \
                    (lessons_all[-2].datetimes - lessons_all[-1].datetimes).days > 6:
                lessons.append({0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: 0})
                lessons[-1][lessons_all[-1].datetimes.weekday()].append(lessons_all[-1])
            else:
                lessons[-1][lessons_all[-1].datetimes.weekday()].append(lessons_all[-1])
        elif len(lessons_all) == 1:
            lessons[-1][lessons_all[-1].datetimes.weekday()].append(lessons_all[-1])
        lessons[(len(lessons) - 1)][7] += 1

    return render_template('main/lesons_past.html', info=info, lessons=lessons, tot_les=tot_les)


from app.main.forms import BankForm


@bp.route('/edit_carts/<int:id>', methods=['GET', 'POST'])
@login_required
def ed_carts(id):
    if (current_user.role < 4) and (current_user.id != id):
        return redirect(url_for('main.index'))
    bank_data = db.session.query(BankInfo).filter(BankInfo.id_user == id).first()
    form = BankForm()
    info = db.session.query(Info).filter(Info.id_user == id).first()
    if form.validate_on_submit():
        if bank_data == None:
            bank_data = BankInfo(id_user=id)
        bank_data.name_bank = form.bank_name.data
        bank_data.number = form.cart.data
        db.session.add(bank_data)
        db.session.commit()
        return redirect(url_for("main.information", id=info.id))
    print(bank_data)
    if bank_data != None :
        form.cart.data = bank_data.number
        form.bank_name.data = bank_data.name_bank

    return render_template('main/edit_bank_data.html', form=form, info=info)


@bp.route('/change_info/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_info(user_id):

    # user_id = request.args.get('id', db.session.query(Info).filter(Info.id_user == current_user.id).first().id, type=int)

    info = db.session.query(Info).filter(Info.id == user_id).first()
    form = InfoForm()
    if current_user.role < 3 and info.id_user != current_user.id:
        return redirect(url_for('main.index'))

    if not (form.source.data):
        form.source.data = info.source

    if not (form.speed.data):
        form.speed.data = info.speed

    if not (form.prize.data):
        form.prize.data = info.value

    if not (form.city.data):
        form.city.data = info.city

    if not (form.occupation.data):
        form.occupation.data = info.occupation

    if form.validate_on_submit():

        info.name = form.name.data
        info.country = form.country.data
        info.date_of_birth = form.date_of_birth.data
        info.phone_number = form.phone_number.data
        info.city = form.city.data
        info.occupation = form.occupation.data
        if current_user.role > 3:
            info.speed = form.speed.data
            info.source = form.source.data
            info.value = form.prize.data

        db.session.add(info)
        db.session.commit()

        return redirect(url_for('main.information', id=user_id, info=info))

    form.name.data = info.name
    form.country.data = info.country
    form.date_of_birth.data = info.date_of_birth
    form.phone_number.data = info.phone_number
    form.city.data = info.city
    form.occupation.data = info.occupation
    form.speed.data = info.speed
    form.source.data = info.source
    form.prize.data = info.value

    return render_template('main/change_information.html', form=form, role=current_user.role, info=info)


@login_required
@bp.route('/add_graph_to/<int:id>', methods=['GET', 'POST'])
def add_graficks(id):
    if current_user.role < 3:
        if id != db.session.query(Info).filter(Info.id_user == current_user.id).first().id:
            return redirect(url_for('main.index'))
    form = GraphForm()
    if form.validate_on_submit():
        graph = Graficks(id_user=id, weekday={'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}[form.weekday.data],
                         hour=form.houer.data, minute=form.minute.data)
        db.session.add(graph)
        db.session.commit()
        return redirect(url_for('main.information', id=id))

    return render_template('/main/chouse_graph.html', form=form, id=id)


@login_required
@bp.route('/del_grapfick/<int:id>')
def dell_graph(id):
    if current_user.role < 3:
        if db.session.query(Info).filter(Info.id == db.session.query(Graficks).filter(Graficks.id == id).
                first().id_user).first().id != db.session.query(Info).filter(Info.id_user == current_user.id).first().id:
            return redirect(url_for('main.index'))
    to_dell = db.session.query(Graficks).filter(Graficks.id == id).first()
    togo = to_dell.id_user
    db.session.delete(to_dell)
    db.session.commit()
    return redirect(url_for('main.information', id=togo))


@bp.route('/edit_graph/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_graph(id):
    if current_user.role < 4:
        g = db.session.query(Graficks).filter(Graficks.id == id).first()
        t_id = db.session.query(Teacher_To_Student).filter(Teacher_To_Student.id_Student == g.id_user).first().id_Teacher
        if current_user.id != t_id:
            flash("you can edit this graph")
            return redirect(url_for('main.index'))

    g = db.session.query(Graficks).filter(Graficks.id == id).first()
    less = db.session.query(Lesson).filter(Lesson.datetimes > (date.today()-timedelta(days=date.today().weekday())))
    for les in less:
        if les.datetimes.weekday() == g.weekday:
            if les.datetimes.hour == g.hour:
                if les.datetimes.minute == g.minute:
                    flash("This lesson was executet you can edit it next week")
                    return redirect(url_for('main.index'))

    form = GraphForm()
    if form.validate_on_submit():
        g.weekday = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}[form.weekday.data]
        g.hour = form.houer.data
        g.minute = form.minute.data
        #print(form.weekday.data, form.houer.data, form.minute.data)
        db.session.add(g)
        db.session.commit()
        return redirect(url_for('main.index'))

    form.weekday.data = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday',
                         5: 'Saturday', 6: 'Sunday'}[g.weekday]
    form.houer.data = g.hour
    form.minute.data = g.minute
    return render_template('/main/chouse_graph.html', form=form)


@login_required
@bp.route('/graphicks/<int:id>')
def graphic(id):
    def retern_hour(list_elem):
        return list_elem.Graficks.hour

    if id == 0:
        id = db.session.query(Info).filter(Info.id_user == current_user.id).first().id

    output = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    info = db.session.query(Info).filter(Info.id == id).first()
    if db.session.query(Info.id_user):
        tempgraph = db.session.query(Graficks, Info.name, Info.id, Info.activa
                                     ).order_by(Graficks.minute).filter(Graficks.id_user == info.id)\
            .join(Info).all()
        for i in tempgraph:
            output[i.Graficks.weekday].append(i)

        stud = []
        for t in db.session.query(Teacher_To_Student.id_Student).filter(Teacher_To_Student.id_Teacher == info.id_user).all():
            if db.session.query(Info).filter(Info.id == t.id_Student).first().activa:
                stud.append(t.id_Student)

        tempss = db.session.query(Graficks, Info.name, Info.id).order_by(Graficks.minute)\
            .filter(Graficks.id_user.in_(stud))\
            .join(Info).all()
        for i in tempss:
            output[i.Graficks.weekday].append(i)

        #sort
        for day in range(7):
            output[day].sort(key=retern_hour)

    else:
        tempgraph = db.session.query(Graficks).filter(Graficks.id_user == id).order_by(Graficks.minute).all()
        for temp in tempgraph:
             output[temp.weekday].append(temp)
    if info.id_user:
        ids = info.id_user
        pass_lesson = db.session.query(Lesson).filter(Lesson.teacher == ids)\
            .filter(Lesson.datetimes > date.today() - timedelta(date.today().weekday())).all()

    out_pass_less = []
    for less in pass_lesson:
        out_pass_less.append([less.datetimes.weekday(), less.datetimes.hour, less.datetimes.minute])

    return render_template('/main/graphics.html', output=output, info=info, out_pass_less=out_pass_less)


@bp.route('/processing/<int:id>')
@login_required
def secsesfuly(id):
    if current_user.role<2:
        return redirect(url_for('main.index'))

    role = current_user.role
    course = db.session.query(Cource).filter(Cource.to_student == id).first()
    party = db.session.query(Part_Course)\
        .filter(Part_Course.id_course == course.id)\
        .order_by(Part_Course.number).all()
    return render_template('/main/progress.html', party=party, course=course, role=role)


@bp.route('/changedatales/<int:id>/<int:numb>', methods=['GET', 'POST'])
@login_required
def changedateoflesson(id, numb):
    if current_user.role < 4:
        return redirect(url_for('main.index'))
    form = Change_progress_data()
    s = db.session.query(Part_Course).filter(Part_Course.id == id).first()

    if form.validate_on_submit():
        if numb == 1:
            s.rypma = form.date.data
        if numb == 2:
            s.repetition = form.date.data
        if numb == 3:
            s.reading = form.date.data
        if numb == 4:
            s.speaking = form.date.data
        if numb == 5:
            s.qetion = form.date.data
        if numb == 6:
            s.topics = form.date.data
        if numb == 7:
            s.associations = form.date.data
        if numb == 8:
            s.assrep = form.date.data
        if numb == 9:
            s.grammar = form.date.data
        db.session.add(s)
        db.session.commit()
        c = db.session.query(Cource).filter(Cource.id == s.id_course).first()
        i = db.session.query(Info).filter(Info.id == c.to_student).first()
        return redirect(url_for('main.secsesfuly', id=i.id))


    c = db.session.query(Cource).filter(Cource.id == s.id_course).first()
    inf = db.session.query(Info).filter(Info.id == c.to_student).first()

    if numb == 1:
        form.date.data = s.rypma.date()
    if numb == 2:
        form.date.data = s.repetition.date()
    if numb == 3:
        form.date.data = s.reading.date()
    if numb == 4:
        form.date.data = s.speaking.date()
    if numb == 5:
        form.date.data = s.qetion.date()
    if numb == 6:
        form.date.data = s.topics.date()
    if numb == 7:
        form.date.data = s.associations.date()
    if numb == 8:
        form.date.data = s.assrep.date()
    if numb == 9:
        form.date.data = s.grammar.date()

    return render_template('/admin_panel/changedatalesson.html', form=form, inf=inf, s=s, numb=numb)


@bp.route('/deletelesson/<int:id>/<int:numb>')
@login_required
def clearlesson(id, numb):
    s = db.session.query(Part_Course).filter(Part_Course.id == id).first()
    null = db.session.query(Part_Course).filter(Part_Course.id_course==s.id_course).filter(Part_Course.number==80).first().rypma
    if numb == 1:
        s.rypma = null
    if numb == 2:
        s.repetition = null
    if numb == 3:
        s.reading = null
    if numb == 4:
        s.speaking = null
    if numb == 5:
        s.qetion = null
    if numb == 6:
        s.topics = null
    if numb == 7:
        s.associations = null
    if numb == 8:
        s.assrep = null
    if numb == 9:
        s.grammar = null

    db.session.add(s)
    db.session.commit()
    c = db.session.query(Cource).filter(Cource.id == s.id_course).first()
    i = db.session.query(Info).filter(Info.id == c.to_student).first()
    return redirect(url_for('main.secsesfuly', id=i.id))



import xlrd
@bp.route('/tempfix')
@login_required
def tempfix():
    if current_user.role < 4:
        return redirect(url_for('main.index'))

    book = xlrd.open_workbook('temp.xls')
    sh = book.sheet_by_index(0)
    i = 1
    nows = date.today()
    while sh.cell_value(rowx=i, colx=0) != 'end':

        ids = db.session.query(Cource).filter(Cource.to_student == int(sh.cell_value(rowx=i, colx=0))).first().id
        keys = sh.cell_value(rowx=i, colx=1)
        for j in range(80):
            if sh.cell_value(rowx=i, colx=j + 2) == "done":
                les = db.session.query(Part_Course).filter(Part_Course.id_course == ids).filter(Part_Course.number == j).first()
                if keys == "rypma":
                    les.rypma = nows
                if keys == "repetition":
                    les.repetition = nows
                if keys == "reading":
                    les.reading = nows
                if keys == "speaking":
                    les.speaking = nows
                if keys == "qetion":
                    les.qetion = nows
                if keys == "topics":
                    les.topics = nows
                if keys == "associations":
                    les.associations = nows
                if keys == "assrep":
                    les.assrep = nows
                if keys == "grammar":
                    les.grammar = nows

                db.session.add(les)
                db.session.commit()

        i += 1

    return redirect(url_for('main.index'))
