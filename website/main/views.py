from operator import pos
from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post

# Create your views here.

@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()

    # delete a post
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        post = Post.objects.filter(id=post_id).first()

        if post and post.author == request.user:
            post.delete()

    return render(request, 'main/home.html', {'posts': posts})


@login_required(login_url='/login')
def create_post(request):
    # create a post with the data from the posted form
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return redirect('/home')
    # load a blank form
    else:
        form = PostForm()

    return render(request, 'main/create_post.html', {'form': form})


def sign_up(request):
    # check if some form was posted
    if request.method == 'POST':
        # create the form with the posted information
        form = RegisterForm(request.POST)

        if form.is_valid():
            # save the new user into the database
            user = form.save()
            # login the new user account
            login(request, user)

            return redirect('/home')

    else:
        # method = GET -> blank form
        form = RegisterForm()

    return render(request, 'registration/sign_up.html',  {'form': form})