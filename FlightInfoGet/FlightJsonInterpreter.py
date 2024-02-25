class FlightInfo:
    def __init__(self):
        # 航班信息字典
        self.flight_info_map = None

        # 舱位信息字典
        self.cabin_info_map = None

        # 中转航班
        self.transfer_flight = list()

        # 航司名称
        self.airline_name = None
        # 出发机场名称
        self.dep_airport_name = None
        # 到达机场名称
        self.arr_airport_name = None
        # 是否提供给餐食
        self.has_food = False
        # 准点率
        self.on_time_rate = None

        # 是否有中转航班
        self.has_transfer = False

    def PrintFlightInfo(self, transfer=False):
        print(self.airline_name, self.flight_info_map["flightNo"], "执飞飞机", self.flight_info_map["flightType"])
        print(self.flight_info_map["depAirport"], self.dep_airport_name, self.flight_info_map["depTerm"], "To",
              self.flight_info_map["arrAirport"], self.arr_airport_name, self.flight_info_map["arrTerm"]
              )
        print("起飞时间:", self.flight_info_map["depTime"], "预计到达时间:", self.flight_info_map["arrTime"],
              "准点率:", self.on_time_rate
              )

        if transfer:
            print("舱位:", self.cabin_info_map["specialType"])
        else:
            print("舱位:", self.cabin_info_map["specialType"], "票价:", self.cabin_info_map["bestPrice"],
                  "基建燃油:", self.flight_info_map["buildPrice"]
                  )

        print("是否提供餐食:", self.has_food, "是否中途停靠:", self.flight_info_map["stop"] == 1)

        if self.has_transfer:
            for dec_transfer_flight in self.transfer_flight:
                dec_transfer_flight.PrintFlightInfo(True)

        return


class FlightJsonInterpreter:
    def __FlightInterpreter(self, dec_flight):
        flight_info = FlightInfo()
        flight_info.flight_info_map = dec_flight

        flight_info.cabin_info_map = flight_info.flight_info_map["cabin"]
        del flight_info.flight_info_map["cabin"]

        if "onTimeRate" in flight_info.flight_info_map:
            flight_info.on_time_rate = flight_info.flight_info_map["onTimeRate"]

        if "hasFood" in flight_info.flight_info_map:
            flight_info.has_food = flight_info.flight_info_map["hasFood"] == 1

        if "transferFlight" in flight_info.flight_info_map:
            for dec_transfer_flight in flight_info.flight_info_map["transferFlight"]:
                flight_info.transfer_flight.append(self.__FlightInterpreter(dec_transfer_flight))
            del flight_info.flight_info_map["transferFlight"]
            flight_info.has_transfer = True

        flight_info.airline_name = self.airline_info_map[flight_info.flight_info_map["airlineCode"]]
        flight_info.arr_airport_name = self.airport_info_map[flight_info.flight_info_map["arrAirport"]]
        flight_info.dep_airport_name = self.airport_info_map[flight_info.flight_info_map["depAirport"]]

        return flight_info

    def __init__(self, flight_json):
        self.airline_info_map = flight_json["data"]["aircodeNameMap"]
        self.airport_info_map = flight_json["data"]["airportMap"]

        self.arrival_city_code = flight_json["data"]["arrCityCode"]
        self.arrival_city_name = flight_json["data"]["arrCityName"]

        self.departure_city_code = flight_json["data"]["depCityCode"]
        self.departure_city_name = flight_json["data"]["depCityName"]

        # 查询到的航班列表
        self.flight_list = list()

        for dec_flight in flight_json["data"]["flight"]:
            self.flight_list.append(self.__FlightInterpreter(dec_flight))

        return
