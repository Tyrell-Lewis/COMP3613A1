from App.models import Job
from App.models import Application
from App.models import User
from App.database import db
from datetime import datetime

def create_job(title, requirements, description, user_id):

    tempUser = User.query.get(user_id)

    if tempUser:
        new_job= Job(title=title, requirements=requirements, description=description, user_id=user_id)
        new_job.created_at = datetime.now()
        #new_job.updated_at = datetime.now()

        db.session.add(new_job)
        db.session.commit()
        return (f'{title} job has succesfully been listed!')
    else:
        return ("Invalid User ID was entered!")

def view_all_jobs():
    jobs = Job.query.all()
    return jobs

def view_all_applicants(job_id, temp_user_id):
    
    tempJob = Job.query.get(job_id)

    if tempJob:
        if tempJob.user_id == temp_user_id:
            applicants = [a.user for a in tempJob.applications]
            return applicants
        else:
            return ["You can only view job applicants for jobs you posted!"]
    else:
        return ["Job not found!"]

def apply_to_job(user_id, job_id, resume):

    

    applicant = User.query.get(user_id)
    job = Job.query.get(job_id)

    

    if applicant and job:
        if applicant.id == job.user_id:
            return "You cannot apply for a job listing posted by yourself!"
        elif applicant.id in [a.id for a in job.applications]:
            return "This job has already been applied to!"
        else:
            application = Application(user_id=user_id, job_id=job_id, resume=resume)
            db.session.add(application)
            db.session.commit()
            return "Application was successful!"
    else:
        return "Invalid Applicant or Job ID!"

