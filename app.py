from flask import Flask, render_template, request
from utils.analyzer import analyze_resume
import os
import tempfile

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    extracted_data = None
    if request.method == "POST":
        resume = request.files["resume"]
        job_description = request.form["job_description"]
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            resume.save(tmp.name)
            extracted_data = analyze_resume(tmp.name, job_description)
            tmp_path = tmp.name

        try:
            os.remove(tmp_path)
        except PermissionError:
            pass  # Silently ignore if the file is in use on Windows

    return render_template("index.html", extracted_data=extracted_data)

if __name__ == "__main__":
    app.run(debug=True)