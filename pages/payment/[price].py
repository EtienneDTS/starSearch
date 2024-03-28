from flask import render_template

def page_offer(price):
    # processeur de paiment
    return render_template("offer.html", price=price)

