from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "user"
    email = db.Column(db.String, primary_key=True)
    company = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String)
    
    def get_id(self):
        return str(self.email)