from util.modbus import Modbus

if __name__ == '__main__':
    modbus = Modbus("127.0.0.1")
    print(modbus.request(0x3, '0003').hex())
