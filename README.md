# 📄 AI Resume Analyzer

**AI Resume Analyzer** is a Streamlit web app powered by **Google Gemini AI** that reviews resumes, gives **ATS scores**, and provides **actionable feedback** to improve them for specific job roles.

---

## 🚀 Features
- 📎 Upload resumes (PDF/TXT)  
- 💼 Role-specific feedback  
- 📊 ATS score (out of 100)  
- 🧠 AI-powered analysis & suggestions  
- 💅 Simple and modern UI  

---

## 🛠️ Tech Stack
- **Streamlit** (frontend)  
- **Google Gemini API** (AI analysis)  
- **PyPDF2** (PDF parsing)  
- **python-dotenv** (env management)  
- **Python 3.9+**  

---

## ⚙️ Installation
```bash
git clone https://github.com/<your-username>/resume_analyzer.git
cd resume_analyzer
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_api_key" > .env
streamlit run main.py
