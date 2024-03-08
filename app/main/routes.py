from app.main import bp
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.models.info import Info, Lesson
from app.models.user import User
from app.models.info import Teacher_To_Student
from app.main.forms import InfoForm
from app.models.info import Info
from app.models.info import Graficks
from app.main.forms import GraphForm
from app.models.info import Cource, Part_Course


@bp.route('/')
@bp.route('/index')
@login_required
def index():
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
        lessons_all = db.session.query(Lesson).filter(Lesson.teacher == info.id_user).order_by(Lesson.datetime.desc()).all()

        j = 0
        lessons = []
        lessons.append({0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []})
        #[ {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []} ]
        #[lesson ...]
        for i in range(len(lessons_all)-1):

            lessons[j][lessons_all[i].datetime.weekday()].append(lessons_all[i])

            if lessons_all[i].datetime.weekday() < lessons_all[i+1].datetime.weekday() or \
                    (lessons_all[i].datetime - lessons_all[i+1].datetime).days > 6:
                #lessons.append(week[j])
                j += 1
                lessons.append({0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []})
        # without last

    graph = db.session.query(Graficks).filter(Graficks.id_user == user_id).all()

    return render_template('main/information.html', info=info,  role=current_user.role, teachers=teachers,
                           lessons=lessons, day=0, graph=graph)


@bp.route('/change_info/', methods=['GET', 'POST'])
@login_required
def change_info():

    user_id = request.args.get('id', db.session.query(Info).filter(Info.id_user == current_user.id).first().id, type=int)

    info = db.session.query(Info).filter(Info.id == user_id).first()

    if current_user.role < 3 and info.id_user != current_user.id:
        return redirect(url_for('main.index'))

    form = InfoForm()

    if form.validate_on_submit():
        #print(form.date_of_birth.data)
        info.name = form.name.data,
        info.country = form.country.data
        info.date_of_birth = form.date_of_birth.data
        info.phone_number = form.phone_number.data

        info.speed = form.speed.data
        info.source = form.source.data
        info.value = form.prize.data

        db.session.add(info)
        db.session.commit()

        return redirect(url_for('main.information', id=info.id))

    # speed = StringField('Speed')
    # sourse = StringField('Sourse')
    # prize = IntegerField('Prize')
    # submit = SubmitField('Submit')

    form.name.data = info.name
    form.country.data = info.country
    form.date_of_birth.data = info.date_of_birth
    form.phone_number.data = info.phone_number

    form.speed.data = info.speed
    form.source.data = info.source
    form.prize.data = info.value

    return render_template('main/change_information.html', form=form, role=current_user.role)


@login_required
@bp.route('/add_graph_to/<int:id>', methods=['GET', 'POST'])
def add_graficks(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    form = GraphForm()
    if form.validate_on_submit():
        graph = Graficks(id_user=id, weekday={'Monday': 0, 'Tuesday': 1, 'Wednessday': 2, 'Thirthday': 3, 'Friday': 4, 'Sartuday': 5, 'Sunday': 6}[form.weekday.data],
                         hour=form.houer.data, minute=form.minute.data)
        db.session.add(graph)
        db.session.commit()
        return redirect(url_for('main.information', id=id))

    return render_template('/main/chouse_graph.html', form=form, id=id)


@login_required
@bp.route('/del_grapfick/<int:id>')
def dell_graph(id):
    if current_user.role < 3:
        return redirect(url_for('main.index'))
    to_dell = db.session.query(Graficks).filter(Graficks.id == id).first()
    togo = to_dell.id_user
    db.session.delete(to_dell)
    db.session.commit()
    return redirect(url_for('main.information', id=togo))


@login_required
@bp.route('/graphicks/<int:id>')
def graphic(id):
    def retern_hour(list_elem):
        return list_elem.Graficks.hour

    output = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
    info = db.session.query(Info).filter(Info.id == id).first()
    if db.session.query(Info.id_user):
        tempgraph = db.session.query(Graficks, Info.name, Info.id).filter(Graficks.id_user == info.id)\
            .join(Info).all()
        for i in tempgraph:
            output[i.Graficks.weekday].append(i)

        stud = []
        for t in db.session.query(Teacher_To_Student.id_Student).filter(Teacher_To_Student.id_Teacher == info.id_user).all():
            stud.append(t.id_Student)

        tempss = db.session.query(Graficks, Info.name, Info.id).filter(Graficks.id_user.in_(stud))\
            .join(Info).all()
        for i in tempss:
            output[i.Graficks.weekday].append(i)


        #sort
        for day in range(7):
            output[day].sort(key=retern_hour)

    else:
        tempgraph = db.session.query(Graficks).filter(Graficks.id_user == id).all()
        for temp in tempgraph:
             output[temp.weekday].append(temp)

    return render_template('/main/graphics.html', output=output, info=info)

@bp.route('/processing/<int:id>')
@login_required
def secsesfuly(id):
    if current_user.role<2:
        return redirect(url_for('main.index'))

    course = db.session.query(Cource).filter(Cource.to_student == id).first()
    party = db.session.query(Part_Course)\
        .filter(Part_Course.id_course == course.id)\
        .order_by(Part_Course.number).all()
    return render_template('/main/progress.html', party=party, course=course)