from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import os
import requests
from utils.process_candidates import process_candidates
from collections import OrderedDict
from dotenv import load_dotenv
import base64

views = Blueprint("views", __name__)
load_dotenv()

# Retrieve data from .env file
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")

@ views.route("/about")
def about():
    return render_template("about.html")

# Upload pdf files
@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        job_requirements = request.form.get('longText')
        session['job_requirements'] = job_requirements
        print(session['job_requirements'])

        if not job_requirements:
            flash('Job requirement is empty!')
            return redirect(url_for('views.upload'))

        uploaded_files = request.files.getlist('pdf_files')

        for file in uploaded_files:
            if file.filename != '':
                pdf_content = file.read()
                upload_to_github(file.filename, pdf_content)
            else:
                flash('No file selected or something went wrong.')
                return redirect(url_for('views.upload'))

        flash('File uploaded successfully.')
        return redirect(url_for('views.result'))

    else:
        return render_template("upload.html")

# Upload files to github
def upload_to_github(filename, content):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/static/candidate_files/{filename}'

    data = {
        'message': f'Add {filename}',
        'content': base64.b64encode(content).decode(),
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f'Successfully uploaded {filename} to GitHub.')
    else:
        print(f'Failed to upload {filename} to GitHub. Status code: {response.status_code}')
        print(response.json())

# Delete files from Github that we upload
def remove_files_from_github():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    folder_path = 'static/candidate_files'
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{folder_path}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        for file_info in files:
            if 'name' in file_info and 'sha' in file_info:
                file_name = file_info['name']
                file_sha = file_info['sha']
                delete_url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{folder_path}/{file_name}'
                data = {
                    'message': f'Remove {file_name}',
                    'sha': file_sha,
                }
                response = requests.delete(delete_url, headers=headers, json=data)
                if response.status_code == 200:
                    print(f'Successfully removed {file_name} from GitHub.')
                else:
                    print(f'Failed to remove {file_name} from GitHub. Status code: {response.status_code}')
                    print(response.json())
    else:
        print(f'Failed to fetch files from GitHub. Status code: {response.status_code}')
        print(response.json())

# Getting pdf contents from GitHub
def get_files_from_github():
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
    }

    folder_path = 'static/candidate_files'
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{folder_path}'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        pdf_files = []
        for file_info in files:
            if 'name' in file_info and 'download_url' in file_info:
                file_name = file_info['name']
                download_url = file_info['download_url']
                pdf_files.append((file_name, download_url))
        return pdf_files
    else:
        return None

@views.route('/result', methods=['GET'])
def result():
    candidate_files = get_files_from_github()
    # print(candidate_files)
    if not candidate_files:
        flash('No result to display.')
        return redirect(url_for('views.upload'))
    candidate_filepaths = [items[1] for items in candidate_files]
    print(candidate_filepaths)
    if candidate_filepaths is None:
        flash('Failed to fetch PDF files from GitHub.')
        return redirect(url_for('views.upload'))

    if 'job_requirements' in session:
        candidate_scores = process_candidates(candidate_filepaths, session.get('job_requirements'))
        print(candidate_scores)
    remove_files_from_github()
    ordered_by_values = OrderedDict(sorted(candidate_scores.items(), key=lambda item: item[1], reverse=True))
    return render_template("result.html", candidate_scores=ordered_by_values)