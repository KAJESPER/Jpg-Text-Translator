#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 20:03:36 2019

@author: xuanwei
"""

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import hashlib
from urllib import parse
from urllib import request
import random
import base64
import json

def dw(boundingBox, linesCount, lineheight, tranContent,draw):
 # 文本box起点x,y,宽，高
 x, y, w, h = boundingBox.split(',')
 x = int(x)
 y = int(y)
 w = int(w)
 h = int(h)
 # 设置字体字号
 word_size = int(lineheight)
 word_css = "SimHei.ttf"
 font = ImageFont.truetype(word_css, word_size)
 # 绘制文字
 W, H = font.getsize(tranContent) # 文字总长和高
 if W > w and int(linesCount) > 1:
     word_len = len(tranContent)
     r = w / W
     limit = int(w / word_size)
     i = limit
     tranContent = list(tranContent)
     while i < word_len:
         tranContent.insert(i, '\n')
         i += limit + 1
     tranContent = ''.join(tranContent)
     X = x + w
     Y = y + h
 # 绘制矩形
     draw.rectangle((x, y, X, Y), 'yellowgreen', 'wheat')
     draw.text((x, y), tranContent, 'DimGrey', font=font)
for index in range(135,136):
    index_str = "%04d" % index
    # 替换成您的应用ID
    appKey = "4055f164a1a78415"
    # 替换您的应用密钥
    appSecret = "Jy57GwobUhK0goGzo82VCoR8JsSjO7xw"
    # 参数部分
    f = open(r'pic/'+index_str+'.jpg', 'rb') # 二进制方式打开图文件
    q = base64.b64encode(f.read()) # 读取文件内容，转换为base64编码
    q = q.decode('UTF-8', 'strict')
    f.close()
    # 源语言
    fromLan = "en"
    # 目标语言
    to = "zh-CHS"
    # 上传类型
    type = "1"
    # 随机数，自己随机生成，建议时间戳
    salt = random.randint(1, 65536)
    # 签名
    sign = appKey + q + str(salt) + appSecret
    m1 = hashlib.md5()
    m1.update(sign.encode("utf8"))
    sign = m1.hexdigest()
    data = {'appKey': appKey, 'q': q, 'from': fromLan, 'to': to, 'type': type, 'salt': str(salt), 'sign': sign}
    data = parse.urlencode(data).encode(encoding='UTF8')
    req = request.Request('http://openapi.youdao.com/ocrtransapi', data)
    response = request.urlopen(req)
    res = response.read()
    print(data)
    print (res)
    res = json.loads(res, encoding='utf-8')
    resRegions = res['resRegions']
    # 输出识别内容
    for i in resRegions:
        print(i)
    im = Image.open('pic/'+index_str+'.jpg')
    textAngle = res['textAngle']
    imNew = im.rotate(float(textAngle))
    draw = ImageDraw.Draw(imNew)
    for resRegion in resRegions:
        boundingBox = resRegion['boundingBox']
        linesCount = resRegion['linesCount']
        lineheight = resRegion['lineheight']
        tranContent = resRegion['tranContent']
        dw(boundingBox, linesCount, lineheight, tranContent,draw)
    imNew = imNew.rotate(-float(textAngle))
    del draw
    imNew.save('pic1/'+index_str+'.jpg')
    imNew.show()
    imNew.close()