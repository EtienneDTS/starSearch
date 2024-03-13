from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt

def page_login():
    return "<h1>Login</h1>"  

page_methods = ['GET', 'POST']