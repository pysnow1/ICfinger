import hashlib
import string


def transformUmas(response, rules):
    plc_model = ""
    # 首先提取response中连续可打印字符超过5个以上的字符串并存储在debug_finger数组里面
    debug_finger = []
    printable_chars = set(string.printable)
    current_str = ""

    for byte in response:
        char = chr(byte)
        if char in printable_chars:
            current_str += char
        else:
            if len(current_str) > 5:
                debug_finger.append(current_str)
            current_str = ""

    if len(current_str) > 5:
        debug_finger.append(current_str)

    # 然后提取response中从PLCSIM到从后往前最后一个0x1之间的字节值，这里就是\x02\x01\x01\x00\x00 \x83\x14\x00\
    try:
        start_index = response.index(b'PLCSIM') + len(b'PLCSIM')
        end_index = response.rindex(b'\x01')
        finger_bin = response[start_index:end_index + 1]
    except ValueError as e:
        print(f"Error extracting finger_bin: {e}")
        return None

    # 将提取到的finger_bin进行md5哈希加密
    md5_hash = hashlib.md5(finger_bin).hexdigest()

    # 在rules这个字典的键名里面搜索，获取到该哈希对应的PLC产品型号，并返回该字符串
    search = rules.get(md5_hash, "未知 PLC 型号")
    plc_model += f"施耐德PLC型号: {search}\n"

    # 将 debug_finger 中的值添加到 plc_model 中
    debug_finger_str = ", ".join(debug_finger)
    plc_model += f"施耐德PLC型号探测返回值: {debug_finger_str}\n"
    plc_model += f"施耐德PLC指纹: {md5_hash}\n"

    return plc_model
