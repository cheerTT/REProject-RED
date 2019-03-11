import requests
import json
import hashlib
import random
from reporjectred.settings import APPID, SECRET


class WechatUtils():

    @staticmethod
    def getOpenid(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session' \
              '?appid={0}' \
              '&secret={1}' \
              '&js_code={2}' \
              '&grant_type=authorization_code'.format(APPID, SECRET, code)

        r = requests.get(url)

        res = json.loads(r.text)
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid

    @staticmethod
    def geneAuthCode(id, codeVerify, state, type):
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (id, codeVerify, state, type)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genCode():
        code = ''
        for i in range(5):
            # random.randint  既包括上限也包括下限
            add = random.choice([random.randrange(10),
                                 chr(random.randint(65, 90)),
                                 chr(random.randint(97, 122))])
            code += str(add)
        return code

