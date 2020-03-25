from django.shortcuts import render,redirect,reverse
from article.models import Post,Category,Tags
import markdown
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from comment.models import Comment
from comment.forms import LoginForm,RegForm
from django.contrib import  auth
from django.contrib.auth.models import User
from comment.forms import CommentForm
import datetime




def index(request):
    post_list  = Post.objects.all().order_by('-create_time')
    paginator = Paginator(post_list,6)
    pages_number = request.GET.get('page')
    page_list = paginator.get_page(pages_number)
    currentr_page_num = page_list.number # 获取当前页
    page_range = list(range(max(currentr_page_num - 2,1),currentr_page_num)) + list(range(currentr_page_num,min(currentr_page_num +2,paginator.num_pages)+1))
    print(request)
    if page_range[0] - 1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] !=1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    return render(request,'index.html',context={'title':'博客首页',
                                                'post_list':post_list,
                                                'page_range':page_range
                                                })


def detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body,extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc'
                                        ]

                                  )
    user = request.user
    blog_content_type = ContentType.objects.get_for_model(post)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=post.pk,parent=None)

    comment_form = CommentForm(initial={'object_id':pk,'content_type':blog_content_type,'reply_comment_id':0})


    return render(request,'article/detail.html',context={'post':post,'user':user,
                                                         'blog_content_type':blog_content_type,
                                                         'comments':comments,
                                                         'comment_form':comment_form,
                                                         })


def archive(request,year,month):
    dataMAX = 30
    months = ['1','3','7','8','10','12']
    if int(month) in months:
        dataMAX = 31
    post_list = Post.objects.filter(create_time__range=(datetime.date(int(year),int(month),1),
                                                        datetime.date(int(year),int(month),dataMAX))).order_by('-create_time')
    print(post_list)
    return render(request, 'index.html', context={'post_list': post_list})


def category(request,pk):
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'index.html',context={'post_list':post_list})


def tag(request,pk):
    t = get_object_or_404(Tags,pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-create_time')
    return render(request,'index.html',context={'post_list':post_list})

def search(request):
    search = request.GET.get('search')
    print(search)
    if search:

        post_list = Post.objects.filter(Q(title__icontains=search) | Q(body__icontains=search))
        context = {'post_list':post_list}
        return render(request,'index.html',context=context)
    else:
        error_msg = '请输入关键词'
        messages.add_message(request,messages.ERROR,error_msg,extra_tags='danger')
        return redirect('article:index')



def login(request):
    # username = request.POST.get('username','')
    # password = request.POST.get('password','')
    # print(password)
    # user = auth.authenticate(request,username=username,password=password)
    # referer = request.META.get('HTTP_REFERER','/')
    # print(referer)
    # if user is not None:
    #     auth.login(request,user)
    #     return redirect(referer)
    # else:
    #     return render(request,'error.html',{'message':'用户名或密码不正确'})
    #
    # referer = request.META.get('HTTP_REFERER', reverse('article:index'))
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('article:index')))

    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form

    return render(request,'login.html',context)



def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        print(reg_form)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            user = User.objects.create_user(username,email,password)
            user.save()

            # user = User()
            # user.username=username
            # user.email = email
            # user.set_password(password)
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('from',reverse('article:index')))

    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form

    return render(request,'register.html',context)

def logout(request):

    auth.logout(request)
    return redirect('article:index')