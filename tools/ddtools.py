import base64
import hashlib
import hmac
import json
import time
import urllib

import requests


def createSign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    print(timestamp)
    print(sign)
    return timestamp, sign


def sendPost(access_token, secret, content):
    try:
        timestamp, sign = createSign(secret)
        params = {'access_token': access_token, 'sign': sign, 'timestamp': timestamp}
        jsonData = json.dumps(content)
        print(jsonData)
        headers = {"Content-Type": "application/json"}
        r = requests.post("https://oapi.dingtalk.com/robot/send", data=jsonData, params=params, headers=headers)
        print("发送结果{}".format(r.json()))
    except Exception as e:
        print("发送错误  {} ".format(e.__str__()))
