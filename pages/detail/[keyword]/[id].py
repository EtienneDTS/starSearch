from flask import render_template, redirect, url_for, request
from utils import query_db
from datetime import datetime


def page_detail(keyword, id):
    context = {}
    if request.method == "POST":
        return redirect(url_for("page_home"))
    if keyword == "acteur":
        query = """select L.urlL 
        from langue L, acteur A, parler P
        where A.idA = P.idA
        and P.nomL = L.nomL
        and A.idA = ?;
        """
        params = [id]
        languages = query_db(query, params)[0]
        query = "select * from acteur where idA = ?"
    elif keyword == "FilmSerie":
        query = "select * from FilmSerie where refFS = ?"
    else:
        return redirect(url_for("page_home"))
    params = [id]
    item = query_db(query, params)[0][0]
    print(item)
    context["item"] = item
    
    
    
    if keyword == "acteur":
        query = """select FS.refFS, FS.nomFS, FS.poster_path, 'FilmSerie' as keyword 
        from FilmSerie FS, acteur A, jouer J
        where A.idA = ?
        and A.idA = J.idA
        and J.refFS = FS.refFS;"""

    if keyword == "FilmSerie":
        query = """select L.urlL 
        from langue L, FilmSerie FS
        where FS.refFS = ?
        and FS.nomL = L.nomL
        """
        params = [id]
        languages = query_db(query, params)[0]
        query = """select A.idA, A.nomA, A.profile_path, 'acteur' as keyword 
        from acteur A, jouer J, FilmSerie FS 
        where FS.refFS = ? 
        and A.idA = J.idA
        and FS.refFS = J.refFS;"""
    params = [id]
    data = query_db(query, params)[0]
    
    context["data"] = data
    context["keyword"] = keyword
    context["languages"] = languages
    
    if keyword == "FilmSerie":
        query = """select G.nomG
        from genre G, FilmSerie FS, appartenir A
        where FS.refFS = ?
        and FS.refFS = A.refFS
        and A.idG = G.idG;
        """
        params = [id]
        genres = query_db(query, params)[0]
        context["genres"] = genres
        percentage = context["item"][5] * 10
        context["percentage"] = "{:.2f}".format(percentage)
        date = context["item"][6]
        date = datetime.strptime(date, "%Y-%m-%d")
        date = date.strftime("%d/%m/%Y")
        context["date"] = date
    return render_template("detail.html", **context)


page_methods = ['GET', 'POST']
