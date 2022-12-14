#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/12/11
# @Author  : ysy
# @Email   : yinshunyao@qq.com 
# @Detail  : 
# @Software: PyCharm
import flet as ft
from copy import deepcopy

drop_down_normal_css = dict(
    width=120, height=30, alignment=ft.alignment.center, content_padding=0,
    text_size=15, hint_style=ft.TextStyle(size=15),
)
def get_drop_down_normal(options):
    return ft.Dropdown(options=options, **drop_down_normal_css)

text_label_normal_css = dict(size=15)

def get_text_label(value):
    return ft.Text(value=value, **text_label_normal_css)

def get_text_input(current_value, label="", on_change=None, width=400):
    params = {
        "value": current_value
    }
    if label:
        params["label"] = label

    if on_change is not None:
        params["on_change"] = on_change
    return ft.TextField(**params, multiline=True, width=width)


def get_list_title_for_expand(label="展开", on_click=None, on_change=None, text_css=None, init_expand_status=False, level=1):
    """

    :param label: 扩展图标左边的名称
    :param on_click: 点击事件
    :param text_css:
    :param init_expand_status:
    :return:
    """
    def on_change_button(e: ft.Event):
        if not on_change:
            return

        on_change(e)
        # 交替图标
        if b.icon == ft.icons.DRAG_HANDLE:
            b.icon = ft.icons.EXPAND_MORE
        else:
            b.icon = ft.icons.DRAG_HANDLE

        b.update()

    rows = ft.Row()

    # b_click = ft.TextButton(text=label, on_click=on_click, **text_css)
    if level == 1:
        b_click = ft.ListTile(title=ft.Text(label, size=18), on_click=on_click, **text_css)
    elif level == 2:
        # 空20像素
        rows.controls.append(ft.Container(width=20))
        b_click = ft.ListTile(title=ft.Text(label, size=15), on_click=on_click, **text_css)
    else:
        raise Exception("level不支持3")

    rows.controls.append(b_click)
    if on_change:
        # 图标为搜索状态或者展开状态
        b = ft.IconButton(on_click=lambda e: on_change_button(e),
                          icon=ft.icons.EXPAND_MORE if not init_expand_status else ft.icons.DRAG_HANDLE)
        rows.controls.append(b)


    return rows

