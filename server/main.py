from flask import request, jsonify
from config import app, db
from models import Job, Resume, CoverLetter

@app.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    json_jobs = list(map(lambda x: x.to_json(), jobs))
    return jsonify({"jobs": json_jobs})

@app.route("/create_job", methods=["POST"])
def create_job():
    job_title = request.json.get("jobTitle")
    company_name = request.json.get("companyName")
    source = request.json.get("source")
    applied = request.json.get("applied")
    application_date = request.json.get("applicationDate")
    resume_data = request.json.get("resume")
    cover_letter_data = request.json.get("coverLetter")

    if not job_title or not company_name or not source:
        return (
            jsonify({"message": "You must include a job title, company name, and job source"}),
            400
        )
    
    resume = None
    if resume_data:
        if isinstance(resume_data, dict):
            resume = Resume(
                technical_skills=resume_data.get("technicalSkills"),
                experience=resume_data.get("experience"),
                projects=resume_data.get("projects"),
                education=resume_data.get("education"),
                changes=resume_data.get("changes")
            )
        else:
            return jsonify({"message": "Invalid format for resume data"}), 400

    cover_letter = None
    if cover_letter_data:
        if isinstance(cover_letter_data, dict):
            cover_letter = CoverLetter(
                about=cover_letter_data.get("about"),
                why_company=cover_letter_data.get("whyCompany"),
                why_me=cover_letter_data.get("whyMe")
            )
        else:
            return jsonify({"message": "Invalid format for cover letter data"}), 400
    

    new_job = Job(
        job_title=job_title, 
        company_name=company_name, 
        source=source, applied=applied, 
        application_date=application_date, 
        resume=resume, 
        cover_letter=cover_letter
    )
    try:
        db.session.add(new_job)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "Job Created"}), 201


@app.route("/update_job/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        return jsonify({"message": "Job not found."}), 404
    
    data = request.json
    job.job_title = data.get("jobTitle", job.job_title)
    job.company_name = data.get("companyName", job.company_name)
    job.source = data.get("source", job.source)
    job.applied = data.get("applied", job.applied)
    job.application_date = data.get("applicationDate", job.application_date)
    job.resume = data.get("resume", job.resume)
    job.cover_letter = data.get("coverLetter", job.cover_letter)

    db.session.commit()

    return jsonify({"message": "Job updated."}), 200

@app.route("/delete_job/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)

    if not job:
        return jsonify({"message": "Job not found."}), 404
    
    db.session.delete(job)
    db.session.commit()

    return jsonify({"message": "Job deleted."}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)