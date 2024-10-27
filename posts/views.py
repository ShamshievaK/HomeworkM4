from re import search

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.defaultfilters import title
from posts.models import Post
from django.db.models import Q
from posts.forms import PostForm, PostForm2, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
import random

def test_view(request):
    return HttpResponse("Big World")

def main_page_view(request):
    return render(request, 'base.html')

@login_required(login_url='/login/')
def post_list_view(request):
    limit = 3
    if request.method == 'GET':
        search = request.GET.get('search', None)
        tag = request.GET.getlist('tag', None)
        ordering = request.GET.get('ordering', None)
        page = int(request.GET.get('page', 1))
        posts = Post.objects.all()
        if search:
            posts = posts.filter(Q(title__icontains=search) | Q(content__icontains=search))
        if tag:
            posts = posts.filter(tags__id__in=tag)
        if ordering:
            posts = posts.order_by(ordering)
        max_pages = posts.count()//limit
        if round(max_pages) < max_pages:
            max_pages = round(max_pages) +1
        else:
            max_pages = max_pages

        start = (page-1)*limit
        end = page*limit
        posts = posts[start:end]

        form = SearchForm()
        context = {"posts": posts, "form": form, "max_pages": range(1, max_pages+1)}
        return render(request, "posts/post_list.html", context=context)  #, context={"posts": posts, "form": form})

@login_required(login_url='/login/')
def post_detail_view(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id=post_id)
        form = CommentForm()
        return render(request, "posts/post_detail.html", context={"post": post, "form": form})

@login_required(login_url='/login/')
def post_create_view(request):
    if request.method == "GET":
        form = PostForm2()
        return render(request, "posts/post_create.html", context={"form": form})
    if request.method == "POST":
        form = PostForm2(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form": form})
        form.save()
        return redirect("/posts/")

def comment_create_view(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if not form.is_valid():
            return render(request, "posts/comment_create.html", context={"form": form})
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect("/posts/{post_id}")







# def post_create_view(request):
#     if request.method == "GET":
#         form = PostForm()
#         return render(request, "post_create.html", context={"form": form})
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if not form.is_valid():
#             return render(request, "post_create.html", context={"form": form})
#         title = form.cleaned_data.get("title")
#         content = form.cleaned_data.get("content")
#         image = form.cleaned_data.get("image")
#         # title = request.POST.get("title")
#         # content = request.POST.get("content")
#         # image = request.FILES.get("image")
#         post = Post.objects.create(title=title, content=content, image=image)
#         return HttpResponse(f"Post with title {post.title} created successfully")