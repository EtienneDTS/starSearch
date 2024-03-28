from flask import render_template, request, redirect, url_for, session
from utils import query_db, bcrypt

def page_login():
    if request.method == "POST":
        emailU = request.form.get("email")
        passwordU = request.form.get("password")
        query = "select * from utilisateur where emailU = ?"
        params = [emailU]
        result = query_db(query, params)
        if len(result[0]) == 0:
            message = "L'email ou le mot de passe est incorrect"
            return render_template("login.html", message=message)
        if bcrypt.check_password_hash(result[0][0][3], passwordU):
            session["user"] = {
                "id": result[0][0][0],
                "nom": result[0][0][1],
                "prenom": result[0][0][2],
                "dateInscription": result[0][0][4],
                "idAbo": result[0][0][5],
                "idStu": result[0][0][6],
                "email": result[0][0][7],
            }
            return redirect(url_for("page_home"))
        else:
            message = "L'email ou le mot de passe est incorrect"
            return render_template("login.html", message=message)
    return render_template("login.html")  

page_methods = ['GET', 'POST']