import os
import base64
import json
import uuid
import datetime
import tensorflow as tf

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from utils.mixin_utils import LoginRequiredMixin
from utils.face_utils import image_array_align_data
from utils.matrix_utils import Matrix
from utils.wechat_utils import WechatUtils
from reporjectred.settings import BASE_DIR, MODELPATH, MAX_DISTINCT, APPID, SECRET
from facenet.align.detect_face import create_mtcnn
from facenet.facenet import get_model_filenames
from scipy import misc
from api.models import Member



class FaceView(View):

    def get(self, request):
        return render(request, 'face/face.html')




class MemberCheckRegView(View):

    def post(self, request):

        ret = [{'code':200, 'msg':'操作成功', 'data':{}}]
        code = request.POST['code']

        if not code or len(code) < 1:
            ret = {'result': 'false', 'msg': '无效的请求code'}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        openid = WechatUtils.getOpenid(code)

        if openid is None:
            ret = {'result': 'false', 'msg': 'openid出错'}
            return HttpResponse(json.dumps(ret), content_type='application/json')

        bind_info = Member.objects.filter(openid=openid)
        if not bind_info:
            ret.append({'result': 'false', 'msg': '未绑定'})
            return HttpResponse(json.dumps(ret), content_type='application/json')

        token = "%s#%s" % (WechatUtils.geneAuthCode(bind_info.values_list()[0][0], bind_info.values_list()[0][12]), bind_info.values_list()[0][0])
        ret.append({'token': token})
        return HttpResponse(json.dumps(ret), content_type='application/json')


class MemberView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'api/member/member.html')


# 前方高能
# 该段代码占用过多CPU资源，放在全局供其他函数调用
with tf.Graph().as_default():
    gpu_memory_fraction = 1.0
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
    sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
    with sess.as_default():
        pnet, rnet, onet = create_mtcnn(sess, None)

with tf.Graph().as_default():
    sess = tf.Session()
    # 加载模型
    meta_file, ckpt_file = get_model_filenames(MODELPATH)
    saver = tf.train.import_meta_graph(os.path.join(MODELPATH, meta_file))
    saver.restore(sess, os.path.join(MODELPATH, ckpt_file))
    # 获得输入输出张量
    images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
    embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
    phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")

    # 进行人脸识别，加载
    print('Creating networks and loading parameters')


    class MemberUploadFace(View):

        def post(self, request):
            ret = dict(status="fail")
            # 接受前端传递过来的uuid -- 判别始于哪一个商家
            img = request.POST['img']

            img1 = img.replace('data:image/png;base64,', '')
            newdata = base64.b64decode(img1)

            memberid = str(uuid.uuid1()).replace('-', '')

            image_path1 = BASE_DIR + os.sep + "media" + os.sep +"face" + os.sep + datetime.datetime.now().strftime('%Y-%m-%d')

            if not os.path.exists(image_path1):
                os.mkdir(image_path1)

            image_path = image_path1 + os.sep + memberid + '.png'

            try:
                with open(image_path, 'wb') as f:
                    f.write(newdata)
            except FileNotFoundError as fnfe:
                pass

            # opencv读取图片，开始进行人脸识别
            img = misc.imread(os.path.expanduser(image_path), mode='RGB')
            # 设置默认插入时 detect_multiple_faces =False只检测图中的一张人脸，True则检测人脸中的多张
            # 一般入库时只检测一张人脸，查询时检测多张人脸
            images = image_array_align_data(img, image_path, pnet, rnet, onet, detect_multiple_faces=False)

            # 设置返回结果
            ret = []

            # 判断如果如图没有检测到人脸则直接返回
            if len(images.shape) < 4:
                ret.append({"info": '没有人脸信息'})
                print(ret)
                return HttpResponse(json.dumps(ret), content_type="application/json")

            feed_dict = {images_placeholder: images, phase_train_placeholder: False}
            # emb_array保存的是经过facenet转换的128维的向量
            emb_array = sess.run(embeddings, feed_dict=feed_dict)

            face_query = Matrix()

            # 分别获取距离该图片中人脸最相近的人脸信息
            # pic_min_scores 是数据库中人脸距离（facenet计算人脸相似度根据人脸距离进行的）
            # pic_min_names 是当时入库时保存的文件名
            # pic_min_uid  是对应的用户id
            pic_min_scores, pic_min_names, pic_min_uid = face_query.get_socres(emb_array)

            for i in range(0, len(pic_min_scores)):
                if pic_min_scores[i] < MAX_DISTINCT:
                    rdict = {'uid': pic_min_uid[i],
                             'distance': pic_min_scores[i],
                             'pic_name': pic_min_names[i]}
                    # 根据uid查询对应的用户信息
                    ret.append(rdict)
            if len(ret) == 0:
                # 新建一个用户
                for j in range(0, len(emb_array)):
                    Member.objects.create(faceid=memberid,
                                          pic_name=memberid + "_" + str(j) + ".png",
                                          face_json=",".join(str(li) for li in emb_array[j].tolist()),
                                          joined_date1=datetime.datetime.now(),
                                          )
                ret.append({"state": "success, add a face"})
            else:
                # 更新操作  已知用户
                ret.append({"state": "update"})

            # filename_base, file_extension = os.path.splitext(image_path)
            # id_list = []
            # 存入数据库
            # 怎么判断是不是同一个人
            # face_info =
            #
            # db.session.add(member_info)
            # db.session.commit()

            filename_base, file_extension = os.path.splitext(image_path)


            print(ret)
            return HttpResponse(json.dumps(ret), content_type="application/json")




