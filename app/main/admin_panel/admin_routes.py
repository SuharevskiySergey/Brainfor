from app.main import bp
from app import db, login
from flask import render_template, url_for, redirect, request
from flask_login import login_required, current_user
from app.models.info import Info
from app.models.user import User
from app.main.forms import InfoForm
from app.models.info import Cource


@bp.route('/admin_panel_main')
@login_required
def admin_panel_main():
    if current_user.role < 2:
        return redirect(url_for('main.index'))

    infos = db.session.query(Info).filter(Info.id_user == None).order_by(Info.id_user).all()

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
                    phone_number=form.phone_number.data)
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