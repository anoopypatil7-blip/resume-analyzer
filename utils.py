# utils.py

import PyPDF2
import re

SKILLS = [
    "python", "java", "c++", "sql", "html", "css", "javascript",
    "react", "node", "flask", "django",
    "mongodb", "mysql", "postgresql",
    "git", "github",
    "aws", "azure", "gcp", "cloud",
    "docker", "kubernetes",
    "machine learning", "data structures", "algorithms",
    "apis", "rest", "linux"
]

def extract_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9+ ]', ' ', text)  # remove symbols
    return text


def extract_skills(text):
    text = clean_text(text)

    # normalization
    text = text.replace("react js", "react")
    text = text.replace("node js", "node")
    text = text.replace("dbms", "sql")
    text = text.replace("database management systems", "sql")
    text = text.replace("reinforcement learning", "machine learning")

    found = set()

    for skill in SKILLS:
        if skill in text:
            found.add(skill)

    return found


def get_score(resume, job_desc):
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(job_desc)

    if len(jd_skills) == 0:
        return 0

    score = len(resume_skills & jd_skills) / len(jd_skills) * 100
    return round(score, 2)


def get_missing_keywords(resume, job_desc):
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(job_desc)

    return list(jd_skills - resume_skills)


def get_matched_keywords(resume, job_desc):
    resume_skills = extract_skills(resume)
    jd_skills = extract_skills(job_desc)

    return list(jd_skills & resume_skills)