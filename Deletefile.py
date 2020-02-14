#删除AllURL中的记录

def Deletefile():

    f = open("ALLURL.txt","w",encoding="utf-8")
    f.write("")
    f.close()

    print("已删除缓存")

