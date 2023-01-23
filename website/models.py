from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

# define db 
class User(db.Model, UserMixin): # db table
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True)
  first_name = db.Column(db.String(255))
  password = db.Column(db.String(30))
  notes = db.relationship('Note')

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  text = db.Column(db.String(5000))
  date = db.Column(db.DateTime(timezone=True), default=func.now())