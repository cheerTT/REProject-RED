import os
from django.test import TestCase
from utils.face_utils import base_dir
from api.models import Member
from django.db.models import Q

# base_dir()

# 测试代码所必须的配置文件
# import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reprojectred.settings")# project_name 项目名称
# django.setup()
# member_list = Member.objects.all(Q(state='1'))
# print(member_list)
# print(len(member_list))

# print(os.sep)

