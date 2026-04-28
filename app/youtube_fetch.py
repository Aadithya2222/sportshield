import requests

API_KEY = "AIzaSyCRUylqYGmfGELI-ay0XMxt6ZPx0irbM9k"

def search_youtube(query):
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []

    for item in data["items"]:
        video = {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["default"]["url"]
        }
        results.append(video)

    return results