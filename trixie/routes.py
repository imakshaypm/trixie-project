import codecs
import io, base64
import random
from PIL import Image
import io
import os
from PIL import Image 
from trixie import app, mongo, bcrypt, login_manager, grid_fs
from flask import make_response, render_template, url_for, request, flash, redirect, session
from trixie.resume_screening import resumes
from trixie.keywordExtractor import keywords
from trixie.emotion import em_predict
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from trixie.froms import User
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

#JOBLISTINGS
@app.route("/interview_list")
@login_required
def interview_list():
    job_list = []
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    resume_id = grid_fs.get(user['resume_id'])
    with open('resume.docx', 'wb+') as output:
        output.write(resume_id.read())
    jobs = mongo.db.JobListings.find({})
    for document in jobs:
        resume_score = document['resume_score']
        selected = document['selected_candidates']
        attented = document['attented_candidates']
        desc_id = grid_fs.get(document['desc_id'])
        with open('description.docx', 'wb+') as output:
            output.write(desc_id.read())
        result = str(resumes('resume.docx', 'description.docx'))
        if result >= resume_score and user['_id'] not in selected and user['_id'] not in attented:
            job_list.append(document)
    return render_template('interview_list.html', title = 'Interview Lists', job_list = job_list)

#FIRST Round
@app.route("/interview/<job_id>", methods=['GET', 'POST'])
@login_required
def interview(job_id):
    que = []
    job = mongo.db.JobListings.find_one({"_id": ObjectId(job_id)})
    qestions = mongo.db.InterviewQuestions.find_one({"_id": ObjectId(job['question'])})
    
    for question in qestions:
        if question != '_id':
            que.append(question)
    return render_template('interview.html', title = 'First Round', job = job, job_id = job_id, question = que)

keys = []
@app.route("/interview_keyword", methods=['GET', 'POST'])
@login_required
def interview_answer():
    # if request.is_json: #You have to add contentType application/json in ajax post request to get true
    if request.method == 'GET':
            pass
    if request.method == 'POST':
        if request.is_json:
            answer=request.json['answer']
            keyword = keywords(answer)
            keys.append(keyword[0])
    print('Keywords', keys)
    return render_template('interview_answer.html', title = 'Answer')

#SECOND ROUND
keyw = mongo.db.KeywordQuestions.find_one({"_id": ObjectId('645b065144e9af71e75e6477')})
keyw.pop("_id")
@app.route("/interview_second/<job_id>", methods=['GET', 'POST'])
@login_required
def interview_second(job_id):
    second_round = []
    job = mongo.db.JobListings.find_one({"_id": ObjectId(job_id)})
    if len(keys) <= 5:
        for i in range(6):
            q_arr = random.choice([arr for arr in keyw.keys()])
            q = random.choice(keyw[q_arr])
            second_round.append(q)
            index = keyw[q_arr].index(q)
            del(keyw[q_arr][index])
            i = i + 1
    else:
        for k in keys:
            if len(second_round) <= 5:
                if k in keyw:
                    q = random.choice(keyw[q_arr])
                    second_round.append(q)
                    index = keyw[q_arr].index(q)
                    del(keyw[q_arr][index])
                else:
                    q_arr = random.choice([arr for arr in keyw.keys()])
                    q = random.choice(keyw[q_arr])
                    second_round.append(q)
                    index = keyw[q_arr].index(q)
                    del(keyw[q_arr][index])
    print("Questions", second_round)
    return render_template('interview_second.html', title = "Second Round", job = job, job_id = job_id, question = second_round)

r1_reaction = []
r2_reaction = []
@app.route("/interview_reaction", methods=['GET', 'POST'])
@login_required
def interview_keyword():
    if request.values['round'] == 'First Round':
        image_b64 = request.values['imageBase64']
        im = Image.open(io.BytesIO(base64.b64decode(image_b64.split(',')[0])))
        im.save("image.png")
        result = em_predict()
        print(result)
        r1_reaction.append(result)
    else:
        image_b64 = request.values['imageBase64']
        im = Image.open(io.BytesIO(base64.b64decode(image_b64.split(',')[0])))
        im.save("image.png")
        result = em_predict()
        r2_reaction.append(result)
    return render_template('interview_answer.html', title = 'Reaction')

@app.route("/interview_finish/<job_id>", methods=['GET', 'POST'])
@login_required
def interview_finish(job_id):
    result = False
    job = mongo.db.JobListings.find_one({"_id": ObjectId(job_id)})
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    score = [{"Angry": 3}, {"Disgusted": 2}, {"Fearful": 1}, {"Happy": 7}, {"Neutral": 5}, {"Sad": 4}, {"Surprised": 6}]
    print("Reactions", r1_reaction, r2_reaction)
    print('Keywords', keys)
    round_1 = most_common(r1_reaction)
    round_2 = most_common(r2_reaction)
    keys.clear()
    r1_reaction.clear()
    r2_reaction.clear()
    for x in score:
        if round_1 in x.keys():
            r1_score = x[round_1]
        if round_2 in x.keys():
            r2_score = x[round_2]
    final_score = max(r1_score, r2_score)
    interview_score = int(job['interview_score'])
    if interview_score <= final_score:
        result = True
        mongo.db.JobListings.update_one({'_id': ObjectId(job_id)}, {'$push': {"selected_candidates": ObjectId(user['_id'])}})
        mongo.db.JobListings.update_one({'_id': ObjectId(job_id)}, {'$push': {"attented_candidates": ObjectId(user['_id'])}})
    else:
        result = False
        mongo.db.JobListings.update_one({'_id': ObjectId(job_id)}, {'$push': {"attented_candidates": ObjectId(user['_id'])}})
    return render_template('interview_finish.html', title = 'Final Result', result = result, final_score = final_score)

def most_common(lst):
    return max(set(lst), key=lst.count)

#USER DASHBOARD
@app.route("/dashboard_user")
def dashboard_user():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    image = grid_fs.get(user['profile_id'])
    base64_data = codecs.encode(image.read(), 'base64')
    image = base64_data.decode('utf-8')
    top_3_c = list(user['top_3_resume_screening'])[1:4]
    print(top_3_c)
    return render_template('dashboard_user.html', title = 'User', user = user, top_3_c = top_3_c, img = image)

#COMPANY DASHBOARD
@app.route("/dashboard_company")
def dashboard_company():
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    image = grid_fs.get(company['profile_id'])
    base64_data = codecs.encode(image.read(), 'base64')
    image = base64_data.decode('utf-8')
    jobs = list(mongo.db.JobListings.find({'company_username': company['username']}))
    jobs = jobs[::-1]
    job_lists = len(list(company['job_lists']))
    # top_3_c = list(user['top_3_resume_screening'])[1:4]
    return render_template('dashboard_company.html', title = 'Company', company = company, job_lists = job_lists, jobs = jobs, img = image)

@app.route("/selected_candidates/<job_id>")
def selected_candidate(job_id):
    p_candidates = []
    job = mongo.db.JobListings.find_one({'_id': ObjectId(job_id)})
    candidates = job['selected_candidates']
    for obj in candidates:
        user = mongo.db.Users.find_one({"_id": ObjectId(obj)})
        image = grid_fs.get(user['profile_id'])
        base64_data = codecs.encode(image.read(), 'base64')
        image = base64_data.decode('utf-8')
        user.update({"profile_id" : image})
        p_candidates.append(user)
    return render_template('selected_candidates.html', title = 'Selected Candidates', p_candidates = p_candidates)

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
            result = resumes(isthisFile, 'trixie/upload/description.docx')
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
        dp = request.files['image']
        profile_id = grid_fs.put(dp, content_type=dp.content_type, filename=dp.filename)
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
                "profile_id": profile_id,
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
        dp = request.files['image']
        profile_id = grid_fs.put(dp, content_type=dp.content_type, filename=dp.filename)
        resume = request.files['resume']
        resume_id = grid_fs.put(resume, content_type=resume.content_type, filename=resume.filename)
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
                "profile_id": profile_id,
                "resume_id": resume_id,
                "interview_list": []
            })
            return redirect(url_for('login_u'))
        else:
            flash("Username already exists", 'danger')
    return render_template('employee.html', title = 'New Employee')

@app.route("/edit_user_profile", methods=['GET', 'POST'])
def edit_user():
    user = mongo.db.Users.find_one({"username": current_user.get_id()})
    if request.method == "POST":
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        h_password = mongo.db.Users.find_one({"email": email}, {"password": 1, "_id": 0})
        if user and bcrypt.check_password_hash(h_password["password"], old_password):
            dp = request.files['image']
            resume = request.files['resume']
            employee_name = request.form.get("employee-name")
            username = request.form.get("username")
            if not mongo.db.Users.find_one({"username": username}):
                mongo.db.Users.update_many({"username": user['username']})
            else:
                flash("Username already exist", 'success')
            mongo.db.Users.update_many({"name": employee_name})
            if resume:
                profile_id = grid_fs.put(dp, content_type=dp.content_type, filename=dp.filename)
                mongo.db.Users.update_many({"username": user['username']}, {"$set" : {"profile_id" : profile_id}})
        
            if dp:
                resume_id = grid_fs.put(resume, content_type=resume.content_type, filename=resume.filename)
                mongo.db.Users.update_many({"username": user['username']}, {"$set" : {"resume_id": resume_id}})
        else:
            flash("Password is incorrect", 'danger') 
    return render_template('edit_user.html', title = 'Search', user = user)

#JOB LISTING
@app.route("/job_lists", methods=['GET', 'POST'])
def job_lists():
    jobs = []
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    job_list = company['job_lists']
    for job in job_list:
        jobs.append(mongo.db.JobListings.find_one({"_id": job}))
    return render_template('job_lists.html', title = 'Job Lists', job_list = jobs)

#ADD JOBS
@app.route("/add_job", methods=['GET', 'POST'])
def add_job():
    company = mongo.db.Company.find_one({"username": current_user.get_id()})
    if request.method == "POST":
        position = request.form.get("position")
        desctription = request.files['desctription']
        type = request.form.get("type")
        date = request.form.get("date")
        resume_score = request.form.get("resume_score")
        salary = request.form.get("salary")
        last_date = request.form.get("last_date")
        interview_score = request.form.get("interview_score")
        location = request.form.get("location")
        desc_id = grid_fs.put(desctription, content_type=desctription.content_type, filename=desctription.filename)
        x = mongo.db.JobListings.insert_one({
            "company_username": company['username'],
            "company_name": company['name'],
            "position": position,
            "desc_id": desc_id,
            "location": location,
            "type": type,
            "date": date,
            "resume_score": resume_score,
            "salary": salary,
            "last_date": last_date,
            "interview_score": interview_score,
            'selected_candidates':[],
            "attented_candidates":[]
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
