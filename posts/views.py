from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.defaultfilters import title
from posts.models import Post
from posts.forms import PostForm, PostForm2, CommentForm
import random

def test_view(request):
    return HttpResponse("Big World")

def main_page_view(request):
    return render(request, 'base.html')


def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "post_list.html", context={"posts": posts})

def post_detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    form = CommentForm()
    return render(request, "post_detail.html", context={"post": post, "form": form})

def post_create_view(request):
    if request.method == "GET":
        form = PostForm2()
        return render(request, "post_create.html", context={"form": form})
    if request.method == "POST":
        form = PostForm2(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "post_create.html", context={"form": form})
        form.save()
        return redirect("/posts/")

def comment_create_view(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if not form.is_valid():
            return render(request, "comment_create.html", context={"form": form})
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