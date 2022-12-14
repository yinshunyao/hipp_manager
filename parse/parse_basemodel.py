#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
from pydantic import BaseModel
import flet as ft
from flet_controls.flet_base import get_text_input
import weakref
from copy import deepcopy


class BaseModelControls(ft.UserControl):

    def load(self, model: BaseModel):
        """
        加载用户数据，不能再init中初始化
        :param model:
        :return:
        """
        self.model = model
        self.model_data = self.model.dict()
        self.model_update = deepcopy(model)
        #
        self.model.schema_json()

    def get_on_change(self, key=""):
        """
        生成事件处理函数
        :param key:
        :return:
        """
        #  定义根据事件更新的处理函数
        def update(e):
            self.model_update.__setattr__(key, e.data)

        return update

    def _build_cfg(self,columns, key="", value=None):
        if isinstance(value, int):
            # 注意这个地方的onchange
            columns.controls.append(get_text_input(current_value=value, label=key,
                                                   on_change=self.get_on_change(key)))
        elif isinstance(value, str):
            # 注意这个地方的onchange
            columns.controls.append(get_text_input(current_value=value, label=key,
                                                   on_change=self.get_on_change(key)))
        elif isinstance(value, dict):
            # 递归字典
            for k, v in value.items():
                self._build_cfg(columns, key=f"{key}.{k}" if key else k, value=v)
        # 列表配置
        elif isinstance(value, list):
            pass
        else:
            raise Exception(f"配置模块暂时不支持类型:{type(value)}")

    def build(self):
        columns = ft.Column()
        self._build_cfg(columns, value=self.model_data)
        return columns