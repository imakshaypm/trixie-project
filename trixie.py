import json
from time import time
from flask import Flask, jsonify, render_template, url_for, request, Response, flash
app = Flask(__name__)


'''global capture,rec_frame, data, grey, switch, neg, face, rec, out, audio, reco
capture=0
grey=0
neg=0
face=0
switch=1
rec=0
audio = 0'''

'''def gen_frames(): 
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            detector = cv2.CascadeClassifier('Haarcascades/haarcascade_frontalface_default.xml')
            eye_cascade = cv2.CascadeClassifier('Haarcascades/haarcascade_eye.xml')
            faces = detector.detectMultiScale(frame, 1.33, 5)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #Drawing rectangle around the face and eyes
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')'''

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
            seconds = time()
            return jsonify({'seconds' : seconds})
        
        if request.method == 'POST':
            #record = speech_rec()
            text = json.loads(request.data).get('data') # .forms or .json
            print(text)

    return render_template('interview.html', title = 'Interview')

@app.route("/dashboard_user")
def dashboard_user():
    return render_template('dashboard_user.html', title = 'User')


if __name__ == '__main__':
    app.run(debug=True)