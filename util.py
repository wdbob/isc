import oss2

import os
import json
import random
import string
import copy


class OssController:
    def __init__(self, auth, bucket, bucket_name):
        self.auth = auth
        self.bucket = bucket
        self.names = {}
        self.bucket_name = bucket_name
    
    def upload(self, fn):
        exist = os.path.exists(fn)
        if exist:
            print('start...')
            name = gen_random_str(10)
            self.curr_url = self.get_url_from_name(name)
            self.names[name] = 1
            self.curr_name = name

            self.bucket.put_object_from_file(name, fn)
        
            print('uploaded')
        
        #with open(fn, 'rb') as fileobj:
            #self.bucket.put_object(gen_random_str(20), fileobj)

    def del_curr_obj(self, name=None):
        if name is None:
            name = self.curr_name
            
        self.bucket.delete_object(name)
        del self.names[name]

    def get_url_from_name(self, name=None):
        if name is None:
            name = self.curr_name
        return 'https://'+self.bucket_name+'.oss-cn-shanghai-internal.aliyuncs.com/'+name

    def get_url(self):
        return self.get_url_from_name()

    def clear(self):
        names = copy.deepcopy(list(self.names.keys()))
        if (len(names)>0):
            for n in names:
                self.del_curr_obj(name=n)
    
    """ TODO: 有bug
    def __del__(self):
        pass
        if (len(self.names.keys())>0):
            for n in self.names.keys():
                print(n)
                self.del_curr_obj(name=n)
    """

def gen_random_str(n):
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, n))
    return ran_str

if __name__ == "__main__":
    with open('config.json', 'r') as f:
        params = json.load(f)
    #print(params['id'], params['key'])
    auth = oss2.Auth(params['id'], params['key'])
    #service = oss2.Service(auth, 'oss-cn-shanghai.aliyuncs.com')
    #l = service.list_buckets()
    #print(l.buckets)
    bucket_name = 'test-kjkfe'
    bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', bucket_name)
    oc = OssController(auth, bucket, bucket_name=bucket_name)
    oc.upload(os.path.join('./imgs', '1.jpg'))
    oc.del_curr_obj()

