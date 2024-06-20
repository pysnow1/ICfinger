import argparse
import ipaddress
import json
import os
import socket
import struct
import sys
import time

from core.scan.mod_scan import mod_scan
from core.pretty.parse_ip import parse_ip_range
from core.pretty.render import render_to_html
from prettytable import PrettyTable

GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'
ORANGE = '\033[91m'

banner = rf'''
_______________________________________________
{GREEN}
  _____ _____  ___                       
 |_   _/ ____|/ __)                      
   | || |    | |_ _ _ __   __ _  ___ _ __ 
   | || |    |  _| | '_ \ / _` |/ _ \ '__|
  _| || |____| | | | | | | (_| |  __/ |   
 |_____\_____|_| |_|_| |_|\__, |\___|_|   
                           __/ |          
                          |___/           
{RESET}
        ICfinger ver1.2 by pysnow

_______________________________________________
'''


def print_result(addr, printable_response):
    table = PrettyTable()
    table.field_names = ["地址", "信息"]
    table.add_row([addr, printable_response["fingerprint"]])
    print(table)


def print_progress_bar():
    sys.stdout.write(f'\r{YELLOW}[SCHEDULE]{RESET} ' + YELLOW + "/" + RESET)
    sys.stdout.flush()
    time.sleep(0.2)
    sys.stdout.write(f'\r{YELLOW}[SCHEDULE]{RESET} ' + YELLOW + "-" + RESET)
    sys.stdout.flush()
    time.sleep(0.2)
    sys.stdout.write(f'\r{YELLOW}[SCHEDULE]{RESET} ' + YELLOW + "\\" + RESET)
    sys.stdout.flush()
    time.sleep(0.2)
    sys.stdout.write(f'\r{YELLOW}[SCHEDULE]{RESET} ' + YELLOW + "|" + RESET)
    sys.stdout.flush()
    time.sleep(0.2)
    print()


def main():
    print(banner)
    parser = argparse.ArgumentParser(description='施耐德PLC指纹识别工具')
    parser.add_argument('-t', '--target', type=str, required=True, help='目标IP地址')
    parser.add_argument('-r', '--rule', type=str, default='./db/rule.json', help='加载指定的规则库json文件')
    parser.add_argument('-o', '--output', default=None, help='指定输出扫描结果文件位置')

    args = parser.parse_args()

    target = args.target
    rule_file = args.rule
    output_file = args.output

    # 加载规则库
    if os.path.exists(rule_file):
        with open(rule_file, 'r') as f:
            rules = json.load(f)
    else:
        print(f"规则库文件 {rule_file} 不存在，使用默认规则。")
        rules = {}

    results = []
    try:
        # 处理目标IP地址
        if '/' in target:
            # 解析网段
            network = ipaddress.IPv4Network(target, strict=False)
            for ip in network:
                print_progress_bar()
                result = mod_scan(str(ip), 502, rules)  # 假设默认端口为502
                print_result(str(ip), result)
                results.append(result)
        elif '-' in target:
            # 解析IP范围
            for ip in parse_ip_range(target):
                print_progress_bar()
                ip = socket.inet_ntoa(struct.pack('!I', ip))
                result = mod_scan(str(ip), 502, rules)
                print_result(str(ip), result)
                results.append(result)
        elif ':' in target:
            # 解析IP和端口
            print_progress_bar()
            ip, port = target.split(':')
            result = mod_scan(ip, int(port), rules)
            print_result(target, result)
            results.append(result)
        else:
            # 默认端口502
            print_progress_bar()
            result = mod_scan(target, 502, rules)
            print_result(target, result)
            results.append(result)
    except KeyboardInterrupt:
        print("\n扫描中止，正在渲染结果...")

    if output_file is not None:
        # 渲染结果为HTML
        html_content = render_to_html(results)
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        file_url = 'file://' + os.path.abspath(output_file)
        print("结果渲染:  " + file_url)


if __name__ == '__main__':
    main()
