from util import OssController
from image_builder import ImageBuilder

import oss2
from aliyunsdkcore.client import AcsClient

import json
import os

def run():
    with open('config.json', 'r') as f:
        params = json.load(f)
    auth = oss2.Auth(params['id'], params['key'])
    bucket_name = 'image-size-change'
    bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', bucket_name)
    oc = OssController(auth, bucket, bucket_name=bucket_name)
    img_fn = os.path.join('./imgs', '1.jpg')
    oc.upload(img_fn)
    url = oc.get_url()
    # 构图
    client = AcsClient(params['id'], params['key'], 'cn-shanghai')
    ib = ImageBuilder(client, url, img_fn=img_fn, output_dir='output', height=100, width=100, n_images=5, oss_controller=oc)
    ib.build(method='build_clip')
    oc.clear()
    print('finished')


if __name__ == "__main__":
    run()