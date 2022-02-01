from django.shortcuts import *
from testapp.models import *
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.core.paginator import Paginator
from django.views.generic import ListView
from taggit.models import Tag



# Create your views here.
def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])


    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)
    return render(request,'testapp/post_list.html',{'post_list':post_list,'tag':tag})

# class PostListView(ListView):
#     model=Post
#     paginate_by=2
from testapp.models import *
from testapp.forms import *

def post_detail_view(request,year,month,day,blog):
    blog_detail=get_object_or_404(Post,slug=blog,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=blog_detail.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=blog_detail
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'testapp/post_detail.html',{'blog_detail':blog_detail,'form':form,'csubmit':csubmit,'comments':comments})

from django.core.mail import send_mail
from testapp.forms import *

def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            subject='{}({}) Recommends You to read "{}"'.format(cd['name'],cd['email'],post.title)
            post_url=request.build_absolute_uri(post.get_absolute_url())
            message='Read post at:\n {}\n\n{}\s comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail('subject','message','suhassmtp@gmail.com',[cd['to']])
            sent=True
    else:
        form=EmailSendForm()

    return render(request,'testapp/sharebyemail.html',{'form':form,'post':post,'sent':sent})
