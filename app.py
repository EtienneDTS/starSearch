from flask import Flask, url_for, render_template, redirect, request
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import current_user, LoginManager, login_user, login_required, logout_user

import os

import requests
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
csrf = CSRFProtect(app)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key
api_token = os.environ.get("API_TOKEN")
back_drop_path = "https://image.tmdb.org/t/p/original"
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
    }

from models import User

@login_manager.user_loader
def load_user(email):
    return User.query.get(email)

@app.route("/")
def home():
    url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=1"
    # faire try catch
    famous_actors = requests.get(url=url, headers=headers).json()["results"][:4]
    url = "https://api.themoviedb.org/3/trending/person/week?language=en-US"
    # faire try catch
    trending_actors = requests.get(url=url, headers=headers).json()["results"][:4]
    url = "https://api.themoviedb.org/3/trending/movie/week?language=fr-FR"
    # faire try catch
    trending_films = requests.get(url=url, headers=headers).json()["results"][:4]
    
    context = {
        "famous_actors": famous_actors,
        "trending_actors": trending_actors,
        "trending_films": trending_films,
        "back_drop_path": back_drop_path
    }
    return render_template('home.html', **context)

@app.route("/get_all/<keyword>/<page>")
def get_all(keyword: str, page: int):
    page = int(page)
    context = {
        "back_drop_path": back_drop_path,
        "keyword": keyword,
        "page": page,
        "max_page": 500, #Limitation de l'api
    }
    if page < 1:
        return redirect(url_for('get_all', keyword=keyword, page=1))
    if keyword == "trending_actors":
        url = f"https://api.themoviedb.org/3/trending/person/week?language=en-US&page={page}"
        r = requests.get(url=url, headers=headers).json()
        context["data"] = r["results"]
        context["title"] = "Les acteurs en tendance"
        
        
    elif keyword == "trending_films":
        url = f"https://api.themoviedb.org/3/trending/movie/week?language=fr-FR&page={page}"
        r = requests.get(url=url, headers=headers).json()
        context["data"] = r["results"]
        context["title"] = "Les films en tendance"
        
    elif keyword == "famous_actors":
        url = f"https://api.themoviedb.org/3/person/popular?language=en-US&page={page}"
        r = requests.get(url=url, headers=headers).json()
        context["data"] = r["results"]
        context["title"] = "Les acteurs populaire"
    else:
        return redirect("home")
    if page == 1:
        context["previous_page"] = 1
    else:
        context["previous_page"] = page - 1
    if page == context["max_page"]:
        context["next_page"] = context["max_page"]
    else:
        context["next_page"] = page + 1
    return render_template("get_all.html", **context)
        
        
        
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    message = False
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.get(email)
        if user and user.password:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                if current_user.is_authenticated:
                    return redirect(url_for('home'))

        else:
            message = "User not Found or wrong password"
            
    return render_template('login.html', message=message)  

if __name__ == "__main__":
    app.run(debug=True)