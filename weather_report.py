# 安装依赖 pip3 install requests html5lib bs4 schedule
import os
import requests
import json
from bs4 import BeautifulSoup
def get_new():
    # 基本参数配置
    apiUrl = 'http://v.juhe.cn/toutiao/index'  # 接口请求URL
    apiKey = '721b5da82bb56005199f0d1692187021'  # 在个人中心->我的数据,接口名称上方查看

    requestParams = {
        'key': apiKey,
        'type': 'caijing',
        'page': '0',
        'page_size': 5,
        'is_filter': 1,
    }

    # 发起接口网络请求
    response = requests.get(apiUrl, params=requestParams)

    # 初始化message为一个空列表
    message = []

    # 解析响应结果
    if response.status_code == 200:
        responseResult = response.json()
        # 提取title
        titles = [item['title'] for item in responseResult['result']['data']]

        # 打印并收集所有title
        for title in titles:
            print(title)
            message.append(title)  # 将每个title添加到列表中
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')

    return message  # 返回包含所有标题的列表
# 从测试号信息获取
appID = "wx499a1d49d6e6cfb4"
appSecret = "cff48bf2ba0df44528f9e813d19fda87"
#收信人ID即 用户列表中的微信号，见上文
openId = "oWagw69BNFVGlArf7oa9vBHQc504,oWagw6-HSBAj79R0CoTBebuw0NGs,oWagw63MjdY9lQBnsTCMP6jzssKw,oWagw6z1DkmJr5tG1UD8buxRQ8QA,oWagw67mbzQOjfQMb00lIj4Y2tbU"
# 天气预报模板ID
weather_template_id = "YZnZroT8SvLREThcBHINh7zCskFWiYXMtu5X-l2ApMQ"

def get_weather(my_city):
    urls = ["http://www.weather.com.cn/textFC/hb.shtml",
            "http://www.weather.com.cn/textFC/db.shtml",
            "http://www.weather.com.cn/textFC/hd.shtml",
            "http://www.weather.com.cn/textFC/hz.shtml",
            "http://www.weather.com.cn/textFC/hn.shtml",
            "http://www.weather.com.cn/textFC/xb.shtml",
            "http://www.weather.com.cn/textFC/xn.shtml"
            ]
    for url in urls:
        resp = requests.get(url)
        text = resp.content.decode("utf-8")
        soup = BeautifulSoup(text, 'html5lib')
        div_conMidtab = soup.find("div", class_="conMidtab")
        tables = div_conMidtab.find_all("table")
        for table in tables:
            trs = table.find_all("tr")[2:]
            for index, tr in enumerate(trs):
                tds = tr.find_all("td")
                # 这里倒着数，因为每个省会的td结构跟其他不一样
                city_td = tds[-8]
                this_city = list(city_td.stripped_strings)[0]
                if this_city == my_city:

                    high_temp_td = tds[-5]
                    low_temp_td = tds[-2]
                    weather_type_day_td = tds[-7]
                    weather_type_night_td = tds[-4]
                    wind_td_day = tds[-6]
                    wind_td_day_night = tds[-3]

                    high_temp = list(high_temp_td.stripped_strings)[0]
                    low_temp = list(low_temp_td.stripped_strings)[0]
                    weather_typ_day = list(weather_type_day_td.stripped_strings)[0]
                    weather_type_night = list(weather_type_night_td.stripped_strings)[0]

                    wind_day = list(wind_td_day.stripped_strings)[0] + list(wind_td_day.stripped_strings)[1]
                    wind_night = list(wind_td_day_night.stripped_strings)[0] + list(wind_td_day_night.stripped_strings)[1]

                    # 如果没有白天的数据就使用夜间的
                    temp = f"{low_temp}——{high_temp}摄氏度" if high_temp != "-" else f"{low_temp}摄氏度"
                    weather_typ = weather_typ_day if weather_typ_day != "-" else weather_type_night
                    wind = f"{wind_day}" if wind_day != "--" else f"{wind_night}"
                    return this_city, temp, weather_typ, wind


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def get_daily_love():
    # 每日一句情话
    url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
    r = requests.get(url)
    all_dict = json.loads(r.text)
    sentence = all_dict['returnObj'][0]
    daily_love = sentence
    return daily_love


def send_weather(access_token, weather):

    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")
    for i in range(len(openId.split(','))):
        body = {
            "touser": openId.split(',')[i],
            "template_id": weather_template_id.strip(),
            "url": "https://weixin.qq.com",
            "data": {
                "date": {
                    "value": today_str
                },
                "region": {
                    "value": weather[0]
                },
                "weather": {
                    "value": weather[2]
                },
                "temp": {
                    "value": weather[1]
                },
                "wind_dir": {
                    "value": weather[3]
                },
                "today_note": {
                    "value": get_daily_love()
                }
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
        print(requests.post(url, json.dumps(body)).text)

def send_new(access_token, news):
    for i in range(len(openId.split(','))):
        body = {
            "touser": openId.split(',')[i],
            "template_id": 'T6FQ7pRcKPWX8U8Usmiixm-TlqaQpK3Sg7Q7wExkyiM',
            "url": "https://weixin.qq.com",
            "data": {
                "new1": {
                    "value": news[0]
                },
                "new2": {
                    "value": news[1]
                },
                "new3": {
                    "value": news[2]
                },
                "new4": {
                    "value": news[3]
                },
                "new5": {
                    "value": news[4]
                },
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
        print(requests.post(url, json.dumps(body)).text)

def weather_report(this_city):
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取天气
    weather = get_weather(this_city)
    print(f"天气信息： {weather}")

    
    # 3. 发送消息
    send_weather(access_token, weather)

def new_report():
    # 1.获取access_token
    access_token = get_access_token()
    news= get_new()
    # 3. 发送消息
    send_new(access_token, news)

if __name__ == '__main__':
    weather_report("泉州")
    new_report()
