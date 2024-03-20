from flask import render_template, redirect, url_for, request
from utils import query_db

def page_detail(keyword, id):
    if request.method == "POST":
        return redirect(url_for("page_home"))
    if keyword == "acteur":
        query = """select L.nomCompletL 
        from langue L, acteur A, parler P
        where A.idA = P.idA
        and P.nomL = L.nomL
        and idA = ?;
        """
        params = [id]
        languages = query_db(query, params)[0]
        query = "select * from acteur where idA = ?"
    if keyword == "FilmSerie":
        query = "select * from FilmSerie where refFS = ?"
    else:
        return redirect("page_home")
    params = [id]
    item = query_db(query, params)[0][0]
    if keyword == "acteur":
        query = """select FS.refFS, FS.nomFS, FS.poster_path, 'FilmSerie' as keyword 
        from FilmSerie FS, acteur A, jouer J
        where idA = ?
        and A.idA = J.idA
        and J.refFS = FS.refFS;"""
        
    if keyword == "FilmSerie":
        query = """select A.idA, A.nomA, A.profile_path, 'acteur' as keyword 
        from acteur A, jouer J, FilmSerie FS 
        where FS.refFS = ? 
        and A.idA = J.idA
        and FS.refFS = J.refFS;"""
    params = [id]
    data = query_db(query, params)[0]
    return render_template("detail.html", item=item, data=data, keyword=keyword, languages=languages)

page_methods = ['GET', 'POST']