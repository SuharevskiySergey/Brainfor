from app.auth import bp
from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.urls import url_parse    #werkzeug 2.7
#from urllib.parse import urlsplit       #werkzeuk 3.0

from app.models.user import User
from app.models.info import Info

from app.auth.forms import LoginForm, RegisterForm, ResetPasswordForm, ResetPasswordRequestForm

from app.email import send_password_reset_email


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_parse('main.index')
            return redirect(url_for('main.index'))

        flash("incorrect data")
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@bp.route('/auth/logout')
@bp.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("you are exit from system")
    return redirect(url_for('auth.login'))


@bp.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        info = Info()
        info.id_user = db.session.query(User.id).filter(User.email == form.email.data)
        db.session.add(info)
        db.session.commit()
        flash('You are now registrated')
        return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', form=form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check you email for the instructions")
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password,', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('You password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
