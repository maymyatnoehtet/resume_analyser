# Import the PyPDF2 library to work with PDF files
import PyPDF2
import os
import requests
import io
from urllib.parse import urlparse

# Define a function to process candidate resumes and find their similarity to job requirements
def process_candidates(candidate_files, job_requirements):

    # Define a function to extract text from a PDF file
    def extract_text_from_pdf(url):
        try:
            # retrieve the pdf file from the url 
            response = requests.get(url)
            candidate_file = io.BytesIO(response.content)

            # Create a PdfReader object to read the PDF file
            pdf_reader = PyPDF2.PdfReader(candidate_file)

            # Initialize an empty string to store the extracted text
            text = ""

            # Loop through each page in the PDF and extract the text
            for page in pdf_reader.pages:
                text += page.extract_text()

            # Return the extracted text
            return text
        except Exception:
            # If there's an error in reading the PDF, return None
            return None

    # Define a function to preprocess the text by converting it to lowercase and splitting it into tokens
    def preprocess_text(text):
        tokens = text.lower().split()
        return tokens

    # Define a function to calculate the similarity between job requirements and candidate qualifications
    def calculate_similarity(job_requirements, candidate_qualifications):
        # Preprocess both job requirements and candidate qualifications
        job_requirements = preprocess_text(job_requirements)
        candidate_qualifications = preprocess_text(candidate_qualifications)

        # Find the common tokens between job requirements and candidate qualifications
        common_tokens = set(job_requirements) & set(candidate_qualifications)

        # Calculate the similarity as the ratio of common tokens to the total job requirements
        similarity = len(common_tokens) / len(job_requirements)

        # Return the calculated similarity
        return similarity

    # Dictionary to store candidate's similarity scores
    candidate_scores = {}
    failed_candidates = []

    # Loop through each candidate file and process their resume
    for candidate_file_url in candidate_files:
        print('Candidate file:', candidate_file_url)
        # Extract text from the candidate's resume
        candidate_resume_text = extract_text_from_pdf(candidate_file_url)

        # Check if text extraction was successful
        if candidate_resume_text:
            # Calculate similarity between job requirements and candidate qualifications
            similarity = calculate_similarity(job_requirements, candidate_resume_text)
            parsed_url = urlparse(candidate_file_url)
            file_path = parsed_url.path
            candidate_filename = os.path.basename(file_path)
            print(candidate_filename)
            candidate_scores[candidate_filename] = similarity
        else:
            failed_candidates.append(candidate_file_url)

    for key,value in candidate_scores.items():
        print(f"{key}: {value}")
    return candidate_scores