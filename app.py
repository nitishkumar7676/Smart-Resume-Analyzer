from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import base64
import os
import io
import mimetypes
from PIL import Image
from pdf2image import convert_from_bytes, exceptions as pdf_exceptions
from docx import Document
import google.generativeai as genai

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY is not set.")
    st.stop()

genai.configure(api_key=api_key)

# Poppler path for Windows (change if needed)
poppler_path = r"C:\Program Files (x86)\poppler\Library\bin"

# Function to process resume file
def process_resume_file(uploaded_file):
    if uploaded_file.size > 10 * 1024 * 1024:
        raise ValueError("File too large. Please upload a file under 10MB.")

    file_type = uploaded_file.name.split('.')[-1].lower()
    mime_type, _ = mimetypes.guess_type(uploaded_file.name)

    if mime_type == "application/pdf" and file_type == "pdf":
        try:
            images = convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
            pdf_parts = []
            for page in images:
                img_byte_arr = io.BytesIO()
                page.save(img_byte_arr, format='JPEG')
                img_byte_arr = img_byte_arr.getvalue()
                pdf_parts.append({
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode("utf-8")
                })
            return pdf_parts
        except pdf_exceptions.PDFPageCountError:
            raise ValueError("The uploaded PDF is invalid or corrupted.")

    elif file_type in ['doc', 'docx']:
        try:
            doc = Document(uploaded_file)
            full_text = "\n".join([para.text for para in doc.paragraphs])
            return [{
                "mime_type": "text/plain",
                "data": full_text
            }]
        except Exception:
            raise ValueError("Failed to read the Word document. Please upload a valid .doc or .docx file.")

    else:
        raise ValueError("It is not supported file format. Please upload a PDF or Word document.")

# Function to interact with Gemini
def get_gemini_response(job_description, resume_parts, prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        resume_input = resume_parts[0] if resume_parts else ""
        response = model.generate_content([job_description, resume_input, prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# ---------- Streamlit UI Starts Here ----------

st.set_page_config(page_title="Smart Resume Analyzer")
st.title("Smart Resume Analyzer")

# Job description input
input_text = st.text_area("Paste the Job Description here:")

# Job role dropdown
job_role = st.selectbox("Select Job Role:", [
    "Data Scientist",
    "Full Stack Developer",
    "Big Data Engineer",
    "DevOps Engineer",
    "Data Analyst"
])

# Resume upload
uploaded_file = st.file_uploader("Upload Your Resume (PDF or Word)", type=["pdf", "doc", "docx"])

if uploaded_file:
    st.success("Resume uploaded successfully!")
    
# Prompts
input_prompt_evaluation = f"""
You are an experienced HR in the {job_role} field. 
Evaluate the resume against the job description provided. 
Highlight strengths, weaknesses, and give feedback for improvement.
"""

input_prompt_percentage = f"""
As an ATS system expert in {job_role}, analyze the resume against the job description.
Give:
1. Percentage match
2. Missing keywords
3. Final thoughts
"""

input_prompt_skills = f"""
You're a career coach specializing in {job_role}. 
Read the resume and job description and suggest:
- Skills to learn or improve
- Certifications or tools to master
- Courses or areas to focus on
"""

input_prompt_keywords = f"""
You're an AI-based keyword scanner. 
Compare the resume and job description. 
List important keywords from the job description that are **missing** in the resume.
"""

# Buttons (ordered)
submit_eval = st.button("Tell Me About the Resume")
submit_skills = st.button("How Can I Improve My Skills")
submit_keywords = st.button("What Keywords Are Missing")
submit_match = st.button("ATS Percentage Match")

# Logic for buttons
if submit_eval:
    if uploaded_file and input_text:
        with st.spinner("Analyzing resume..."):
            try:
                resume_parts = process_resume_file(uploaded_file)
                response = get_gemini_response(input_text, resume_parts, input_prompt_evaluation)
                st.subheader("Resume Evaluation")
                st.write(response)
            except ValueError as ve:
                st.error(str(ve))
    else:
        st.warning("Please upload a resume and enter the job description.")

if submit_skills:
    if uploaded_file and input_text:
        with st.spinner("Analyzing skills..."):
            try:
                resume_parts = process_resume_file(uploaded_file)
                response = get_gemini_response(input_text, resume_parts, input_prompt_skills)
                st.subheader("Skill Improvement Suggestions")
                st.write(response)
            except ValueError as ve:
                st.error(str(ve))
    else:
        st.warning("Please upload a resume and enter the job description.")

if submit_keywords:
    if uploaded_file and input_text:
        with st.spinner("Scanning for missing keywords..."):
            try:
                resume_parts = process_resume_file(uploaded_file)
                response = get_gemini_response(input_text, resume_parts, input_prompt_keywords)
                st.subheader("Missing Keywords")
                st.write(response)
            except ValueError as ve:
                st.error(str(ve))
    else:
        st.warning("Please upload a resume and enter the job description.")

if submit_match:
    if uploaded_file and input_text:
        with st.spinner("Calculating ATS match..."):
            try:
                resume_parts = process_resume_file(uploaded_file)
                response = get_gemini_response(input_text, resume_parts, input_prompt_percentage)
                st.subheader("ATS Match Percentage")
                st.write(response)
            except ValueError as ve:
                st.error(str(ve))
    else:
        st.warning("Please upload a resume and enter the job description.")

# --------- Final Section: Ask Anything ---------
st.markdown("---")
st.header("Ask Anything About Your Resume or Job Role")

user_question = st.text_input("Type your question here:")
ask_button = st.button("Go")

if ask_button:
    if uploaded_file and user_question:
        with st.spinner("Thinking..."):
            try:
                resume_parts = process_resume_file(uploaded_file)
                response = get_gemini_response(user_question, resume_parts, f"Answer this question based on the resume: {user_question}")
                st.subheader("Go")
                st.write(response)
            except ValueError as ve:
                st.error(str(ve))
    else:
        st.warning("Please upload a resume and enter your question.")



