from flask import Flask, redirect, render_template, request, url_for, session
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import random

load_dotenv()


app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
app.config["SECRET_KEY"] = secret_key

path = "./database.db"

bcrypt = Bcrypt(app)

def create_connexion(path: str):
    if not os.path.exists(path):
        print("La base de données n'existe pas")
        return None
    try:
        conn = sqlite3.connect(path)
        return conn
    except:
        print("Erreur lors de la connexion à la base de données")
    return None

def query_db(query, params=None):
    connexion = create_connexion(path)
    cursor = connexion.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connexion.commit()
    result = cursor.fetchall()
    metadata = cursor.description
    connexion.close()
    return result, metadata


@app.route("/")
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


@app.route("/find")
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


@app.route("/login", methods=["POST", "GET"])
def page_login():
    if request.method == "POST":
        emailU = request.form.get("email")
        passwordU = request.form.get("password")
        query = "select * from utilisateur where emailU = ?"
        params = [emailU]
        result = query_db(query, params)
        if len(result[0]) == 0:
            message = "L'email ou le mot de passe est incorrect"
            return render_template("login.html", message=message)
        if bcrypt.check_password_hash(result[0][0][3], passwordU):
            session["user"] = {
                "id": result[0][0][0],
                "nom": result[0][0][1],
                "prenom": result[0][0][2],
                "dateInscription": result[0][0][4],
                "idAbo": result[0][0][5],
                "idStu": result[0][0][6],
                "email": result[0][0][7],
            }
            return redirect(url_for("page_home"))
        else:
            message = "L'email ou le mot de passe est incorrect"
            return render_template("login.html", message=message)
    return render_template("login.html")  


@app.route("/logout", methods=["GET", "POST"])
def page_logout():
    session.pop("user", None)
    return redirect(url_for("page_home"))


@app.route("/register", methods=["POST", "GET"])
def page_register():
    if request.method == "POST":
        nomU = request.form.get("lastname")
        prenomU = request.form.get("firstname")
        passwordU = request.form.get("password")
        passwordU2 = request.form.get("password2")
        emailU = request.form.get("email")
        if passwordU != passwordU2:
            message = "Les mots de passe ne correspondent pas"
            return render_template("register.html", message=message)
        query = "select * from utilisateur where emailU = ?"
        params = [emailU]
        result = query_db(query, params)
        if len(result[0]) > 0:
            print(result[0])
            print(True)
            message = "Cet email est déjà utilisé"
            return render_template("register.html", message=message)
        # cryptage du mot de passe pour ne pas le garder en clair dans la base de données
        passwordU = bcrypt.generate_password_hash(password=passwordU)
        query = "insert into utilisateur (nomU, prenomU, passwordU, dateInscriptionU, emailU) values (?, ?, ?, ?, ?)"
        
        dateInscriptionU = datetime.now().strftime("%y-%m-%d")
        params = [nomU, prenomU, passwordU, dateInscriptionU, emailU]
        query_db(query, params)
        return redirect(url_for("page_login"))
        
    return render_template("register.html")


@app.route("/info", methods=["POST"])
def page_info():
    key = request.form.get("key")
    if key == "contact":
        actor_name = request.form.get("actor_name")
        message = "Un message a été envoyé à l'acteur " + actor_name
    else:
        price = request.form.get("price")
        message = "Nous avons reçu votre paiement de " + price + ". Nous espérons que vous appricez notre service !"
        
    return render_template("info.html", message=message)


@app.route("/discover")
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


@app.route("/detail/<keyword>/<id>", methods=["POST", "GET"])
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


@app.route("/get_all/<keyword>/<page>")
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


@app.route("/payment/<price>")
def page_offer(price):
    # processeur de paiment
    return render_template("offer.html", price=price)

if __name__ == "__main__":
    app.run(debug=True)



        
        
        
    

