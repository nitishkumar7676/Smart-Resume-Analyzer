# 📄 Smart Resume Analyzer (AI-Powered ATS Tool)

Smart Resume Analyzer is an AI-powered web app that analyzes resumes against job descriptions using Google Gemini AI. It helps candidates optimize resumes for ATS (Applicant Tracking Systems), identify missing skills and keywords, and provides actionable career improvement suggestions.

# 💻 Live Demo:
[Click here to see the app](https://smart-resume-analyzer-ihzkwg8lqrhj9x26mrxndy.streamlit.app/)

# 🚀 Features

📊 ATS Match Percentage – Calculates resume fit for a job description.

🧠 AI Resume Evaluation – Highlights strengths, weaknesses, and improvement tips.

🔍 Missing Keyword Detection – Detects important keywords missing in the resume.

🎯 Skill & Career Guidance – Suggests skills, tools, certifications, and learning paths.

🧑‍💼 Role-Based Analysis – Custom analysis for Data Scientist, Full Stack Developer, Big Data Engineer, DevOps Engineer, Data Analyst.

📂 Multi-Format Resume Support – PDF, DOC, DOCX.

💬 Ask Anything Mode – Ask questions about your resume or job role.

# 🛠️ Tech Stack
Category	Tools
Frontend	Streamlit
AI Model	Google Gemini 1.5 Flash
Language	Python
PDF Processing	pdf2image, Pillow
DOCX Processing	python-docx
Environment Management	python-dotenv

# 📁 How It Works

Upload your resume (PDF/DOC/DOCX)

Paste the job description

Select your target job role

Choose an analysis option:

Resume Evaluation

Skill Improvement

Missing Keywords

ATS Match Percentage

Get AI-generated insights instantly

# 🔧 Setup Instructions
1. Clone Repo
git clone https://github.com/your-username/smart-resume-analyzer.git
cd smart-resume-analyzer

2. Install Dependencies
pip install -r requirements.txt

3. Create .env for Local Testing
GOOGLE_API_KEY=your_google_gemini_api_key

4. Run App
streamlit run app.py

# 🔐 Deployment on Streamlit Cloud

Push your code to GitHub.

Open Streamlit Cloud → New App → Connect to repo

In Secrets / Environment Variables, add:

GOOGLE_API_KEY = "your_google_gemini_api_key"

Reboot the app.

# 📂 Project Structure

smart-resume-analyzer/

│── app.py

│── requirements.txt

│── README.md

│── .gitignore

│── .env.example

│── assets/


# 🌟 Why This Project Stands Out

Real-world ATS simulation

Practical use of Generative AI

Secure secret management

Clean, user-focused design

Strong portfolio project for Data, AI, and Full Stack roles

# 📌 Future Enhancements

Resume score visualization

Multi-language support

PDF report export

Resume rewriting suggestions

Job scraping integration

# 🙌 Author

Nitish kumar
B.Tech in Computer Science and Engineering (AI & DS)

