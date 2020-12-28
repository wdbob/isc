#!/usr/bin/env python
#coding=utf-8
from util import gen_random_str, OssController

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

import json
import cv2
import os
import numpy as np
import urllib
import requests
import copy
import time

"""
with open('config.json', 'r') as f:
    params = json.load(f)
client = AcsClient(params['id'], params['key'], 'cn-shanghai')

base_dir = "imgs"
img_names = ['1.jpg', '2.jpeg', '3.jpg', '4.jpg', '5.png', '6.jpg', '7.png', '8.jpg']

urls = [
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/1.jpg?Expires=1608825947&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=aABGl4utbZIrymQ%2FMA7HTrjA7ow%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/2.jpeg?Expires=1608826669&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=cEu7oV3UCHY37gSvPc79SEDhguc%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/3.jpg?Expires=1608826699&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=JspCKCtAYVW8WNh0rz8Fagd4KQ0%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/4.jpg?Expires=1608826732&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=AuCnYnrBHpEsEsVX9Rdsv%2BOl%2Foc%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/5.png?Expires=1608826811&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=zJf2YJhp9db0GYTwsLE3Cq57TaM%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/6.jpg?Expires=1608826772&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=saMHY%2FkTIncd4ImZLqg%2FNqa82gk%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/7.png?Expires=1608827027&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=WcdA1TJOYtHD5sp7RbXYHsdHfTM%3D",
    "https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/8.jpg?Expires=1608826791&OSSAccessKeyId=TMP.3Ki8L8gHyv2pyXuMJmTaL9S2PRxXbpxLd4Rs8hK49RnSK9AsFh53mK61XPmSaxQ4E7HPrHXfckremPrg7ocDNMwQZgaL6k&Signature=a9AwvDhawBGB7uaG9jXbHLXh3RY%3D"
]

def build_image(idx, output_dir, n_images=5):
    img_fn = os.path.join(base_dir, img_names[idx])
    url = urls[idx]
    print(img_fn)
    img = cv2.imread(img_fn)
    bbs = []

    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('imageenhan.cn-shanghai.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2019-09-30')
    request.set_action_name('IntelligentComposition')

    request.add_query_param('RegionId', "cn-shanghai")
    request.add_query_param('ImageURL', url)
    request.add_query_param('NumBoxes', str(n_images))

    response = client.do_action(request)
    try:
        bbs = str(response, encoding='utf-8')
        bbs = json.loads(bbs)['Data']['Elements']
        for i, ele in enumerate(bbs):
            rb_x = int(ele['MaxX'])
            rb_y = int(ele['MaxY'])
            lt_x = int(ele['MinX'])
            lt_y = int(ele['MinY'])
            score = ele['Score']
            new_img = img[lt_x:rb_x, lt_y:rb_y]
            output_fn = os.path.join(output_dir, str(idx+1), str(score)+'-' +str(i)+'.png')
            cv2.imwrite(output_fn, new_img)
    except:
        print('error at '+str(idx+1))
"""


class ImageBuilder:
    def __init__(self, client, url, img_fn, output_dir, height, width, n_images=5, oss_controller=None):
        
        self.url = url
        self.output_dir = output_dir
        self.n_images = n_images
        self.height = height
        self.width = width
        self.client = client
        self.img_fn = img_fn
        self.output_fn_list = []
        self.oss_controller = oss_controller

    def _get_bbox(self, url=None):
        if url is None:
            url = self.url
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('imageenhan.cn-shanghai.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2019-09-30')
        request.set_action_name('IntelligentComposition')

        request.add_query_param('RegionId', "cn-shanghai")
        request.add_query_param('ImageURL', url)
        request.add_query_param('NumBoxes', str(self.n_images))

        result = []
        response = self.client.do_action(request)
        bbs = str(response, encoding='utf-8')
        bbs = json.loads(bbs)['Data']['Elements']
        for ele in bbs:
            rb_x = int(ele['MaxX'])
            rb_y = int(ele['MaxY'])
            lt_x = int(ele['MinX'])
            lt_y = int(ele['MinY'])
            score = ele['Score']
            result.append((rb_x, rb_y, lt_x, lt_y, score))
        self.bbox_list = list(set(result))
        return result

    def build(self, method='naive_build'):
        if (method=='naive_build'):
            self.naive_build()
        elif (method == 'naive_clip'):
            self.naive_clip()
        elif (method=='build_clip'):
            self.build_clip()


    def naive_build(self):
        """
        只构图，图片尺寸无法控制
        """
        self._get_bbox()
        img = cv2.imread(self.img_fn)
        i = 0
        _dir = os.path.join(self.output_dir, 'tmp')
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        for rb_x, rb_y, lt_x, lt_y, score in self.bbox_list:
            new_img = img[lt_x:rb_x, lt_y:rb_y]
            output_fn = os.path.join(_dir, str(score)+'-' +str(i)+'.png')
            cv2.imwrite(output_fn, new_img)
            self.output_fn_list.append(output_fn)
            i += 1

    def naive_clip(self, url=None, name=None):
        """
        只裁剪，可以控制尺寸大小，但位置选择策略较差
        """
        if url is None:
            url = self.url
        if name is None:
            name = 'tmp.png'
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('imageenhan.cn-shanghai.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2019-09-30')
        request.set_action_name('ChangeImageSize')

        request.add_query_param('RegionId', "cn-shanghai")
        request.add_query_param('Width', self.width)
        request.add_query_param('Height', self.height)
        request.add_query_param('Url', url)

        response = self.client.do_action(request)
        response = str(response, encoding='utf-8')
        url = json.loads(response)['Data']['Url']
        _dir = os.path.join(self.output_dir, 'tmp')
        if not os.path.exists(_dir):
            os.mkdir(_dir)
        output_fn = os.path.join(_dir, name)
        url2img(url, output_fn)
        img = cv2.imread(output_fn)
        cv2.imwrite(output_fn, img)
        self.output_fn_list.append(output_fn)

    def build_clip(self):
        if self.oss_controller is None:
            raise 'oss controller is None!'
        oc = self.oss_controller
        self.naive_build()
        time.sleep(1)
        ol = copy.deepcopy(self.output_fn_list)
        for fn in ol:
            #print(fn)
            basename = os.path.basename(fn)
            oc.upload(fn)
            url = oc.get_url()
            self.naive_clip(url, basename)
            oc.del_curr_obj()
            time.sleep(1)

    def get_output_list(self):
        return self.output_fn_list

def url2img(url, output_fn):
    res = requests.get(url)
    with open(output_fn, 'wb') as f:
        f.write(res.content)
    return


if __name__ == "__main__":
    url2img('https://test-kjkfe.oss-cn-shanghai.aliyuncs.com/1.jpg', 'output/tmp/tmp.png')
    """
    for i in range(len(img_names)):
        build_image(i, 'output', 5)
    """
