from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm, UserForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


def post_list(request):
    #if request.user.is_authenticated():
        users= User.objects.all()
        posts = Post.objects.all().order_by('published_date')
        return render(request, 'blog/post_list.html', {'posts': posts,'users':users})
    #if not request.user.is_authenticated():
        #return render(request, 'blog/login.html')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, pk):
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
                form = PostForm(instance=post)
                return render(request, 'blog/post_edit.html', {'form': form})


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
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('post_list')

    return render(request, 'blog/register.html',{'form':form})


def uploadfile(request):
    if request.method == 'POST' and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        image = fs.url(filename)
        return render(request, 'blog/fileupload.html', {
            'uploaded_file_url': image,
        })
    return render(request, 'blog/fileupload.html')