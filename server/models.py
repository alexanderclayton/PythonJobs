from config import db

class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(80), unique=False, nullable=False)
    company_name = db.Column(db.String(80), unique=False, nullable=False)
    source = db.Column(db.String(80), unique=False, nullable=False)
    applied = db.Column(db.Boolean, unique=False, default=False)
    application_date = db.Column(db.String(80), unique=False, nullable=True)
    resume = db.relationship("Resume", lazy="joined", back_populates="job")
    cover_letter = db.relationship("CoverLetter", lazy="joined", back_populates="job")

    def to_json(self):
        return {
            "id": self.id,
            "jobTitle": self.job_title,
            "companyName": self.company_name,
            "source": self.source,
            "applied": self.applied,
            "applicationDate": self.application_date,
            "resume": self.resume,
            "coverLetter": self.cover_letter,
        }
    
class Resume(db.Model):
    __tablename__ = "resumes"
    id = db.Column(db.Integer, primary_key=True)
    id_job = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    technical_skills = db.Column(db.Text, unique=False, nullable=True)
    experience = db.Column(db.Text, unique=False, nullable=True)
    projects = db.Column(db.Text, unique=False, nullable=True)
    education = db.Column(db.Text, unique=False, nullable=True)
    changes = db.Column(db.Text, unique=False, nullable=True)
    job = db.relationship("Job", back_populates="resume")

    def to_json(self):
        return {
            "id": self.id,
            "technicalSkills": self.technical_skills,
            "experience": self.experience,
            "projects": self.projects,
            "education": self.education,
            "changes": self.changes,
        }
    
class CoverLetter(db.Model):
    __tablename__ = "cover_letters"
    id = db.Column(db.Integer, primary_key=True)
    id_job = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=True)
    about = db.Column(db.Text, unique=False, nullable=True)
    why_company = db.Column(db.Text, unique=False, nullable=True)
    why_me = db.Column(db.Text, unique=False, nullable=True)
    job = db.relationship("Job", back_populates="cover_letter")

    def to_json(self):
        return {
            "about": self.about,
            "whyCompany": self.why_company,
            "whyMe": self.why_me,
        }