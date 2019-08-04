from django.shortcuts import render
from customlogin.forms import SigninForm,SignupForm
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib.auth import authenticate, login, logout
#회원가입
#GET - 사용자에게 빈 회원가입란을 제공하는 HTML파일 전달
#POST - 사용자 입력을 바탕으로 회원가입 진행
def signup(request):
    if request.method == "GET":
        #SignupForm에서 입력할 수있는 공간을 input태그로 변환
        result = SignupForm().as_table()
        return render(request,"cl/signup.html",
                      {'result':result})
    elif request.method == 'POST':
        form = SignupForm(request.POST)
        #사용자의 입력이 유효한 값이 있는지 확인
        #-> is_valid() 함수 호출 결과가 True면 정상입력
        # False면 유효하지 않은 값
        #(아이디중복,이메일형식,비밀번호형식확인)
        if form.is_valid():
            #is_valid함수의 결과가 True인 경우,
            #form.cleaned_data변수로 원본데이터를  접근할 수 있음
            #비밀번호 란과 비밀번호 확인란이 같은값이 있는지 확인
            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
                #User 객체 생성 및 데이터베이스에 저장
                #User 모델클래스는 비밀번호가 원본데이터가 아닌 암호화된 데이터를 저장함
                # 새로운 User 객체를 생성할때 원본 비밀번호를 암호화해 객체생성해주는 
                # 함수를 사용해야함. => User.objects.create_user 함수
                #create_user(id문자열,이메일,원본비밀번호문자열)
                #->원본비밀번호는 암호화된상태로 새로운 User객체를 생성 및 반환
                new_user = User.objects.create_user(form.cleaned_data['username'],
                                         form.cleaned_data['email'],
                                         form.cleaned_data['password'])
                #성과 이름 저장변수에 사용자입력을 대입
                new_user.first_name = form.cleaned_data['first_name']
                new_user.last_name = form.cleaned_data['last_name']
                #변경된 사항을 데이터베이스에게 통보
                new_user.save()
                #main 페이지로 이동
                return HttpResponseRedirect(
                    reverse('main'))

#로그인
#GET - 폼 제공
#POST - 로그인 처리
def signin(request):
    if request.method == "GET":
        return render(request,"cl/signin.html",
            {'result' : SigninForm().as_table()})
    elif request.method == "POST":
        #사용자가 아이디나 비밀번호가 틀렸을때 전달할 form객체
        form = SigninForm(request.POST)
        #아이디와 비밀번호 추출
        id = request.POST.get('username')
        pw = request.POST.get("password")
        #데이터베이스에 User 객체들 중 아이디와 암호화된비밀번호가
        #같은 객체 추출
        user = authenticate(username=id,password=pw)
        print('데이터베이스에서 찾은 User 객체 :',user)
        #웹클라이언트를 추출한 User객체로 로그인처리
        if user: #데이터베이스에서 유저객체를 찾았는지 확인
            #login(request, 추출한 User객체)
            #로그인처리가된 웹클라이언트는 request.user를 사용할수있음
            #request.user.is_authenticated()
            #: 해당 웹클라이언트의 로그인 여부를 확인하는 함수
            login(request,user)
            return HttpResponseRedirect(reverse('main'))
#로그아웃
def signout(request):
    #logout(request) : 해당 요청을 한 웹클라이언트의
    #user정보를 제거
    #request.user 에 None값이 저장됨
    logout(request)
    #cl그룹의 signin별칭을 가진 뷰의 인터넷주소를 클라이언트에게전달
    return HttpResponseRedirect(
        reverse('cl:signin'))











