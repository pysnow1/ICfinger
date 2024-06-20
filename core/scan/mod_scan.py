from core.scan.modbus import Modbus
from core.transform.transformModbus import transformModbus
from core.transform.transformUmas import transformUmas


def mod_scan(ip, port, rules):
    fingerprint = ""
    try:
        modbus = Modbus(ip, port)
    except Exception as e:
        fingerprint += "TCP连接异常，可能IP不可达\n"
        return {
            "ip": ip,
            "port": port,
            "fingerprint": fingerprint
        }

    # 第一步，通过modbus.send(0x3, '0000000b', 0)发包判断目标端口是否为modbus服务，如果存在则添加结果到fingerprint
    try:
        response = modbus.send(0x3, b'\x00\x00\x00\x0b', 1)
        if response:
            fingerprint += "Modbus服务: 存在\n"
    except Exception as e:
        fingerprint += "Modbus连接超时\n"
        return {
            "ip": ip,
            "port": port,
            "fingerprint": fingerprint
        }

    # 第二步，成功识别到modbus服务之后,发送modbus.send(0x2b, '0e01', 0)，循环第三个参数从0到10，直到返回的值不会报错，则将结果插入到fingerprint
    for unit_id in range(11):
        try:
            response = modbus.send(0x2b, b'\x0e\x01\x00', unit_id)
            modbus_finger = transformModbus(response)
            if modbus_finger is not None:
                fingerprint += f"Modbus协议指纹： {modbus_finger}\n"
                break
        except Exception as e:
            print(f"Modbus指纹识别错误 unit {unit_id}: {e}\n")
            break

    # 第三步，通过umas_data = modbus.send_umas("02")发送umas查看目标PLC的机器情况，调用umas结果解析函数将结果处理成fingerprint插入到fingerprint变量中
    try:
        umas_data = modbus.send_umas("02")
        response = transformUmas(umas_data, rules)
        if response is not None:
            fingerprint += f"施耐德PLC指纹识别: {response}"
        else:
            fingerprint += f"施耐德PLC指纹识别: Unknow"
    except Exception as e:
        print(f"Error retrieving UMAS data: {e}")

    return {
        "ip": ip,
        "port": port,
        "fingerprint": fingerprint
    }
