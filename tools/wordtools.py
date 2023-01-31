# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
import random

import requests

type_list = ["chp", "pyq", "du"]
random.choice(type_list)

def get_words(self, times=5):
    # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause
    # program to hang indefinitely.
    url = "https://api.shadiao.pro/" + random.choice(type_list)
    words = requests.get(url, timeout=100)
    if words.status_code != 200 and times > 0:
        return self.get_words(times - 1)
    r = words.json()['data']['text']
    print("get_words:{}:{}".format(url, r))
    return r


