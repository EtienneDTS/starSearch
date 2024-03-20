from utils import query_db
from flask import render_template, redirect, url_for, request

def page_get_all(keyword: str, page: int):
    page = int(page)
    filter = request.args.get("filter", None)
    if filter != None:
        arg, order = filter.split()
    gender = request.args.get("gender", None)
    if gender and gender in ("1", "2"):
        # Ajout du 0 car deux parametres sont attendus
        gender = [int(gender), 0]
    else:
        # par defaut tout les genres
        gender = [1, 2]    
    
    if page < 1:
        return redirect(url_for('page_get_all', keyword=keyword, page=1))

    start = (page -1) * 20
    end = start + 20
    
    context = {
        "keyword": keyword,
        "page": page,
    }
    
    if keyword == "acteurs":
        detail_keyword = "acteur"
    elif keyword == "films" or keyword == "series":
        detail_keyword = "FilmSerie"
    context["detail_keyword"] = detail_keyword    
    print(context["detail_keyword"])
    
    
    if keyword == "films":
        title = "Tous les films"
        query = "select * from FilmSerie where formatFS = 'F'  order by voteFS"
        if filter != None:
            query = f"select * from FilmSerie where formatFS = 'F' order by {arg} {order}; "
        result = query_db(query)[0]
        context["max_page"] = len(result) // 20
        if len(result) % 20 != 0:
            context["max_page"] += 1
        context["data"] = result[start:end]
        
        
    elif keyword == "series":
        title = "Toutes les series"
        query = "select * from FilmSerie where formatFS = 'S'  order by voteFS desc"
        if filter != None:
            query = f"select * from FilmSerie where formatFS = 'S' order by {arg} {order}; "
        result = query_db(query)[0]
        context["max_page"] = len(result) // 20
        if len(result) % 20 != 0:
            context["max_page"] += 1
        context["data"] = result[start:end]
        
    elif keyword == "acteurs":
        title = "Tous les acteurs"
        query = f"select * from acteur where genreA in (?,?);"
        if filter != None:
            query = f"select * from acteur where genreA in (?,?) order by {arg} {order};"
        result = query_db(query, gender)[0]
        context["max_page"] = len(result) // 20
        if len(result) % 20 != 0:
            context["max_page"] += 1
        context["data"] = result[start:end]
    else:
        return redirect("page_home")
    if page == 1:
        context["previous_page"] = 1
    else:
        context["previous_page"] = page - 1
    if page == context["max_page"]:
        context["next_page"] = context["max_page"]
    else:
        context["next_page"] = page + 1
    return render_template("get_all.html", **context, title=title, filter=filter, gender=gender)