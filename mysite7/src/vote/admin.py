from django.contrib import admin
#추가할 모델클래스가 있는 파이썬파일을 import
#vote/models.py 에 있는 Question클래스를 접근할수있도록 import
from vote.models import Question,Choice
'''
admin.py : 완성된 모델클래스를 관리자사이트에서 조회/삽입/삭제/수정
/검색 작업을 수행할때 모델클래스를 등록하는 파이썬 파일
admin.site.register(모델클래스)
: 해당 모델클래스를 관리자 사이트에서 접근할수있도록 허용하는 함수
'''
admin.site.register(Question)
admin.site.register(Choice)






