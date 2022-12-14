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
from parse.parse_basemodel import BaseModelControls

class Addr(BaseModel):
    province: str = ""
    city: str = Field(title="城市")

class Contact(BaseModel):
    email: str = Field(title="email")
    mobile: str = Field(title="电话号码")
    addr: Addr = Field(title="地址")

class Test(BaseModel):
    name: str = Field(title="姓名")
    age: int = Field(title="年龄")
    contact: Contact = Field(title="联系方式", description="详细的联系方式，包含电话地址等")


def main(page: ft.Page):
    # page.title = f"base mode测试"
    test_data = Test(name="yin", age=18, contact={"email": "ysy@163.com", "mobile":"139", "addr": {"province": "四川省", "city": "成都市"}})
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT
    w, h = page.width, page.height
    controls = BaseModelControls()
    controls.load(test_data)
    logging.warning(f"页面的宽度高度：{w}-{h}")
    page.controls.append(controls)
    page.update()

if __name__ == '__main__':
    # upload_dir=open_ai_dir,
    ft.app(name="index", port=8090, target=main, view=ft.WEB_BROWSER,  web_renderer="html")
