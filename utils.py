import sqlite3
import os

path = "./database.db"

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