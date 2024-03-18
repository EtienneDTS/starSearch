from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt

def page_login():
    return render_template("login.html")  

page_methods = ['GET', 'POST']