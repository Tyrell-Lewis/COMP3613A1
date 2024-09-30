from App.models import Job
from App.models import Application
#from App.models import Applicant
from App.models import User
from App.database import db

def create_job(name, requirements, description, applicant_id):

    tempUser = User.query.get(applicant_id)

    if tempUser:
        new_job= Job(name=name, requirements=requirements, description=description, applicant_id=applicant_id)

        db.session.add(new_job)
        db.session.commit()
        return (f'{name} has succesfully been listed!')
    else:
        return ("Invalid User ID was entered!")

def view_all_jobs():
    jobs = Job.query.all()
    return jobs

def view_all_applicants(job_id):
    #applicants = Applicant.query.all()
    tempJob = Job.query.get(job_id)

    if tempJob:
        applicants = [a.user for a in tempJob.applications]
        return applicants
    else:
        return None

def apply_to_job(applicant_id, job_id):

    # print (applicant_id)
    # print (job_id)

    applicant = User.query.get(applicant_id)
    job = Job.query.get(job_id)

    # print (applicant.id)
    # print (job.id)

    if applicant and job:
        if applicant.id == job.applicant_id:
            return "You cannot apply for a job listing posted by yourself!"
        elif applicant.id in [a.id for a in job.applications]:
            return "This job has already been applied to!"
        else:
            application = Application(name=applicant.username, applicant_id=applicant_id, job_id=job_id)
            db.session.add(application)
            db.session.commit()
            return "Application was successful!"
    else:
        return "Invalid Applicant or Job ID!"

