from flask import render_template
from utils import query_db
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from io import BytesIO as bytesIO

def page_discover():
    query = """select distinct A.nomA, A.idA, A.profile_path
    from acteur A, langue L, langue L2, parler P, FilmSerie FS, appartenir AP, jouer J, genre G
    where P.idA = A.idA
    and L.nomL = P.nomL
    and J.idA = A.idA
    and J.refFS = FS.refFS
    and FS.refFS = AP.refFS
    and AP.idG = G.idG
    and FS.nomL = L2.nomL
    and L.nomCompletL = 'Francais'
    and L2.nomCompletL = 'Anglais'
    and G.nomG = 'Comédie'"""
    french = query_db(query)[0]
    
    query = """select A.nomA, G.nomG
    from acteur A, FilmSerie FS, genre G, appartenir AP, jouer J
    where AP.idG = G.idG
    and AP.refFS = FS.refFS
    and J.idA = A.idA
    and J.refFS = FS.refFS
    and A.popularity = (select max(popularity) from acteur)"""
    result = query_db(query)[0]
    trend_actor = result[0][0]
    print(result)
    count = 0
    genre_list = []
    count_list = []
    for item in result:
        genre = item[1]
        for genre_name in result:
            if genre_name[1] == genre:
                count += 1
        genre_list.append(genre)
        count_list.append(count)
        count = 0
    plt.figure(figsize=(10, 10))
    plt.pie(count_list, labels=genre_list, normalize=True, autopct='%1.1f%%')
    
    plt.savefig("static/charts/pie.png", transparent=True)
    
    
            
    
    return render_template("discover.html", french=french, trend_actor=trend_actor)