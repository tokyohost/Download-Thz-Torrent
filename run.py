import requests
from bs4 import BeautifulSoup
import time
from Get_pid import Get_pid
from Log_set import Log_set
from MainRunNumber import MainRunNumber
from DownloadTorrent import DownloadTorrent
from mkdir import mkdir
from Save_img import Save_img
from Get_Imgurl import Get_Imgurl
from Get_nextPage import Get_nextPage
from multiprocessing import Pool
from GetAllurl import Get_All_URL
import config
import Get_AllUrl_by_file
import _thread
import os
from Deletefile import Deletefile

Sleeptime = 0

def Start(urls,url = "null"):

    if(url != "null"):
        config.positionNum = urls.index(url)

    print("目前进度：（"+str(config.positionNum)+"/"+str(len(urls)-1)+")")


    if(int(len(urls)-1) == int(config.positionNum)):
        Deletefile()
        print("已爬取完毕，本次共爬取了："+str(config.positionNum)+"页,保存在本程序目录下“Download”文件夹内！，谢谢您的使用！本项目地址为：https://github.com/tokyohost/Download-Thz-Torrent")

def Main(Nowurl):
    #设置休眠时间
    time.sleep(Sleeptime)



    #统计抓取页面总数
    # NowNumber = MainRunNumber(NowNumber)
    #print("已抓取页面数："+str(NowNumber))

    #构造虚拟浏览器参数
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    strhtml = requests.get(Nowurl,headers = header)  #Get Html Data
    #print(strhtml.text)


    #解析网页，获得介绍信息
    # temp_stehtml = str(strhtml.text)
    new_strhtml = strhtml.text
    soup = BeautifulSoup(new_strhtml,'lxml') #使用lxml解析文档


    #调用Get_pid 获取页面唯一pid
    try:
        pidnumber = Get_pid(soup)
    except Exception:
        print("获取失败，请检查输入链接是否是论坛帖子链接！")
        return -1
    data = soup.select('#postmessage_'+pidnumber) #定位到资源信息界面
    line_data = str(data).replace('<br/>','\n')


    #获取资源名字
    name = soup = BeautifulSoup(new_strhtml,'lxml')
    name = soup.select('#thread_subject') #定位到资源名字
    name = str(name).replace('<span id="thread_subject">','').replace('</span>','').replace('/','').replace('*','').replace('?','').replace('<','').replace('>','').replace(':','')  #去掉Windows文件夹命名不允许的符号 bug：\ 未检查！
    # print(name)


    #新建目录单独保存
    mkdirPatch = "Download"+"\\"+name+"\\"
    isMake = mkdir(mkdirPatch) #调用函数新教目录

    if(isMake == False):
        # 获取下一页url,递归调用主函数
        if(config.isOpenThread != True):
            url = Get_nextPage(soup)
        else:
            url = ""


        print('本页已爬取过，直接进入下一页！')
        Start(Get_AllUrl_by_file.Get_AllUrl_by_file(),Nowurl)

        return

    #获取图片介绍，并保存为文件
    # imgid = Get_imgid(soup,"#postmessage_"+pidnumber) #获取定位的图片容器id
    # get_img = soup.select(imgid)


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
            print("图片下载失败！")
        else:
            print("第"+str(Img_number)+"张图片正在下载... [共"+str(len(ImgUrl))+"张]")

        i+=1
        Img_number+=1


    #下载种子文件
    Downloadurl = DownloadTorrent(soup) #获取种子下载页面
    #print(len(Downloadurl))
    if (len(Downloadurl) == 1): #判断 是否存在1080p种子
        DownTorrenturl = config.newDomin + "forum.php?mod=attachment&" + Downloadurl[0]
        r = requests.get(DownTorrenturl)
        with open(mkdirPatch+name+' 720p'+'.torrent', "wb") as code:
            code.write(r.content)

        print("种子下载完成!")
    elif (len(Downloadurl)>1):

        TorrentName = ["720p","1080p","2k","4k"]
        i = 0
        while (i < len(Downloadurl)):
            # 下载720p资源
            DownTorrenturl = config.newDomin + "forum.php?mod=attachment&" + Downloadurl[i]
            r = requests.get(DownTorrenturl)
            # print("正在下载种子文件！")
            with open(mkdirPatch + name + TorrentName[i] + ".torrent", "wb") as code:
                code.write(r.content)
            i+=1

        print(str(len(Downloadurl))+"个种子下载完成!")
    else:
        print("未找到种子文件！")


    if(config.isOpenThread):
        Start(Get_AllUrl_by_file.Get_AllUrl_by_file(),Nowurl)
        return 0
    else:
        #获取下一页url,递归调用主函数
        url = Get_nextPage(soup)

    print("已下载")

    time.sleep(config.sleepTime) #休眠

    print("现在休眠"+str(config.sleepTime)+"秒")
    Start(Get_AllUrl_by_file.Get_AllUrl_by_file(),Nowurl)
    return Main(url) #返回下一页面url



if __name__ == '__main__':


    print("感谢您的使用！如有用，请给个star，本项目地址：https://github.com/tokyohost/Download-Thz-Torrent")
    print("按Ctrl+Z 退出！")
    Staticurl = config.startUrl #初始化链接地址
    if(Staticurl == ""):
        print("请修改配置文件中的startUrl！")

    Deletefile()



    global url
    # url = input("请输入开始爬取的论坛帖子链接：(输入‘Y’即使用默认地址：http://thz5.net/thread-1930952-1-1.html)").strip()
    # if (url == 'Y'):
    #     url = Staticurl
    url = Staticurl
    Sleeptime = config.sleepTime
    print("每篇页面休眠时间"+str(Sleeptime)+"毫秒")

    MaxNumber = config.maxPage
    print("本次爬取最多"+str(MaxNumber)+"篇页面")

    if(config.isOpenThread):
        print("已开启多线程下载，下载前会提前获取所有页面地址")
    else:
        print("未开启多线程下载。")

    MaxNumber = int(MaxNumber)

    config.positionNum = MainRunNumber(-2)#初始化统计页面参数

    # 初始化Log日志文件输出
    logger = Log_set()

    #获取所有url
    AllURL = Get_All_URL(MaxNumber,url)
    pool = Pool() #初始化多线程
    try:
        pool.map(Main,AllURL)
    except Exception as e:
        print(e)

