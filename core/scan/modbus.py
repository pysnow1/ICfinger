import socket

from core.modbus.error import UmasError
from core.modbus.modbusPacket import ModbusPacket
from core.modbus.umasPacket import UmasPacket

MODBUS_PORT = 502


class Modbus:
    def __init__(self, ip, port=MODBUS_PORT, timed=5):
        self.ip = ip
        self.port = port
        self.timed = timed
        self.sock = None
        self._connect()

    def _connect(self):
        if self.sock is None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.timed)
                self.sock.connect((self.ip, self.port))
            except socket.error as e:
                raise Exception(f"目标 {self.ip}:{self.port} 不存在或无法连接: {e}")

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def send(self, func_code, data, unit_id=0):
        self._connect()
        self.sock.send(ModbusPacket(unit_id=unit_id, func_code=func_code, data=data).pack())
        reply = self.sock.recv(1024)
        return ModbusPacket(func_code, unit_id=unit_id).unpack(reply)

    def send_umas(self, umas_code, payload="", session="00", trans_id=0, unit_id=0):
        self._connect()
        umask_packet = UmasPacket(umas_code, payload=payload, session=session, trans_id=trans_id, unit_id=unit_id)
        self.sock.send(umask_packet.pack())
        reply = self.sock.recv(1024)

        res = umask_packet.unpack(reply)
        if res[0] == 254:
            return res[1]
        elif res[0] == 253:
            print("[+] UmasPacket 返回结果 false：" + str(res[1]))
            return False
        else:
            raise UmasError(f"[Umas协议]返回状态码错误: {res[0]}")
