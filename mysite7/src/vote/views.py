from django.shortcuts import render, get_object_or_404

'''
views.py : MTV패턴 중 실질적인 데이터 추출, 연산, HTML 전달의
기능이 구현되는 파일
view의 기능을 구현할 때는 클래스/함수를 정의해 사용할 수 있음.
함수를 정의해 view의 기능을 구현할때는 첫번째매개변수를 필수적으로있어야함

request : 웹 클라이언트의 요청정보가 저장된 매개변수
request안에는 <form>를 바탕으로 사용자가 입력한 값이나
로그인 정보, 요청방식, 등을 변수형태로 저장하고있음
'''
#테스트용 뷰함수
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth.decorators import login_required

def test(request):
    #render(request,HTML파일경로, 사전형데이터)
    #해당 요청을 보낸 웹클라이언트에게 전송할 HTML파일을
    #사전형데이터로 편집한 뒤 전송하는 함수
    #뷰함수는 반드시 HTML파일이나 다른사이트주소, 파일데이터를
    #return 시켜야함
    return render(request,"test.html", {})
#뷰함수가 템플릿이 HTML를 변경할 수 있도록 변수값 전달
def test_value(request):
    #render함수의 인자값으로 사용할 사전형데이터 생성
    dict = { 'a':'홍길동님' ,'b' : [1,2,3,4,5] }
    #dict['a']
    return render(request,"test_value.html", dict)
#뷰함수가 request외에 추가 매개변수를 사용
def test_input(request, number):
    print(number)
    return render(request, "test_input.html",
                   {'a':number})
#Question 모델클래스 import
from vote.models import Question, Choice
#메인화면 - 데이터베이스에 저장된 Question객체를 바탕으로 HTML를전달
def main(request):
    #데이터베이스에 저장된 모든 Question 객체를 추출
    '''
    Question.objects : 데이터베이스에 저장된 Question객체들을
    접근할 때 사용하는 변수.
    객체를 접근할 때는 4가지 함수로 접근할수 있음.
    all() : 데이터베이스에 저장된 모든 객체를 리스트형태로 추출
    get(조건) : 데이터베이스에 저장된 객체 중 조건을 만족하는 
    객체1개를추출
    filter(조건) : 데이터베이스에 저장된 객체중 조건을 만족하는 모든
    객체를 리스트형태로 추출
    exclude(조건) : 데이터베이스에 저장된 객체중 조건을 만족하지않는
    객체를 리스트형태로 추출
    '''
    q = Question.objects.all()
    print(q)
    #추출된 Question 객체를 HTML 편집에 사용할수있도록 전달
    return render(request, "vote/main.html",{'q':q})

#웹클라이언트가 요청한 Question객체 한개와 연결된Choice객체추출
#q_id : 웹클라이언트가 요청한 Question객체의 id변수값
def detail(request, q_id):
    #Question객체를 한개추출 - id변수값이 q_id와 같은 조건
    q = Question.objects.get(id=q_id)
    #추출한 Question객체와 연동된 Choice객체들을 추출
    #외래키로 연결된 Question객체가 Choice객체들을 대상으로
    #추출 함수를 사용하려면 객체.choice_set.추출함수로 추출
    #외래키로 연결된객체.외래키로연결한모델클래스명_set.all, get
    c = q.choice_set.all()
    print(q)
    print(c)
    #HTML코드로 추출한 객체들 전달
    return render(request,"vote/detail.html",
                  {'q' : q, 'c' : c })

#detail화면에서 웹클라이언트가 선택한 Choice객체 id로 투표 진행
#@login_required : 비로그인상태일때 해당뷰함수를 요청하면
#setting.py에 지정된 로그인페이지로 리다이렉트함
@login_required
def vote(request):
    #조건문 - 요청한 방식이 post를 사용했는지 확인.
    #request.method : 웹클라이언트의 요청방식을 저장한 변수
    #"GET" 또는 "POST" 문자열을 저장하고있음 (대문자)
    if request.method == "POST":
        #post요청으로 들어온 데이터 중 name=select 에 저장된값을 추출
        #POST 요청으로 들어온 데이터는 request.POST에 사전형으로 저장됨
        #GET 요청으로 들어온 데이터는 request.GET에 사전형으로 저장됨
        #<form>태그에 작성된 사용자입력을 추출할때는 name속성에 적힌 문자열로
        #추출할수있음
        print(request.POST)
        c_id = request.POST.get('select')
        #Choice객체 한개 추출 - select 값을 id변수에 저장한 객체
        c=Choice.objects.get(id=c_id)
        #추출한 Choice객체에 votes변수값을 +1 누적
        #c.votes += 1
        c.votes = c.votes + 1
        #변경된 값을 데이터베이스에게 알려줌
        c.save()
        #result 뷰함수의 주소를 웹클라이언트에게 전송
        #return HttpResponseRedirect('/vote/result/%s/'% c.id)
        #별칭기반으로 result 뷰함수의 URL을 추출 및 전달
        #url =reverse('result', args=(c.id,) )
        #return HttpResponseRedirect(url) 
        return HttpResponseRedirect(
            reverse('result', args=(c.id,) ))
        '''
        HttpResponseRedirect(URL 문자열)
        : 웹 클라이언트에게 HTML이나 파일을 전달하는 것이 아닌 다른 뷰함수의
        URL 주소를 넘겨주는 클래스. 웹클라이언트가 리다이랙트 주소를 받으면
               해당 주소로 웹서버에게 재 요청을 함.
        reverse(별칭문자열, args) : urls.py에서 등록한 별칭으로 
        URL주소를 반환하는 함수. 등록한 view함수가 매개변수를 요구하면 args
               사용
        
        '''

#Choice의 id를 바탕으로 설문결과 출력
def result(request, c_id):
    #c_id 기반의 Choice객체 한개 찾기
    c = Choice.objects.get(id=c_id)
    #Choice객체와 연동된 Question객체 추출
    q_2 = Question.objects.get(id= c.q.id)
    q = c.q
    print("c.q : ",  c.q)
    print("q_2 : ", q_2)
    print("q : ", q)
    #Question객체와 연동된 모든 Choice객체 추출
    #c_list = c.q.choice_set.all()
    c_list =  q.choice_set.all()
    #결과화면 HTML에 Question객체와 Choice객체리스트를전달
    return render(request, "vote/result.html",
                  {'q': q, "c_list":c_list})

#Question 객체 추가 함수
#GET - 사용자에게 Question객체를 생성할때 사용할 변수값을 입력할
#수 있는 input태그와 form태그(POST방식요청) 제공
#POST - 사용자가 입력한 데이터를 바탕으로 Question객체를 생성
# 및 데이터베이스 저장
from vote.forms import QuestionForm
@login_required
def q_registe(request):
    #사용자 요청이 GET인지 POST인지 구분
    if request.method == "GET":
        #QuestionForm 객체를 생성
        #QuestionForm 객체를 생성할때 입력값이 없는 형태로 생성하면
        #input태그에 아무런 값도 입력되있지 않은상태의 객체가 생성됨
        form = QuestionForm()
        #객체를 바탕으로 HTML 코드로 변환
        #as_p,as_table,as_ul 함수 : Form객체에 입력할수있는
        #공간들을 <input>로 변환하면서 <p>,<tr>과<td>,<li>태그로
        #감싸주는 기능이 있는 함수
        rendered = form.as_p()
        print(rendered)
        #변환값을 HTML파일에 전달
        return render(request,"vote/q_registe.html",
                      {'rendered':rendered})
    elif request.method == "POST":
        #QuestionForm 객체를 생성 - 사용자 입력을 바탕으로 생성
        form = QuestionForm(request.POST)
        #QuestionForm 객체와 연동된 Question객체를 생성및저장
        #form.save(commit=False)
        #-> 연동된 모델클래스의 객체로 변환만 하는 함수 
        #form.save() : 연동된 모델클래스의 객체를 생성 및 데이터베이스에저장
        new_q = form.save()
        print(new_q)
        #생성된 Question객체의 id값으로 detail뷰의 링크를 전달
        return HttpResponseRedirect(
            reverse('detail', args=(new_q.id,)  )  )
#Question 객체 수정 함수
#q_id : 사용자가 수정할 대상의 id값
@login_required
def q_update(request, q_id):
    #수정할 Question 객체를 추출
    #get_object_or_404 : 모델클래스의 객체들중 id변수값을 이용해
    #객체 한개를 추출하는 함수. 단, 해당id값으로 된 객체가 없는경우
    #사용자의 요청에 잘못있는 걸로 판단해 404에러페이지를 전달함
    q = get_object_or_404(Question,id=q_id)
    #조건문 - POST, GET 구분
    if request.method == "GET":
        #GET요청시 QuestionForm객체생성-수정할 객체를 바탕으로 생성
        #폼클래스 객체생성시 instance매개변수에 연동된 객체를 전달하면
        #해당 객체가 가진 값을 input태그에 채운상태로 폼객체가 생성됨
        form = QuestionForm(instance=q)
        #as_table() : 각 입력공간과 설명을 <tr>과<td>로 묶어주는 함수
        result = form.as_table()
        return render(request,"vote/q_update.html",
                      {'result':result})
    elif request.method == "POST":
        #POST 요청시 QuestionForm객체생성-수정대상객체+사용자입력
        #수정대상 객체와 사용자입력으로 폼객체 생성시
        #기존 객체 정보를 사용자입력으로 수정한 상태의 폼객체가 생성됨
        form = QuestionForm(request.POST,instance=q)
        qq = form.save() #사용자입력으로 수정한 결과를 데이터베이스에 반영
        print(q, qq)
        #detail 뷰로 이동
        return HttpResponseRedirect(
            reverse('detail', args=(q.id,) ) )
#Question 객체 삭제 함수
#GET - 정말로 지우시겠습니까?가 뜨는 HTML 전달
#POST - 데이터베이스에 삭제하는 처리 및 메인페이지 주소를 전달
@login_required
def q_delete(request, q_id):
    q = get_object_or_404(Question,id=q_id)
    if request.method =="GET":
        return render(request, "vote/q_delete.html",
                      {'q' : q })
    elif request.method=="POST":
        #추출한 Question객체를 데이터베이스에 제거
        print("삭제할 대상의 id변수값 :", q.id)
        q.delete() #데이터베이스에 해당 객체정보를 삭제하는 함수
        #삭제를 하더라도 id변수값을 제외한 변수들 값은 사용할 수 있음
        print("삭제된 대상의 id변수값 :", q.id)
        print('삭제된 대상의 title값 :',q.title)
        return HttpResponseRedirect(reverse('main'))

#Choice 객체 추가
#GET - 빈 ChoiceForm객체 생성 및 html파일 전달
#POST - 사용자입력기반의 ChoiceForm객체 생성 및
#데이터베이스에 객체 저장 - detail 뷰로 이동 (20분까지)
from vote.forms import ChoiceForm
@login_required
def c_registe(request):
    if request.method == "GET":
        form = ChoiceForm()
        result = form.as_p()
        return render(request,"vote/c_registe.html",
                      {'result':result})
    elif request.method =="POST":
        form = ChoiceForm(request.POST)
        new_c = form.save()
        idx = new_c.q.id
        return HttpResponseRedirect(
            reverse("detail", args=(idx,) ) )
#Choice 객체 수정
#c_id : 수정할 Choice객체의 id값
#공통 : 수정할 Choice객체를 추출
#GET - 추출한 Choice객체 기반의 ChoiceForm 객체 생성및 html전달
#POST - 추출한 Choice객체+사용자입력 기반의 ChoiceForm객체생성
#및 수정사항을 데이터베이스에 반영 - detail 뷰로 이동 
@login_required
def c_update(request, c_id):
    c = get_object_or_404(Choice, id=c_id)
    if request.method == "POST":
        form = ChoiceForm(request.POST, instance=c)
        form.save()
        return HttpResponseRedirect(
            reverse('detail', args=(c.q.id,)))
    elif request.method =="GET":
        form = ChoiceForm(instance = c)
        result = form.as_table()
        #result = ChoiceForm(instance=c).as_table()
        #result : form태그 안에 들어갈 input태그 문자열
        #q_id (옵션): HTML코드에 detail페이지로 이동하기 위한
        #            Question객체의 id값 전달 
        #detail_url : 해당 수정페이지와 연관된 detail페이지의 주소전달
        detail_url = reverse('detail', args=(c.q.id,) )
        return render(request, "vote/c_update.html",
            {'result' : result, 'q_id' : c.q.id,
             'detail_url' : detail_url})
        
#Choice 객체 삭제
#c_id : 삭제할 Choice객체의 id값
#공통 : 삭제할 Choice객체 추출
#GET - 삭제여부를 물어보는 HTML파일 전달
#POST - 추출한 Choice객체를 삭제 및 main(또는detail)로 이동
@login_required
def c_delete(request, c_id):
    c = get_object_or_404(Choice, id = c_id)
    c.delete() #데이터베이스에서 제거 및 id변수값 삭제
    return HttpResponseRedirect(
        reverse('detail', args=(c.q.id,) ) )





















