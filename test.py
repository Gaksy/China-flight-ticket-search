# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import fake_useragent

from FlightInfoGet import FlightGetter
from FlightInfoGet import ZmhttpProxyPool
from datetime import datetime


def main():
    # 航班信息
    flight_info = FlightGetter.FlightInfo()
    flight_info.SetArrivalCity("SHA", "上海")            # 设置到达城市
    flight_info.SetDepartureCity("DLC", "大连")          # 设置出发城市
    flight_info.SetDepartureDate(datetime(2024, 2, 26))  # 设置出发日期

    # Proxy
    # proxy_info = ZmhttpProxyPool.ZmhttpProxyPool("...", "...")
    # dec_proxy = proxy_info.Get3Proxy(1)[0]

    # 请求头
    # ua = fake_useragent.UserAgent()
    # dec_heaaders = {'User-Agent': str(ua.random)}

    # Getter
    flight_getter = FlightGetter.FlightGetter()
    flight_getter.SetFlightInfo(flight_info)        # 设置要查询的信息
    # flight_getter.SetProxyInfo(dec_proxy)         # 设置代理，接受FlightInfoGet.Proxy类型
    # flight_getter.SetHeaders(dec_heaaders)        # 设置请求头

    # print(dec_proxy)
    
    # 查询
    # print(flight_getter.GetHeaders())
    print(flight_getter.BuildFlightSearchUrl())    # 获取组合出来的查询链接
    flight_json = flight_getter.GetFlightJson()    # 查询并获取json，可能会抛出异常，None代表查询成功但结果为空
    print(flight_getter.GetCookies())              # 获取cookies
    print(flight_json)                             # 打印查询到的数据

    flight_interpreter = FlightJsonInterpreter.FlightJsonInterpreter(flight_json)
    flight_interpreter.flight_list[0].PrintFlightInfo()       # 打印第一个机票信息

    


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
