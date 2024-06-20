from util.modbus import Modbus

if __name__ == '__main__':
    modbus = Modbus("127.0.0.1")
    # modbus_data = modbus.send(0x5a, '0002')

    umas_data = modbus.send_umas("03")
    print(umas_data)
