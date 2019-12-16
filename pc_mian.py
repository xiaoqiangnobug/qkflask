import requests
import time
import random
from tool import get_ip

t = time.time()
st = int(round(t * 1000))
url = "https://flight.qunar.com/touch/api/inter/wwwsearch"


# 时间格式处理函数
def cl_date(d, c):
    l = d.split(c)
    return "".join(l)


# 接收时间格式处理
def f_cl_date(d, c):
    return d[:4] + c + d[4:6] + c + d[6:]


# 航班信息处理函数
def fenxi_info(i):
    info = i.get('journey').get('trips')[0].get("flightSegments")
    fares_info = i.get("price")
    info_list = []
    for j, start_info in enumerate(info):
        j += 1
        info_list.append({
            "flightNumber": start_info.get('code'),
            "carrier": start_info.get("carrierCode"),
            "aircraftCode": start_info.get("planeTypeCode"),
            'depAirport': start_info.get('depAirportCode'),
            "depTerminal": start_info.get('depTerminal'),
            "depTime": cl_date(start_info.get("depDate"), '-') + cl_date(start_info.get("depTime"), ":"),
            "arrAirport": start_info.get('arrAirportCode'),
            "arrTime": cl_date(start_info.get("arrDate"), "-") + cl_date(start_info.get("arrTime"), ":"),
            "arrTerminal": start_info.get('arrTerminal') if start_info.get('arrTerminal') else "",
            "shared": start_info.get("codeShareStatus"),
            "realFlightNumber": "",
            "stopCity": "",
            "cabins": (fares_info.get("lowPriceBase").get("cabin"))[2*j-2]
        })
    fares = [
        {
            "priceType": "PRICE",
            "tripType": "OW",
            "packageType": "Regular",
            "adultPrice": fares_info.get("lowPrice"),
            "adultTax": fares_info.get("tax"),
            "childPrice": fares_info.get("lowChildPrice"),
            "childTax": fares_info.get("childTaxType"),
            "infantPrice": "",
            "infantTax": "",
            "currency": "CNY",
            "cabinCode": fares_info.get("priceTag"),
            "cabinlevel": fares_info.get("totalCainLevel"),
            "cabinNum": "",
            "cabins": fares_info.get("lowPriceBase").get("cabin"),
            "fareBase": fares_info.get("lowChildPrice"),
            "info": str({"\"supplier\"": "\"" + fares_info.get("originDomain") + "\""}),
        }
    ]

    return {
        "fromSegments": info_list,
        "fares": fares
    }


# 请求头
HEAD = {
    "accept": '*/*',
    "cookie": "QN99=5468; QN1=O5cv5V3uLhBEwDpkBpWDAg==; QunarGlobal=10.86.213.149_-5d2b6b2c_16eea5f2445_2b19|1575890448884; QN269=9A8A8701180E11EA95BBFA163E531C43; _i=ueHd8Skw0r-X98gX4Dq-BjsVezAX; QN601=d8dc9670e8f19f0fc86a36373958daa5; QN48=82fe09c0-0eb2-4b83-b77a-f49083bf0914; fid=192fe013-61a7-405a-8092-9eac1baef328; SplitEnv=D; QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; Alina=0482a684-1cf590-98446664-34a67222-228acb24d788; QN170=111.18.33.214_3e0094_0_JbA2eqru7o1VGxRySFfw%2BP2azQWhHSqBIiK01pFbIRA%3D; quinn=1265ac7a45f3777f668eb85c68529c14bfebabb879edbf7af1c3aec874ef0e41352c4d1f1168b203ec3e9dc5f7e65ecb; QN66=qunar; QN205=auto_4e0d874a; QN277=auto_4e0d874a; csrfToken=nAN9exzNjvPrTz2SBgEsqDV93yjZFIU4; QN163=0; F235=1575939888029; _vi=c2B3qTmlyoo7YSockUG5GLaFrPq9yn7qHaDiax_QM46x_QbM-6uksVSj7yz_OWfacyGgXkTTqakwh2rYBV05-BOi_cn8aKF7v1i1LkZFGzC5ypPO_gLh2zb6mm3F_-juC8zcbD5wesAhcndU1CVHmMNSI5bGfmXCJFnnFB47twCS; QN300=3w; QN271=747f406a-541a-4594-853c-b70f21edf350; QN267=02105388092ee1e11ae; _abck=b54e88f1-1ab7-47b2-b3d7-dc835a584896~0~1575954272169~-1~-1~-1",
    "referer": "https://flight.qunar.com/site/interroundtrip_compare.htm",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"

}

# 请求参数
data = {
    "depCity": "北京",
    "arrCity": "曼谷",
    "depDate": '2019-12-18',
    # "retDate": "2019-12-18",
    "adultNum": 1,
    "childNum": 0,
    "from": "qunarindex",
    "ex_track": '',
    "_v": 8,
    "st": st,
}


# 爬取信息
def get_data(data, head, ):
    response = ''
    for _ in '123':
        self_ip = get_ip()
        try:
            response = requests.get(url, params=data, headers=head, proxies=self_ip if self_ip else None, timeout=10)
        except:
            print('重新获取代理中...')
        else:
            break
    if not response:
        return {"code": -2}
    response = requests.get(url, params=data, headers=head, proxies=self_ip if self_ip else None, timeout=10000)
    response.encoding = "utf-8"

    if response.status_code == 200:
        try:
            response.json()['code']
        except:
            data = response.json().get("result")
            return data.get("flightPrices") if data else "数据解析失败"
        else:
            return "数据获取失败!"
    return "请求失败"


# 单程信息处理函数
def get_info(xinxi: dict, carrier):
    head_info = xinxi.get(random.choice(list(xinxi.keys())))
    jp = []
    jipiao = {
        "arrCity": head_info.get('journey').get('trips')[0].get("flightSegments")[-1].get("arrCityCode"),
        "carrier": carrier,
        "depCity": head_info.get('journey').get('trips')[0].get("flightSegments")[0].get("depCityCode"),
        "depDate": cl_date(head_info.get('journey').get('trips')[0].get("flightSegments")[0].get('depDate'), '-'),
        "retDate": "",
        "meg": "success",
    }
    for i in xinxi.values():
        s = fenxi_info(i)
        if i.get('journey').get('trips')[0].get("flightSegments")[0].get("carrierCode") == carrier or carrier == None:
            jp.append(s)
        jipiao.update({"routings": jp})

    if not jp:
        jipiao.update({"status": -1})
        return jipiao

    return jipiao


# 往返信息采集函数
def get_infos(xinxi: dict):
    jipiao = []
    for i in xinxi.values():
        # 航班具体信息
        jipiao.append({"qu": fenxi_info(i.get('journey').get('trips')[0].get("flightSegments")),
                       "fan": fenxi_info(i.get('journey').get('trips')[1].get("flightSegments"))})
    return jipiao


if __name__ == "__main__":
    pass
