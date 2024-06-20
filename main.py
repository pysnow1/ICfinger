import argparse
import os
import sys

banner = '''Usage: main.py [options]

Options:
  -t, --target    目标IP地址
  -p, --port      目标Modbus端口号，默认502
  -f, --file      指定url.txt用于批量指纹识别
  -o, --output    输出目录，默认为./output
  -d, --data      指定规则目录，用于存储指纹规则
  -m, --mode      使用数据库存储还是使用json文件存储规则的模式
                  可选值: {db, json}
  -h, --help      显示此帮助信息并退出'''


def parse_args():
    parser = argparse.ArgumentParser(description="工业资产识别工具", formatter_class=argparse.RawTextHelpFormatter,
                                     usage=banner)
    parser.add_argument('-t', '--target', type=str, help='目标IP地址')
    parser.add_argument('-p', '--port', type=int, default=502, help='目标Modbus端口号，默认502')
    parser.add_argument('-f', '--file', type=str, help='指定url.txt用于批量指纹识别')
    parser.add_argument('-o', '--output', type=str, default='./output', help='输出目录，默认为./output')
    parser.add_argument('-d', '--data', type=str, required=True, help='指定规则目录，用于存储指纹规则')
    parser.add_argument('-m', '--mode', type=str, default='json', choices=['db', 'json'], required=True,
                        help='使用数据库存储还是使用json文件存储规则的模式')
    return parser.parse_args()


def ExtractData():
    pass


def main():
    args = parse_args()

    # 检查输出目录是否存在，不存在则创建
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # 单个目标IP地址处理
    if args.target:
        print(f"正在处理目标: {args.target}:{args.port}")
        extractor = ExtractData(ip=args.target, port=args.port)
        extractor.get_dev_info()
        # 这里可以将结果保存到输出目录中
        # 例如：保存到 args.output 目录下的文件中

    # 批量处理目标IP地址
    elif args.file:
        if not os.path.exists(args.file):
            print(f"文件 {args.file} 不存在")
            sys.exit(1)

        with open(args.file, 'r') as f:
            targets = f.readlines()

        for target in targets:
            target = target.strip()
            if target:
                print(f"正在处理目标: {target}:{args.port}")
                extractor = ExtractData(ip=target, port=args.port)
                extractor.get_dev_info()
                # 这里可以将结果保存到输出目录中
                # 例如：保存到 args.output 目录下的文件中

    else:
        print("请指定目标IP地址或批量处理文件")
        sys.exit(1)

    # 处理指纹规则存储模式
    if args.mode == 'db':
        print("使用数据库存储指纹规则")
        # 这里可以添加使用数据库存储指纹规则的逻辑
    elif args.mode == 'json':
        print("使用JSON文件存储指纹规则")
        # 这里可以添加使用JSON文件存储指纹规则的逻辑


if __name__ == '__main__':
    main()
