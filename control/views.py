import mimetypes
from os import path

from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
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
        file_name = start_transcode_record(mac_address)
        return JsonResponse(data={"file_name": file_name}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"error": e, "status": 400}, status=400)


def intercept_image(request):
    """
    截取保存视频图片
    :param request:
    :return:
    """
    dir_name = request.POST.get('dir_name')
    second = request.POST.get('second')
    if not all([dir_name, second]):
        return JsonResponse(data={"error": "缺少必传参数", "status": 400})
    try:
        second = int(second)
        scan_video_image(dir_name, second)
        image_path = "/fsdata/videos/" + dir_name + "/playback/" + str(second) + ".png"
        return JsonResponse(data={"image_path": image_path}, status=200)
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"error": e, "status": 400}, status=400)


def video_stop(request):
    """
    停止录制视频
    :param request:
    :return:
    """
    mac_address = request.POST.get('mac_address')
    video_file = request.POST.get('video_file')
    if not mac_address:
        return JsonResponse(data={"error": "缺少必传参数", "status": 400})
    try:
        stop_record(mac_address)
        video_path = "/fsdata/videos/" + video_file + "/"
        note_list = os.listdir(video_path + "blackboard")
        note_data = list()
        for i in note_list:
            note_dict = dict()
            note_time, suffix = os.path.splitext(i)
            note_path = video_path + "blackboard/" + i
            note_thumb_path =video_path + "blackboard_thumb/" + i
            note_dict["note_path"] = note_path
            note_dict["note_thumb_path"] = note_thumb_path
            note_dict["note_time"] = int(note_time)
            note_data.append(note_dict)
        return JsonResponse(data={"data": {"note_path": note_data}, "status": 200})
    except Exception as e:
        logger.error(e)
        return JsonResponse(data={"error": e, "status": 400}, status=400)


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
