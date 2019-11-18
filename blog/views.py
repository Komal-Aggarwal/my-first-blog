from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect 
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def render_base(request):
    return render(request, 'blog/base.html', {})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})
    
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    dictV = {}   
    post = get_object_or_404(Post, pk=pk)
    user = post.author
    if request.user == user:
        if request.method =="POST":
           post.title = request.POST.get('title')
           post.text = request.POST.get('text')
           post.cover = request.FILES.get('coveimage')
           datestring = request.POST.get('Publishdate')
           post.published_date = timezone.now()
           post.save()
           dictV['message'] = "Blog Post Updated !!"
           return redirect('post_detail', pk=post.pk)
    else:
        return HttpResponseRedirect('/')
    dictV['post'] = post
    return render(request, 'blog/post_edit.html', dictV)
def login(request):
    dictV = {}
    if request.method=="POST":
        username = request.POST.get('inputUser')
        password = request.POST.get('inputPassword')
        print(password)
        user = auth.authenticate(username = username, password = password)
        print(username, password, user)
        if not user:
            dictV['error'] = "Invalid username and password combination."
            return render(request, 'blog/login.html', dictV)
        auth.login(request, user)
        print('loged in')
        return HttpResponseRedirect('/')
    return render(request,'blog/login.html',{})


def signup(request):
    dictV={}
    if request.method=='POST':
        username=request.POST.get('inputUser')
        email=request.POST.get('inputEmail')
        password1=request.POST.get('inputPassword1')
        password2=request.POST.get('inputPassword2')

        if password1 != password2:
           dictV['error'] = "Password does not match !"
           return render(request, 'blog/signup.html',dictV)  

        if User.objects.filter(username=username).count() > 0:
            dictV['error'] = "Username already taken"
            return render(request, 'blog/signup.html',dictV)

        if User.objects.filter(email=email).count() > 0:
            dictV['error'] = "Email ID already registered! Try Logging in"
            return render(request, 'blog/signup.html',dictV)

        user = User.objects.create_user(username=username,
                                 email=email)
        user.set_password(password2)
        user.save()
        dictV['success'] = "User "+username+" Created Successfully!! You can login now"

    return render(request, 'blog/signup.html',dictV)

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

@login_required
def post_delete(request, pk):
    dictV = {}   
    post = get_object_or_404(Post, pk=pk)
    confirmed = request.GET.get('confirm')
    user = post.author
    if request.user == user:
        if confirmed == 'yes':
            post.delete()
            return HttpResponseRedirect('/')
        dictV['post'] = post
    else:
        return HttpResponseRedirect('/')   
    return render(request, 'blog/post_delete.html', dictV)


    