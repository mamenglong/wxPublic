import argparse
import base64
import hashlib
import hmac
import json
import os
import time
import urllib
from datetime import date, datetime, timedelta
import requests

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d")  # 今天的日期
print("nowtime:{} today:{}".format(nowtime, today))
nowdatetime = "{} {}".format(today, nowtime)
access_token = os.getenv('DD_ACCESS_TOKEN')
secret = os.getenv('DD_SIGN_SECRET')

# 彩虹屁 接口不稳定，所以失败的话会重新调用，直到成功
def get_words(times=5):
    # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause program to hang indefinitely.
    words = requests.get("https://api.shadiao.pro/chp", timeout=100)
    if words.status_code != 200 and times > 0:
        return get_words(times - 1)
    r = words.json()['data']['text']
    print("get_words:{}".format(r))
    return r


def createSign():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    return timestamp, sign


def sendPost():
    try:
        timestamp, sign = createSign()
        params = {'access_token': access_token, 'sign': sign, 'timestamp': timestamp}
        jsonData = json.dumps(createJsonContent())
        print(jsonData)
        headers = {"Content-Type": "application/json"}
        r = requests.post("https://oapi.dingtalk.com/robot/send", data=jsonData, params=params, headers=headers)
        print("发送结果{}".format(r.json()))
    except Exception as e:
        print("发送错误  {} ".format(e.__str__()))


def createJsonContent():
    return {
        "msgtype": "markdown",
        "markdown": {
            "title": "每日提醒",
            "text": """#### 点饭啦，点饭啦 ![来一幅]({}) \n> 今日 {}\n> 来一杯：{}""".format(getBingPic(), nowtime, get_words(5))
        },
        "at": {
            "isAtAll": True
        }
    }


def getBingPic():
    r = requests.get(url="https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1")
    pic = r.json()["images"][0]["url"]
    print("https://www.bing.com{}".format(pic))
    return "https://www.bing.com{}".format(pic)


if __name__ == '__main__':
    sendPost()
