import json
import os
from trixie import app, mongo, bcrypt, login_manager
from flask import render_template, url_for, request, flash, redirect, session
from trixie.resume_screening import resumes
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from trixie.froms import User
from PIL import Image
from bson import  ObjectId


@login_manager.user_loader
def load_user(username):
    u = mongo.db.Users.find_one({"username": username}) or mongo.db.Company.find_one({"username": username})
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
            loginuser = User(company['username'])
            login_user(loginuser)
            next_page = request.values.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Invalid username and password", 'danger')
    return render_template('login_c.html', title = 'Login Company')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/interview_list")
@login_required
def interview_list():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})

    return render_template('interview_list.html', title = 'Interview Lists')

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

#USER DASHBOARD
@app.route("/dashboard_user")
def dashboard_user():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    top_3_c = list(user['top_3_resume_screening'])[1:4]
    print(top_3_c)
    return render_template('dashboard_user.html', title = 'User', user = user, top_3_c = top_3_c)

#COMPANY DASHBOARD
@app.route("/dashboard_company")
def dashboard_company():
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    job_lists = len(list(company['job_lists']))
    # top_3_c = list(user['top_3_resume_screening'])[1:4]
    return render_template('dashboard_company.html', title = 'Company', company = company, job_lists = job_lists)

@app.route("/resume", methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        isthisFile = request.files['file']
        filename = secure_filename(isthisFile.filename)
        mongo.save_file(isthisFile.filename, isthisFile)
        mongo.db.Users.insert_one({"resume": isthisFile.filename})
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

#COMPANY REGISTRATION
@app.route("/signup/company", methods=['GET', 'POST'])
def company():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_user'))
    if request.method == "POST":
        comapny_name = request.form.get("comapny-name")
        comapny_email = request.form.get("comapny-email")
        username = request.form.get("username")
        password = request.form.get("password")
        h_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if not mongo.db.Company.find_one({"username": username}):
            mongo.db.Company.insert_one({
                "name": comapny_name,
                "email" : comapny_email,
                "username" : username,
                "password" :h_password,
                "profile_pic": "",
                "job_lists": []
            })
            return redirect(url_for('login_c'))
        else:
            flash("Company already exist", 'danger')
        #print(email, password)
    return render_template('company.html', title = 'New Company')

#USER REGISTRATION
@app.route("/signup/employee", methods=['GET', 'POST'])
def employee():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_user'))
    if request.method == "POST":
        profile_image = "../static/profile_pics/pngegg.png"
        filename = secure_filename(profile_image.filename)
        mongo.save_file(profile_image.filename, profile_image)
        employee_name = request.form.get("employee-name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        h_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if not mongo.db.Users.find_one({"email": email}):
            mongo.db.Users.insert_one({
                "name": employee_name,
                "username": username,
                "email": email,
                "password": h_password,
                "profile_picture": "",
                "interview_got": 0,
                "interview_attented": 0,
                "resume_score": 0,
                "points": 0,
                "top_3_resume_screening": [],
                "top_3_interview_performance": [],
                "interview_list": []
            })
            return redirect(url_for('login_u'))
        else:
            flash("Username already exists", 'danger')
    return render_template('employee.html', title = 'New Employee')

@app.route("/file/<path:filename>", methods = ['GET', 'POST'])
def file(filename):
    return mongo.send_file(filename)

@app.route("/edit_user_profile", methods=['GET', 'POST'])
def edit_user():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    # image = mongo.send_file(user['profile_picture'])
    # print("hai",user['profile_picture'])
    if request.method == "POST":
        isthisFile = request.files['file']
        filename = secure_filename(isthisFile.filename)
        mongo.save_file(isthisFile.filename, isthisFile)
        employee_name = request.form.get("employee-name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        mongo.db.Users.update_many({"username": user['username']}, {"$set" : {"profile_picture" : isthisFile.filename}})
    return render_template('edit_user.html', title = 'Search', user = user)

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html', title = 'Search')

#JOB LISTING
@app.route("/job_lists", methods=['GET', 'POST'])
def job_lists():
    jobs = []
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    job_list = company['job_lists']
    job_list.pop(0)
    for job in job_list:
        jobs.append(mongo.db.JobListings.find_one({"_id": job}))
    return render_template('job_lists.html', title = 'Job Lists', job_list = jobs)

#ADD JOBS
@app.route("/add_job", methods=['GET', 'POST'])
def add_job():
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    if request.method == "POST":
        position = request.form.get("position")
        desctription = request.form.get("desctription")
        type = request.form.get("type")
        date = request.form.get("date")
        resume_score = request.form.get("resume_score")
        salary = request.form.get("salary")
        last_date = request.form.get("last_date")
        interview_score = request.form.get("interview_score")
        location = request.form.get("location")
        x = mongo.db.JobListings.insert_one({
            "company_username": company['username'],
            "company_name": company['name'],
            "position": position,
            "desctription": desctription,
            "location": location,
            "type": type,
            "date": date,
            "resume_score": resume_score,
            "salary": salary,
            "last_date": last_date,
            "interview_score": interview_score
        })
        mongo.db.Company.update_one({"username": current_user.get_id()}, {"$push" : {"job_lists": x.inserted_id}})
        flash("Job Added to Database", 'success')
        session['object_id'] = str(x.inserted_id)
        return redirect(url_for('question'))
    return render_template('add_job.html', title = 'Add Job')


@app.route("/question", methods=['GET', 'POST'])
def question():
    if request.method == "POST":
        question_1 = request.form.get("question-1")
        answer_1 = request.form.get("answer-1")
        question_2 = request.form.get("question-2")
        answer_2 = request.form.get("answer-2")
        question_3 = request.form.get("question-3")
        answer_3 = request.form.get("answer-3")
        question_4 = request.form.get("question-4")
        answer_4 = request.form.get("answer-4")
        question_5 = request.form.get("question-5")
        answer_5 = request.form.get("answer-5")
        x = mongo.db.InterviewQuestions.insert_one({
            question_1: answer_1,
            question_2: answer_2,
            question_3: answer_3,
            question_4: answer_4,
            question_5: answer_5,
        })
        mongo.db.JobListings.update_many({"_id": ObjectId(session['object_id'])}, {"$set" : {"question": x.inserted_id}})
        print(session['object_id'])
        flash("Successfully added the job", 'success')
        return redirect(url_for('dashboard_company'))
    return render_template('question.html', title = 'Question')

@app.route("/logout")
def logout():
    logout_user()
    flash("Logged Out", 'success')
    return redirect(url_for('home'))
