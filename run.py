import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re
import time
import logging,os
import eventlet





def Main(Nowurl,NowNumber,Sleeptime):

    Sleeptime = Sleeptime


    NowNumber = MainRunNumber(NowNumber)

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    strhtml = requests.get(Nowurl,headers = header)


    new_strhtml = strhtml.text
    soup = BeautifulSoup(new_strhtml,'lxml')


    pidnumber = Get_pid(soup)

    data = soup.select('#postmessage_'+pidnumber)
    line_data = str(data).replace('<br/>','\n')



    name = soup = BeautifulSoup(new_strhtml,'lxml')
    name = soup.select('#thread_subject')
    name = str(name).replace('<span id="thread_subject">','').replace('</span>','')




    mkdirPatch = "已爬取资源"+"\\"+name+"\\"
    mkdir(mkdirPatch)


    imgid = Get_imgid(soup,'#postmessage_'+pidnumber)
    get_img = soup.select(imgid)


    f = open(mkdirPatch+name+'.txt','w',encoding='utf-8')
    f.write(str(data).replace('<br/>',''))
    f.close()



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


    Downloadurl = DownloadTorrent(soup)
    r = requests.get(Downloadurl)
    with open(mkdirPatch+name+'.torrent', "wb") as code:
        code.write(r.content)




    url = Get_nextPage(soup,pidnumber)

    time.sleep(3)


    return url

def Save_img(url,Img_name,dirpath):

    with eventlet.Timeout(2, False):
        response = requests.get(url, verify=False)
        print("connect Success ！")
        img = Image.open(BytesIO(response.content))
        img.save(dirpath + str(Img_name) + '.jpg')








def Get_pid(soup):
    pid = soup.findAll('div', {'class': "pls"})
    Get_pid = str(pid)
    p = re.compile(r'\d+')
    pidnumber = p.findall(Get_pid)

    return pidnumber[0]


def Get_imgid(soup,pidselect):

    data = soup.select(pidselect+' > ignore_js_op > img')
    Get_imgid = str(data)
    p = re.compile(r'\d+')
    imgIdNumber = p.findall(Get_imgid)
    return '#aimg_'+imgIdNumber[0]

def mkdir(path):

    import os


    path=path.strip()
    path=path.rstrip("\\")

    isExists=os.path.exists(path)


    if not isExists:

        print (path+' 创建成功')

        os.makedirs(path)
        return True
    else:

        print (path+' 目录已存在')
        return False

def Get_nextPage(soup,pidnumber):

    nextpageid = soup.findAll('div', {'class': 'pcb'})

    Get_nextpageid = str(nextpageid)
    p = re.compile(r'thread-'+'\d+')
    urlnumber = p.findall(Get_nextpageid)
    url ="http://thz5.net/"+urlnumber[0]+"-1-1.html"


    print("现在休眠3秒")
    return url

def DownloadTorrent(soup):
    dl = soup.findAll('dl',{'class':"tattl"})
    Get_dl = str(dl)
    p = re.compile(r'aid='+'\w+')
    urlend = p.findall(Get_dl)
    url = "http://thz5.net/forum.php?mod=attachment&"+urlend[0]

    return url

def Get_Imgurl(soup):
    data = soup.findAll('td',{'class':"t_f"})
    Get_SmallImgurl = str(data)
    p = re.compile(r"http://"+'\w*'+"."+'\w+'+"."+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+"\w+"+"."+"\w+")
    p2 = re.compile(r"http://"+'\w*'+"."+'\w+'+"."+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"/"+'\w+'+"."+'?\w+')
    p3 = re.compile(
        r"http://" + '\w*' + "." + '\w+' + "." + '\w+' + "/" + '\w+' + "/" + '\w+' + "/" + '\w+' + "/" + '\w+'+"/" + '\w+' + "." + '?\w+')
    Imgurlend = p.findall(Get_SmallImgurl)
    Imgurlend2 = p2.findall(Get_SmallImgurl)
    Imgurlend3 = p3.findall(Get_SmallImgurl)
    Imgurlend = Imgurlend +Imgurlend2+Imgurlend3

    new_Imgurl = []


    i = 0
    while (i<len(Imgurlend)):
        if (Imgurlend[i]):
            temp = Imgurlend[i]
            Findjpg = '.jpg'
            isFind = temp.find(Findjpg)
            if (isFind > 0):
                print("后缀正常！:"+str(temp))
                new_Imgurl.append(temp)
            else:
                del Imgurlend[i]
                print("Remove:"+temp)

        i+=1





    print("去重筛选后所有图片链接为："+str(new_Imgurl))
    Imgurl = new_Imgurl

    return Imgurl
def Log_set():
    logger = logging.getLogger()
    fh = logging.FileHandler("run.log",encoding="utf-8")
    sh = logging.StreamHandler()
    fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')  # 格式化对象
    fh.setFormatter(fm)
    sh.setFormatter(fm)
    logger.addHandler(fh)
    logger.addHandler(sh)
    logger.setLevel(logging.DEBUG)

    return logger

def MainRunNumber(NowNumber):


    MainRunNumber = NowNumber
    MainRunNumber += 1

    return MainRunNumber

if __name__ == '__main__':



    print("按Ctrl+Z 退出！")
    url = input("请输入开始爬取的页面：")
    Sleeptime = input("请输入爬取页面等待事件：（单位：秒）")

    NowNumber = MainRunNumber(-1)



    logger = Log_set()



    while True:
        url  = Main(url,NowNumber,Sleeptime)
