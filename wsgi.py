import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Application, Job
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, create_job, view_all_applicants, view_all_jobs, apply_to_job )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli




job_cli = AppGroup('job', help='Job object commands')

@job_cli.command("create", help="Creates a job listing!")
@click.argument("name", default="Peasant")
@click.argument("description", default="Its a peasant.... not much else tbh")
@click.argument("requirements", default="Literally nothing")
@click.argument("applicant_id", default=1)
def create_job_command(name, description, requirements, applicant_id):
    result = create_job(name, description, requirements, applicant_id)
    print(result)




@job_cli.command("view", help="Views all jobs!")
def view_jobs_command():
    jobs = view_all_jobs()

    if jobs:

        for job in jobs:
            print(f"Job title: {job.name}")
            print(f"Job description: {job.description}")
            print(f"Job requirements: {job.requirements}")
            print(f"Posted By Applicant ID : {job.applicant_id}")
            print(f"Job ID : {job.id}")
            print("------------------------")
    else:
        print ("No Jobs are currently listed!")

@job_cli.command("viewapp", help="Views all jobs!")
def view_applicants_command():

    job_id = int(input("Enter the job ID you want to search for: "))

    applicants = view_all_applicants(job_id)
    if applicants:

        for app in applicants:
            print("------------------------")
            print(f"Applicant Name: {app.username}")
            print(f"Applicant ID : {app.id}")
            
    else:
        print ("No Applicants are currently available!")


@job_cli.command("apply", help="Applies to a job!")
def apply_to_job_command():
    applicant_id = int(input("Enter your applicant ID: "))
    job_id = int(input("Enter the job ID you want to apply to: "))

    # print (applicant_id)
    # print(job_id)

    result = apply_to_job(applicant_id, job_id)
    print(result)

app.cli.add_command(job_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)