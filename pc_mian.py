import requests
import time
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
    cabins = fares_info.get("lowPriceBase").get("cabin")
    info_list = []
    for j, start_info in enumerate(info):
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
            "cabins": cabins[2 * (j + 1) - 2] if len(cabins) > 1 else cabins,
        })

    fares = [
        {
            "priceType": "PRICE",
            "tripType": "OW",
            "packageType": "Regular",
            "adultPrice": fares_info.get("lowTotalPrice"),
            "adultTax": fares_info.get("tax"),
            "childPrice": "",
            "childTax": "",
            "infantPrice": "",
            "infantTax": "",
            "currency": "CNY",
            "cabinCode": fares_info.get("lowPriceBase").get("cabin"),
            "cabinlevel": "",
            "cabinNum": 2,
            "cabins": "",
            "fareBase": fares_info.get("lowChildPrice"),

            "info": "{\"supplier\"" + ": " + "\"" + str(fares_info.get("originDomain", '')) + "\"}",

        }
    ]

    return {
        "fromSegments": info_list,
        "fares": fares
    }


# 请求头
HEAD = {
    "accept": '*/*',
    "cookie": "QN99=5468; QN1=O5cv5V3uLhBEwDpkBpWDAg==; QunarGlobal=10.86.213.149_-5d2b6b2c_16eea5f2445_2b19|1575890448884; QN269=9A8A8701180E11EA95BBFA163E531C43; _i=ueHd8Skw0r-X98gX4Dq-BjsVezAX; QN601=d8dc9670e8f19f0fc86a36373958daa5; QN48=82fe09c0-0eb2-4b83-b77a-f49083bf0914; fid=192fe013-61a7-405a-8092-9eac1baef328; SplitEnv=D; QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; QN170=111.18.33.214_3e0094_0_JbA2eqru7o1VGxRySFfw%2BP2azQWhHSqBIiK01pFbIRA%3D; quinn=1265ac7a45f3777f668eb85c68529c14bfebabb879edbf7af1c3aec874ef0e41352c4d1f1168b203ec3e9dc5f7e65ecb; SC1=f5cfefa304912bba4615c0604954eccb; SC18=; Alina=5762a981-98f041-78468038-60b02a91-198798698991; QN205=partner; QN277=partner; QN668=51%2C55%2C57%2C56%2C51%2C54%2C53%2C52%2C56%2C52%2C55%2C56%2C53; QN300=3w; QN66=qunar; QN163=0; F235=1576630904542; QN25=ba17d4e8-ba55-452d-9ccc-0bc5b52f29c1-9f992f90; QN43=2; QN42=zxel2304; _q=U.fguxdnr2168; _t=26519149; csrfToken=XTzqSU1KqzqjGkckTelajgqFmzKJebur; _s=s_KM7UQPLYFHQHLFUOEAVQT62SJY; _v=vSYP2vDZ82AMb87uySf7jpo2N-E8DxJaq_1nI3zBMeWv_dZ5FvliUafdGy2crum602dKromAsNbNIrc_J30RBUIga4Kv0W8YxumPVYK8bat2z2Mt_jhUGVOzVLdKJFLx2EHLqhe6XNURowDr9VdzpyUF-F-CvHgA_OrPgR7WS72u; QN44=fguxdnr2168; _vi=WhZtDaNjzKG-2kEh0j0-O3dgNCjfjHHk_ZmPW821iMMkVtCZt9bV-QYlje6A625WY-g9iEEvUgCy9CKugtKuLhfDGRvyMye7lseErYoXfg2EE80Ep66Z31LxYbS_nx9EAM0AeoIEWLQRkNnuSnvqvOky91Xo4COb5WboR-HS3VvQ; _abck=84f62cdb-8a25-4198-8f5d-8491e7c9c6f2~0~1576635341294~-1~-1~-1; QN267=0210538809218433f1e; QN271=83baff72-8c86-4584-b650-56abac34b29c",
    "referer": "https://flight.qunar.com/site/interroundtrip_compare.htm",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "pre": "7ba3f948-41e776-84493953-23be6a10-bf4ae677d440",

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
    "es": "4xeYghIB+vU4YhNeujUpYjNB6xUxYjNe6NPBXi+YYMxVWjJY6N======|1576633979136",
    "queryId": "10.88.66.145:l:-17b00e7b:16f1498deed:498d"
}


# 爬取信息
def get_data(data, head):
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
        return {"code": -2, "msg": "代理失效", "status": -2}
    # response = requests.get(url, params=data, headers=head, proxies=self_ip if self_ip else None, timeout=10)
    response.encoding = "utf-8"

    if response.status_code == 200:
        try:
            response.json()['code']
        except:
            data = response.json().get("result")
            return data.get("flightPrices") if data else {"code": -2, "msg": "请求未返回json数据", "status": -2}
        else:
            return {"code": -2, "msg": "请求成功，未返回任何数据", "status": -2}
    return {"code": -2, "msg": "代理有效，抓取数据超时", "status": -2}


# 单程信息处理函数
def get_info(xinxi: dict, carrier, depCity, depDate, arrCity):
    jp = []
    jipiao = {
        "arrCity": arrCity,
        "carrier": carrier,
        "depCity": depCity,  # head_info.get('journey').get('trips')[0].get("flightSegments")[0].get("depCityCode"),
        "depDate": cl_date(depDate, '-'),
        "retDate": "",
        "meg": "success",
    }
    for i in xinxi.values():
        s = fenxi_info(i)
        if i.get('journey').get('trips')[0].get("flightSegments")[0].get("carrierCode") == carrier or carrier == None:
            jp.append(s)
        jipiao.update({"routings": jp, 'status': 0})

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
