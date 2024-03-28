import matplotlib.pyplot as plt
from flask import render_template
from utils import query_db
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import random


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
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.pie(count_list, labels=genre_list, normalize=True, autopct='%1.1f%%')
    plt.savefig("static/charts/pie.png", transparent=True)

    query = """select FS.nomFS, (FS.recetteFS - FS.budgetFS), A.nomA
    from FilmSerie FS, jouer J, acteur A
    where J.refFS = FS.refFS
    and J.idA = A.idA
    and A.idA = (select A.idA
    from acteur A, FilmSerie FS, jouer J
    where A.idA = J.idA
    and J.refFS = FS.refFS
    and FS.budgetFS is not NULL
    and FS.recetteFS is not Null
    GROUP by A.idA
    order by count(FS.refFS) desc
    limit 1)"""
    box_office = query_db(query)[0]
    actor_name = box_office[0][2]
    film_name = [item[0] for item in box_office]
    box_office = [item[1] for item in box_office]
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.xlabel("Films")
    plt.ylabel("Millions de d'euros")
    ax.bar(film_name, box_office)
    plt.savefig("static/charts/bar.png", transparent=True)

    query = """select substr(FS.dateFS,1,4), avg(FS.avisFS) as popularity
    from FilmSerie FS, genre G, appartenir A
    where FS.refFS = A.refFS
    and A.idG = G.idG
    and G.nomG = 'Action'
    group by substr(FS.dateFS, 1, 4), FS.formatFS
    order by date(dateFS)
    """
    result = query_db(query)[0]
    year = {int(item[0]): item[1] for item in result}
    mini, maxi = int(min(year.keys())), int(max(year.keys()))
    i = mini
    while i < maxi:
        if i not in year.keys():
            year[i] = None
        i += 1
    year = sorted(year.items())
    fig, ax = plt.subplots(figsize=(10, 10))
    x = [item[0] for item in year]
    y = [item[1] for item in year]
    df = pd.DataFrame({'x': x, 'y': y})
    df = df.interpolate(method='linear', limit=None)
    ax.plot(df["x"], df["y"])
    plt.xlabel('Année')
    plt.ylabel('Popularité')
    plt.savefig("static/charts/line.png", transparent=True)
    
    query = """
    select STU.nomStu, count(distinct L.nomL)
    from acteur A, studio STU, produire PR, FilmSerie FS, jouer J, parler P, langue L
    where PR.refFS = FS.refFS
    and PR.idStu = STU.idStu
    and J.refFS = FS.refFS
    and J.idA = A.idA
    and P.idA = A.idA
    and P.nomL = L.nomL
    group by STU.nomStu
    order by count(distinct L.nomL) desc, STU.idStu
    limit 20"""
    result = query_db(query)[0]
    random.shuffle(result)
    studio = [item[0] for item in result]
    language = [item[1] for item in result]
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.barh(studio, language)
    plt.xlabel('Nombre de langues')
    plt.ylabel('Studio')
    plt.savefig("static/charts/barh.png", transparent=True)
    
    return render_template("discover.html", french=french, trend_actor=trend_actor, actor_name=actor_name)
