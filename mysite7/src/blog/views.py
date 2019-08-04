from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from blog.models import Post, PostFile, PostImage
from django.views.generic.detail import DetailView
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls.base import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from blog.forms import PostingForm
from django.template.context_processors import request

#제네릭뷰 : 장고에서 제공하는 여러가지 뷰 기능을 구현한 클래스모음
#ListView : 특정 모델클래스의 객체들을 목록화할수 있는 기능이 구현된 뷰
#글목록이 뜨는 페이지
class Main(ListView):
    #사용자에게 전달할 HTML파일의 경로
    template_name = 'blog/main.html'
    #리스트로 뽑을 모델클래스
    model = Post
    #리스트로 추출한 객체를 HTML에 전달할때 사용할 이름
    context_object_name = 'list'
    #한페이지에 몇개의 객체가 보여질지 설정
    paginate_by = 5
#글 상세보기 페이지
#DetailView : 특정 모델클래스의 특정 객체 한개를 추출할때 사용하는 뷰
class Detail(DetailView):
    #사용자에게 전달할 HTML파일의 경로
    template_name = 'blog/detail.html'
    #리스트로 뽑을 모델클래스
    model = Post
    #리스트로 추출한 객체를 HTML에 전달할때 사용할 이름
    context_object_name = 'obj'
#글 작성 페이지




class Posting(LoginRequiredMixin, FormView):
    #사용자에게 전달할 HTML파일경로
    template_name='blog/posting.html'
    #연동할 폼클래스의 이름
    form_class = PostingForm
    #GET방식으로 요청이 들어오면 등록된 폼클래스의 객체생성후 HTML파일과 함께 전달
    #POST방식으로 요청이 들어오면 사용자의 읩력을 바탕으로 폼클래스 생성후 유효값인지(is_valid) 확인한 뒤 True 값이 반환되면
    #폼 객체를 저장하는 함수가 호출


def form_valled(self, form):
    #Form 객체를 Post 객체로 변환
    #why? : Post 객체를 데이터베이스에 저장할때 user 변수에 값이 들어있지 않은 상태이기 때문에 에러발생
    #p : 사용자입력을 바탕으로 category, title, content변수가 채워져있는 새로운 Post객체
    p = form.seve(commit=False)
    #User 정보를 클라이언트의 유저정보로 대입 
    #self.request : 해당 뷰를 요청한 클라이언트의 요청정보가 저장된 변수
    #self.request.user : 요청한 클라이언트의 User모델클래스 객체저장변수
    p.user = self.request.user
    #데이터베이스에 Post 객체 저장
    p.save()
    #사용자가 업로드한 파일 데이터를 바탕으로 PostFile 객체생성
    #사용자가 업로드한 파일의 갯수만큼 반복하기 위해
    #self.request.FILES : 사용자가 업로드한 파일을 저장한 변수
    #slef.request.FIELS.getlist(name 속성이름)
    # : 해당 입력공간에 업로드된 파일 데이터들을 추출
    for f in self.request.FILES.get_list('files'):
        pf = PostFile # 새로운 PostFile객체생성 - 데이터베이스에 저장 x
        pf.post = p #새로만들어진 Post객체와 연동
        pf.file = f #사용자가 업로드한 파일을 FIleField에 저장
        pf.save()
    #사용자가 업로드한 이미지데이터를 바탕으로 PostImage객체생성
    #사용자가 'images' 입력공간에 업로드한 파일들을 바탕으로 객체생성
    for i in self.request.FILES.getlist('images'):
        #새로운 PostImage객체 생성 - 데이터베이스에 저장 X
        pi = PostImage()
        pi.post = p
        pi.image = i 
        pi.save()
    #blog:detail로 리다이렉트
    #새로 만들어진 Post객체의 id값으로 detail뷰의 주소 전달
    return HttpResponseRedirect(reverse('blog:detail',args=(p.id,)))


#글 삭제기능
def post_delete(request, p_id):
    #post객체 한개 추출
    p = get_object_or_404(Post,id=p_id)
    #추출한 객체의 user정보와 요청한 클라이언트의 user정보를 비교
    if p.user == request.user:
        #자기가 쓴 글을 지우는 요청 : 추출한 객체를 삭제
        p.delete()
        #메인페이지로 이동
        return HttpResponseRedirect(reverse('blog:main'))
    else:
        #자기가 쓴 글이 아닌데 요청을 한 경우 : 404Error 전달
        return HttpResponseNotAllowed() # 허용되지 않은 요청









