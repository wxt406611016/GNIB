#coding:utf8
import os
from PIL import Image,ImageDraw,ImageFile
import imagehash

def compare_image_with_hash(image_file1,image_file2, max_dif=0):
        """
        max_dif: 允许最大hash差值, 越小越精确,最小为0
        推荐使用
        """
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        hash_1 = None
        hash_2 = None
        with open(image_file1, 'rb') as fp:
            hash_1 = imagehash.average_hash(Image.open(fp))
        with open(image_file2, 'rb') as fp:
            hash_2 = imagehash.average_hash(Image.open(fp))
        dif = hash_1 - hash_2
        if dif < 0:
            dif = -dif
        if dif <= max_dif:
            return True
        else:
            return False
# print(compare_image_with_hash('./1.png','./test.png'))