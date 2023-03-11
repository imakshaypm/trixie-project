import json
import os
from trixie import app
from flask import jsonify, render_template, abort, url_for, request, Response, flash, redirect
from trixie.resume_screening import resumes
from werkzeug.utils import secure_filename

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template('login.html', title = 'Login')

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/interview", methods=['GET', 'POST'])
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
    return render_template('dashboard_user.html', title = 'User')

@app.route("/resume", methods=['GET', 'POST'])
def resume():
    if request.method == 'POST':
        isthisFile = request.files['file']
        filename = secure_filename(isthisFile.filename)
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


@app.route("/signup_category", methods=['GET', 'POST'])
def signup_category():
    return render_template('signup_category.html', title = 'New User')
