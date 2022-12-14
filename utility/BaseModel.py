#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import logging

from pydantic import BaseModel as BM
from typing import Optional, Any


class Schema(BM):
    """ the schema for field """
    title: Optional[str] = ""
    type: Optional[str] = ""
    default: Optional[Any] = None
    description: Optional[str] = ""


class BaseModel(BM):

    def __setattr__(self, key: str, value):
        """
        key支持点间隔，表示层级
        :param key:
        :param value:
        :return:
        """
        keys = key.split(".")
        if not keys:
            raise Exception("key is null")

        if len(keys) == 1:
            return super(BaseModel, self).__setattr__(keys[0], value)

        temp = self
        for k in keys[:-1]:
            temp = self.__getattribute__(k)

        return temp.__setattr__(keys[-1], value)

    def _get_info(keys: list, schema_json: dict):
        # "title": "Test", "type": "object","properties": {
        # "name": {"title": "\u59d3\u540d", "type": "string"}
        # "contact": {"title":"", "allOf": [{"$ref": "#/definitions/Contact"}]}}, "definitions": {"Contact":...}
        key = keys[0]
        properties = schema_json.get("properties")
        if key not in properties:
            raise Exception(f"{key}")

        # 像name一样，已经定义类型
        if "type" in properties[key]:
            if len(keys) > 1:
                logging.warning(f"the {key} not last field, may be error {keys}")

            return Schema(**properties[key])

        if "allOf" in properties[key]:
            properties[key]['allOf']

    def get_info(self, key: str):
        keys = key.split(".")
        if not keys:
            raise Exception("key不能为空")

        if len(keys) == 1:
            return self.schema_json()["definitions"].get(keys[0])



