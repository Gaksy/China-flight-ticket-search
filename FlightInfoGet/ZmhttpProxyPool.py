import json
import urllib.parse
import requests

from FlightInfoGet import FlightException
from FlightInfoGet import Proxy
from datetime import datetime


class ZmhttpProxyInfo(Proxy.ProxyInfo):
    def __init__(self, proxy_ip: str = None, proxy_port: int = 0, protocol: str = "http"):
        super().__init__(proxy_ip, proxy_port, protocol)

        self.expire_time = None
        self.city = None
        self.isp = None
        self.outip = None

    def __str__(self):
        return super().__str__() + f"\nZmhttpProxyInfo: {{'expire_time':{self.expire_time}, 'city':{self.city}, 'isp':{self.isp}, 'outip':{self.outip}}}"


class ZmhttpProxyPool:
    def __init__(self, appkey: str = None, neek: str = None):
        self.__userinfo_map = {
            "appkey": appkey,
            "neek": neek
        }

        self.__proxy_get3_url = "http://http.tiqu.letecs.com/getip3"
        self.__proxy_get3_map = {
            "type": 2,  # 数据格式：1:TXT 2:JSON 3:html
            "time": 4,  # 稳定时长 1:5-25min 2:25min-3h 3:3-6h 4:1-5min
            "pro": 0,  # 省份，默认全国
            "city": 0,  # 城市，默认全国
            "yys": 0,  # 0:不限 100026:联通 100017:电信
            "port": 1,  # IP协议 1:HTTP 2:SOCK5 11:HTTPS
            "pack": 0,  # 用户套餐ID
            "ts": 1,  # 是否显示IP过期时间: 1显示 0不显示
            "ys": 1,  # 是否显示IP运营商: 1显示
            "cs": 1,  # 否显示位置: 1显示
            "lb": 0,  # 分隔符(1:\r\n 2:/br 3:\r 4:\n 5:\t 6 :自定义)
            "sb": None,  # 自定义分隔符
            "pd": 4,  # 端口位数（4:4位端口 5:5位端口）
            "mr": 1,  # 去重选择（1:自动去重 2:单日去重 3:不去重）
            "regions": None  # 全国混拨地区
        }

    @staticmethod
    def __GetWebContent(url):
        web_response = requests.get(url)
        web_content = web_response.content.decode("utf-8")

        # 网页内容为空
        if web_content is None:
            raise FlightException.WebContentNull("网页返回内容为空")

        # 解析Json
        dec_json = json.loads(web_content)

        # 检查是否获取成功
        if dec_json["code"] != 0:
            raise FlightException.ZmHttpProxyError(dec_json["msg"])

        return dec_json

    def GetBalance(self):
        # 生成查询URL
        balance_url_arg = urllib.parse.urlencode(self.__userinfo_map)
        balance_url = urllib.parse.urljoin("https://wapi.proxy.linkudp.com/api/get_my_balance", balance_url_arg)

        # 获取Json
        balance_json = self.__GetWebContent(balance_url)

        # 获取余额信息
        balance = balance_json["data"]["balance"]

        return balance

    def SetGet3Protocol(self, protocol: str = "http"):
        if protocol == "http":
            self.__proxy_get3_map["port"] = 1
        elif protocol == "sock5":
            self.__proxy_get3_map["port"] = 2
        elif protocol == "https":
            self.__proxy_get3_map["port"] = 3

    def GetGet3Protocol(self):
        protocol = None

        if self.__proxy_get3_map["port"] == 1:
            protocol = "http"
        elif self.__proxy_get3_map["port"] == 2:
            protocol = "sock5"
        elif self.__proxy_get3_map["port"] == 3:
            protocol = "https"

        return protocol

    def Get3Proxy(self, num: int = 1):
        # 设置用户ID参数
        get3_url_age_map = self.__proxy_get3_map
        get3_url_age_map["neek"] = self.__userinfo_map["neek"]
        # 设置代理数量
        get3_url_age_map["num"] = num
        # 生成URL
        get3_url_arg = urllib.parse.urlencode(get3_url_age_map)
        get3_url = urllib.parse.urljoin(self.__proxy_get3_url, "?" + get3_url_arg)

        # 获取Json
        proxy_list_json = self.__GetWebContent(get3_url)

        proxy_info_list = list()
        protocol = self.GetGet3Protocol()

        for dec_proxy_info in proxy_list_json["data"]:
            proxy_info = ZmhttpProxyInfo(dec_proxy_info["ip"], dec_proxy_info["port"], protocol)
            proxy_info.city = dec_proxy_info["city"]
            if "isp" in dec_proxy_info:
                proxy_info.isp = dec_proxy_info["isp"]
            proxy_info.outip = dec_proxy_info["outip"]
            proxy_info.expire_time = datetime.strptime(dec_proxy_info["expire_time"], "%Y-%m-%d %H:%M:%S")
            proxy_info_list.append(proxy_info)

        return proxy_info_list
