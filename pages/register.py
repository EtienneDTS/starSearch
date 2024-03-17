from flask import Flask, render_template, request, redirect, url_for
from utils import query_db
from flask_bcrypt import Bcrypt


def page_register():
    if request.method == "POST":
        nomU = request.form.get("firstname")
        prenomU = request.form.get("lastname")
        passwordU = request.form.get("password")
        passwordU2 = request.form.get("password2")
        emailU = request.form.get("email")
        if passwordU != passwordU2:
            message = "Les mots de passe ne correspondent pas"
            return redirect(url_for("page_register", message=message))
        query = "select * from utilisateur where emailU = ?"
        params = [emailU]
        result = query_db(query, params)
        if len(result[0]) > 0:
            message = "Cet email est déjà utilisé"
            return redirect(url_for("page_register", message=message))
        # cryptage du mot de passe pour ne pas le garder en clair dans la base de données
        passwordU = Bcrypt.generate_password_hash(passwordU).decode("utf-8")
        query = "insert into utilisateur (nomU, prenomU, passwordU, emailU) values (?, ?, ?, ?, ?)"
        params = [nomU, prenomU, passwordU, emailU]
        return redirect(url_for("page_login"))
        
    return render_template("register.html")