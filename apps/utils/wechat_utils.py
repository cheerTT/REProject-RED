"""
微信工具类
"""
# @Author  : cheertt
# @Time    : 2019/3/10 21:13
# @Remark  : 微信工具类
import requests
import json
import hashlib
import random
from django.http import request
from reporjectred.settings import APPID, SECRET
from api.models import Member


class WechatUtils():
    """
    微信工具类
    """

    @staticmethod
    def getOpenid(code):
        """
        获取openid
        :param code:
        :return:
        """
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
        """
        获取授权码
        :param id: 编号
        :param codeVerify: 验证码
        :param state: 状态
        :param type: 用户类型
        :return:
        """
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (id, codeVerify, state, type)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genCode():
        """
        获取生成的随机码，作为用户的验证码
        :return:
        """
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
        """
        判断用户是否登陆
        :param request:
        :return:
        """
        auth_cookie = request.META.get('HTTP_AUTHORIZATION')
        print(auth_cookie)
        if auth_cookie is None:
            return False

        auth_info = auth_cookie.split('#')
        if len(auth_info) != 2:
            return False

        try:
            member_info = Member.objects.filter(id=auth_info[1]).first()
        except Exception:
            return False

        if member_info is None:
            return False

        if auth_info[0] != WechatUtils.geneAuthCode(
                id=member_info.id,
                codeVerify=member_info.codeVerify,
                state=member_info.state,
                type=member_info.type):
            return False

        if member_info.state != '0' and member_info.type != '1':
            return False

        return member_info
