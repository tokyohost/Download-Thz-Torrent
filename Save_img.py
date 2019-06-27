
import requests
from PIL import Image
from io import BytesIO
import eventlet

def Save_img(url,Img_name,dirpath):

    #保存图片
    with eventlet.Timeout(2, False):
        response = requests.get(url, verify=1)

        img = Image.open(BytesIO(response.content))  # 下载链接图片并保存
        img.save(dirpath + str(Img_name) + '.jpg')