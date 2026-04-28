from youtube_fetch import search_youtube

videos = search_youtube("IPL highlights")

for v in videos:
    print(v)
    