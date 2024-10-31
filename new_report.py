# 安装依赖 pip3 install requests html5lib bs4 schedule
import os
import requests
import json
from bs4 import BeautifulSoup


# 从测试号信息获取
appID = "wx499a1d49d6e6cfb4"
appSecret = "cff48bf2ba0df44528f9e813d19fda87"
#收信人ID即 用户列表中的微信号，见上文
openId = "oWagw69BNFVGlArf7oa9vBHQc504"
# 新闻模板ID
new_template_id = "F90_AyoqqPDWWaXxLDhzELpHdSEl-22L1tbAGXOyTqs"

def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token

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
        #print(responseResult)
        # 提取title
        items = [(item['title'], item['url'],item['author_name']) for item in responseResult['result']['data']]
        # 打印并收集所有title
        for title,url,author_name in items:
            message.append({'title':title,'url':url,'author_name':author_name})  # 将每个title添加到列表中
    else:
        # 网络异常等因素，解析结果异常。可依据业务逻辑自行处理。
        print('请求异常')

    return message  # 返回包含所有标题的列表
def send_new(access_token, news):
    for i in range(len(openId.split(','))):
        for i1 in range(len(news)):
            body = {
                "touser": openId.split(',')[i],
                "template_id": new_template_id,
                "url":  news[i1]['url'],
                "data": {
                    "title": {
                        "value": news[i1]['title']
                    },
                    "author_name": {
                        "value": news[i1]['author_name']
                    }
                }
            }
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
            print(requests.post(url, json.dumps(body)).text)


def new_report():
    # 1.获取access_token
    access_token = get_access_token()
    news= get_new()
    # 3. 发送消息
    send_new(access_token, news)

if __name__ == '__main__':
    new_report()
