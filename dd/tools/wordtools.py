# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
import random

import requests

type_list = ["chp", "pyq", "du"]
random.choice(type_list)

wordUrlList = [
    "https://api.ixiaowai.cn/ylapi/index.php"
    "https://api.ixiaowai.cn/tgrj/index.php"
    "https://zj.v.api.aa1.cn/api/wenan-wm/?type=text"
]
typeList = [0, 0]


def get_words(times=5):
    print("get_words:{}".format(times))
    if random.choice(typeList) == 0:
        print("getShaDiao:{}".format(times))
        return getShaDiao(times)
    else:
        print("getOther:{}".format(times))
        return getOther(times)


def getShaDiao(times):
    # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause
    # program to hang indefinitely.
    url = "https://api.shadiao.pro/" + random.choice(type_list)
    words = requests.get(url, timeout=1000)
    if words.status_code != 200 and times > 0:
        return get_words(times - 1)
    r = words.json()['data']['text']
    print("getShaDiao:{}:{}".format(url, r))
    return r


def getOther(times):
    url = random.choice(wordUrlList)
    try:
        words = requests.get(url, timeout=5000)
        print("getOther:{}:{}".format(url, words))
        if words == "" and times > 0:
            return get_words(times - 1)
        return words
    except Exception as e:
        if times > 0:
            return get_words(times - 1)
        else:
            return "文案获取失败！！！"


if __name__ == '__main__':
    url = random.choice(wordUrlList)
    words = requests.get(url, timeout=5000)
    print(words)