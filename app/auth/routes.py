from flask import request, render_template, url_for, redirect, g, session

from app import db
from app.auth import auth as bp
from app.auth.models import User
from app.auth.forms import RegisterUserForm, LoginForm

import functools


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id', None)

    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            g.user = user
        else:
            session.pop('user_id', None)
            return redirect(url_for('auth.login'))
    else:
        g.user = None


@bp.route(rule='/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('chat.all_chat'))
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@bp.route(rule='/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        session['user_id'] = user.id
        
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html', form=form)


@bp.route(rule='/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if not g.user:
            return redirect(url_for('auth.login'))
        
        return view(*args, **kwargs)
    
    return wrapped_view