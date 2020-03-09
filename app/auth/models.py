from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True,
                         unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    friends = db.relationship('Relation', foreign_keys='Relation.user_id',
                              backref='auth', lazy=True)
    is_friend = db.relationship('Relation', foreign_keys='Relation.friend_id',
                                backref='friend', lazy=True)
    messages = db.relationship('Message', foreign_keys='Message.from_user',
                               backref='auth', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Relation(db.Model):
    __tablename__ = 'relations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))