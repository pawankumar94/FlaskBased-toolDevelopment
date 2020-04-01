
from flask import Flask, redirect, url_for, render_template, request, session,flash,g,send_from_directory
from datetime import timedelta
import subprocess
from werkzeug.utils import secure_filename
import os
import datetime as dt
import urllib.request
import uuid,shutil,time
from pathlib import Path

app = Flask(__name__,template_folder=Path(r'env\Scripts\static').resolve())
app.permanent_session_lifetime = timedelta(minutes=1)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]iasdfffsd/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
app.config['UPLOAD_FOLDER'] = Path(r'env\filename').resolve()
path= Path(r'env\filename').resolve()

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home(): 
    return render_template('try.html')

def makefolder():
    user = request.form["name"]
    session["users"] = user 
    os.chdir(path)
    newfolder = user
    os.makedirs(newfolder)
    return newfolder 


@app.route('/login' , methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["users"] = user 
        return redirect(url_for("user"))

    return render_template('login.html')

@app.before_request
def before_request():
    g.user = None
    if "users" in session:
        g.user = session["users"]
        
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

def delete():
    seconds= time.time() - (3600)
    if os.path.exists(path):
        for root_folder, folders, files in os.walk(path):

            for folder in folders:
                folder_path = os.path.join(root_folder, folder)
                if seconds >= get_file_or_folder_age(folder_path):
                    remove_folder(folder_path)
                        
                   
    else:
        print(f'"{path}" is not found')

def remove_folder(path):
	if not shutil.rmtree(path):
		print(f"{path} is removed successfully")

	else:
		print(f"Unable to delete the {path}")


def get_file_or_folder_age(path):
	ctime = os.stat(path).st_ctime
	return ctime


@app.route('/upload',methods=['POST'])
def upload():
    if g.user:
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        path = os.path.join(app.config['UPLOAD_FOLDER'],str(uuid.uuid4().hex))
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
    session.pop("users", None)
    return redirect(url_for("login"))



def main():
    delete()
    app.debug = True
    app.run()
    

if __name__ == "__main__":
    main()
    
    	
       

