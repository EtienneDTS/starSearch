from app import app, db, bcrypt
from models import User

def create_user(email:str, password:str, admin: bool): 
    with app.app_context():
        user = User.query.get(email)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        if user:
            print("user found")
            user.admin = admin
            user.password = hashed_password
        else:
            user = User(email=email, password=hashed_password, admin=admin)
        db.session.add(user)
        db.session.commit()
        
def grant_admin(email:str): 
    with app.app_context():
        user = User.query.get(email)
        if user:
            print("user found")
            user.admin = True
        db.session.add(user)
        db.session.commit()
        
create_user(email="detoisienetienne@gmail.com", password="22004784", admin=True)