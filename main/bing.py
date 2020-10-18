import environ
import requests
import json
offset = 100
offset_str = str(offset)
env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()
api_key = env('BING_API_KEY')

url = "https://bing-image-search1.p.rapidapi.com/images/search"
trending_url = "https://bing-image-search1.p.rapidapi.com/images/trending"

headers = {
    'x-rapidapi-host': "bing-image-search1.p.rapidapi.com",
    'x-rapidapi-key': api_key
    }
def search():
    global offset, offset_str
    print(offset, offset_str)
    querystring = {"offset": offset_str, "count": "7", "q": "Daily Life and places"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    offset += 7
    offset_str = str(offset)
    return list(map(lambda result: result['contentUrl'], json.loads(response.text)['value']))
