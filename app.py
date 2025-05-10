from asyncio.windows_events import NULL
from datetime import datetime
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,Response
from flask_mail import Mail,Message
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from bs4 import BeautifulSoup
import requests
import cv2
import requests
import os,sys
from contextlib import redirect_stderr, redirect_stdout
from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import numpy as np
import time

app=Flask(__name__)
name1=""
usernname1=""
email1=""
password1=""
username2=""

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='music'
app.config['MYSQL_CURSORCLASS']='DictCursor'

app.config.from_pyfile('config.cfg')
mail=Mail(app)

s=URLSafeTimedSerializer('secret123')

mysql=MySQL(app)

camera=cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier('D:/Emotion-based-Music-Recommendation-System/haarcascade_frontalface_default.xml')
classifier =load_model('D:/Emotion-based-Music-Recommendation-System/fer.h5')
emotion_labels = ['Angry','Fear','Happy','Neutral', 'Sad', 'Surprise']

def generate_frames():
    camera=cv2.VideoCapture(0) 
    while True:
        success,frame=camera.read()
        if not success:
            break
        else:
            capture_duration = 5
            start_time = time.time()
            while( int(time.time() - start_time) < capture_duration ):
                _, frame = camera.read()
                frame=cv2.flip(frame,1)
                labels = []
                gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

                for (x,y,w,h) in faces:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
                    roi_gray = gray[y:y+h,x:x+w]
                    roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                    if np.sum([roi_gray])!=0:
                        roi = roi_gray.astype('float')/255.0
                        roi = img_to_array(roi)
                        roi = np.expand_dims(roi,axis=0)
                        prediction = classifier.predict(roi)[0]
                        global label
                        label=emotion_labels[prediction.argmax()]
                        label_position = (x,y)
                        cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                        print(label)
                ret,buffer=cv2.imencode('.jpg',frame)
                frame=buffer.tobytes()
                cv2.waitKey(0)
                yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n\r\n')

class RegisterForm(Form):
	name=StringField('Name',[validators.Length(min=1,max=50)])
	username=StringField('Username',[validators.Length(min=4,max=25)])
	email=StringField('Email',[validators.Length(min=6,max=50)])
	password=PasswordField('Password',[validators.DataRequired(),validators.EqualTo('confirm',message='Password do not match')])
	confirm=PasswordField('confirm Password')

#to prevent using of app without login
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('unauthorised,please login','danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
@is_logged_in
def index():
    return render_template('index.html')

@app.route('/happy')
@is_logged_in
def happy():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'happy-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('happy.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('happy.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('happy.html',albu=albu3)

@app.route('/angry')
@is_logged_in
def angry():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'angry-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('angry.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('angry.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('angry.html',albu=albu3)


@app.route('/fear')
@is_logged_in
def fear():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'fear-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('fear.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('fear.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('fear.html',albu=albu3)

@app.route('/neutral')
@is_logged_in
def neutral():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'neutral-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('neutral.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('neutral.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('neutral.html',albu=albu3)


@app.route('/surprise')
@is_logged_in
def surprise():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'surprise-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('surprise.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('surprise.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('surprise.html',albu=albu3)

@app.route('/sad')
@is_logged_in
def sad():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'sad-eng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('sad.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('sad.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('sad.html',albu=albu3)

@app.route('/topeng')
@is_logged_in
def topeng():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'topeng%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('topeng.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('topeng.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('topeng.html',albu=albu3)

@app.route('/tophindi')
@is_logged_in
def tophindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'tophindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('tophindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('tophindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('tophindi.html',albu=albu3)

@app.route('/topmarathi')
@is_logged_in
def topmarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'topmarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('topmarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('topmarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('topmarathi.html',albu=albu3)

@app.route('/toppunjabi')
@is_logged_in
def toppunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'toppunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('toppunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('toppunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('toppunjabi.html',albu=albu3)

@app.route('/angrymarathi')
@is_logged_in
def angrymarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'angrymarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('angrymarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('angrymarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('angrymarathi.html',albu=albu3)

@app.route('/happymarathi')
@is_logged_in
def happymarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'happymarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('happymarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('happymarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('happymarathi.html',albu=albu3)

@app.route('/sadmarathi')
@is_logged_in
def sadmarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'sadmarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('sadmarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('sadmarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('sadmarathi.html',albu=albu3)

@app.route('/neutralmarathi')
@is_logged_in
def neutralmarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'neutralmarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('neutralmarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('neutralmarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('neutralmarathi.html',albu=albu3)

@app.route('/fearmarathi')
@is_logged_in
def fearmarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'fearmarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('fearmarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('fearmarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('fearmarathi.html',albu=albu3)

@app.route('/surprisemarathi')
@is_logged_in
def surprisemarathi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'surprisemarathi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('surprisemarathi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('surprisemarathi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('surprisemarathi.html',albu=albu3)

@app.route('/angryhindi')
@is_logged_in
def angryhindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'angryhindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('angryhindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('angryhindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('angryhindi.html',albu=albu3)

@app.route('/happyhindi')
@is_logged_in
def happyhindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'happyhindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('happyhindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('happyhindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('happyhindi.html',albu=albu3)

@app.route('/sadhindi')
@is_logged_in
def sadhindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'sadhindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('sadhindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('sadhindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('sadhindi.html',albu=albu3)

@app.route('/neutralhindi')
@is_logged_in
def neutralhindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'neutralhindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('neutralhindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('neutralhindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('neutralhindi.html',albu=albu3)

@app.route('/fearhindi')
@is_logged_in
def fearhindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'fearhindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('fearhindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('fearhindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('fearhindi.html',albu=albu3)

@app.route('/surprisehindi')
@is_logged_in
def surprisehindi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'surprisehindi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('surprisehindi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('surprisehindi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('surprisehindi.html',albu=albu3)

@app.route('/angrypunjabi')
@is_logged_in
def angrypunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'angrypunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('angrypunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('angrypunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('angrypunjabi.html',albu=albu3)

@app.route('/happypunjabi')
@is_logged_in
def happypunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'happypunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('happypunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('happypunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('happypunjabi.html',albu=albu3)

@app.route('/sadpunjabi')
@is_logged_in
def sadpunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'sadpunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('sadpunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('sadpunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('sadpunjabi.html',albu=albu3)

@app.route('/neutralpunjabi')
@is_logged_in
def neutralpunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'neutralpunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('neutralpunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('neutralpunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('neutralpunjabi.html',albu=albu3)

@app.route('/fearpunjabi')
@is_logged_in
def fearpunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'fearpunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('fearpunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('fearpunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('fearpunjabi.html',albu=albu3)

@app.route('/surprisepunjabi')
@is_logged_in
def surprisepunjabi():
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs_list WHERE album LIKE 'surprisepunjabi%'")
	albu3=cur.fetchall()
	result=cur.execute("SELECT * from songs WHERE user_id = %s",[session['id']])
	songs=cur.fetchall()
	if result>0:
		return render_template('surprisepunjabi.html',songs=songs,albu=albu3)
	else:
		songs=0
		return render_template('surprisepunjabi.html',albu=albu3,song=songs)
	cur.close()
	#    app.logger.info(albu[11]["path"]
	return render_template('surprisepunjabi.html',albu=albu3)


@app.route('/video')
@is_logged_in
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/register',methods=['GET','POST'])
def register():
	form =RegisterForm(request.form)
	if request.method=='POST' and form.validate():
		name=form.name.data
		email=form.email.data
		username=form.username.data
		password=sha256_crypt.encrypt(str(form.password.data))
		global usernname1,name1,email1,password1
		usernname1=username
		name1=name
		email1=email
		password1=password

		token=s.dumps(email,salt='email-confirm')

		msg=Message('Confirm Email',sender='akhil1.as42@gmail.com',recipients=[email])

		link=url_for('confirm_email',token=token,_external=True)

		msg.body='Your link is {}'.format(link)

		mail.send(msg)

		cur=mysql.connection.cursor()
		result=cur.execute("SELECT * FROM users WHERE username= %s",[username])
		result2=cur.execute("SELECT * FROM users WHERE email=%s",[email])
		if result>0:
			error='User name already exists,please try another user name'
			return render_template('register.html',form=form,error=error)
		if result2>0:
			error='Email already exists,please try another Email'
			return render_template('register.html',form=form,error=error)
		else:
			flash('A confirmation link has been sent to your email','success')
			return redirect(url_for('login'))

	return render_template('register.html',form=form)


#sendind the confirmation link to email
@app.route('/confirm_email/<token>')
def confirm_email(token):
	cur=mysql.connection.cursor()
	try:
		email=s.loads(token,salt='email-confirm',max_age=3600)
	except SignatureExpired:
		flash('The confirmation link is invalid or has expired.','danger')
	else:
		cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s,%s,%s,%s)",(name1,email1,usernname1,password1))
		
		
		mysql.connection.commit()
		cur.close()
		flash('Successfully verified','success')
	return redirect(url_for('login'))


#login
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		username=request.form['username']

		password_candidate=request.form['password']

		cur=mysql.connection.cursor()

		result=cur.execute("SELECT * FROM users WHERE username= %s",[username])

		if result>0:
			data=cur.fetchone()
			password=data['password']

			if sha256_crypt.verify(password_candidate,password):
				session['logged_in']=True
				session['username']=username
				session['id']=data['id']

				flash('login successful','success')
				return redirect(url_for('main'))
			else:
				error='wrong password'
			return render_template('login.html',error=error)
			cur.close()
		else:
			error='Username not found'
			return render_template('login.html',error=error)

	return render_template('login.html')



@app.route('/save_playlist/<string:ide>/<string:emo>')
@is_logged_in
def save(ide,emo):
	res=""
	playl=[]
	flag=0
	title="like"
	cur=mysql.connection.cursor()
	
	result=cur.execute("SELECT * FROM songs WHERE user_id= %s and _songs= %s",([session['id']],ide))
	
	if result>0:
			flash("songs already exist",'danger')
			return redirect(url_for(emo))
	else:
		cur.execute("INSERT INTO songs(title,_songs,user_id) VALUES(%s,%s,%s)",(title,ide,[session['id']]))

	

		mysql.connection.commit()

	cur.close()
	flash("Song is added to liked playlist",'success')
	return redirect(url_for(emo))

#logout
@app.route('/logout')
def logout():
	session.clear()
	flash('you are now logout','success')
	return redirect(url_for('login'))




@app.route('/play_playlist')
@is_logged_in
def play_playlist():
	res=""
	playl=[]
	data=[]
	title="like"
	cur=mysql.connection.cursor()
	cur.execute("SELECT * FROM songs WHERE user_id= %s and title= %s",([session['id']],title))
	results=cur.fetchall()
	
	if results is None:
		flash("no song in playlist",'danger')
		return redirect(url_for('main'))
	else:
		cur.execute("SELECT _songs FROM songs WHERE user_id= %s and title= %s",([session['id']],title))
		result=cur.fetchall()
		length=len(result)
		for i in result:
				val=i['_songs']
				print(val)
				cur.execute("SELECT * FROM songs_list WHERE id=%s",[i['_songs']])
				data.append(cur.fetchone())
		return render_template('liked_songs.html',albu=data,len=length)

@app.route('/delete_song/<string:idd>')
@is_logged_in
def delete_song(idd):
	cur=mysql.connection.cursor()
	cur.execute("delete  FROM songs WHERE _songs =%s",[idd])
	mysql.connection.commit()
	
	
	cur.close()
	flash("song successfully deleted",'success')

	return redirect(url_for('play_playlist'))


## Code for displaying Videos or Music ##
@app.route('/result',methods = ["POST", "GET"])
def result():
        
        try:
            label
        except NameError:
            return Response("Emotion was not detected properly")
        else:
            input=[]
            input=label
            print(input)
                    

            if input=='Happy':
                return redirect(url_for('happy'))
                
            elif input=='Sad':
                return redirect(url_for('sad'))
                    
            elif input=='Neutral':
                return redirect(url_for('neutral'))
                    
            elif input=='Angry':
                
                return redirect(url_for('angry'))
            elif input=='Surprise':
                
                return redirect(url_for('surprise'))
            elif input=='Fear':
                          
                return redirect(url_for('fear'))
            else:
                return Response("emotion not matched")
            



        
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)