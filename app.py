# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, session, url_for
from flask_pymongo import PyMongo
import os

# -- Initialization section --
app = Flask(__name__)
app.secret_key = os.getenv('session_secret_key')
# name of database
app.config['MONGO_DBNAME'] = 'upperline'

# URI of database
app.config['MONGO_URI'] = os.getenv('mongo_URI')
mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    if session:
        print("testing session") 
        currentuser = session['username']
        users = mongo.db.users
        userslist = users.find({})
        userclass = users.find_one({'username':currentuser})['classyear']
        classusers = users.find({'classyear':userclass}).sort('lastname')
        return render_template('index.html', users = userslist, classusers = classusers)
    else:
        print("testing else session")
        return render_template('index.html')

# SIGNUP PAGE
@app.route('/signup', methods=['GET', 'POST'])

def signup():
    if request.method == "GET":
        return render_template('signup.html')
    else:
        username = request.form["username"]
        password = request.form["password"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        classyear = request.form["class-year"]
        highschool = request.form["high-school"]
         
        users = mongo.db.users
        existing_user = users.find_one({'username': username})

        #not sure when to use is vs ==
        if existing_user == None:
            users.insert({"username":username, "password":password, "firstname":firstname, "lastname":lastname, "classyear":classyear, "highschool": highschool})
            session['username'] = username
            session['firstname'] = firstname
            return redirect("/")
        
        error = "That username is taken. Try logging in instead or using a different username."
        return render_template('signup.html', error = error)

@app.route('/login', methods=['GET', 'POST'])

def login():
    users = mongo.db.users
    username = request.form["username"]
    password = request.form["password"]
    user_login = users.find_one({'username': username})

    if user_login:
        if password == user_login['password']:
            firstname = user_login['firstname']
            session['username'] = username
            session['firstname'] = firstname
            return redirect('/')
        else:
            error1 = "That's not the correct password."
            return render_template('index.html', error = error1)
    
    error1 = "That username does not exist. Try making an account instead."
    return render_template('index.html', error = error1)


@app.route('/logout')

def logout():
    session.clear()
    return redirect("/" )

# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    user = mongo.db.users
    # insert new data
    user.insert({'name':'Thor', 'birthday':'1988-06-28'})
    # return a message to the user
    return "Added User!"
