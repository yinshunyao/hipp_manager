#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/02
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import datetime
import unittest
from InputBaseModel import input_basemodel
from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    """
    用户信息录入
    """
    name: str = Field(title="姓名")
    # 可选属性
    age: Optional[int] = Field(default=0, title="年龄")
    birthday: Optional[datetime.date] = Field(default=None, title="生日")
    agree: bool = Field(title="是否同意")


class TestCfg(unittest.TestCase):

    def test_load_cls(self):
        # 从 input_basemodel 获取结果
        input_result = input_basemodel(User, validate=False)
        print(input_result)

        input_result = input_basemodel(User)
        print(input_result)

    def test_load_obj(self):
        input_result = input_basemodel(User(name="test", agree=True), validate=False)
        print(input_result)