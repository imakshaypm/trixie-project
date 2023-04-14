import json
import os
from trixie import app, mongo, bcrypt, login_manager
from flask import jsonify, render_template, abort, url_for, request, flash, redirect
from trixie.resume_screening import resumes
from flask_login import login_user, UserMixin, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from trixie.froms import User


@login_manager.user_loader
def load_user(username):
    u = mongo.db.Users.find_one({"username": username})
    if not u:
        return None
    return User(username=u['username'])
    # return User(mongo.db.Users.find_one({'username': username}, {}))

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login_category", methods=['GET', 'POST'])
def login_category():
    return render_template('login_category.html', title = 'Login')

@app.route("/login_category/login_u", methods=['GET', 'POST'])
def login_u():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_user'))
    # form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        user = mongo.db.Users.find_one({"email": email})
        password = request.form.get("password")
        h_password = mongo.db.Users.find_one({"email": email}, {"password": 1, "_id": 0})
        if user and bcrypt.check_password_hash(h_password["password"], password):
            loginuser = User(user['username'])
            print(loginuser)
            login_user(loginuser)
            next_page = request.values.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Invalid username and password", 'danger')
    return render_template('login_u.html', title = 'Login User')

@app.route("/login_category/login_c", methods=['GET', 'POST'])
def login_c():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_company'))
    # form = LoginForm()
    if request.method == "POST":
        email = request.form.get("email")
        company = mongo.db.Company.find_one({"email": email})
        password = request.form.get("password")
        h_password = mongo.db.Company.find_one({"email": email}, {"password": 1, "_id": 0})
        if company and bcrypt.check_password_hash(h_password["password"], password):
            loginuser = User(company)
            login_user(loginuser)
            next_page = request.values.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Invalid username and password", 'danger')
    return render_template('login_c.html', title = 'Login Company')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/interview", methods=['GET', 'POST'])
@login_required
def interview():
    if request.is_json: #You have to add contentType application/json in ajax post request to get true
        if request.method == 'GET':
            #seconds = time()
            #return jsonify({'seconds' : seconds})
            pass
        
        if request.method == 'POST':
            #record = speech_rec()
            text = json.loads(request.data).get('data') # .forms or .json
            print(text)

    return render_template('interview.html', title = 'Interview')

@app.route("/dashboard_user")
def dashboard_user():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    top_3_c = list(user['top_3_resume_screening'])[1:4]
    print(top_3_c)
    return render_template('dashboard_user.html', title = 'User', user = user, top_3_c = top_3_c)

@app.route("/resume", methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        isthisFile = request.files['file']
        filename = secure_filename(isthisFile.filename)
        mongo.save_file(isthisFile.filename, isthisFile)
        users = mongo.db.Users.insert_one({"resume": isthisFile.filename})
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
        if file_ext not in ['.doc', '.docx']:
            flash("Please select doc or docx file", 'danger')
            return redirect(url_for('resume'))
        else:
            print("true")
            job = request.form.get('job')
            company = request.form.get('company')
            print(job, company)
            result = resumes(isthisFile, 'trixie/upload/python-job-description.docx')
            return render_template('resume_result.html', title = 'Resume Result', final=result)
        #text = json.loads(request.data) # .forms or .json
        #print()
        #if result:
            #users = mongo.db.Users.insert_one({"online": True})
            #for doc in users:
            #   print(doc) 
        #print(text['clicked'])
    return render_template('resume.html', title = 'Resume')

#Works Very Well Dont Touch It!!!!!!
@app.route("/resume_result", methods=['GET', 'POST'])
def resume_result():
    return render_template('resume_result.html', title = 'Resume Result')


@app.route("/signup/company", methods=['GET', 'POST'])
def company():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_user'))
    if request.method == "POST":
        comapny_name = request.form.get("comapny-name")
        comapny_email = request.form.get("comapny-email")
        gst_number = request.form.get("gst-number")
        password = request.form.get("password")
        h_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if not mongo.db.Company.find_one({"gst_number": gst_number}):
            mongo.db.Company.insert_one({"comapny_name": comapny_name,
                                        "email" : comapny_email,
                                        "gst_number" : gst_number,
                                        "password" :h_password})
            return redirect(url_for('login_c'))
        else:
            flash("Company already exist", 'danger')
        #print(email, password)
    return render_template('company.html', title = 'New Company')

@app.route("/signup/employee", methods=['GET', 'POST'])
def employee():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_user'))
    if request.method == "POST":
        employee_name = request.form.get("employee-name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        h_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if not mongo.db.Users.find_one({"email": email}):
            mongo.db.Users.insert_one({"name": employee_name,
                                        "username": username,
                                        "email": email,
                                        "password": h_password,
                                        "interview_got": 0,
                                        "interview_attented": 0,
                                        "resume_score": 0,
                                        "points": 0,
                                        "top_3_resume_screening": {
                                            "": 0,
                                            "": 0,
                                            "": 0
                                        },
                                         "top_3_interview_performance": {
                                            "": 0,
                                            "": 0,
                                            "": 0
                                        } })
            return redirect(url_for('login_u'))
        else:
            flash("Username already exists", 'danger')
    return render_template('employee.html', title = 'New Employee')

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', title = 'Search')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
