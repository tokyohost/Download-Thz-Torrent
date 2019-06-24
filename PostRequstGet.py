import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
import time
import logging,os
import eventlet





def Main(Nowurl,NowNumber,Sleeptime):
    #设置休眠时间
    Sleeptime = Sleeptime



    #统计抓取页面总数
    NowNumber = MainRunNumber(NowNumber)
    # print("已抓取页面数："+str(NowNumber))

    #构造虚拟浏览器参数
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    strhtml = requests.get(Nowurl,headers = header)  #Get Html Data
    #print(strhtml.text)


    #解析网页，获得介绍信息
    # temp_stehtml = str(strhtml.text)
    new_strhtml = strhtml.text
    soup = BeautifulSoup(new_strhtml,'lxml') #使用lxml解析文档


    #调用Get_pid 获取页面唯一pid
    pidnumber = Get_pid(soup)

    data = soup.select('#postmessage_'+pidnumber) #定位到资源信息界面
    line_data = str(data).replace('<br/>','\n')


    #获取资源名字
    name = soup = BeautifulSoup(new_strhtml,'lxml')
    name = soup.select('#thread_subject') #定位到资源名字
    name = str(name).replace('<span id="thread_subject">','').replace('</span>','')
    # print(name)


    #新建目录单独保存
    mkdirPatch = "已爬取资源"+"\\"+name+"\\"
    mkdir(mkdirPatch) #调用函数新教目录


    #获取图片介绍，并保存为文件
    imgid = Get_imgid(soup,'#postmessage_'+pidnumber) #获取定位的图片容器id
    get_img = soup.select(imgid)


    #打开文件保存资源详细信息
    f = open(mkdirPatch+name+'.txt','w',encoding='utf-8')
    f.write(str(data).replace('<br/>',''))
    f.close() #关闭文件



    #获取图片链接并下载
    Img_number = 1
    ImgUrl = Get_Imgurl(soup)
    i = 0
    while (i < len(ImgUrl)):
        try:
            Save_img(ImgUrl[i],Img_number,mkdirPatch)
        except OSError:
            print("暂时不支持png格式")
        else:
            print("图片保存成功！")

        i+=1
        Img_number+=1


    #下载种子文件
    Downloadurl = DownloadTorrent(soup) #获取种子下载页面
    r = requests.get(Downloadurl)
    # print("正在下载种子文件！")
    with open(mkdirPatch+name+'.torrent', "wb") as code:
        code.write(r.content)




    #获取下一页url,递归调用主函数
    url = Get_nextPage(soup,pidnumber)

    time.sleep(3) #休眠3秒

    # 写入本页面日志
    # logger.info(" 当前处理页面： " + str(Nowurl) +" 下一页："+str(url)+ " 当前页面Pid为： " + str(pidnumber) + " 目前已爬取页面： " + str(NowNumber))  # 输出日志到文件

    return url #返回下一页面url

def Save_img(url,Img_name,dirpath):

    #保存图片
    with eventlet.Timeout(2, False):
        response = requests.get(url, verify=False)
        print("connect Success ！")
        img = Image.open(BytesIO(response.content))  # 下载链接图片并保存
        img.save(dirpath + str(Img_name) + '.jpg')








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


def Get_imgid(soup,pidselect): #页面信息，pid资源容器
    #返回资源图片介绍链接
    data = soup.select(pidselect+' > ignore_js_op > img') #在文本中定位图片img标签
    Get_imgid = str(data) # 转换成文本文档
    p = re.compile(r'\d+') #获取id数字
    imgIdNumber = p.findall(Get_imgid)#获取id数字
    return '#aimg_'+imgIdNumber[0]

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print (path+' 创建成功')
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print (path+' 目录已存在')
        return False

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
    print("现在休眠3秒")
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

def DownloadTorrent(soup):
    dl = soup.findAll('dl',{'class':"tattl"}) #匹配到下载跳转容器
    Get_dl = str(dl) #转换为文本文档
    p = re.compile(r'aid='+'\w+') #匹配下载页面的链接后半段
    urlend = p.findall(Get_dl) #在Get_dl中开始匹配
    url = "http://thz5.net/forum.php?mod=attachment&"+urlend[0]  #拼接种子链接
    # print("种子下载链接："+url)
    return url

def Get_Imgurl(soup):
    data = soup.findAll('td',{'class':"t_f"}) # 在文本中定位图片img标签父容器
    Get_SmallImgurl = str(data)#转换为文本格式
    p = re.compile(r"http://"+'\w*'+"."+'\w+'+"."+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+"\w+"+"."+"\w+") #匹配图片的链接后半段
    p2 = re.compile(r"http://"+'\w*'+"."+'\w+'+"."+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"."+'?\w+')#匹配另外一张图片链接
    p3 = re.compile(
        r"http://" + '\w*' + "." + '\w+' + "." + '\w+' + "/" + '\w+' + "/" + '\w+' + "/" + '\w+' + "/" + '\w+'+"/" + '\w+' + "." + '?\w+')  # 匹配另外一张图片链接
    Imgurlend = p.findall(Get_SmallImgurl)
    Imgurlend2 = p2.findall(Get_SmallImgurl)
    Imgurlend3 = p3.findall(Get_SmallImgurl)
    Imgurlend = Imgurlend +Imgurlend2+Imgurlend3

    new_Imgurl = []


    #去重 and 筛选非图片链接 --version 2
    i = 0
    while (i<len(Imgurlend)):
        if (Imgurlend[i]):
            temp = Imgurlend[i]
            Findjpg = '.jpg'
            isFind = temp.find(Findjpg)  #查找获取的图片链接中是否具有图片后缀，如果没有则删除对应元素,返回值小于0则表示未找到
            if (isFind > 0):
                print("后缀正常！:"+str(temp))
                new_Imgurl.append(temp)
            else:
                del Imgurlend[i] #删除错误的图片链接元素
                print("Remove:"+temp)
            #print("截取后缀为："+str(isFind))
        i+=1
        # time.sleep(1)

    #去重 --旧版本  --version 0
    # i = 0
    # while (i<len(Imgurlend)):
    #     if(Imgurlend[i]):
    #         temp = Imgurlend[i]
    #         FindRepeat = temp
    #         print(FindRepeat)
    #         j = i+1
    #         while (j <len(Imgurlend)):
    #             isFind = Imgurlend[j].find(FindRepeat) #查找重复链接并删除
    #             #print("查找的链接为："+str(FindRepeat))
    #             # isFindjpg =  Imgurlend[j].find(".jpg")
    #             if (isFind > 0):
    #                 Imgurlend.pop(i) #根据链接删除下标
    #
    #             j+=1
    #     i+=1

    #去重-优化后   --version 1
    #
    # new_Imgurl = []
    #
    #
    # for id in Imgurlend:
    #     Findjpg = '.jpg'
    #     isFind = temp.find(Findjpg)  # 查找获取的图片链接中是否具有图片后缀，如果没有则删除对应元素,返回值小于0则表示未找到
    #     if id not in new_Imgurl and isFind>0:
    #         new_Imgurl.append(id)


    print("去重筛选后所有图片链接为："+str(new_Imgurl))
    Imgurl = new_Imgurl

    return Imgurl #返回所有链接数组

def Log_set():
    logger = logging.getLogger()  # logging对象
    fh = logging.FileHandler("run.log",encoding="utf-8")  # 文件对象
    sh = logging.StreamHandler()  # 输出流对象
    fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')  # 格式化对象
    fh.setFormatter(fm)  # 设置格式
    sh.setFormatter(fm)  # 设置格式
    logger.addHandler(fh)  # logger添加文件输出流
    logger.addHandler(sh)  # logger添加标准输出流（std out）
    logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示

    return logger

def MainRunNumber(NowNumber):
    #统计共爬取多少 个页面

    MainRunNumber = NowNumber
    MainRunNumber += 1

    return MainRunNumber

if __name__ == '__main__':



    print("按Ctrl+Z 退出！")
    # url = input("请输入开始爬取的页面：")
    Sleeptime = input("请输入爬取页面等待事件：（单位：秒）")

    NowNumber = MainRunNumber(-1)#初始化统计页面参数
    url = 'http://thz5.net/thread-1999668-1-1.html' #开始爬的第一个页面

    # 初始化Log日志文件输出
    logger = Log_set()

    # 写入本页面日志
    #logger.info(" 当前处理页面： " + str(Nowurl) +" 下一页："+str(url)+ " 当前页面Pid为： " + str(pidnumber) + " 目前已爬取页面： " + str(NowNumber))  # 输出日志到文件

    while True:
        url  = Main(url,NowNumber,Sleeptime)
