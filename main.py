import streamlit as st
import PyPDF2
import io
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# 🌟 Page Config
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

# 💅 Custom Styling
st.markdown("""
    <style>
        body {
            background-color: #f9fafb;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 2.2em;
            font-weight: 700;
            color: #2563eb;
            margin-top: 0.5em;
        }
        .subtitle {
            text-align: center;
            color: #555;
            font-size: 1.1em;
            margin-bottom: 2em;
        }
        .stFileUploader, .stTextInput {
            background: #ffffff;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .stButton>button {
            background: linear-gradient(to right, #2563eb, #1d4ed8);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.6em 1.4em;
            border: none;
            transition: 0.3s ease;
        }
        .stButton>button:hover {
            transform: scale(1.04);
            background: linear-gradient(to right, #1d4ed8, #1e40af);
        }
        .result-box {
            background: #f1f5f9;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-top: 20px;
            font-size: 1em;
        }
    </style>
""", unsafe_allow_html=True)

# 🧠 Header
st.markdown("<div class='main-title'>📄 AI Resume Analyzer</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload your resume and get smart, structured feedback powered by Gemini AI!</div>", unsafe_allow_html=True)

# 🔑 Gemini API setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# 📤 File Upload & Job Role Input
uploaded_file = st.file_uploader("📎 Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("💼 Target Job Role (optional)", placeholder="e.g. Data Scientist, Product Manager")
analyze = st.button("🔍 Analyze Resume")

# 📄 Helper Functions
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

# 🤖 Gemini Analyzer
def analyze_resume_with_gemini(resume_text, job_role):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an expert resume reviewer with 10+ years of experience in HR and recruitment.
    Analyze this resume and provide constructive feedback focused on:

    1. Content clarity and overall impact
    2. Skills presentation and relevance
    3. Experience and achievements descriptions
    4. Specific improvements for {job_role if job_role else 'general job applications'}
    5. provide with ATS score out of 100
    Resume content:
    {resume_text}

    Please provide your analysis in a **clear, structured, and bullet-point format**.
    Include actionable recommendations and avoid generic comments.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# 🚀 Main Logic
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("⚠️ File does not contain any text content.")
            st.stop()

        with st.spinner("🧠 Analyzing your resume... please wait a moment..."):
            feedback = analyze_resume_with_gemini(file_content, job_role)

        st.success("✅ Analysis complete!")
        st.markdown("<h4>📋 AI Feedback</h4>", unsafe_allow_html=True)
        st.markdown(f"<div class='result-box'>{feedback}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
