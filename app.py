# app.py

from flask import Flask, render_template, request
from utils import extract_text, extract_skills, get_score, get_missing_keywords, get_matched_keywords

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    missing = []
    matched = []

    if request.method == 'POST':
        file = request.files.get('resume')
        job_desc = request.form.get('job_desc')

        if file and file.filename != "":
            try:
                resume_text = extract_text(file)

                # DEBUG (you can remove later)
                print("Resume Skills:", extract_skills(resume_text))
                print("JD Skills:", extract_skills(job_desc))

                score = get_score(resume_text, job_desc)
                missing = get_missing_keywords(resume_text, job_desc)
                matched = get_matched_keywords(resume_text, job_desc)

            except Exception as e:
                print("ERROR:", e)
        else:
            print("No file uploaded")

    return render_template(
        'index.html',
        score=score,
        missing=missing,
        matched=matched
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)