import re

def Get_nextPage(soup,pidnumber):
    #返回下一页url
    nextpageid = soup.findAll('div', {'class': 'pcb'})  # 匹配到指定容器
    #print(nextpageid)
    Get_nextpageid = str(nextpageid) #转换为文本供正则匹配
    p = re.compile(r'thread-'+'\d+')  # 匹配数字也就是每个页面单独的 Pid
    urlnumber = p.findall(Get_nextpageid) #开始正则匹配
    url ="http://thz5.net/"+urlnumber[0]+"-1-1.html"  #合成下一页url页面地址#获取到的下一页url id存储在下标114中
    #print(urlnumber)
    # print("下一页："+url)
    # print("现在休眠3秒")
    return url
    #以下代码测试获取下一页页面ID的代码
    # print(urlnumber)
    # print(len(urlnumber))
    #
    # i = 0
    # while i <= len(urlnumber):
    #     if ('1999702' == urlnumber[i]):
    #         print(i)
    #     else:
    #         i+=1