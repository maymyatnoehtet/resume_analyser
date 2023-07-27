# Profilyser - Resume Analyzing App

Profilyser is a web application built using Python Flask that allows recruiters to analyze job candidates' resumes and score them based on a provided job description. The app is designed to simplify the hiring process by automatically evaluating the suitability of candidates for a specific job, making it easier for recruiters to find the best match for their open positions.

## Demo Video Link

[https://drive.google.com/drive/u/1/my-drive](https://drive.google.com/file/d/1VKUwsyXFd5UqtRbBABMEyRJA5VbYn-PU/view?usp=drive_link)

## Deployed App Link

https://profilyser-resume-analyser.azurewebsites.net/home

## Features

- **Job Description Analysis**: Users can paste or write the job description in a text box, and the app will use this description as the basis for evaluating the candidates' resumes.

- **Resume Upload**: Recruiters can upload candidates' resumes in PDF format through the web interface. The app will analyze the contents of these resumes against the provided job description.

- **Scoring**: Each candidate's resume will be scored based on how well it aligns with the job description. The scoring mechanism can be customized and fine-tuned according to the specific requirements of the job.

- **GitHub Integration**: For now, the app is integrated with GitHub to store the uploaded resume files and the analysis results. A GitHub token, repository, and account name are required for the integration to function properly.

## Prerequisites

Before running the Profilyser app, ensure you have the following:

1. Python 3.11 installed on your system.

2. The required Python packages installed. You can install them using the following command:

   ```
   pip install flask azure-storage-blob python-docx PyPDF2
   ```

3. A GitHub account with a repository where the resume files and analysis results will be stored.

4. GitHub personal access token with sufficient permissions to upload files to the repository.

5. Azure account to deploy the app and set up the database for storing resume files and analysis results.

## Configuration

Before deploying the app, make sure to configure the following:

1. Configure GitHub Integration:
   - Update the `GITHUB_TOKEN`, `GITHUB_REPO`, and `GITHUB_ACCOUNT_NAME` variables in `views.py` with your GitHub token, repository name, and account name, respectively.

## Deployment

To deploy Profilyser on Azure, follow these steps:

1. Create a new Azure Web App service.
2. Deploy the app files to the Azure Web App.
3. Configure the required environment variables (e.g., GitHub token, port, host, environment) on the Azure Web App.

## Known Issues

- **500 Internal Server Error**: There is currently an issue with the app deployment on Azure that causes the internal server error after uploading files. Debugging is required to identify the root cause and implement a fix.

- **Scoring Inaccuracy**: I have observed that the scoring function provides inaccurate results. Entering the same PDF document as the job description results in unexpectedly low scores. Investigation and debugging of the scoring algorithm are necessary to address this issue and ensure the accuracy of the evaluation process.

## Future Improvements

To improve Profilyser, consider implementing the following features:

- **User Authentication**: Introduce user authentication to secure the app and allow only authorized users to access it.

- **Customizable Scoring System**: Allow recruiters to customize the scoring mechanism based on their specific evaluation criteria.

- **Data Visualization**: Provide visual representations of candidates' scores and comparisons for easier analysis.

- **Email Notifications**: Notify recruiters when a new resume is uploaded or when analysis results are ready.

## Support and Contributions

For support or to report issues, please contact may.mn.htet@gmail.com. Contributions to improve Profilyser are welcome. Please submit pull requests to the https://github.com/maymyatnoehtet/resume_analyser.
