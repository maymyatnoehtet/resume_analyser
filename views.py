from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import os
from utils.process_candidates import process_candidates
from collections import OrderedDict

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
        job_requirements  = request.form.get('longText')
        session['job_requirements'] = job_requirements
        print(session['job_requirements'])

        if not job_requirements:
            flash('Job requirement is empty!')
            return redirect(url_for('views.upload')) 
        
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
    
# 
def remove_files_from_directory(directory):
    try:
        for file in os.listdir(directory):
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("All files in the directory have been removed.")
    except Exception as e:
        print(f"An error occurred: {e}")


@views.route("/result")
def result():
    folder_path = os.path.abspath("./static/candidate_files")
    candidate_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, filename))]
    if 'job_requirements' in session:
        candidate_scores, failed_candidates = process_candidates(candidate_files, session.get('job_requirements'))
    
    remove_files_from_directory(folder_path)
    ordered_by_values = OrderedDict(sorted(candidate_scores.items(), key=lambda item: item[1], reverse=True))
    return render_template("result.html", candidate_scores=ordered_by_values)