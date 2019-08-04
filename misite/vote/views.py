from django.shortcuts import render

'''
views.py : MTV패턴 중 실질적인 데이터 추출, 연산, HTML 전달의 기능이 구현되는 파일
view의 기능을 구현할 때는 클래스/함수를 정의해 사용 할 수 있음
함수를 정의해 view의 기능을 구현할때는 첫번째 매개변수가 필수적으로 있어야함

request : 웹 클라이언트의 요청정보가 저장된 매개변수이다.
request안에는 <form>을 바탕으로 사용자가 입력한 값이나 로그인정보, 요청방식 등을 변수형태로 저장하고있다.
'''
#테스트용 뷰함수
from django.template.context_processors import request
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
def test(request):
    #render(request, HTML파일경로, 사전형데이터)
    #해당 요청을 보낸 웹클라이언트에게 전송할 HTML 파일을 사전형데이터로 편집 후 전송하는 함수
    #뷰함수는 반드시 HTML파일이나 다른사이트주소, 파일데이터를 return시켜햐한다.
    return render(request,"test.html",{})
def test_value(request):
    dict = {'a':'홍길동', 'b':[1,2,3,4,5]}
    return render(request, "test_value.html", dict)
    #render함수의 인자값으로 사용할 사젼형데이터 생성
    #dict['a']
def test_input(request, number):
    print(number)
    return render(request, "test_input.html", {'a':number})
#메인회면 - 데이터베이스에 저장된 Question객체를 바탕으로 HTML을 전달
#Question 모델클래스 import
from vote.models import Question, Choice

def main(request):
    #데이터베이스에 저장된 모든 Question객체 추출
    '''
    Question.object : 데이터베이스에 저장된 Question 객체들을 접근할 때 사용하는 변수
    객체 접근 시 4가지 함수로 접근 가능
    all() : 데이터베이스에 저장된 모든 객체를 리스트형태로 추출
    get(조건) : 데이터베이스에 저장된 객체 중 조건을 만족하는 객체 1개를 추출
    filter(조건) : 데이터베이스에 저장된 객체중 조건을 만족하는 모든 객체를 리스트형태로 추출
    exclude(조건) : 데이터베이스에 저장된 객체중 조건을 만족하지 않는 객체를 리스트형태로 추출
    '''
    q = Question.objects.all()
    print(q)
    #추출된 Question 객체를 HTML 편집에 사용할 수 있도록 전달
    return render(request, "vote/main.html", {'q':q})
#웹클라이언트가 요청한 Question객체 한개와 연결된 Choice객체추출
#q_id : 웹클라이언트가 요청한 Question객체의 id변수값
def detail(request,q_id):
    #Question 객체를 한개 추출 - id변수값이 q_id와 같은 조건
    q = Question.objects.get(id=q_id)
    #추출한 Question객체와 연동된 Choice객체들을 추출
    #외래키로 연결된 Question객체가 Choice객체들을 대상으로 추출 함수를 사용하려면
    #객체.choice_set.추출함수로 추출
    #외래키로 연결된객체.외래키로연결한모델클래스명_set.all,get
    c = q.choice_set.all()
    print(q)
    print(c)
    #HTML코드로 추출한 객체를 전달
    return render(request,"vote/detail.html",{'q' : q, 'c' : c})


#detail화면에서 웹클라이언트가 선택한 Choice객체 id로 투표진행
def vote(request):
    #조건문 - 요청한 방식이 post를 사용했는지 확인.
    #request.method : 웹클라이언트의 요청방식을 저장한 변수
    #"GET" 또는 "POST" 문자열을 저장하고있음 (대문자)
    if request.method == "POST":
        #post 요청으로 들어온 데이터중 name=select 에 저장된값을 추출
        #POST요청으로 들어온 데이터는 request.POST에 사전형으로 저장됨
        #GET요청으로 들어온 데이터는 request.GET에 사전형으로 저장됨
        #<form>태그에 작송된 사용자입력을 추출할때는 name 속성에 적힌 문자열로 추출할 수 있음
        print(request.POST)
        c_id = request.POST.get('select')
        #choice객체 한개 추출 - select 값을 id변수에 저장한 객체
        c = Choice.objects.get(id=c_id)
        #추출한 Choice객체에 votes변수값을 +1 누적
        #c.votes += 1
        c.votes = c.votes + 1
        #변경된값을 데이터베이스에게 알려줌
        c.save()
        #resutl 뷰함수의 주소를 웹클라이언트에게 전송
        #return HttpResponseRedirect('/vote/result/%s/'% c.id)
        #별칭기반으로 result 뷰함수의 URL을 추출 및 전달
        return HttpResponseRedirect(reverse('result', args=(c.id,)))
        '''
        HttpResponseRedirect(URL 문자열)
        : 웹클라이언트에게 HTML이나 파일을 전달하는 것이 아닌 다른 뷰함수의 URL주소를 넘겨주는 클래스.
               웹클라이언트가 리다이렉트 주소를 받으면 해당 주소로 웹서버에게 재요청을 함
          reverse(별칭문자열, args) : urls.py에서 등록한 별칭으로 URL주소를 반환하는 함수.
               등록한 view함수가 매개변수를 요구하면 args 사용
        '''
        
        
#Choice의 id를 바탕으로 설문결과 출력
def result(request, c_id):
    #c_id 기반의 Choice 객체 한개 찾기
    c = Choice.objects.get(id=c_id)
    #Choice객체와 연동된 Question객체 추출
    #q = Question.object.get(id= c.q.id)
    q = c.q
    q_2 = Question.objects.get(id= c.q.id)
    q = c.q
    print("c.q : ", c.q)
    print("q_2 : ", q_2)
    print("q : ", q)
    #Question객체와 연동된 모든 Choice객체 추출        
    #c_list = c.q.choice_set.al()
    c_list = q.choice_set.all()
    #결과화면 HTML에 Question객체와 Choice객체 리스트를 전달
    return render(request, "vote/result.html", {'q':q, "c_list":c_list})







