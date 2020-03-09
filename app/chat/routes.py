from flask import render_template, request, redirect, url_for, session, g

from app.chat import chat as bp
from app.auth.routes import login_required
from app.auth.models import User, Relation
from app.chat.models import Channel, Message

from app import db

def get_channel(first_id, second_id):
    channel = Channel.query.filter_by(from_user=first_id, to_user=second_id).first()
    if channel:
        return channel
    else:
        channel = Channel.query.filter_by(to_user=first_id, from_user=second_id).first()
        return channel

@bp.route(rule='/', methods=['GET'])
@login_required
def all_chat():

    return render_template('chat/all_chat.html')


@bp.route(rule='/chat/<username>', methods=['GET'])
@login_required
def room(username):
    user = User.query.filter_by(username=username).first_or_404()
    channel = get_channel(user.id, g.user.id)
    print(channel)
    if not channel:
        channel = Channel()
        channel.from_user = g.user.id
        channel.to_user = user.id
        
        db.session.add(channel)
        db.session.commit()
    session['room'] = channel.id

    return render_template('chat/room.html', user=user, channel=channel)

