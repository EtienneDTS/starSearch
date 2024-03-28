from flask import render_template
from utils import query_db

def page_home():
    query = "select * from acteur order by popularity desc limit 4"
    famous_actors = query_db(query, None)[0]
    print(famous_actors)
    query = "select * from FilmSerie where formatFS = 'F'  order by voteFS desc limit 4"
    trending_films = query_db(query, None)[0]
    query = "select * from FilmSerie where formatFS = 'S'  order by voteFS desc limit 4"
    trending_series = query_db(query, None)[0]
    
    context = {
        "famous_actors": famous_actors,
        "trending_series": trending_series,
        "trending_films": trending_films,
    }
    
    return render_template('home.html', **context)