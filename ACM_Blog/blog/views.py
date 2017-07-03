from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post,Avatar
from .forms import PostForm, UserForm , ProfileImageForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

def post_list(request):
        if request.user.is_authenticated():
                avatar = Avatar.objects.get(userprof=request.user)
        else:
                avatar=None
        users= User.objects.all()
        posts = Post.objects.all().order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts,'users':users,'avatar':avatar})


def post_detail(request, pk):
    users=User.objects.all()
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post,'users':users})

def post_edit(request, pk):
     users=User.objects.all()
     if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
                if request.user == post.author:
                        form = PostForm(instance=post)
                        return render(request, 'blog/post_edit.html', {'form': form,'users':users})
                else:
                        return HttpResponseForbidden()
            

def post_new(request):
    users=User.objects.all()
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
    return render(request, 'blog/post_edit.html', {'form': form,'users':users})

def logout_user(request):
    logout(request)
    return redirect('post_list')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('post_list')
            else:
                return render(request, 'blog/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'blog/login.html', {'error_message': 'Invalid login'})
    return render(request, 'blog/login.html')


def register(request):
    form = UserForm(request.POST or None)
    imgform = ProfileImageForm(request.POST, request.FILES)
    if form.is_valid() and imgform.is_valid():
        user = form.save(commit=False)
        
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        

        if user is not None:
            if user.is_active:
                login(request, user)
                img=Avatar()
                img.userprof=request.user
                img.profile_image= imgform.cleaned_data['profile_image']
                img.save()
                return redirect('post_list')

    return render(request, 'blog/register.html',{'form':form,'imgform':imgform})
