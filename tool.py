import json
import requests


# 城市三字代码获取
def get_city(code):
    data = {"lang": "zh", "q": code.upper(), "sa": True}
    response = requests.get(url="https://www.qunar.com/suggest/livesearch2.jsp", params=data)
    response.encoding = "utf-8"
    city_code = ""

    if (not response.status_code == 200) and (not response.json()):
        return ''
    for i in response.json().get("result"):
        if i.get("code") == code.upper():
            city_code = i.get("key")
            print(city_code)
    # 查询成功, 将数据返回并写入csv文件
    if not city_code:
        return ''
    # 先读一次
    with open("code_city.json", 'r', encoding='utf-8') as f:
        try:
            d = json.load(f)
        except:
            d = {}

    with open('code_city.json', 'w', encoding='utf-8') as f:
        if d:
            d.update({code.upper(): city_code})
            json.dump(d, f)
        else:
            d = {code.upper(): city_code}
            json.dump(d, f)

    return city_code


# 三字代码转换城市函数
def code_city(code):
    # 本地读取文件
    with open('code_city.json', 'r', encoding='utf-8') as f:
        try:
            d = json.load(f)
        except:
            d = {}
    # 在本地获取
    city_name = d.get(code.upper())
    if city_name:
        return city_name
    else:
        return get_city(code)


# 重新获取代理请求
def get_ip():
    url = 'http://47.92.24.159:6998/api/Vps/GetProxyAuth?groupCode=search&token=d6361595545b4847b25a111fd3c4b35f'
    response = requests.get(url)
    response.encoding = 'utf-8'
    status_json = response.json()
    if response.status_code == 200 and status_json:
        host = status_json.get('data').get("ip")
        if host:
            return {"http": 'xiy_001:G232323@' + host + ":36912", "https": "xiy_001:G232323@" + host + ":36912"}
    return ''


if __name__ == "__main__":
    pass
