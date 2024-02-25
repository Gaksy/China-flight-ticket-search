# 中国机票查询

1. 使用 *FlightInfoGet.FlightInfo* 创建查询内容包
在iata_city_3code_cn.xlsx找到需要查询的出发城市，到达城市的IATA城市三字码，如上海是SHA，北京是BJS，大连是DLC
然后创建一个 *FlightGetter.FlightInfo* 类型的数据，在构造函数参数如下
```
class FlightInfo:
    def __init__(self, dep_city_code: str = None,
                 dep_city_name: str = None,
                 arr_city_code: str = None,
                 arr_city_name: str = None,
                 dep_date: datetime = None)
```
当然也可以使用函数的形式将数据写入查询包中
```
    def SetArrivalCity(self, arr_city_code: str, arr_city_name: str):

    def SetDepartureCity(self, dep_city_code: str, dep_city_name: str):

    def SetDepartureDate(self, dep_date: datetime):
```


2. 使用 *FlightInfoGet.FlightGetter* 获取查询结果Json
使用 *FlightGetter::SetFlightInfo* 将查询内容包传入，然后调用 *flight_getter.GetFlightJson()* 函数获取查询结果Json
```
    flight_getter = FlightGetter.FlightGetter()
    flight_getter.SetFlightInfo(flight_info)
    flight_json = flight_getter.GetFlightJson()
```

4. 使用 *FlightJsonInterpreter.FlightJsonInterpreter* 将每个机票信息从 *flight_json* 中分割出来

```
flight_interpreter = FlightJsonInterpreter.FlightJsonInterpreter(flight_json)
flight_ticket_list = flight_interpreter.flight_list
```

6. 其它功能
## 代理：
*FlightInfoGet.Proxy* 中的 *ProxyInfo* 是 *FlightInfoGet.FlightGetter.SetProxyInfo* 可接受的数据类型
可以通过函数设置代理信息
```
proxy_info = FlightInfoGet.Proxy()
proxy_info.SetProxyIP("---.---.---")
proxy_info.SetProxyPort(1234)
proxy_info.SetProtocol("http")
```
## 设置请求头
*FlightInfoGet.FlightGetter.FlightGetter* 中 SetHeaders 可以用于设置请求头
Cookies默认持久化，可以通过将__cookies_persistence更改为False取消cookies持久化

