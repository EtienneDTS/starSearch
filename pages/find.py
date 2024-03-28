from flask import render_template, request
from utils import query_db


def page_find():
    response_list = []
    search_request = request.args.get("search_request")
    query = f"select idA, nomA, profile_path, 'acteur' as keyword  from acteur;"
    result = query_db(query)[0]
    
    for actor in result:
        if search_request.lower() in actor[1].lower():
            response_list.append(actor)
    query = f"select refFS, nomFS, poster_path, 'FilmSerie' as keyword from FilmSerie;"
    result = query_db(query)[0]
    
    for fs in result:
        if search_request.lower() in fs[1].lower():
            response_list.append(fs)
            
    return render_template("find.html", data=response_list, search_request=search_request)
