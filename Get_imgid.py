#conding=utf-8
import re

def Get_imgid(soup,pidselect): #页面信息，pid资源容器
    #返回资源图片介绍链接
    data = soup.select(pidselect+' > ignore_js_op > img') #在文本中定位图片img标签
    Get_imgid = str(data) # 转换成文本文档
    p = re.compile(r'\d+') #获取id数字
    imgIdNumber = p.findall(Get_imgid)#获取id数字
    return "#aimg_"+imgIdNumber[0]