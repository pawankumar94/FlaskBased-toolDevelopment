
from flask import Flask, redirect, url_for, render_template, request, session,flash,g,send_from_directory
from datetime import timedelta
import subprocess
from werkzeug.utils import secure_filename
import os
import datetime
import urllib.request
import uuid

app = Flask(__name__,template_folder=r'C:\Users\Pawan\Desktop\Flask\venv\pawankumar94\app\Template')
app.permanent_session_lifetime = timedelta(minutes=1)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = r'C:\Users\Pawan\Desktop\Flask\venv\pawankumar94\app\filename'

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home(): 
    return render_template('try.html')

def makefolder():
    user = request.form["name"]
    session["user"] = user 
    os.chdir(r'C:\Users\Pawan\Desktop\Flask\venv\pawankumar94\app\Template')
    newfolder = user
    os.makedirs(newfolder)
    return newfolder


@app.route('/login' , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user 
        return redirect(url_for("user"))

    return render_template('login.html')

@app.before_request
def before_request():
    g.user = None
    if "user" in session:
        g.user = session["user"]
        

@app.route('/user' )
def user():
    if g.user:
        user = g.user
        return f"<h1> Welcome {user}</h1>"'<br>' + \
                "<b><a href = '/uploader'> Click here to uploads the files </a></b>"
    
    return redirect(url_for("login"))

@app.route('/uploader')
def uploader():
    return render_template('upload1.html')


@app.route('/upload',methods=['POST'])
def upload():
    if g.user:
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        directory = g.user
        path = os.path.join(app.config['UPLOAD_FOLDER'],directory)
        try:
            os.makedirs(path, exist_ok = True) 
        except OSError as error:
            print("Directory '%s' can not be created") 
        
        for file in uploaded_files:
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(path, filename))
                filenames.append(filename)
            
        return render_template('upload2.html', filenames=filenames)
    return redirect(url_for("login"))
    

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
       
    
@app.route("/logout")
def logout():   
    session.pop("pawan", None)#pops out the key value of the session , if the is not present then it will print none
    return redirect(url_for("login"))


if __name__ == "__main__":
    	app.run(debug=True)
    

