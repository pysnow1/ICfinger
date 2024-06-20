from struct import pack, unpack

from core.modbus.error import ModbusError


class ModbusPacket:
    def __init__(self, func_code, trans_id=0, unit_id=0, data=''):
        self.trans_id = trans_id
        self.unit_id = unit_id
        self.func_code = func_code
        self.data = data if isinstance(data, bytes) else bytes.fromhex(data)

    def pack(self):
        return pack('!HHHBB',
                    self.trans_id,  # 事务标识符
                    0,  # 协议标识符
                    len(self.data) + 2,  # 长度
                    self.unit_id,  # 单元标识符
                    self.func_code  # 功能码
                    ) + self.data

    def unpack(self, packet):
        if not packet:
            raise ModbusError("未收到回复")
        elif len(packet) < 8:
            raise ModbusError('响应太短')

        trans_id, prot_id, length, unit_id, func_code = unpack('!HHHBB', packet[:8])
        if unit_id != self.unit_id:
            raise ModbusError('意外的单元ID; 回复: {}'.format(packet))
        elif func_code != self.func_code:
            raise ModbusError('意外的功能码; 回复: {}'.format(packet))
        elif len(packet) < 6 + length:
            raise ModbusError('响应太短')

        self.data = packet[8:]
        return self.data
