from flask import render_template, request, redirect, url_for
from utils import query_db, bcrypt
from datetime import datetime




def page_register():
    if request.method == "POST":
        nomU = request.form.get("lastname")
        prenomU = request.form.get("firstname")
        passwordU = request.form.get("password")
        passwordU2 = request.form.get("password2")
        emailU = request.form.get("email")
        if passwordU != passwordU2:
            message = "Les mots de passe ne correspondent pas"
            return render_template("register.html", message=message)
        query = "select * from utilisateur where emailU = ?"
        params = [emailU]
        result = query_db(query, params)
        if len(result[0]) > 0:
            print(result[0])
            print(True)
            message = "Cet email est déjà utilisé"
            return render_template("register.html", message=message)
        # cryptage du mot de passe pour ne pas le garder en clair dans la base de données
        passwordU = bcrypt.generate_password_hash(password=passwordU)
        query = "insert into utilisateur (nomU, prenomU, passwordU, dateInscriptionU, emailU) values (?, ?, ?, ?, ?)"
        
        dateInscriptionU = datetime.now().strftime("%y-%m-%d")
        params = [nomU, prenomU, passwordU, dateInscriptionU, emailU]
        query_db(query, params)
        return redirect(url_for("page_login"))
        
    return render_template("register.html")

page_methods = ['GET', 'POST']