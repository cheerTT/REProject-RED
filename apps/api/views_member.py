"""
与小程序交互的会员模块
"""
# @Author  : cheertt && ttwen
# @Time    : 2019/3/8 8:22
# @Remark  : 收银界面以及小程序会员登陆注册与个人信息显示部分信息
import os
import base64
import json
import uuid
import time
import datetime
import tensorflow as tf
from scipy import misc
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from utils.face_utils import image_array_align_data
from utils.matrix_utils import Matrix
from utils.wechat_utils import WechatUtils
from reporjectred.settings import BASE_DIR, MODELPATH, MAX_DISTINCT
from facenet.align.detect_face import create_mtcnn
from facenet.facenet import get_model_filenames
from api.models import Member, Credit
from order.models import Transaction
from commodity.models import Commodity

os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'  # 只显示 warning 和 Error


class FaceView(View):
    """
    收款界面跳转路径
    """
    def get(self, request):
        """
        收款界面跳转路径 get请求
        :param request:
        :return:
        """
        return render(request, 'face/face.html')


class MemberLoginView(View):
    """
    会员登陆视图
    用于小程序界面会员登陆实现
    """
    def post(self, request):
        """
        小程序登陆业务逻辑实现-post方法
        :param request:
        :return:
        """
        ret = {'code': 200, 'msg': '操作成功', 'data': {}}
        code = request.POST['code']
        code_verify = request.POST['codeVerify'] if request.POST['codeVerify'] else ''

        if not code:
            ret['code'] = 500
            ret['msg'] = '无效的code请求'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        openid = WechatUtils.getOpenid(code)

        if openid is None:
            ret['code'] = 500
            ret['msg'] = 'openid出错'
            ret = {'result': 'false', 'msg': 'openid出错'}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        if code_verify == '-1':
            ret['code'] = 500
            ret['msg'] = '无效的code请求'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        nickname = request.POST['nickName'] if request.POST['nickName'] else ''
        gender = request.POST['gender'] if request.POST['gender'] else ''
        city = request.POST['city'] if request.POST['city'] else ''
        province = request.POST['province'] if request.POST['province'] else ''
        avatar_url = request.POST['avatarUrl'] if request.POST['avatarUrl'] else ''

        # 判断是否已经注册过
        bind_info = Member.objects.filter(codeVerify=code_verify, openid=0)

        print('bind_info')
        print(bind_info)

        # 正常注册的情况，通过code bind_info 不为空
        if bind_info:
            Member.objects.filter(id=bind_info[0].id).update(openid=openid,
                                                             nickname=nickname,
                                                             gender=gender,
                                                             city=city,
                                                             province=province,
                                                             avatarUrl=avatar_url,
                                                             state=0,
                                                             type=1,
                                                             joined_date2=datetime.datetime.now(),
                                                             last_login_date=datetime.datetime.now())

        print(bind_info.values_list())

        print(bind_info.first())

        if bind_info.first() is not None:
            now = datetime.datetime.now()  # 现在的时间
            last_login_date = Member.objects.get(id=bind_info[0].id).last_login_date  # 上次登录的时间

            if now.strftime('%Y-%m-%d') != last_login_date.strftime('%Y-%m-%d'):
                # 今天第一次登陆
                print("今天第一次登录")
                ret['first_time_login'] = '恭喜你，今天首次登陆获得2积分'
                print("credit insert:")
                Credit.objects.create(
                    behave=0,
                    creditpoints=2,
                    credittype=0,
                    createtime=datetime.datetime.now(),
                    userid_id=bind_info[0].id
                )

            Member.objects.filter(id=bind_info[0].id).update(
                last_login_date=datetime.datetime.now())  # 每次登陆更新last_login_date

        token = ""
        if bind_info.first():
            token = "%s#%s" % (WechatUtils.geneAuthCode(
                id=bind_info.values_list()[0][0],
                codeVerify=bind_info.values_list()[0][13],
                state=bind_info.values_list()[0][12],
                type=bind_info.values_list()[0][14],
            ), bind_info.values_list()[0][0])

        else:
            token = "%s#%s" % (WechatUtils.geneAuthCode(
                id='-1',
                codeVerify='-1',
                state='0',
                type='0',
            ), -1)
        ret['data'] = {'token': token}

        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberCheckRegView(View):
    """
    是否是会员状态验证
    """
    def post(self, request):
        """
        会员状态验证-post方法
        :param request:
        :return:
        """
        ret = {'code': 200, 'msg': '操作成功', 'data': {}}

        code = request.POST['code']
        code_verify = request.POST['codeVerify'] if request.POST['codeVerify'] else ''

        if not code:
            ret['code'] = 500
            ret['msg'] = '无效的请求code'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        openid = WechatUtils.getOpenid(code)

        if openid is None:
            ret['code'] = 500
            ret['msg'] = 'openid出错'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        if code_verify == '-1':
            ret['code'] = 500
            ret['msg'] = '无效的code请求'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        bind_info = Member.objects.filter(openid=openid)

        if not bind_info:
            ret['code'] = 500
            ret['msg'] = '未绑定'
            return HttpResponse(json.dumps(ret), content_type='application/json')

        now = datetime.datetime.now()  # 现在的时间
        last_login_date = Member.objects.get(id=bind_info[0].id).last_login_date  # 上次登录的时间

        if now.strftime('%Y-%m-%d') != last_login_date.strftime('%Y-%m-%d'):
            # 今天第一次登陆
            print("今天第一次登录")
            ret['first_time_login'] = '恭喜你，今天首次登陆获得2积分'
            print("credit insert:")
            Credit.objects.create(
                behave=0,
                creditpoints=2,
                credittype=0,
                createtime=datetime.datetime.now(),
                userid_id=bind_info[0].id
            )

        Member.objects.filter(id=bind_info[0].id).update(
            last_login_date=datetime.datetime.now())  # 每次登陆更新last_login_date

        token = "%s#%s" % (WechatUtils.geneAuthCode(
            id=bind_info.values_list()[0][0],
            codeVerify=bind_info.values_list()[0][13],
            state=bind_info.values_list()[0][12],
            type=bind_info.values_list()[0][14],
        ), bind_info.values_list()[0][0])
        ret['data'] = {'token': token}
        ret['user_id'] = bind_info.values_list()[0][0]
        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberInfoView(View):
    """
    会员首页信息显示
    """
    def get(self, request):
        """
        获取会员基本信息，并返回小程序端
        :param request:
        :return:
        """
        ret = {}

        auth_cookie = WechatUtils.checkMemberLogin(request)
        print('auth_cookie:',auth_cookie)

        ret['id'] = auth_cookie.id
        ret['openid'] = auth_cookie.openid
        ret['pic_name'] = auth_cookie.pic_name
        ret['nickname'] = auth_cookie.nickname
        ret['gender'] = auth_cookie.gender
        ret['city'] = auth_cookie.city
        ret['province'] = auth_cookie.province
        # ret['last_login_date'] = auth_cookie.last_login_date 不能json化
        ret['avatarUrl'] = auth_cookie.avatarUrl
        ret['codeVerify'] = auth_cookie.codeVerify
        ret['type'] = auth_cookie.type

        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberOrderView(View):
    """
    会员订单视图
    """
    def get(self, request):
        """
        显示会员订单信息
        :param request:
        :return:
        """
        ret = []
        fields = ['id', 'num', 'joined_date', 'commodity_id', 'member_id', 'orderid']
        filters = dict()
        if 'userid' in request.GET and request.GET['userid']:  # 要查询的订单列表的用户id #43
            filters['member_id'] = request.GET['userid']
            transaction = Transaction.objects.filter(**filters).values(*fields)
            # print("transaction:",transaction)
            for order in transaction:
                singleorder = {}
                singleorder['commodity_id'] = order['commodity_id']
                singleorder['id'] = order['id']
                singleorder['orderid'] = order['orderid']
                singleorder['num'] = order['num']
                singleorder['joined_date'] = order['joined_date'].strftime("%m-%d %H:%M:%S")
                singleorder['picurl'] = Commodity.objects.filter(id=order['commodity_id']).first().imUrl
                singleorder['presentprice'] = Commodity.objects.filter(id=order['commodity_id']).first().present_price
                singleorder['title'] = Commodity.objects.filter(id=order['commodity_id']).first().title
                # print("singleorder:",singleorder)
                ret.append(singleorder)
        # print("ret:",ret)
        return HttpResponse(json.dumps(ret), content_type='applications/json')


class MemberView(LoginRequiredMixin, View):
    """
    会员视图
    """
    def get(self, request):
        """
        用于web端对会员基本信息的展示操作
        :param request:
        :return:
        """
        return render(request, 'api/member/member.html')


# 前方高能
# 该段代码占用过多CPU资源，放在全局供其他函数调用
# with tf.Graph().as_default():
#     gpu_memory_fraction = 1.0
#     gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
#     sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
#     with sess.as_default():
#         pnet, rnet, onet = create_mtcnn(sess, None)
#
# with tf.Graph().as_default():
#     sess = tf.Session()
#     # 加载模型
#     meta_file, ckpt_file = get_model_filenames(MODELPATH)
#     saver = tf.train.import_meta_graph(os.path.join(MODELPATH, meta_file))
#     saver.restore(sess, os.path.join(MODELPATH, ckpt_file))
#     # 获得输入输出张量
#     images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
#     embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
#     phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
#
#     # 进行人脸识别，加载
#     print('Creating networks and loading parameters')
#
#
#     class MemberUploadFace(View):
#         """
#         确认收款界面相关功能，包括人脸识别以及生成订单
#         """
#         def post(self, request):
#             """
#             接受base64编码的人脸数据，并把商品数据生成订单
#             :param request:
#             :return:
#             """
#             ret = dict(status="fail")
#
#             # 接受前端传递过来的uuid -- 判别始于哪一个商家
#             img = request.POST['img']
#
#             img1 = img.replace('data:image/png;base64,', '')
#             newdata = base64.b64decode(img1)
#
#             memberid = str(uuid.uuid1()).replace('-', '')
#
#             image_path1 = BASE_DIR + os.sep + "media" + os.sep + "face" + os.sep + datetime.datetime.now().strftime(
#                 '%Y-%m-%d')
#
#             if not os.path.exists(image_path1):
#                 os.mkdir(image_path1)
#
#             image_path = image_path1 + os.sep + memberid + '.png'
#
#             try:
#                 with open(image_path, 'wb') as file:
#                     file.write(newdata)
#             except FileNotFoundError as fnfe:
#                 print(fnfe)
#
#             # opencv读取图片，开始进行人脸识别
#             img = misc.imread(os.path.expanduser(image_path), mode='RGB')
#             # 设置默认插入时 detect_multiple_faces =False只检测图中的一张人脸，True则检测人脸中的多张
#             # 一般入库时只检测一张人脸，查询时检测多张人脸
#             images = image_array_align_data(img, image_path, pnet, rnet, onet, detect_multiple_faces=False)
#
#             # 设置返回结果
#
#             ret = {}
#
#             # 判断如果如图没有检测到人脸则直接返回
#             if len(images.shape) < 4:
#                 ret['info'] = '没有人脸信息,请重新输入，以确保有人脸信息'
#
#                 print(ret)
#                 return HttpResponse(json.dumps(ret), content_type="application/json")
#
#             feed_dict = {images_placeholder: images, phase_train_placeholder: False}
#             # emb_array保存的是经过facenet转换的128维的向量
#             emb_array = sess.run(embeddings, feed_dict=feed_dict)
#
#             face_query = Matrix()
#
#             code_verify = WechatUtils.genCode()
#
#             # 不让生成已经存在的验证码
#             while Member.objects.filter(codeVerify=code_verify):
#                 code_verify = WechatUtils.genCode()
#
#             if code_verify == '-1':
#                 ret['info'] = '验证码非法操作'
#                 return HttpResponse(json.dumps(ret), content_type="application/json")
#
#             # 分别获取距离该图片中人脸最相近的人脸信息
#             # pic_min_scores 是数据库中人脸距离（facenet计算人脸相似度根据人脸距离进行的）
#             # pic_min_names 是当时入库时保存的文件名
#             # pic_min_uid  是对应的用户id
#             # if face_query.get_socres(emb_array) is not None:
#             pic_min_scores, pic_min_names, pic_min_uid = face_query.get_socres(emb_array)
#             for i in range(0, len(pic_min_scores)):
#                 if pic_min_scores[i] < MAX_DISTINCT:
#                     ret['faceid'] = pic_min_uid[i]
#                     ret['distance'] = pic_min_scores[i]
#                     ret['picname'] = pic_min_names[i]
#
#             if ret is None:
#                 # 新建一个用户
#                 is_video = Member.objects.filter(codeVerify=code_verify)
#                 print('isVideo')
#                 print(is_video.exists())
#                 if not is_video.exists():
#                     print('进来了')
#                     for j in range(0, len(emb_array)):
#                         Member.objects.create(faceid=memberid,
#                                               pic_name=memberid + "_" + str(j) + ".png",
#                                               face_json=",".join(str(li) for li in emb_array[j].tolist()),
#                                               joined_date1=datetime.datetime.now(),
#                                               codeVerify=code_verify.lower()
#                                               )
#
#                     ret['type'] = 1  # 表示新用户
#                     ret['codeVerify'] = code_verify
#                     ret['info'] = 'success, add a face new'
#             else:
#                 # 更新操作  已知用户
#
#                 ret['type'] = 0  # 表示老用户
#                 ret['codeVerify'] = Member.objects.filter(faceid=ret['faceid']).first().codeVerify
#                 ret['info'] = 'update'
#
#             # 作为一个多次购物的用户，
#             # 作为一个第一次注册的用户，
#             member_foreign = Member.objects.filter(codeVerify=ret['codeVerify'].lower()).first()
#
#             # 不能用于检验验证码
#
#             print('member_foreign')
#             print(member_foreign)
#
#             if member_foreign is None:
#                 ret['state'] = '当前用户未识别'
#
#                 return HttpResponse(json.dumps(ret), content_type="application/json")
#
#             # 生成一条订单
#             if request.POST['param'] is None or request.POST['param'] == {}:
#                 ret['state'] = '订单错误'
#
#                 return HttpResponse(json.dumps(ret), content_type="application/json")
#
#             orderid = str(int(time.time() * 1000)) + str(uuid.uuid1()).replace('-', '')[0:10]
#
#             param = eval(request.POST['param'])
#             total = 0
#             for key_value in param.items():
#                 comm = Commodity.objects.filter(id=key_value[0])
#                 total += float(comm[0].present_price) * int(key_value[1])
#                 Transaction.objects.create(rating=3,
#                                            num=key_value[1],
#                                            member=member_foreign,
#                                            commodity=comm[0],
#                                            joined_date=datetime.datetime.now(),
#                                            orderid=orderid)
#
#             Credit.objects.create(
#                 behave=4,
#                 creditpoints=int(total),
#                 credittype=0,
#                 createtime=datetime.datetime.now(),
#                 userid=member_foreign
#             )
#
#             print('结果展示')
#             print(ret)
#             return HttpResponse(json.dumps(ret), content_type="application/json")
