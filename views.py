from flask import Blueprint, render_template, request, flash, redirect, url_for
import os
from utils.process_candidates import process_candidates
views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@ views.route("/about")
def about():
    return render_template("about.html")

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('pdf_files')

        for file in uploaded_files:
            if file.filename != '':
                file_path = os.path.join('static/candidate_files/', file.filename)
                file.save(file_path)
            else:
                flash('No file selected or something went wrong.')
                return redirect(url_for('views.upload')) 

        flash('File uploaded successfully.')
        return redirect(url_for('views.result'))
    
    else:
        return render_template("upload.html")

@views.route("/result")
def result():
    folder_path = os.path.abspath("./static/candidate_files")
    candidate_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]
    process_candidates(candidate_files)
    return render_template("result.html")