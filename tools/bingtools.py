import requests


def getBingPic():
    r = requests.get(url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1")
    pic = r.json()["images"][0]["url"]
    print("https://www.bing.com{}".format(pic))
    return "https://www.bing.com{}".format(pic)