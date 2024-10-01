```python

job_cli = AppGroup('job', help='Job object commands')

This command creates a job by the user inputting the job title, description, requirements and their own user ID.

@job_cli.command("create", help="Creates a job listing!")
@click.argument("name", default="Peasant")
@click.argument("description", default="Its a peasant.... not much else tbh")
@click.argument("requirements", default="Literally nothing")
@click.argument("user_id", default=1)
def create_job_command(name, description, requirements, user_id):
    
    result = create_job(name, description, requirements, user_id)
    print(result)


This command lists/views all the jobs which are currently listed.

@job_cli.command("view", help="Views all jobs!")
def view_jobs_command():
    jobs = view_all_jobs()

    if jobs:

        for job in jobs:
            print(f"Job Title: {job.title}")
            print(f"Job Description: {job.description}")
            print(f"Job Requirements: {job.requirements}")
            print(f"Posted By User ID : {job.user_id}")
            print(f"Job ID : {job.id}")
            print(f"Job posted at : {job.posted_date}")
            print("------------------------")
    else:
        print ("No Jobs are currently listed!")


This command allows the user to input the specific job ID and their User ID to view the applicants of jobs which they themselves have posted.

@job_cli.command("applicants", help="Views Applicants for specified Jobs!")
def view_applicants_command():

    job_id = (input("Enter the job ID you want to search for: "))


    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = User.query.filter_by(username=username).first()
    user_id = None

    if user and user.check_password(password):
        print("Login successful!")
        
        user_id = user.id
        

        while not job_id:
            job_id = (input("Enter the Job ID you want to apply to: "))

        if job_id:

            job_id= int(job_id)
            

            if user_id:

               

                applicants = view_all_applicants(job_id, user_id)

                if applicants:
                    print("------------------------")
                    print("List of curent Applicants: ")

                    if isinstance(applicants, str):
                        print(applicants)
                    else:
                        for app in applicants:
                            if isinstance(app, str):
                                print(app)
                            else:
                                print("------------------------")
                                print(f"Applicant Name: {app.username}")
                                print(f"Applicant ID : {app.id}")  
                else:
                    print ("No Applicants are currently available!")
            else:
                ("Please provide your User ID!")
        else:
            ("Please provide the Job ID!")
    else:
         print("Invalid username or password!")


This command allows for a user to apply for a job, as long as it has a valid job ID, they provide their valid user ID, and the job is not one which they themselves have listed.

@job_cli.command("apply", help="Applies to a job!")
def apply_to_job_command():
    job_id = (input("Enter the Job ID you want to apply to: "))

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = User.query.filter_by(username=username).first()

    user_id = None

    if user and user.check_password(password):
        print("Login successful!")
        
        user_id = user.id
        

        while not job_id:
            job_id = (input("Enter the Job ID you want to apply to: "))

        if job_id:

            job_id= int(job_id)
            
            if user_id:

                
                resume = str(input("Submit your resume here: "))

                if resume:
                    result = apply_to_job(user_id, job_id, resume)
                    print("------------------------")
                    print(result)
                else:
                    print("Please submit your resume!")
            else:
                print("Please provide your User ID!")
        else:
            print("Please provide the Job ID!")
    else:
         print("Invalid username or password!")

app.cli.add_command(job_cli)
```








[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Tyrell-Lewis/COMP3613A1.git)
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

Then execute the command invoking with flask cli with command name and the relevant parameters

```bash
$ flask user create bob bobpass
```


# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what the production server executes):_
```bash
$ gunicorn wsgi:app
```

# Deploying
You can deploy your version of this app to render by clicking on the "Deploy to Render" link above.

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Database Migrations
If changes to the models are made, the database must be'migrated' so that it can be synced with the new models.
Then execute following commands using manage.py. More info [here](https://flask-migrate.readthedocs.io/en/latest/)

```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
$ flask db --help
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example

```python
@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "User"]))
```

You can then execute all user tests as follows

```bash
$ flask test user
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests.

You can run all application tests with the following command

```bash
$ pytest
```

## Test Coverage

You can generate a report on your test coverage via the following command

```bash
$ coverage report
```

You can also generate a detailed html report in a directory named htmlcov with the following comand

```bash
$ coverage html
```

# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

## Cannot Update Workflow file

If you are running into errors in gitpod when updateding your github actions file, ensure your [github permissions](https://gitpod.io/integrations) in gitpod has workflow enabled ![perms](./images/gitperms.png)

## Database Issues

If you are adding models you may need to migrate the database with the commands given in the previous database migration section. Alternateively you can delete you database file.
