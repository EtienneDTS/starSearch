from flask import Flask
from flask_bcrypt import Bcrypt
from flask_pagerouter import PageRouter


import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
PageRouter(app)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    app.run(debug=True)



        
        
        
    

