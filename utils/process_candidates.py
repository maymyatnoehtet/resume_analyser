# Import the PyPDF2 library to work with PDF files
import PyPDF2
import os

# Define a function to process candidate resumes and find their similarity to job requirements
def process_candidates(candidate_files, job_requirements):

    # Define a function to extract text from a PDF file
    def extract_text_from_pdf(file):
        try:
            # Create a PdfReader object to read the PDF file
            pdf_reader = PyPDF2.PdfReader(file)

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

    # Define a function to get user input for job requirements
    # def get_user_input():
    #     job_requirements = input("Please enter the job requirements or skills: ")
    #     return job_requirements

    # # Get user input for job requirements
    # job_requirements = get_user_input()

    # Dictionary to store candidate's similarity scores
    candidate_scores = {}
    failed_candidates = []

    # Loop through each candidate file and process their resume
    for candidate_file in candidate_files:
        # Extract text from the candidate's resume
        candidate_resume_text = extract_text_from_pdf(candidate_file)

        # Check if text extraction was successful
        if candidate_resume_text:
            # Calculate similarity between job requirements and candidate qualifications
            similarity = calculate_similarity(job_requirements, candidate_resume_text)
            candidate_filename = os.path.basename(candidate_file)
            candidate_scores[candidate_filename] = similarity
        else:
            failed_candidates.append(candidate_file)

    for key,value in candidate_scores.items():
        print(f"{key}: {value}")
    return candidate_scores,failed_candidates