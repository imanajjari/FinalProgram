from django.shortcuts import render,redirect
from django.views import  View
from blog.models import Post
from django.contrib import messages
from .forms import CommentForm



# Create your views here.


def Comment_register_view (request, post_id):
    post = Post.objects.get(pk=post_id, status=1)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            messages.success(request, 'نظر شما ثبت شد', 'success')
            form.save()
            return redirect('blog:post-detail', post.id )