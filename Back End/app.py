import peewee
from flask import (Flask, g, render_template, flash, redirect, url_for)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required
from flask_peewee.admin import Admin
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_admin import Admin, AdminIndexView, BaseView, expose

from flask.ext.admin.contrib.peewee import ModelView
import forms
import models


class MyHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class UserView(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['email']
    page_size = 50

DEBUG = False
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'ScertKeyInsertHere'




login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("You registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('apply'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("you've been logged out! Come back soon", "success")
    return redirect(url_for('index'))

@app.route('/appinfo')
@login_required
def appinfo():
    form = forms.ApplyForm()
    if form.validate_on_submit():
        models.Apply.create(fullname=form.fullname.data,
                            email=form.email.data)
        flash("your application has been submitted", "success")

    return render_template('appinfo.html')

@app.route('/apply', methods=('GET', 'POST'))
@login_required
def apply():
    form = forms.ApplyForm()
    if form.validate_on_submit():
        models.Apply.create(fullname = form.fullname.data,
                            email = form.email.data)
        flash("your application has been submitted", "success")
        return redirect(url_for('index'))
    return render_template('apply.html', title = 'Apply', form = form)


@app.route('/')
def index():
    return 'Tacos'
#auth = Auth(app, models.DATABASE)
#admin = Admin(app, auth)
#admin.register(models.User)
#admin.setup()

if __name__ == '__main__':
    models.initialize()

    # needed for authentication
    admin = Admin(app, name="GrizzHacks")
    admin.add_view(UserView(models.User))
    admin.add_view(MyModelView(models.Apply))
#    admin.set_password('admin')
    try:
        models.User.create_user(
            email='rughaniarpan@gmail.com',
            password='password',
            admin=True
        )



    except ValueError:
        pass


    app.run(debug=DEBUG, host=HOST, port=PORT)


