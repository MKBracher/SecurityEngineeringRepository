from datetime import timedelta
import email
from flask_sqlalchemy import SQLAlchemy
from unicodedata import name
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, session, flash, g
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)


bcrypt = Bcrypt(app)

#todo - Make a proper key 
app.secret_key = "testkey"
app.config["SQLALCHEMY_DATABASE_URI"] ='sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#Choose a session lifetime - Maybe 10 minutes?
app.permanent_session_lifetime = timedelta(minutes = 10)

db =  SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)

class Credentials(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    website = db.Column(db.String(100))
    login = db.Column(db.String(100))
    password = db.Column(db.String(100))
    userId = db.Column(db.Integer)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})


    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        
        if existing_user_username:
            flash("Username already exists")
            raise ValidationError("That username already exists. Please choose a different one")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=30)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")

class AddCredentialsForm(FlaskForm):

    website = StringField(validators=[Length(
        min=4, max=20)], render_kw={"placeholder": "Website"})

    login = StringField(validators=[Length(
        min=4, max=20)], render_kw={"placeholder": "Login"})

    password = PasswordField(validators=[Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Add Credentials")

    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/manager",methods=["POST", "GET"])
@login_required
def manager():
    form = AddCredentialsForm()
    

    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_credentials = Credentials(login = form.login.data, password=form.password.data, website=form.website.data, userId = current_user.id)
        db.session.add(new_credentials)
        db.session.commit()
        flash("Login Added")
        return redirect(url_for('manager'))
            
    return render_template("manager.html", form=form, values=Credentials.query.filter_by(userId=current_user.id).all())

@app.route("/login",methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('manager'))
            else:
                flash("Username or password is incorrect")
    return render_template('login.html', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration Successful")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)



@app.route("/logout", methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Logout Successful")
    return redirect(url_for('login'))
    
    


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)


