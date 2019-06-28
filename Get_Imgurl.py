#conding=utf-8
import re

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


    #去重 and 筛选非图片链接 --version 2
    new_Imgurl = []
    End_imgurl = []
    i = 0
    while (i<len(Imgurlend)):
        if (Imgurlend[i]):
            temp = Imgurlend[i]
            Findjpg = '.jpg'
            isFind = temp.find(Findjpg)  #查找获取的图片链接中是否具有图片后缀，如果没有则删除对应元素,返回值小于0则表示未找到
            if (isFind > 0):
                print("chick ok:"+str(temp))
                new_Imgurl.append(temp)
            else:
                del Imgurlend[i] #删除错误的图片链接元素
                print("Remove:"+temp)
            #print("截取后缀为："+str(isFind))


        i+=1

    for id in new_Imgurl:
        if id not in End_imgurl:
            End_imgurl.append(id)
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


    #print("去重筛选后所有图片链接为："+str(End_imgurl))
    Imgurl = End_imgurl

    return Imgurl #返回所有链接数组