import socket  # 导入socket模块，用于网络通信
from struct import pack, unpack  # 从struct模块中导入pack和unpack函数

MODBUS_PORT = 502  # 定义MODBUS协议的默认端口号


class ModbusPacket:  # 定义ModbusPacket类，用于封装和解析Modbus数据包
    def __init__(self, func_code, trans_id=0, unit_id=0, data=''):
        self.trans_id = trans_id  # 事务标识符
        self.unit_id = unit_id  # 单元标识符
        self.func_code = func_code  # 功能码
        self.data = data if isinstance(data, bytes) else bytes.fromhex(data)  # 数据部分，确保是字节类型
        self.sock = None  # 套接字对象，初始为None

    def pack(self):  # 封装数据包
        return pack('!HHHBB',
                    self.trans_id,  # 事务标识符
                    0,  # 协议标识符，固定为0
                    len(self.data) + 2,  # 长度字段，数据长度加上两个字节的单元标识符和功能码
                    self.unit_id,  # 单元标识符
                    self.func_code  # 功能码
                    ) + self.data  # 返回封装后的数据包

    def unpack(self, packet):  # 解析数据包
        if not packet:  # 如果数据包为空
            raise ModbusError("Not a reply")  # 抛出ModbusError异常
        elif len(packet) < 8:  # 如果数据包长度小于8字节
            raise ModbusError('Response too short')  # 抛出ModbusError异常

        trans_id, prot_id, length, unit_id, func_code = unpack('!HHHBB', packet[:8])  # 解包前8字节
        if unit_id != self.unit_id:  # 检查单元标识符是否匹配
            raise ModbusError('Unexpected unit ID; with reply: {}'.format(packet))  # 抛出ModbusError异常
        elif func_code != self.func_code:  # 检查功能码是否匹配
            raise ModbusError('Unexpected function code; with reply: {}'.format(packet))  # 抛出ModbusError异常
        elif len(packet) < 6 + length:  # 检查数据包长度是否正确
            raise ModbusError('Response too short')  # 抛出ModbusError异常

        self.data = packet[8:]  # 提取数据部分
        return self  # 返回自身对象


class Modbus:  # 定义Modbus类，用于与Modbus设备通信

    def __init__(self, ip, port=MODBUS_PORT, timed=5):
        self.ip = ip  # 设备IP地址
        self.port = port  # 设备端口号
        self.timed = timed  # 超时时间
        self.sock = None  # 套接字对象，初始为None

    def request(self, func_code, data, unit_id=0):  # 发送请求并接收响应
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建TCP套接字
        self.sock.settimeout(self.timed)  # 设置超时时间
        self.sock.connect((self.ip, self.port))  # 连接到设备

        self.sock.send(ModbusPacket(unit_id=unit_id, func_code=func_code, data=data).pack())  # 发送封装后的数据包
        reply = self.sock.recv(1024)  # 接收响应数据
        return ModbusPacket(func_code, unit_id=unit_id).unpack(reply).data  # 解析响应数据并返回


class ModbusError(Exception):  # 定义ModbusError异常类
    def __init__(self, message=''):
        self.message = message  # 异常信息

    def __str__(self):
        return "[ERROR][ModbusProtocol] %s" % self.message  # 返回异常信息字符串


class ExtractData:  # 定义ExtractData类，用于从设备提取数据
    def __init__(self, ip, port=MODBUS_PORT, timed=5):
        self.mb = Modbus(ip=ip, port=port, timed=timed)  # 创建Modbus对象
        self.device_data = {}  # 存储设备数据的字典

    def get_dev_info(self):  # 获取设备信息
        self.device_data['vendor'] = 'Schneider Electric'  # 设置设备厂商
        self.device_data['device_type'] = 'PLC'  # 设置设备类型

        self.mb.request(0x5a, '0002').hex()  # 发送请求获取设备信息


if __name__ == '__main__':  # 主程序入口
    ExtractData(ip='192.168.xxx.xxx').get_dev_info()  # 创建ExtractData对象并获取设备信息
