#conding=utf-8
import re

def DownloadTorrent(soup):
    dl = soup.findAll('dl',{'class':"tattl"}) #匹配到下载跳转容器
    Get_dl = str(dl) #转换为文本文档
    p = re.compile(r'aid='+'\w+') #匹配下载页面的链接后半段
    urlend = p.findall(Get_dl) #在Get_dl中开始匹配
    #print("获取种子链接："+str(urlend))
    return urlend
