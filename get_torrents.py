from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

def get_seeds(title_string: str):
    if "📺" in title_string:
        return int(title_string.split("\n")[2].split("💾")[0].strip().split(" ")[-1])
    else:
        return int(title_string.split("\n")[1].split("💾")[0].strip().split(" ")[-1])
        

def convert_size(size_string:str):
    print(size_string)
    number = float(size_string.strip().split(" ")[0])
    if "GB" in size_string:
        return number * 1000000000
    if "MB" in size_string:
        return number * 1000000
    else:
        return number

def get(title:str):

    # title = "Fast X"
    url = 'http://www.imdb.com/find?s=all&q=' + quote_plus(title)

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

    request = requests.get(url, headers=header)
    soup = BeautifulSoup(request.content, 'html.parser')

    finds = soup.find_all("li",{'class':'find-title-result'})
    links = [find.find("a") for find in finds]

    links = {link.text:link.get("href").split("/")[2] for link in links}

    print("Found results (selecting only first):",links)

    imdb_id = list(links.values())[0]


    base_url = f"https://thepiratebay-plus.strem.fun/stream/movie/{imdb_id}.json"


    torrents = requests.get(base_url).json()['streams']

    results = []

    for item in torrents:
        print(item)
        item['title_clean'] = item["title"].split("\n")[0]
        item['size'] = convert_size(item["title"].split("💾")[-1])
        item['seeds'] = get_seeds(item["title"])
        item['quality'] = item["title"].split("\n")[1] if "📺" in item["title"] else item.get('tag',"")
        item['magnet'] = "magnet:?xt=urn:btih:" + item["infoHash"]
        

        movie_info = {
            "Tracker":item['name'],
            "Details":"https://google.com",
            "Title":item["title_clean"],
            "Size": item['size'],
            "PublishDate": "2023-05-18T14:50:12",
            "Category": [
                    2000
                ],
            "CategoryDesc": "Movies",
            "Seeders": item['seeds'],
            "Peers": 0,
            "MagnetUri": item['magnet']
        }
        results.append(movie_info)
        

    return {"Results":results}