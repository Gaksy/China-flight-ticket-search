class ProxyInfo:
    def __init__(self, proxy_ip: str = None, proxy_port: int = 0, protocol: str = "http"):
        self.__proxy_ip = proxy_ip
        self.__proxy_port = proxy_port
        self.__protocol = protocol

    def __str__(self):
        return f"ProxyInfo: {{'proxy_ip':{self.__proxy_ip}, 'proxy_port':{self.__proxy_port}, 'protocol':{self.__protocol}}}"

    def SetProxyIP(self, proxy_ip: str):
        self.__proxy_ip = proxy_ip

    def GetProxyIP(self):
        return self.__proxy_ip

    def SetProxyPort(self, proxy_port: int):
        self.__proxy_port = proxy_port

    def GetProxyPort(self):
        return self.__proxy_port

    def SetProtocol(self, protocol: str):
        self.__protocol = protocol

    def GetProtocol(self):
        return self.__protocol

    def GetIpPort(self):
        return "{}:{}".format(self.__proxy_ip, self.__proxy_port)

    def IsHttps(self):
        return self.__protocol == "https"
