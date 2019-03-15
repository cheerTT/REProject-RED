import unittest
from django.http import request
from api.views_member import FaceView


def func(x):
    return x+1

def test_answer():
    assert func(3) == 5


