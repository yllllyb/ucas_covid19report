import pytz
import requests
from datetime import datetime

s = requests.Session()

user = "USERNAME"
passwd = "PASSWORD"

def login(s: requests.Session, username, password):
    payload = {
        "username": username,
        "password": password
    }
    r = s.post("https://app.ucas.ac.cn/uc/wap/login/check", data=payload)

    if r.json().get('m') != "操作成功":
        print(r.text)
        print("登录失败")
        exit(1)


def get_daily(s: requests.Session):
    daily = s.get("https://app.ucas.ac.cn/ucasncov/api/default/daily?xgh=0&app_id=ucas")
    j = daily.json()
    d = j.get('d', None)
    if d:
        return daily.json()['d']
    else:
        print("获取昨日信息失败")
        exit(1)


def submit(s: requests.Session, old: dict):
    new_daily=old.copy()
    new_daily['date']=datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d")
    new_daily['app_id']='ucas'
    new_daily['sfzx']='5'
    new_daily['sfjshsjc']='0'
    new_daily['geo_api_info']="ADDRESS"


    print("提交信息:\n", new_daily)
    r = s.post("https://app.ucas.ac.cn/ucasncov/api/default/save", data=new_daily)
    print(r.text)
    result = r.json()
    if result.get('m') == "操作成功":
        print("打卡成功")
    else:
        print("打卡失败，错误信息: ", r.json().get("m"))


print(datetime.now(tz=pytz.timezone("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S %Z"))
login(s, user, passwd)
yesterday = get_daily(s)
submit(s, yesterday)
