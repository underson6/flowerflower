# -*- coding: utf-8 -*-

def isEmpty(target):
    u"""引数に与えられた文字列が空ならTrueを返す"""
    empty = False

    if target is None or target == "":
        empty = True

    return empty