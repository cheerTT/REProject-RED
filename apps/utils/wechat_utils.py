import requests
import json
import hashlib
import random
from django.http import request
from reporjectred.settings import APPID, SECRET
from api.models import Member


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

    @staticmethod
    def checkMemberLogin(request):
        '''
        判断用户是否登陆
        :return:
        '''
        auth_cookie = request.META.get('HTTP_AUTHORIZATION')
        if auth_cookie is None:
            print('1')
            return False

        auth_info = auth_cookie.split('#')
        if len(auth_info) != 2:
            print('2')
            return False

        try:
            member_info = Member.objects.filter(id=auth_info[1]).first()
        except Exception:
            print('3')
            return False

        if member_info is None:
            print('4')
            return False

        if auth_info[0] != WechatUtils.geneAuthCode(
                id=member_info.id,
                codeVerify=member_info.codeVerify,
                state=member_info.state,
                type=member_info.type):
            print('5')
            return False

        if member_info.state != '0' and member_info.type != '1':
            print('6')
            return False

        return member_info

