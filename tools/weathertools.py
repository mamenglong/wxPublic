import requests

#weather 直接返回对象，在使用的地方用字段进行调用
# 城市列表 https://github.com/qwd/LocationList/blob/master/China-City-List-latest.csv
# 接口文档 https://dev.qweather.com/docs/api/weather/weather-now/
def get_weather(city, weather_key):
    url = "https://devapi.qweather.com/v7/weather/now?location={}&key={}&lang=zh".format(city, weather_key)
    # OpenRefactory Warning: The 'requests.get' method does not use any 'timeout' threshold which may cause program to hang indefinitely.
    try:
        res = requests.get(url, timeout=100).json()
        if res is None:
            return None
        if res['code'] != "200":
            return None
        weather = res["now"]
        return weather
    except Exception as e:
        print(e)
        return None
