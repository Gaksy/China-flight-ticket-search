from datetime import datetime
from FlightInfoGet import FlightException
from FlightInfoGet import Proxy

import urllib.parse
import re
import requests
import json

KEY_CITY_CODE = "cityCode"
KEY_CITY_NAME = "cityName"


class FlightInfo:
    def __init__(self, dep_city_code: str = None,
                 dep_city_name: str = None,
                 arr_city_code: str = None,
                 arr_city_name: str = None,
                 dep_date: datetime = None):
        self.__dep_city_code = dep_city_code
        self.__dep_city_name = dep_city_name
        self.__arr_city_code = arr_city_code
        self.__arr_city_name = arr_city_name
        self.__dep_date = dep_date

    def SetArrivalCity(self, arr_city_code: str, arr_city_name: str):
        self.__arr_city_code = arr_city_code
        self.__arr_city_name = arr_city_name

    def SetDepartureCity(self, dep_city_code: str, dep_city_name: str):
        self.__dep_city_code = dep_city_code
        self.__dep_city_name = dep_city_name

    def SetDepartureDate(self, dep_date: datetime):
        self.__dep_date = dep_date

    def GetArrivalCityCode(self):
        return self.__arr_city_code

    def GetArrivalCityName(self):
        return self.__arr_city_name

    def GetDepartureCityCode(self):
        return self.__dep_city_code

    def GetDepartureCityName(self):
        return self.__dep_city_name

    def GetDepartureDate(self):
        return self.__dep_date


class FlightGetter:
    def __init__(self,
                 proxy: Proxy.ProxyInfo = None,
                 headers=None,
                 cookies=None,
                 cookies_persistence: bool = True,
                 flight_search_url: str = "sjipiao.fliggy.com/searchow/search.htm"):
        # network
        self.__proxy = proxy
        self.__headers = headers
        self.__cookies = cookies
        self.__cookies_persistence = cookies_persistence

        # url
        self.__flight_search_url = flight_search_url
        self.__url_arg_map = {
            "_ksTS": "1704728329550_158",
            "callback": "jsonp159",
            "tripType": "0",
            "depCity": None,  # 出发城市ID
            "depCityName": None,  # 出发城市名称
            "arrCity": None,  # 到达城市ID
            "arrCityName": None,  # 到达城市名称
            "depDate": None,  # 出发日期
            "searchSource": "99",  # 99
            "searchBy": "1277",  # 1277
            "sKey": None,
            "qid": None,
            "needMemberPrice": "false",
            "_input_charset": "utf-8",
            "ua": None,
            "itemId": None,
            "OpenCb": "false"
        }

    def SetFlightInfo(self, flight_info: FlightInfo):
        self.__url_arg_map["depCity"] = flight_info.GetDepartureCityCode()
        self.__url_arg_map["depCityName"] = urllib.parse.quote(flight_info.GetDepartureCityName())

        self.__url_arg_map["arrCity"] = flight_info.GetArrivalCityCode()
        self.__url_arg_map["arrCityName"] = urllib.parse.quote(flight_info.GetArrivalCityName())

        self.__url_arg_map["depDate"] = flight_info.GetDepartureDate().strftime("%Y-%m-%d")

    def SetProxyInfo(self, proxy: Proxy.ProxyInfo):
        self.__proxy = proxy

    def SetHeaders(self, headers):
        self.__headers = headers

    def SetCookies(self, cookies):
        self.__cookies = cookies

    def GetCookies(self):
        return self.__cookies

    def GetHeaders(self):
        return self.__headers

    def BuildFlightSearchUrl(self):
        url_arg_str = urllib.parse.urlencode(self.__url_arg_map)
        flight_search_url = urllib.parse.urljoin(self.__flight_search_url, "?" + url_arg_str)

        if self.__proxy is not None and not self.__proxy.IsHttps():
            flight_search_url = "http://{}".format(flight_search_url)
        else:
            flight_search_url = "https://{}".format(flight_search_url)

        return flight_search_url

    @staticmethod
    def __PreProcessingWebContent(web_content):
        if web_content is None:
            return None

        # 提取JSON部分
        flight_json_txt = web_content.replace("jsonp159(", "").rstrip(")")

        # 修复错误数据
        return re.sub(r'"promotionSceneCfgMap":{(\d+):', r'"promotionSceneCfgMap":{"\1":', flight_json_txt)

    def __GetWebContentWithProxy(self):
        if self.__proxy is None:
            return

        # proxy_protocol = "http"
        # proxy_protocol_url = "http://{}"

        try:
            # 使用https代理
            # if self.__proxy.IsHttps():
                # proxy_protocol = self.__proxy.GetProtocol()
                # proxy_protocol_url = "https://{}".format(self.__proxy.GetIpPort())
            # 使用http代理
            # else:
                # proxy_protocol_url = proxy_protocol_url.format(self.__proxy.GetIpPort())

            # web_response = requests.get(self.BuildFlightSearchUrl(),
                                        # proxies={proxy_protocol: proxy_protocol_url},
                                        # headers=self.__headers,
                                        # cookies=self.__cookies)
            proxy = {"http": "http://{}".format(self.__proxy.GetIpPort()),
                     "https": "http://{}".format(self.__proxy.GetIpPort())}
            
            web_response = requests.get(self.BuildFlightSearchUrl(),
                                        proxies=proxy,
                                        headers=self.__headers,
                                        cookies=self.__cookies,
                                        allow_redirects=True)
        except requests.exceptions.ProxyError:
            raise FlightException.NetworkError("Proxy or Network Error")

        return web_response

    def __GetWebContent(self):
        web_response = None

        # 获取网页内容
        # 不使用代理
        if self.__proxy is None:
            try:
                web_response = requests.get(self.BuildFlightSearchUrl(),
                                            headers=self.__headers,
                                            cookies=self.__cookies)
            except requests.exceptions.RequestException:
                raise FlightException.NetworkError("网络错误")
        # 使用代理
        else:
            web_response = self.__GetWebContentWithProxy()

        # cookies 持久化
        if self.__cookies_persistence:
            self.__cookies = web_response.cookies

        web_content = web_response.content.decode("utf-8")

        web_content = self.__PreProcessingWebContent(web_content)

        return web_content

    def GetFlightJson(self):
        if self.__url_arg_map["arrCity"] is None or self.__url_arg_map["depCity"] is None:
            raise FlightException.MissingArg("缺少到达城市与出发城市参数")

        if self.__url_arg_map["depDate"] is None:
            self.__url_arg_map["depDate"] = datetime.today().strftime("%Y-%m-%d")

        # 获取网页内容
        web_content = self.__GetWebContent()
        # 检查是否为空
        if web_content is None:
            raise FlightException.WebContentNull("网页为空")

        # 解析 Json
        try:
            flight_json = json.loads(web_content)

        # 错误处理
        except json.decoder.JSONDecodeError:
            # 人机验证错误
            if "function(win,key)" in web_content:
                raise FlightException.NeedCaptcha("需要人机验证")
            raise FlightException.WebContentUnintelligible("无法理解网页内容")

        # 查询成功，但结果为空
        if "error" in flight_json:
            return None

        return flight_json
