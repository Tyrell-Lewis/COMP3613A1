from App.database import db
from datetime import datetime

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    requirements = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    posted_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    def __init__(self, title, description, requirements, user_id):
        self.title = title
        self.description = description
        self.requirements = requirements
        self.user_id = user_id
        