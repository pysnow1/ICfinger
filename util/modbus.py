import socket

from core.modbus.packet import ModbusPacket

MODBUS_PORT = 502


class Modbus:
    def __init__(self, ip, port=MODBUS_PORT, timed=5):
        self.ip = ip
        self.port = port
        self.timed = timed
        self.sock = None

    def request(self, func_code, data, unit_id=0):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timed)
        self.sock.connect((self.ip, self.port))

        self.sock.send(ModbusPacket(unit_id=unit_id, func_code=func_code, data=data).pack())
        reply = self.sock.recv(1024)
        return ModbusPacket(func_code, unit_id=unit_id).unpack(reply).data
