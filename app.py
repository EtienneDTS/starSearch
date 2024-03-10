from flask import Flask, url_for, render_template, redirect, request
from flask_bcrypt import Bcrypt
from flask_pagerouter import PageRouter


import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
PageRouter(app)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key
bcrypt = Bcrypt(app)



        
        
        
    

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