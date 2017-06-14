from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email=StringField('email',validators=[Required(),Length(1,64),Email()])
    password=PasswordField('password',validators=[Required()])
    remember_me=BooleanField('keep me logged in')
    submit=SubmitField('log in')


class RegisterForm(Form):
	email=StringField('Email',validators=[Required(),Length(1,64),Email()])
	username=StringField('username',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
	password=PasswordField('password',validators=[Required(),EqualTo('password2',message='password must match')])
	password2=PasswordField('confirm password',validators=[Required()])
	submit=SubmitField('Register')

	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('eamil already registered')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')