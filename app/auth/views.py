from flask import render_template,redirect,request,url_for,flash
from flask.ext.login import login_user, logout_user , login_required,current_user
from . import auth
from ..models import User 
from .forms import LoginForm,RegisterForm
from ..import db
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user=User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user,form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))
		flash('invalid username or password')
	return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('you have been logged out')
	return redirect(url_for('main.index'))

@auth.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		user=User(email=form.email.data,password=form.password.data,username=form.username.data)
		db.session.add(user)
		db.session.commit()
		token=user.generate_confirmation_token()
		send_email(user.email,'confirm you account','auth/email/confirm',user=user,token=token)
		flash('A confirmation email has been sent to you by email')
		return redirect(url_for('main.index'))
	return render_template('auth/register.html',form=form)

@auth.route('confirm/<token>')
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash('you have confirmed your account,thanks!')
	else:
		flash('the confirmation link is invalid or has expired.')
		return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
	if current_user.is_authenticated and not current_user.confirmed \
		and request.endpoint[:5] != 'auth.' \
		and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')