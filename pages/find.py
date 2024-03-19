from flask import render_template, request
from utils import query_db

def page_find():
    actors_list = []
    search_request = request.args.get("search_request")
    query = f"select * from acteur "
    result = query_db(query)[0]
    return "find"