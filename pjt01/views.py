import json
from django.http import HttpResponse
from django.shortcuts import render
from myanalysis.p108 import P108
from myanalysis.part04 import P109

from myanalysis.wsanalysis import wsAnalysis

# Create your views here.
def home(request):
    return render(request, 'home.html')

def c1(request):
    return render(request, 'c1.html')

def c1data(request):
    result = P108().p108()
    return HttpResponse(json.dumps(result), content_type='application/json')

def img(request):
    P109().mat01()        # 데이터 분석 후 이미지를 저장한 뒤, 이동한 img.html에서 이미지를 불러온다
    return render(request, 'img.html')

def map(request):
    P109().mat07()
    return render(request, 'seoul_map.html')

def chart1(request):
    return render(request, 'chart1.html')

def chart2(request):
    return render(request, 'chart2.html')

def chart3(request):
    return render(request, 'chart3.html')

def chart4(request):
    return render(request, 'chart4.html')


def chart1s(request):
    frm = request.GET['from']
    # print(frm)
    # 분석결과 받기
    result = wsAnalysis().P130(frm)
    # print('받은 데이터:', result)
    return HttpResponse(json.dumps(result), content_type='application/json')

def chart2s(request):
    start = request.GET['start']
    end = request.GET['end']
    con = request.GET['con']
    # print(start, end)
    # 분석결과 받기
    result = wsAnalysis().P136(start, end, con)
    # print(result)
    return HttpResponse(json.dumps(result), content_type='application/json')

def chart3s(request):
    return render(request, 'chart3.html')

def chart4s(request):
    year = int(request.GET['year'])           # 분석할 때 숫자가 필요해서 바꿔줌
    # print(year)
    # 분석결과 해서 choropleth 저장
    wsAnalysis().P168(year)
    # print('까꿍')
    return render(request, 'map.html')

def test(request):
    return render(request, 'test.html')

## iot logging-------------------------------------------------------------------------------------------
import logging

def iots(request):
    speed = request.GET['speed']
    rpm = request.GET['rpm']
    temp = request.GET['temp']
    # logging
    u_logger = logging.getLogger('users')
    u_logger.debug(speed + ', ' + rpm + ', ' + temp)     # debug level로 메세지를 기록
    u_logger.error('Error log!!!')                       # error level로 메세지를 기록

    return render(request, 'iotresult.html')
