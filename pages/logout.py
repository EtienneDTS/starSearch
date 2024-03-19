from flask import session, redirect, url_for

def page_logout():
    session.pop("user", None)
    return redirect(url_for("page_home"))