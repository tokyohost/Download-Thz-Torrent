#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

def Get_pid(soup):
    #返回当前页面的唯一pid
    pid = soup.findAll('div', {'class': "pls"}) #匹配到指定容器
    Get_pid = str(pid)  # 转换成文本文档
    p = re.compile(r'\d+')  # 匹配数字也就是每个页面单独的 Pid
    pidnumber = p.findall(Get_pid)
   # print(pidnumber)
   #  print("页面唯一pid为："+pidnumber[0])
    #infoMsg = soup.select('#postmessage_' + pidnumber[0])  # 获取的数字数组中第一个才是当前页面唯一的pid
    return pidnumber[0] #返回pid