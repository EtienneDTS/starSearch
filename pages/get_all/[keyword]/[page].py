from utils import query_db
from flask import render_template, redirect, url_for

def page_get_all(keyword: str, page: int):
    page = int(page)
    if page < 1:
        return redirect(url_for('page_get_all', keyword=keyword, page=1))

    start = (page -1) * 20
    end = start + 20
    
    context = {
        "keyword": keyword,
        "page": page,
    }
    
    if keyword == "films":
        query = "select * from FilmSerie where formatFS = 'F'  order by voteFS desc"
        result = query_db(query)[0]
        context["max_page"] = len(result) // 20
        if len(result) % 20 != 0:
            context["max_page"] += 1
        context["data"] = result[start:end]
        
        
    elif keyword == "series":
        query = "select * from FilmSerie where formatFS = 'S'  order by voteFS desc"
        result = query_db(query)[0]
        context["max_page"] = len(result) // 20
        if len(result) % 20 != 0:
            context["max_page"] += 1
        context["data"] = result[start:end]
        
    elif keyword == "acteurs":
        query = "select * from acteur order by popularity desc"
        result = query_db(query)[0]
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
    return render_template("get_all.html", **context)