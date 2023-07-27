## Profilyser

Profilyser is a web application designed to streamline the recruitment process by analyzing candidates' resumes and matching them with a given job description. With its user-friendly features and seamless deployment on Azure, Profilyser is the ideal tool for recruiters seeking to identify the best-suited candidates efficiently.

### Demo Video
https://drive.google.com/file/d/1utYxkjJIr0aSp8eTFQGth8BuVMd49a72/view?usp=sharing

### Deployed App
https://profilyser-resume-analyser.azurewebsites.net/home

### Features

- **Job Description Analysis**: Analyze job descriptions provided by users to evaluate candidates' resumes effectively.

- **Resume Upload**: Recruiters can easily upload candidates' resumes in PDF format through the web interface for analysis.

- **Scoring**: Each candidate's resume is scored based on its alignment with the specified job description.

### Prerequisites

Before running the Profilyser app, please ensure you have the following:

1. Python 3.11 installed on your system.

2. The required Python packages installed. Refer to the `requirements.txt` file for installation using the following command:

   ```
   pip install -r requirements.txt
   ```

3. To run in a local environment, use the following command:

   ```
   python3 app.py
   ```

4. An Azure account to deploy the app and set up the database for storing resume files.

### Deployment

To deploy Profilyser on Azure, follow these steps:

1. Create a new Azure Web App service.
2. Deploy the app files to the Azure Web App.
3. Configure the required environment variables (e.g., port, host, environment) on the Azure Web App.
4. Create a new Azure Storage Account service.

### Future Improvements

To enhance Profilyser further, consider implementing the following features:

- **User Authentication**: Introduce user authentication to secure the app and restrict access to authorized users only.

- **Customizable Scoring System**: Allow recruiters to customize the scoring mechanism based on their specific evaluation criteria.

- **Data Visualization**: Provide visual representations of candidates' scores and comparisons for easier analysis.

### Support and Contributions

For support or to report issues, please contact may.mn.htet@gmail.com. Contributions to improve Profilyser are welcome. Please submit pull requests to the [GitHub repository](https://github.com/maymyatnoehtet/resume_analyser).
