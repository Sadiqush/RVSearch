import time
from multiprocessing import Manager
from typing import Callable

class Signals:
    working = True
    _funcs = []

    @staticmethod
    def stop():
        exit(0)
    @staticmethod
    def connect(func:Callable[[str], None]):
        Signals._funcs.append(func)
    @staticmethod
    def _text_changed(text):
        for func in Signals._funcs:
            func(text)
    @staticmethod
    def do_log(text):
        print(text)
        Signals._text_changed(text)
