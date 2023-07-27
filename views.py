from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import os
import requests
from utils.process_candidates import process_candidates
from collections import OrderedDict
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, BlobType
import base64

views = Blueprint("views", __name__)
load_dotenv()

## Azure Blob Storage configuration
AZURE_STORAGE_CONNECTION_STRING = 'DefaultEndpointsProtocol=https;AccountName=profilyser;AccountKey=eozBGihPdqxH5M4oTOBfRd0qhf+AR+ewqSsGHasx+7y8iLag1dJRBBFaJfiTJT3yOANmHzg1jBle+AStKUeDVQ==;EndpointSuffix=core.windows.net'
AZURE_CONTAINER_NAME = 'profilyser'

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
                upload_to_azure(file.filename, pdf_content)
            else:
                flash('No file selected or something went wrong.')
                return redirect(url_for('views.upload'))

        flash('File uploaded successfully.')
        return redirect(url_for('views.result'))

    else:
        return render_template("upload.html")

# Upload files to github
def upload_to_azure(filename, content):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    blob_client = container_client.get_blob_client(filename)
    blob_client.upload_blob(content, blob_type=BlobType.BlockBlob)

    print(f'Successfully uploaded {filename} to Azure Blob Storage.')

# Delete files from Azure
def remove_files_from_azure():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    blob_list = container_client.list_blobs()

    for blob in blob_list:
        blob_client = container_client.get_blob_client(blob)
        blob_client.delete_blob()

def get_files_from_azure():
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    blob_list = container_client.list_blobs()

    pdf_files = []
    for blob in blob_list:
        file_name = blob.name
        download_url = f"{container_client.url}/{file_name}"
        pdf_files.append((file_name, download_url))

    return pdf_files

@views.route('/result', methods=['GET'])
def result():
    candidate_files = get_files_from_azure()

    if not candidate_files:
        flash('No result to display.')
        return redirect(url_for('views.upload'))

    candidate_filepaths = [items[1] for items in candidate_files]

    if candidate_filepaths is None:
        flash('Failed to fetch PDF files from Azure Blob Storage.')
        return redirect(url_for('views.upload'))

    if 'job_requirements' in session:
        candidate_scores = process_candidates(candidate_filepaths, session.get('job_requirements'))

    ordered_by_values = OrderedDict(sorted(candidate_scores.items(), key=lambda item: item[1], reverse=True))
    remove_files_from_azure()
    return render_template("result.html", candidate_scores=ordered_by_values)