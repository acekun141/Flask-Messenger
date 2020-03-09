from app import socketio, db
from flask import session, g
from flask_socketio import emit, join_room, leave_room
from app.chat.models import Message
from app.auth.models import User
from app.chat.routes import get_channel


@socketio.on('joined')
def joined(message):
    print(g.__dict__)
    user = User.query.filter_by(id=session.get('user_id', '')).first()
    if user:
        room = session.get('room')
        join_room(room)
        emit('status', {'msg': '{}: Has entered the room.'.format(user.username)}, room=room)

@socketio.on('send_message')
def take(message):
    from_user = User.query.filter_by(id=session.get('user_id', '')).first_or_404()
    to_user = User.query.filter_by(username=message['user']).first_or_404()
    channel = get_channel(from_user.id, to_user.id)
    if channel and message['msg']:
        new_message = Message()
        new_message.channel = channel
        new_message.from_user = from_user.id
        new_message.to_user = to_user.id
        new_message.message = message['msg']

        db.session.add(new_message)
        db.session.commit()
        
        room = session.get('room')
        join_room(room)
        emit('message', {'user': from_user.username, 'msg': message['msg']}, room=room)
