from flask import Flask
from flask import request
from flask import jsonify
import time

from pc_mian import get_data, get_info

app = Flask(__name__)


# 添加地点对应字符串


@app.route('/', methods=["GET"])
def hello_world():
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
        depDate = request.args.get("depDate")  # 出发日期
        st = int(round(time.time() * 1000))  # 当前时间戳

        # 还需要判断请求地点是否正确

        if all((depCity, arrCity, depDate)):
            data.update(
                {"st": st, "depCity": depCity, "arrCity": arrCity, "depDate": depDate, "adultNum": 1,
                 "childNum": 0})
            info = get_data(data, HEAD)
            if type(info) != "str":

                return jsonify({"info": get_info(info, carrier), "code": 200})
        else:
            return jsonify({"code": 400, "mes": "缺少必要的参数"})



if __name__ == '__main__':
    app.run()
