from .user import create_user
from .job import create_job
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_user('shane', 'shanepass')
    create_user('mary', 'marypass')
    create_user('gomez', 'gomezpass')
    create_job('king', "rules over peasants", "royalty", 2)
    create_job('knight', "protects the king", "swordmanship", 3)
    create_job('baker', "bakes bread, maybe cake", "does not burn bread", 4)
    