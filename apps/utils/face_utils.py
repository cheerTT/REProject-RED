import os
import datetime
import numpy as np
from scipy import misc
from facenet.align.detect_face import detect_face
from facenet.facenet import prewhiten, crop, flip
from reporjectred.settings import MINSIZE, THRESHOLD, FACTOR, BASE_DIR


def image_array_align_data(image_arr, image_path, pnet, rnet, onet, image_size=160, margin=32,
                           gpu_memory_fraction=1.0,detect_multiple_faces=True):
    minsize = MINSIZE  # minimum size of face
    threshold = THRESHOLD  # three steps's threshold
    factor = FACTOR  # scale factor

    img = image_arr
    # 识别图片中的脸，返回人脸框以及人的关键点
    # img 输入图像
    # minsize 图像最小大小
    # pnet rnet onet caffe 模型
    # threshold  阈值 每一步的阈值
    # factor  影响因子
    bounding_boxes, _ = detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
    nrof_faces = bounding_boxes.shape[0]

    nrof_successfully_aligned = 0
    if nrof_faces > 0:
        det = bounding_boxes[:, 0:4]
        det_arr = []
        img_size = np.asarray(img.shape)[0:2]
        if nrof_faces > 1:
            if detect_multiple_faces:
                for i in range(nrof_faces):
                    det_arr.append(np.squeeze(det[i]))
            else:
                bounding_box_size = (det[:, 2] - det[:, 0]) * (det[:, 3] - det[:, 1])
                img_center = img_size / 2
                offsets = np.vstack(
                    [(det[:, 0] + det[:, 2]) / 2 - img_center[1], (det[:, 1] + det[:, 3]) / 2 - img_center[0]])
                offset_dist_squared = np.sum(np.power(offsets, 2.0), 0)
                index = np.argmax(
                    bounding_box_size - offset_dist_squared * 2.0)  # some extra weight on the centering
                det_arr.append(det[index, :])
        else:
            det_arr.append(np.squeeze(det))

        images = np.zeros((len(det_arr), image_size, image_size, 3))
        for i, det in enumerate(det_arr):
            det = np.squeeze(det)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, img_size[1])
            bb[3] = np.minimum(det[3] + margin / 2, img_size[0])
            cropped = img[bb[1]:bb[3], bb[0]:bb[2], :]
            # 进行图片缩放 cv2.resize(img,(w,h))
            scaled = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
            nrof_successfully_aligned += 1

            # 保存检测的头像

            filename_base = BASE_DIR + os.sep + 'media' + os.sep + 'face_160' + os.sep + datetime.datetime.now().strftime('%Y-%m-%d')

            if not os.path.exists(filename_base):
                os.mkdir(filename_base)

            filename = os.path.basename(image_path)
            filename_name, file_extension = os.path.splitext(filename)
            output_filename_n = "{}/{}_{}{}".format(filename_base, filename_name, i, file_extension)
            # 多个人脸时，在picname后加_0 _1 _2 依次累加。
            misc.imsave(output_filename_n, scaled)

            scaled = prewhiten(scaled)
            scaled = crop(scaled, False, 160)
            scaled = flip(scaled, False)

            images[i] = scaled
    if nrof_faces > 0:
        return images
    else:
        # 如果没有检测到人脸  直接返回一个1*3的0矩阵  多少维度都行  只要能和是不是一个图片辨别出来就行
        return np.zeros((1, 3))


def base_dir():
    print('BASE_DIR:')
    print(BASE_DIR)
