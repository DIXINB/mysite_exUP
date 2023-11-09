from django.shortcuts import get_object_or_404, render, redirect, HttpResponse, Http404
from django.http import FileResponse
import os
from books.models import Book # импорт модели Book из файла books/models.py
from books.models import Author
from books.models import Hist
from books.models import Artc
from books.models import Dict
from books.models import Pros
from books.models import Ip
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import Post, Replie, Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

# Метод для получения айпи
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR') # В REMOTE_ADDR значение айпи пользователя
    return ip	
	
def view(request, id):
    b = get_object_or_404(Book, id=id)
    return render(request, "view.html", {"Book": b})
def my_homepage(request):
    #book_list = Book.objects.all().order_by('id')
    return render(request, "books/my_homepage.html")
def mail(request):
    return render(request, "books/mail_repair.html")
def forum_repair(request):
    return render(request, "books/forum_repair.html")	
def history(request):
    hist_list = Hist.objects.all()
       
    page = request.GET.get('page', 1)
    paginator = Paginator(hist_list, 7)
    try:
        hist_list = paginator.page(page)
    except PageNotAnInteger:
        hist_list = paginator.page(1)
    except EmptyPage:
        hist_list = paginator.page(paginator.num_pages)
    
    return render(request, "books/history.html",{"hist_list": hist_list})	

def hist(request,histid):
    h1 = Hist.objects.get(ind=histid)
    ip = get_client_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        h1.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        h1.views.add(Ip.objects.get(ip=ip))
    return render(request, "books/hist.html", {"h1": h1})


def articles(request):
    artc_list = Artc.objects.all()
       
    page = request.GET.get('page', 1)
    paginator = Paginator(artc_list, 7)
    try:
        artc_list = paginator.page(page)
    except PageNotAnInteger:
        artc_list = paginator.page(1)
    except EmptyPage:
        artc_list = paginator.page(paginator.num_pages)
    
    return render(request, "books/articles.html",{"artc_list": artc_list})	

def artc(request,artcid):
    a1 = Artc.objects.get(ind=artcid)
    ip = get_client_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        a1.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        a1.views.add(Ip.objects.get(ip=ip))

    p_l=[[]]
    
    range=[[a1.picture1,a1.capt1],[a1.picture2,a1.capt2],[a1.picture3,a1.capt3],
	    [a1.picture4,a1.capt4],[a1.picture5,a1.capt5],[a1.picture6,a1.capt6]]
    print(range[1][1])
    for a in range:
        cort=()
        cort += (a[0],)
        cort += (a[1],)
        p_l.append(cort)  		
    print(p_l)
    return render(request, "books/artc.html", {"a1": a1, "picture_list":p_l})
	
def dict(request):
    dict_list = Dict.objects.all().order_by('id')
    return render(request, "books/dict.html", {"dict_list": dict_list})	
def prose(request):
    pros_list = Pros.objects.all()       
    page = request.GET.get('page', 1)
    paginator = Paginator(pros_list, 7)
    try:
        pros_list = paginator.page(page)
    except PageNotAnInteger:
        pros_list = paginator.page(1)
    except EmptyPage:
        pros_list = paginator.page(paginator.num_pages)
    
    return render(request, "books/prose.html",{"pros_list": pros_list})


def prse(request,prseid):	
    p1 = Pros.objects.get(ind=prseid)
    ip = get_client_ip(request)
    if Ip.objects.filter(ip=ip).exists():
        p1.views.add(Ip.objects.get(ip=ip))
    else:
        Ip.objects.create(ip=ip)
        p1.views.add(Ip.objects.get(ip=ip))
    filepath=os.path.join('media/story', f'Story{prseid}.pdf')
    return FileResponse(open(filepath,'rb'),content_type='application/pdf')



def forum(request):
    profile = Profile.objects.all()
    if request.method=="POST":   
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content','')
        post = Post(user1=user, post_content=content, image=image)
        post.save()
        alert = True
        return render(request, "books/forum.html", {'alert':alert})
    posts = Post.objects.filter().order_by('-timestamp')
    return render(request, "books/forum.html", {'posts':posts})

def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
        user = request.user
        image = request.user.profile.image
        desc = request.POST.get('desc','')
        post_id =request.POST.get('post_id','')
        reply = Replie(user = user, reply_content = desc, post=post, image=image)
        reply.save()
        alert = True
        return render(request, "books/discussion.html", {'alert':alert})
    return render(request, "books/discussion.html", {'post':post, 'replies':replies})

def UserRegister(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'books/login.html')        
    return render(request, "books/register.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/myprofile")
        else:
            messages.error(request, "Invalid Credentials")
        alert = True
        return render(request, 'books/login.html', {'alert':alert})            
    return render(request, "books/login.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url = '/login')
def myprofile(request):
    if request.method=="POST":
        user = request.user    
        profile = Profile(user=user)
        profile.save()
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "books/profile.html",{'obj':obj})
    else:
        form=ProfileForm()
    return render(request, "books/profile.html", {'form':form})
