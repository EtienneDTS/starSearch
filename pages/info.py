from flask import request, render_template

def page_info():
    key = request.form.get("key")
    if key == "contact":
        actor_name = request.form.get("actor_name")
        message = "Un message a été envoyé à l'acteur " + actor_name
    else:
        price = request.form.get("price")
        message = "Nous avons reçu votre paiement de " + price + ". Nous espérons que vous appricez notre service !"
        
    return render_template("info.html", message=message)

page_methods = ['POST']