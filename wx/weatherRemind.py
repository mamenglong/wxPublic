import os
import sys
from datetime import date, datetime, timedelta
import math

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
import random
import re
from tools.weathertools import get_weather
from tools.wordtools import get_words

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d")  # 今天的日期

start_date = os.getenv('START_DATE')
wedding_anniversary_date = os.getenv('WEDDING_ANNIVERSARY_DATE')
wedding_anniversary_date_day = datetime.strptime(wedding_anniversary_date, "%Y-%m-%d").strftime("%m-%d")
city = os.getenv('CITY')
birthday = os.getenv('BIRTHDAY')

app_id = os.getenv('APP_ID')
app_secret = os.getenv('APP_SECRET')

user_ids = os.getenv('USER_ID', '').split("\n")
template_id = os.getenv('TEMPLATE_ID')
weather_key = os.getenv('WEATHER_KEY')

if app_id is None or app_secret is None:
    print('请设置 APP_ID 和 APP_SECRET')
    exit(422)

if not user_ids:
    print('请设置 USER_ID，若存在多个 ID 用回车分开')
    exit(422)

if template_id is None:
    print('请设置 TEMPLATE_ID')
    exit(422)


# 获取当前日期为星期几
def get_week_day():
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    week_day = week_list[datetime.date(today).weekday()]
    return week_day


# 纪念日正数
def get_memorial_days_count(start):
    if start is None:
        print('没有设置 START_DATE')
        return 0
    delta = today - datetime.strptime(start, "%Y-%m-%d")
    return delta.days


# 各种倒计时
def get_counter_left(aim_date):
    if aim_date is None:
        return 0

    # 为了经常填错日期的同学们
    if re.match(r'^\d{1,2}\-\d{1,2}$', aim_date):
        next = datetime.strptime(str(date.today().year) + "-" + aim_date, "%Y-%m-%d")
    elif re.match(r'^\d{2,4}\-\d{1,2}\-\d{1,2}$', aim_date):
        next = datetime.strptime(aim_date, "%Y-%m-%d")
        next = next.replace(nowtime.year)
    else:
        print('日期格式不符合要求')

    if next < nowtime:
        next = next.replace(year=next.year + 1)
    return (next - today).days


def format_temperature(temperature):
    return math.floor(temperature)


# 随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


# 返回一个数组，循环产生变量
def split_birthday():
    if birthday is None:
        return None
    return birthday.split('\n')


weather = get_weather(city, weather_key)
if weather is None:
    print('获取天气失败')
    exit(422)
data = {
    "city": {
        "value": city,
        "color": get_random_color()
    },
    "date": {
        "value": "今天是 "+today.strftime('%Y年%m月%d日'),
        "color": get_random_color()
    },
    "week_day": {
        "value": get_week_day(),
        "color": get_random_color()
    },
    "weather": {
        "value": "天气『{}』".format(weather['text']),
        "color": get_random_color()
    },
    "temperature": {
            "value": "温度『{}°』".format(weather['temp']),
            "color": get_random_color()
        },
    "humidity": {
        "value": "湿度『{}%』".format(weather['humidity']),
        "color": get_random_color()
    },
    "wind": {
        "value": weather['windDir'],
        "color": get_random_color()
    },
    "windScale": {
        "value": "『{}级』".format(weather['windScale']),
        "color": get_random_color()
    },
    "love_days": {
        "value": "距离我们相恋 {} 已经 {}天 啦".format(start_date, get_memorial_days_count(start_date)),
        "color": get_random_color()
    },
    "marry_days": {
        "value": "自从 {} 结婚已经 {}天 啦".format(wedding_anniversary_date, get_memorial_days_count(wedding_anniversary_date)),
        "color": get_random_color()
    },
    "wedding_anniversary_days": {
        "value": "距离下一次结婚纪念日{}还有: {}天".format(wedding_anniversary_date_day, get_counter_left(wedding_anniversary_date)),
        "color": get_random_color()
    },
    "words": {
        "value": "一言：{}".format(get_words()),
        "color": get_random_color()
    },
}

for index, aim_date in enumerate(split_birthday()):
    key_name = "birthday_left"
    if index != 0:
        key_name = key_name + "_%d" % index
    data[key_name] = {
        "value": "距离你的生日{}还有：{}天".format(aim_date, get_counter_left(aim_date)),
        "color": get_random_color()
    }

if __name__ == '__main__':
    try:
        client = WeChatClient(app_id, app_secret)
    except WeChatClientException as e:
        print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
        exit(502)

    wm = WeChatMessage(client)
    count = 0
    try:
        for user_id in user_ids:
            print('正在发送给 %s, 数据如下：%s' % (user_id, data))
            res = wm.send_template(user_id, template_id, data)
            count += 1
    except WeChatClientException as e:
        print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
        exit(502)

    print("发送了" + str(count) + "条消息")
