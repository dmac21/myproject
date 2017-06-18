#coding:utf-8
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,SelectField
from wtforms.validators import Required,Length,Regexp,Email
from ..models import Role, User

class EditProfileForm(Form):
	name=StringField(u'真实姓名',validators=[Length(0,64)])
	location=StringField(u'所在地址',validators=[Length(0,64)])
	about_me=TextAreaField(u'自我简介')
	submit=SubmitField(u'提交')

class PostForm(Form):
	body=TextAreaField(u'说点什么？',validators=[Required()])
	submit=SubmitField(u'提交')

class EditProfileAdminForm(Form):
	email=StringField(u'电子邮箱',validators=[Required(),Length(1,64),Email()])
	username=StringField(u'用户名',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores')])
	confirmed=BooleanField(u'已经确认')
	role=SelectField('Role',coerce=int)
	name = StringField(u'真实姓名', validators=[Length(0, 64)])
	location = StringField(u'所在地址', validators=[Length(0, 64)])
	about_me = TextAreaField(u'自我简介')
	submit = SubmitField(u'提交')

	def __init__(self,user,*args,**kwargs):
		super(EditProfileAdminForm,self).__init__(*args,**kwargs)
		self.role.choices=[(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
		self.user=user

	def validate_email(self,field):
		if field.data !=self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered')

	def validate_username(self,field):
		if field.data !=self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use')