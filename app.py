from tool import code_city
from flask import Flask
from flask import request
from flask import jsonify
import time

from pc_mian import get_data, get_info, f_cl_date

app = Flask(__name__)


# 添加地点对应字符串


@app.route('/', methods=["GET"])
def hello_world():
    HEAD = {
        "accept": '*/*',
        "cookie": "QN99=5468; QN1=O5cv5V3uLhBEwDpkBpWDAg==; QunarGlobal=10.86.213.149_-5d2b6b2c_16eea5f2445_2b19|1575890448884; QN269=9A8A8701180E11EA95BBFA163E531C43; _i=ueHd8Skw0r-X98gX4Dq-BjsVezAX; QN601=d8dc9670e8f19f0fc86a36373958daa5; QN48=82fe09c0-0eb2-4b83-b77a-f49083bf0914; fid=192fe013-61a7-405a-8092-9eac1baef328; SplitEnv=D; QN621=1490067914133%3DDEFAULT%26fr%3Dqunarindex; QN170=111.18.33.214_3e0094_0_JbA2eqru7o1VGxRySFfw%2BP2azQWhHSqBIiK01pFbIRA%3D; quinn=1265ac7a45f3777f668eb85c68529c14bfebabb879edbf7af1c3aec874ef0e41352c4d1f1168b203ec3e9dc5f7e65ecb; SC1=f5cfefa304912bba4615c0604954eccb; SC18=; Alina=5762a981-98f041-78468038-60b02a91-198798698991; QN205=partner; QN277=partner; QN668=51%2C55%2C57%2C56%2C51%2C54%2C53%2C52%2C56%2C52%2C55%2C56%2C53; QN300=3w; QN66=qunar; csrfToken=FFoAHPPIcPDZhqxR6e4APnJtP4KW6Lri; QN163=0; F235=1576630904542; _vi=CnmYlNlldqAnGZlV84ulppQYxyhz6Rmg4mOBNBv5zMYkCthPGY3jcLOxH2fTbiMIlrp5mA3BP0z6HpzwcgjwK0X-Oj7f6xFlHxl2mzIv2cSSjGrqGwGw3IomGId666798rajN87oTXTILkY9PxIlLC-H3NNmxlT9jaJmED-p5J4A; QN267=02105388092ca00d893; QN271=71a92c56-20a5-4920-85d3-73fa06203755",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        # "pre": "9b027f92-3b1c26-3949aa78-73b41530-de12dd0b9da6",
        "ontent-type" : "application/x-www-form-urlencoded",
        "referer": "https://flight.qunar.com/site/oneway_list_inter.htm?searchDepartureAirport=%E5%8C%97%E4%BA%AC&searchArrivalAirport=%E5%90%89%E9%9A%86%E5%9D%A1&searchDepartureTime=2019-12-20&searchArrivalTime=2019-12-25&nextNDays=0&startSearch=true&fromCode=BJS&toCode=KUL&from=qunarindex&lowestPrice=null&favoriteKey=&showTotalPr=null&adultNum=1&childNum=0&cabinClass=",


    }

    # 请求参数
    data = {
        "depCity": "北京",
        "arrCity": "曼谷",
        "adultNum": 1,
        "childNum": 0,
        "from": "qunarindex",
        "ex_track": '',
        "_v": 8,
    }
    st = int(round(time.time() * 1000))

    if request.method == 'GET':

        carrier = request.args.get("carrierCode")  # 出港航空公司两字代码
        depCity = request.args.get('depCity')  # 出发城市
        arrCity = request.args.get("arrCity")  # 到达城市
        depDate = f_cl_date(request.args.get("depDate"), '-')
        # 出发日期
        st = int(round(time.time() * 1000))  # 当前时间戳

        # 还需要判断请求地点是否正确

        if all((depCity, arrCity, depDate, carrier)):
            # 查看转换是否成功
            if not all([code_city(arrCity), code_city(depCity)]):
                return jsonify({"code": 400, "msg": "获取三字代码失败", "status": -2}, )

            # 更新请求参数
            data.update(
                {"st": st, "depCity": code_city(depCity), "arrCity":code_city(arrCity), "depDate": depDate, "adultNum": 1,
                 "childNum": 0, "carrier": carrier})
            info = get_data(data, HEAD)
            if info.get('code') == -2:
                return jsonify(info)
            if type(info) is not str:
                return jsonify(get_info(xinxi=info, carrier=carrier, depDate=depDate, depCity=depCity.upper(), arrCity=arrCity.upper()))
            else:
                return jsonify({"status": -3, "msg": "信息解析错误"})
        else:
            return jsonify({"code": 400, "mes": "信息参数格式不正确, 请确认参数全部存在且格式正确", "status": -2}, )


if __name__ == '__main__':
    app.run()
