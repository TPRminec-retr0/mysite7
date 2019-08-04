from django.db import models

'''
models.py : 모델클래스를 정의할때 사용하는 파일
모델 클래스 개발 및 반영 순서
1) 모델클래스 정의 시, 미리 import된 models 파일에 있는 Model클래스
상속. 해당 클래스에 저장할 변수들을 클래스변수로 선언
2) 모델클래스를 migration파일로 변환 - manage.py에게 명령
3) 애플리케이션별 migration파일을 데이터베이스에 반영 - manage.py
4) admin.py에 정의된 모델클래스를 등록

모델클래스의 클래스 변수는 해당 클래스가 저장할수있는 데이터를 의미함
클래스 변수에 저장할 데이터 형식을 models.XXXXField의 객체를 저장해
지정할 수 있음

'''
#설문항목을 저장하는 모델클래스
class Question(models.Model):
    
    #제목 - title변수 생성
    #100글자로 제한된 문자열을 저장할 수 있는 공간을 생성
    #CharField : 글자수 제한이 있는 저장공간을 생성할때 사용하는클래스
    #CharField객체 생성시 max_length(최대글자제한)매개변수에
    #정수값을 필수적으로 입력해야함
    title = models.CharField("제목",max_length=100)
    #생성일 - pub_date변수 생성
    #DateField : 년월일 데이터를 저장할 수 있는 공간
    #DateTimeField : 년월일+시분초 데이터를 저장할 수 있는 공간
    #옵션) auto_now_add 매개변수 : True 설정 시, 서버의 시간을
    #데이터베이스에 저장할때 자동으로 입력
    pub_date = models.DateTimeField(auto_now_add=True)
    #관리자 사이트에 객체 출력 함수를 오버라이딩
    def __str__(self):
        return "%s. %s" % (self.id, self.title)
    
#설문항목에 연결된 답변항목을 저장하는 모델클래스
'''
ForeignKey(연결할 다른모델클래스, on_delete)
: ForeignKey 객체를 만든 모델클래스의 객체들이 연결할 다른모델클래스
의 객체와 1:n 관계로 연결할 수 있는 클래스
연결된 모델클래스의 객체들은 데이터 추출을 할 수 있음
ex) Choice객체.q.title
on_delete : 연결된 다른모델클래스의 객체가 삭제된 경우 어떤처리를
할지 저장하는 매개변수  
models.CASCADE : 연결된 객체도 같이 삭제됨
models.PROTECT : 연결된 객체가 삭제되지않도록 삭제명령 취소
models.SET_NULL : 아무 객체와 연결되지않은 상태 유지
'''
class Choice(models.Model):
    #어떤 Question 객체에 연결되있는지 저장하는 공간
    q = models.ForeignKey(Question,on_delete=models.CASCADE)
    #답변 내용을 저장하는 공간
    name = models.CharField("항목",max_length=50)
    #투표수를 저장하는 공간
    #IntegerField : 정수값을 저장하는 공간을 생성할때 사용하는 클래스
    #default : 모든 Field 클래스의 생성자에 있으며 객체 생성시
    #값을 입력하지 않더라도 저장공간에 기본값을 설정
    votes = models.IntegerField("투표 수",default=0)
    def __str__(self):
        #Question객체의 title + Choice객체의 name
        return "%s - %s" % (self.q.title, self.name)
















