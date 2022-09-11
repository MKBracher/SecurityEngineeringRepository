from re import S
from flask import Blueprint, render_template, request,jsonify,redirect,url_for
import sqlite3

views = Blueprint(__name__, "views")

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("db.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@views.route("/",methods=["GET","POST"])
def home():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor = conn.execute("SELECT * FROM database")
        test = [
            dict(id=row[0], username=row[1], password=row[2], website=row[3])
            for row in cursor.fetchall()
        ]
        if test is not None:
            return jsonify(test)

    if request.method == "POST":
        new_username = request.form["Username"]
        new_password = request.form["Password"]
        new_website = request.form["Website"]
        sql = """INSERT INTO database (username, password, website)
            VALUES(?,?,?)"""

        cursor = cursor.execute(sql, (new_username, new_password, new_website))
        conn.commit()
        return f"test id {cursor.lastrowid} created successfully "

    if request.method == "DELETE":
        sql = """DELETE FROM database WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
    
    return render_template("index.html", name = "Matt")

    

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/json")
def get_json():
    return jsonify({'name':'tim','coolness':10})

@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

@views.route('/addRegion', methods=['POST'])
def addRegion():
    return (request.form['Username'])


@views.route('/delete/<int:id>')
def delete(id):
    return render_template("index.html", name = "Matt")



    
    
