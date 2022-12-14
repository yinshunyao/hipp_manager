#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import logging
from pydantic import BaseModel
from utility.BaseModel import BaseModel
from pydantic import Field
import flet as ft
from parse.parse_ini import IniControls
from configparser import ConfigParser
import os


def main(page: ft.Page):
    # page.title = f"base mode测试"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT

    columns = ft.Column(expand=True)

    controls = IniControls(expand=8)
    c1 = "config_common.ini"
    c2 = "config_grpc.ini"
    cfg_path_list = [c1, c2]
    config_data = {}
    for cfg_path in cfg_path_list:
        if not os.path.exists(cfg_path) or not os.path.isfile(cfg_path):
            raise Exception(f"file {cfg_path} not exists or isn't file")
        file_name = os.path.basename(cfg_path)
        config_data[file_name] = ConfigParser()
        config_data[file_name].read(cfg_path, encoding="utf8")

    def save_cfg(file_name, cfg: ConfigParser):
        # 测试其中一个配置
        logging.warning(cfg.get("RUN", "target_dir"))

    controls.load(config_data=config_data, save_func=save_cfg)
    # columns.controls.append(controls)

    columns.controls.append(ft.Container(expand=1, content=ft.Tabs(expand=10, tabs=[
        ft.Tab(text="INI配置", content=controls), ft.Tab(text="基础数据配置", content=ft.Text("第二个菜单预留"))
    ])))
    page.controls.append(columns)
    page.update()
    logging.warning("页面启动完成")

if __name__ == '__main__':
    # upload_dir=open_ai_dir,
    ft.app(name="index", port=8090, target=main, view=ft.WEB_BROWSER,  web_renderer="html")
