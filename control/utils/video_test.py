#!/usr/bin/python3.6
import os
from ctypes import *
import time

d = os.path.dirname(__file__)
cur = cdll.LoadLibrary(d + '/libVideoCV.so')

init_lib = cur.initLib
deinit_lib = cur.deInitLib

start_mux = cur.start_mux
start_mux.restype = c_int
start_mux.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_char_p)]

start_transcode = cur.start_transcode
start_transcode.restype = c_int
start_transcode.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_char_p)]

scan_image = cur.scan_image
scan_image.restype = c_int
scan_image.argtypes = [c_char_p, c_int, POINTER(c_char_p)]

stop = cur.stop
stop.argtypes = [c_char_p]

mfree = cur.mfree
mfree.argtypes = [c_void_p]


def start_transcode_record(id):
    str_dir_path = c_char_p()
    str_err = c_char_p()
    res = start_transcode(id.encode(), byref(str_dir_path), byref(str_err))
    if res is not 0:
        err = str_err.value.decode("ascii")
        print(err)
        mfree(str_err)
        raise Exception(err)

    dir_path = str_dir_path.value.decode("ascii")
    print(dir_path)
    mfree(str_dir_path)
    return dir_path


def start_mux_record(id):
    str_dir_path = c_char_p()
    str_err = c_char_p()
    res = start_mux(id.encode(), byref(str_dir_path), byref(str_err))
    if res is not 0:
        err = str_err.value.decode("ascii")
        print(err)
        mfree(str_err)
        raise Exception(err)

    dir_path = str_dir_path.value.decode("ascii")
    print(dir_path)
    mfree(str_dir_path)
    return dir_path


def scan_video_image(dir_path, second):
    str_err = c_char_p()
    res = scan_image(dir_path.encode(), second, byref(str_err))
    if res is not 0:
        err = str_err.value.decode("ascii")
        print(err)
        mfree(str_err)
        raise Exception(err)

    return


def stop_record(id):
    stop(id.encode())


init_lib()
if __name__ == '__main__':
    init_lib()
    id = "b827ebe96bce"
    for i in range(10):
        print("???????????????" + str(i) + "?????????????????")
        dir_path = start_transcode_record(id)
        time.sleep(10)
        print("stop begin!!!")
        stop_record(id)
        print("stop complete!!!")
    print("!!!!!!!!!!!!!!!!!!!!!!")
    #deinit_lib()
