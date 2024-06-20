# ICfinger

基于Umas协议的指纹识别工具，能够识别modbus服务指纹，重点针对施耐德PLC进行指纹识别，基于umas协议的0x2操作码进行识别，通过逆向该协议建立的识别规则

## 介绍

ICfinger是一款工业指纹识别工具，能够识别各种modbus协议机器信息，能通umas识别施耐德PLC机器型号

## 使用

```
usage: main.py [-h] -t TARGET [-r RULE] [-o OUTPUT]

施耐德PLC指纹识别工具

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        目标IP地址
  -r RULE, --rule RULE  加载指定的规则库json文件
  -o OUTPUT, --output OUTPUT
                        指定输出扫描结果文件位置
```



**单目标识别**

![img](D:\pythonProject\ICfinger\images\8bfc0f93016641f0f0314510ad0db228.png)

**多目标识别**

![image.png](D:\pythonProject\ICfinger\images\1718923972641-2ca084bf-17b8-4882-a166-80cab9167078.png)

![image.png](D:\pythonProject\ICfinger\images\1718923977237-398cedc6-241a-4677-b30b-e642732bf8cc.png)

**结果渲染输出**

![image.png](D:\pythonProject\ICfinger\images\1718924007234-e1f1e7f6-ffd1-4c46-8c26-37e1f6cb7567.png)

# 参考链接

[https://www.ics-cert.org.cn/portal/page/121/a9c6ec01a8b747ee9dcee7b9ac41cb38.html](https://www.ics-cert.org.cn/portal/page/121/a9c6ec01a8b747ee9dcee7b9ac41cb38.html)

https://www.secrss.com/articles/30362

https://cloud.tencent.com/developer/article/1639560

https://www.anquanke.com/post/id/231884

[https://github.com/ffffffff0x/1earn/blob/master/1earn/Security/ICS/%E5%AE%9E%E9%AA%8C/Modbus%E4%BB%BF%E7%9C%9F%E7%8E%AF%E5%A2%83%E6%90%AD%E5%BB%BA.md](https://github.com/ffffffff0x/1earn/blob/master/1earn/Security/ICS/实验/Modbus仿真环境搭建.md)

https://github.com/Fupo-series/ICS-Tools/blob/main/ModbusPLC_InfoScan.py
