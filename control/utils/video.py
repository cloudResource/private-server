#!/usr/bin/python3.6
import os
from ctypes import *
import time

d = os.path.dirname(__file__)
cur = cdll.LoadLibrary(d + '/libVideoCV.so')

start = cur.start
start.restype = c_int
start.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_char_p)]

stop = cur.stop
stop.argtypes = [c_char_p]

mfree = cur.mfree
mfree.argtypes = [c_void_p]


def start_record(id):
    str_dir_path = c_char_p()
    str_err = c_char_p()
    res = start(id.encode(), byref(str_dir_path), byref(str_err))
    if res is not 0:
        err = str_err.value.decode()
        print(err)
        mfree(str_err)
        raise Exception(err)

    dir_path = str_dir_path.value.decode()
    print(dir_path)
    mfree(str_dir_path)
    return dir_path


def stop_record(id):
    stop(id.encode())

# if __name__ == '__main__':
#     id = "b827ebe96bce"
#     dir_path = start_record(id)
#     print(dir_path)
#     print("sleep begin...")
#     time.sleep(30)
#     print("sleep complete...")
#     stop_record(id)
