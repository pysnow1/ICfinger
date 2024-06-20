import struct

from core.modbus.error import UmasError
from core.modbus.modbusPacket import ModbusPacket


class UmasPacket:
    def __init__(self, umas_code, payload="", session="00", trans_id=0, unit_id=0):
        self.session = session if isinstance(session, bytes) else bytes.fromhex(session)
        self.modbus = ModbusPacket(func_code=0x5a, data=session + umas_code + payload, trans_id=trans_id,
                                   unit_id=unit_id)

    def pack(self):
        return self.modbus.pack()

    def unpack(self, packet):
        umas_data = self.modbus.unpack(packet)

        session = umas_data[:1]
        if session != self.session:
            raise UmasError(f"[Umas协议]回话秘钥不一致 {session}-{self.session}")
        status = umas_data[1]
        response = umas_data[2:]
        return status, response
