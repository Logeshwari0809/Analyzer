import fitz  # PyMuPDF
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
import re
import os

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def clean_text(text):
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())
    words = text.split()
    return " ".join([word for word in words if word not in stop_words])

def extract_skills(text):
    skills_keywords = ["python", "sql", "machine learning", "data analysis", "power bi", "excel",
                       "flask", "tensorflow", "nlp", "deep learning", "communication", "teamwork",
                       "problem-solving", "leadership"]
    return [skill for skill in skills_keywords if skill in text]

def calculate_match(resume_text, jd_text):
    resume_vec = model.encode([resume_text])[0]
    jd_vec = model.encode([jd_text])[0]
    score = cosine_similarity([resume_vec], [jd_vec])[0][0]
    return round(score * 100, 2)

def analyze_resume(pdf_path, job_description):
    text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(text)
    cleaned_jd = clean_text(job_description)
    skills = extract_skills(cleaned_text)
    score = calculate_match(cleaned_text, cleaned_jd)
    return {"skills": skills, "match_score": score}