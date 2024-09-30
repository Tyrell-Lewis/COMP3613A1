from App.database import db



class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=True) #make not nulla ble aftrer
    applicant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)#make not nulla ble aftrer
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)#make not nulla ble aftrer
    job = db.relationship('Job', backref='applications', lazy=True)

