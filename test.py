import os

import requests
from dotenv import load_dotenv

load_dotenv()


api_token = os.environ.get("API_TOKEN")
back_drop_path = "https://image.tmdb.org/t/p/original"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {api_token}"
    }

# url = "https://api.themoviedb.org/3/trending/person/week?language=en-US&page=1000"
url = "https://api.themoviedb.org/3/person/popular?language=en-US&page=1000"
r = requests.get(url=url, headers=headers).json()
print(r)