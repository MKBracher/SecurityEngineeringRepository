from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from unicodedata import name
from flask import Flask, Blueprint, render_template, request, jsonify, redirect, url_for, session, flash

app = Flask(__name__)

#todo - Make a proper key 
app.secret_key = "testkey"
app.config["SQLALCHEMY_DATABASE_URI"] ='sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#Choose a session lifetime - Maybe 10 minutes?
app.permanent_session_lifetime = timedelta(minutes = 10)

db =  SQLAlchemy(app)

class users(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/manager",methods=["POST", "GET"])
def manager():
    if request.method == "POST":
        user = request.form["nm"]
        found_user = users.query.filter_by(name=user).delete()
        #if found_user:
            #found_user.delete()
            
    return render_template("manager.html", values=users.query.all())

@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email            
        else:
            usr = users(user, "", "")
            db.session.add(usr)
            db.session.commit()

        flash("Login Successful!")
        return redirect(url_for("user"))

    else:  
        if "user" in session:
            flash("You are already logged in!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved")

        else:
            if 'email' in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=8000)


