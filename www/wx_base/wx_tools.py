# -*- coding: utf-8 -*-

def jsapi_sign_wrapper(func):
    def wrapper():
        func()
    return wrapper