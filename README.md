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

## flight_interpreter.flight_list
返回一个存储FlightInfo类型数据的列表，可以使用FlightInfo::PrintFlightInfo()函数打印机票信息，示例：
```
春秋 9C6658 执飞飞机 320
DLC 周水子机场 -- To PVG 浦东国际机场 T2
起飞时间: 2024-02-26 20:55 预计到达时间: 2024-02-26 23:10 准点率: None
舱位: 经济舱 票价: 620 基建燃油: 120
是否提供餐食: False 是否中途停靠: False
```
使用字典获取数据（FlightInfo::PrintFlightInfo函数中的代码）：
```
        print(self.airline_name, self.flight_info_map["flightNo"], "执飞飞机", self.flight_info_map["flightType"])
        print(self.flight_info_map["depAirport"], self.dep_airport_name, self.flight_info_map["depTerm"],"To",self.flight_info_map["arrAirport"], self.arr_airport_name, self.flight_info_map["arrTerm"])
        print("起飞时间:", self.flight_info_map["depTime"], "预计到达时间:", self.flight_info_map["arrTime"],"准点率:", self.on_time_rate)

        if transfer:
            print("舱位:", self.cabin_info_map["specialType"])
        else:
            print("舱位:", self.cabin_info_map["specialType"], "票价:", self.cabin_info_map["bestPrice"],"基建燃油:", self.flight_info_map["buildPrice"])

        print("是否提供餐食:", self.has_food, "是否中途停靠:", self.flight_info_map["stop"] == 1)
```
