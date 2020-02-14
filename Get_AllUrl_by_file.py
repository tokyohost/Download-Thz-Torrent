#从ALLURL.txt 中获取所有链接
import os

def Get_AllUrl_by_file():
    file_obj = open("ALLURL.txt")
    AllURL = list()

    all_lines = file_obj.readlines()
    for line in all_lines:
        AllURL.append(line.replace("\n",""))
    file_obj.close()

    return AllURL




