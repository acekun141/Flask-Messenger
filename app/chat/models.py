from datetime import datetime
from app import db


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(), index=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    from_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    to_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    messages = db.relationship('Message', backref='channel', lazy=True)