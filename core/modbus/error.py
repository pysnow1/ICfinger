

class ModbusError(Exception):
    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return "[错误][Modbus协议] %s" % self.message