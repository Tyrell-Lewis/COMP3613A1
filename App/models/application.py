from App.database import db



class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    resume = db.Column(db.String(5000), unique=False, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    job = db.relationship('Job', backref='applications', lazy=True)


    def __init__(self, user_id, job_id, resume):
        self.resume = resume
        self.user_id = user_id
        self.job_id = job_id