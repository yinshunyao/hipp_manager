#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/02
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import datetime
import unittest
from input_basemode import input_basemodel
from pydantic import BaseModel, Field


class User(BaseModel):
    """
    用户信息录入
    """
    name: str = Field(default="", title="姓名")
    age: int = Field(default=0, title="年龄")
    birthday: datetime.date = Field(default=None, title="生日")


class TestCfg(unittest.TestCase):

    def test_load(self):
        input_result = input_basemodel(User)
        print(input_result)