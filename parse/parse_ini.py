#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import logging
import flet as ft
from flet_controls.flet_base import get_text_input, get_list_title_for_expand
from configparser import ConfigParser
from typing import List, Dict


class IniControls(ft.UserControl):

    def load(self, config_data: Dict[str, ConfigParser], save_func=None):
        """
        加载用户数据，不能再init中初始化
        :param config_data: ini内容传递，key是名称（独立）， 内容是ConfigParser
        :param save_func: 改变时触发的回调函数，按照文件级保存，传入参数file_name  和  对应的config配置
        :return:
        """
        self.config_data = config_data
        # 保存回调函数
        self.save_func = save_func

    def _save_cfg(self, e, file_name):
        logging.warning(f"{file_name}需要更新")
        if callable(self.save_func):
            self.save_func(file_name, self.config_data[file_name])

        e.control.disabled = True
        e.control.update()

    def get_on_change(self, key: str, cfg, save_button):
        """
        生成事件处理函数
        :param key:
        :return:
        """
        section, option = key.split(".")
        #  定义根据事件更新的处理函数
        def update(e):
            cfg.set(section=section, option=option, value=e.data)
            # 有数据更新，保存按钮生效
            save_button.disabled = False
            save_button.update()

        return update

    def _build_cfg_param(self, columns, section, option, cfg: ConfigParser, save_button, value=None):
        key = f"{section}.{option}"
        value = value or cfg.get(section=section, option=option)
        # 注意这个地方的onchange
        columns.controls.append(get_text_input(current_value=value, label=key,
                                               on_change=self.get_on_change(key, cfg, save_button)))

    def _build_section(self,  columns_tree,  columns_content, file_name,   section,  cfg: ConfigParser):

        def click_on_section(e):
            columns_content.controls.clear()
            save_button = ft.TextButton(text="保存", on_click=lambda e: self._save_cfg(e, file_name), disabled=True)
            # 增加保存按钮
            columns_content.controls.append(ft.Container(content=save_button))
            # 展开
            for option in cfg.options(section=section):
                self._build_cfg_param(columns_content, section, option, cfg, save_button)
            columns_content.update()

        section_control = get_list_title_for_expand(
            label=section,
            on_click=click_on_section,
            init_expand_status=False,
            text_css={"width": 180}, level=2
        )
        section_control.visible = False

        columns_tree.controls.append(section_control)
        return section_control

    def _build_section_button(self, columns_content, section, cfg: ConfigParser):
        def click_on_section(e):
            columns_content.controls.clear()
            # 上方空10个像素
            columns_content.controls.append(ft.Container(height=10))
            # 展开
            for option in cfg.options(section=section):
                self._build_cfg_param(columns_content, section, option, cfg)
            columns_content.update()

        return ft.ListTile(title=ft.Text(section, size=20), on_click=click_on_section)

    def _build_cfg(self, columns_tree,  columns_content, cfg_name,  cfg: ConfigParser):

        cfg_sections = []

        # 展开文件下的section
        def click_on(e):
            columns_content.controls.clear()
            # 上方空10个像素
            columns_content.controls.append(ft.Container(height=10))
            for section in cfg.sections():
                # 添加section标记，可以展开和隐藏的
                columns_content.controls.append(ft.Text(value=section))

            columns_content.update()

        def expand_on(e):
            for s in cfg_sections:
               s.visible = not s.visible

            columns_tree.update()

        cfg_button = get_list_title_for_expand(
            label=cfg_name, on_change=expand_on,
            on_click=click_on,
            init_expand_status=False,
            text_css={"width": 200}, level=1
        )

        columns_tree.controls.append(cfg_button)

        for section in cfg.sections():
            # 添加section标记，可以展开和隐藏的
            section_control = self._build_section(columns_tree, columns_content, cfg_name, section, cfg)
            cfg_sections.append(section_control)

    def build(self):
        rows = ft.Row(vertical_alignment=ft.CrossAxisAlignment.START, expand=True)
        columns_tree = ft.Column(scroll=ft.ScrollMode.AUTO)

        columns_content = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        # 按照文件遍历构造
        for file_name, cfg in self.config_data.items():
            self._build_cfg(columns_tree, columns_content, file_name, cfg)

        columns_tree.scroll = ft.ScrollMode.ALWAYS
        columns_content.scroll = ft.ScrollMode.ALWAYS
        rows.controls.append(ft.Container(content=columns_tree))
        # 间隔
        rows.controls.append(ft.VerticalDivider(width=5, color=ft.colors.BLUE, thickness=3))
        rows.controls.append(ft.Container(content=columns_content))
        return ft.Container(content=rows)