from flask import Flask, url_for, render_template, redirect, request
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key

@app.route("/")
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)