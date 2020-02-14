# from run import Main
# from run import MaxNumber
# from run import logger
# from run import Sleeptime
from Get_nextPage import Get_nextPage
import requests
from bs4 import BeautifulSoup
import lxml

def Get_All_URL(MAXNumber,url):

    print("正在解析所有页面，请稍等！时间可能会比较长，请耐心等待")
    #创建文件保存url
    f = open("ALLURL.txt",'a',encoding='utf-8') #a 为追加模式打开文本

    AllUrl = []
    i = 0
    AllUrl.append(url)
    f.write(url+'\n')
    f.close()
    while MAXNumber > 0:

        # 构造虚拟浏览器参数
        try:
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
            strhtml = requests.get(AllUrl[i], headers=header)  # Get Html Data
        # print(strhtml.text)
        except Exception as e:
            print("链接失败")
            print(e)
            continue
        # 解析网页，获得介绍信息
        print("正在解析"+str(AllUrl[i]))
        # temp_stehtml = str(strhtml.text)
        new_strhtml = strhtml.text
        soup = BeautifulSoup(new_strhtml, 'lxml')  # 使用lxml解析文档
        url = Get_nextPage(soup)
        print("nextPage is {}".format(url))

        f = open("ALLURL.txt", 'a', encoding='utf-8')  # a 为追加模式打开文本
        f.write(url+'\n')#存入文本保存
        f.close()
        AllUrl.append(url)
        MAXNumber -= 1
        i+=1

    print("共提取链接"+str(len(AllUrl)-1)+"个")
    return AllUrl