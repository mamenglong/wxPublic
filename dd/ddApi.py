import os
from datetime import datetime, timedelta
from chinese_calendar import is_workday
import dd.tools.bingtools
import dd.tools.ddtools
import dd.tools.wordtools

nowtime = datetime.utcnow() + timedelta(hours=8)  # 东八区时间
today = datetime.strptime(str(nowtime.date()), "%Y-%m-%d")  # 今天的日期
print("nowtime:{} today:{}".format(nowtime, today))
nowdatetime = "{} {}".format(today, nowtime)
access_tokens = os.getenv('DD_ACCESS_TOKEN')
secrets = os.getenv('DD_SIGN_SECRET')


def createJsonContent():
    return {
        "msgtype": "markdown",
        "markdown": {
            "title": "点饭提醒",
            "text": """
#### 点饭提醒 ![来一幅]({}) 
>日期 {}  
>文案：{}""".format(dd.tools.bingtools.getPicUrl(), nowtime, dd.tools.wordtools.get_words(5))
        },
        "at": {
            "isAtAll": True
        }
    }


if __name__ == '__main__':
    date = datetime.now().date()
    #date = datetime(2023, 1, 2)
    print(date)
    if is_workday(date):
        print("工作日")
        ats = access_tokens.split("\n")
        ss = secrets.split("\n")
        index = 0
        for at in ats:
            dd.tools.ddtools.sendPost(at, ss[index], createJsonContent())
            index = index + 1
    else:
        print("休息日")
