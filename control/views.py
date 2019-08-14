import mimetypes
import os
from os import path

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.shortcuts import render
import logging

# Create your views here.
from werkzeug.wsgi import FileWrapper

from control.service import *
from control.utils.video import *

logger = logging.getLogger("django.request")


def video_start(request):
    """
    开始录制视频
    :param request:
    :return:
    """
    mac_address = request.POST.get('mac_address')
    if not mac_address:
        return JsonResponse(data={"error": "缺少必传参数", "status": 400})
    try:
        file_name = start_record(mac_address)
        return JsonResponse(data={"file_name": file_name}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"error": "开始录制失败", "status": 400}, status=400)


def video_stop(request):
    """
    停止录制视频
    :param request:
    :return:
    """
    mac_address = request.POST.get('mac_address')
    if not mac_address:
        return JsonResponse(data={"error": "缺少必传参数", "status": 400})
    try:
        stop_record(mac_address)
        return JsonResponse(data={"message": "结束录制成功", "status": 200})
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"error": "结束录制失败", "status": 400}, status=400)


def video_address(request):
    """
    视频播放地址
    :param request:
    :return:
    """
    file_path = request.GET.get('file_path')
    if not file_path:
        return JsonResponse(data={"message": "缺少必传参数", "status": 400})
    try:

        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = range_re.match(range_header)
        size = os.path.getsize(file_path)
        content_type, encoding = mimetypes.guess_type(file_path)
        content_type = content_type or 'application/octet-stream'
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte) if first_byte else 0
            last_byte = int(last_byte) if last_byte else size - 1
            if last_byte >= size:
                last_byte = size - 1
            length = last_byte - first_byte + 1
            resp = StreamingHttpResponse(RangeFileWrapper(open(file_path, 'rb'), offset=first_byte, length=length),
                                         status=206, content_type=content_type)
            resp['Content-Length'] = str(length)
            resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
        else:
            resp = StreamingHttpResponse(FileWrapper(open(file_path, 'rb')), content_type=content_type)
            resp['Content-Length'] = str(size)
            resp['Accept-Ranges'] = 'bytes'
        return resp
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"message": "获取数据失败", "status": 400})


def cover_image(request):
    """
    获取封面图片
    :param request:
    :return:
    """
    image_path = request.GET.get('image_path')
    if not image_path:
        return JsonResponse(data={"message": "缺少必传参数", "status": 400})
    try:
        image_path = path.join(image_path)
        image_data = open(image_path, "rb").read()
        return HttpResponse(image_data, content_type="image/png")
    except Exception as e:
        logger.error(e)
        e = str(e)
        pat = r"No such file or directory:"
        result = re.findall(pat, e)
        if result:
            return JsonResponse(data={"error": "图片不存在", "status": 400})
        return JsonResponse(data={"message": "获取图片失败", "status": 400})
