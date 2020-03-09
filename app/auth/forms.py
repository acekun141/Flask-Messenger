from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from app.auth.models import User 


class RegisterUserForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired()])
    password = PasswordField(label='Password',
                           validators=[DataRequired()])
    confirm_password = PasswordField(label='Confirm Password',
                                   validators=[DataRequired(),
                                               EqualTo('password')])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username has already registered!')
    
    def validate_password(self, password):
        if password.data == self.username.data:
            raise ValidationError('Password must be different from username!')
        pass_lenth = len(password.data)
        if pass_lenth < 6 or pass_lenth > 30:
            raise ValidationError('Password length must be less than 30 and large than 6!')
        

class LoginForm(FlaskForm):
    username = StringField(label='Username',
                           validators=[DataRequired()])
    password = PasswordField(label='Password',
                              validators=[DataRequired()])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Username or Password not correct!')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if not user.check_password(password.data):
                raise ValidationError('Username or Password not correct!')