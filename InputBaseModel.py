#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/02
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import datetime

from pywebio import input
from pydantic import BaseModel, AnyUrl, EmailStr

_model_field_map_input_type = {
    str: input.TEXT,
    int: input.NUMBER,
    float: input.FLOAT,
    AnyUrl: input.URL,
    datetime.datetime: input.DATETIME_LOCAL,
    datetime.date: input.DATE,
    datetime.time: input.TIME,
}

_bool_options = [
    {"label": "是", "value": True, "selected": False, "disabled": False},
    {"label": "否", "value": False, "selected": False, "disabled": False},
]

def input_basemodel(model_cls, validate=True, cancelable=True):
    value_show=False
    if isinstance(model_cls, BaseModel):
        value_show = True
    elif issubclass(model_cls, BaseModel):
        pass
    else:
        raise Exception("model_cls must be class BaseModel or sub class")


    inputs = []
    for k, field in model_cls.__fields__.items():
        label = field.field_info.title or field.name
        help_text = field.field_info.description or None
        value = None if not value_show else model_cls.__getattribute__(k)
        validate_func = None if not validate else field.validate
        # bool type use radio
        if field.type_ is bool:
            inputs.append(input.radio(label=label, name=k, options=_bool_options,
                                      validate=validate_func, value=value, help_text=help_text,
                                      required=field.required
                                      ))
            continue

        inputs.append(
            input.input(label=label, name=k,
                  type=_model_field_map_input_type.get(field.type_, input.TEXT),
                        validate=validate_func, value=value, help_text=help_text,
                        required=field.required
                        ))

    return input.input_group(model_cls.__doc__, inputs=inputs, cancelable=cancelable)
