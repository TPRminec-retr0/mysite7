"""misite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    
urls.py : 웹 프로젝트가 실행될때 웹클라이언트가 요청을 한 인터넷주소에 해당하는 뷰클래스/함수를 호출하기 위한
등록 파일

뷰클래스/함수를 등록할때는 urlpatterns 변수의 요소로 추가하면 됨
요소를 추가할때는 path함수를 사용

path(웹클라이언트가 요청할 url주소(문자열), 호출될 뷰클래스/함수이름)
"""
from django.contrib import admin
from django.urls import path
from vote.views import test, test_value, test_input, main, detail, vote, result
#등록할 뷰함수를 import
urlpatterns = [
    path('admin/', admin.site.urls),
    #vote/views.py 에 존재하는 test함수 import 
    path('',test),
    path('value/', test_value),
    #127.0.0.1:8000/숫자/로 요청하는 처리는 test_input함수를 호출 호출할 대 숫자값을 number변수에 인자값으로 사용
    path('<int:number>/', test_input),
    #path함수에 name매개변수 : 등록된 뷰의 별칭을 지정하는 매개변수
    #템플릿 : {% url 별칭의 이름(문자열) %}
    #뷰 함수 : reverse 함수로 별칭 기반의 사이트주소 추출가능
    path('vote/', main, name = "main"),
    #127.0.0.1/vote/숫자/
    path('vote/<int:q_id>/', detail, name = "detail"),
    path('vote/vote/', vote, name = "vote"),
    path('vote/result/<int:c_id>/', result, name = "result"),
]

