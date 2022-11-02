#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/02
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import datetime

from pywebio.input import *
from pydantic import BaseModel, AnyUrl, EmailStr

_model_field_map_input_type = {
    str: TEXT,
    int: NUMBER,
    float: FLOAT,
    AnyUrl: URL,
    datetime.datetime: DATETIME_LOCAL,
    datetime.date: DATE,
    datetime.time: TIME
}

def input_basemodel(model_cls):
    if not issubclass(model_cls, BaseModel):
        raise Exception("model_cls must be class BaseModel or sub class")

    inputs = []
    for k, field in model_cls.__fields__.items():
        inputs.append(
            input(label=field.field_info.title or field.name, name=k,
                  type=_model_field_map_input_type.get(field.type_, TEXT)))

    return input_group(model_cls.__doc__, inputs=inputs)
