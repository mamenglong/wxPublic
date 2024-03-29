import random

import requests


def getBingPic():
    r = requests.get(url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1")
    pic = r.json()["images"][0]["url"]
    print("https://www.bing.com{}".format(pic))
    return "https://www.bing.com{}".format(pic)


urlList = [
    "https://api.paugram.com/bing",
    "https://api.paugram.com/wallpaper",
    "https://api.r10086.com/img-api.php?type=动漫综合1",
    "https://api.ixiaowai.cn/api/api2.php",
    "https://api.yimian.xyz/img",
    "https://api.dujin.org/pic/yuanshen/",
    "https://api.btstu.cn/sjbz/api.php?lx=suij&format=images",
    "https://api.btstu.cn/sjbz/api.php?lx=meizi&format=images",
    "https://api.btstu.cn/sjbz/api.php?lx=dongman&format=images",
    "https://api.r10086.com/img-api.php?type=少女前线1",
    "https://api.ixiaowai.cn/mcapi/mcapi2.php",
    "https://api.ixiaowai.cn/api/api.php",
]


def getPicUrl():
    url = random.choice(urlList)
    print("getPicUrl:" + url)
    return url
