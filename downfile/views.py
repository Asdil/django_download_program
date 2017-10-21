# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.http import HttpResponse

pwd = os.getcwd() # 当前文件路径

# Create your views here.
from django.http import StreamingHttpResponse
import zipfile
# 目标文件目录
file_path = pwd + '/the_file'
# 输出文件目录
output_path = pwd + '/the_file.zip'


def zip_wrong_file(startdir, output_path):
    z = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            z.write(os.path.join(dirpath, filename))
    z.close()


def big_file_download(request, file_path=file_path, output_path=output_path):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = file_path
    zip_wrong_file(the_file_name, output_path)
    response = StreamingHttpResponse(file_iterator(output_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(output_path)
    return response



