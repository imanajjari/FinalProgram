from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, JsonResponse
from .models import Post
from django.shortcuts import get_object_or_404
from .forms import PostForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)

# test
from django.views import View
from comment.models import Comment
from django.contrib import messages
from comment.forms import CommentForm
from accounts.models import Profile
from accounts.models import User
import requests
# Create your views here.

# Function Base View show a template

class IndexView(TemplateView):
    """
    a class based view to show index page
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        return context


class PostListView(ListView):
    permission_required = "blog.view_post"
    # queryset = Post.objects.all()
    # model = Post
    context_object_name = "posts"
    # paginate_by = 2
    ordering = "-id"
    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts


class PostDetailView(View):
    form_class = CommentForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        commments = Comment.objects.filter(post=self.post_instance.id)
        return render(request, 'blog/blog-single.html',{'post':self.post_instance,'commments':commments, 'form':self.form_class})


    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comments = form.save(commit=False)
            new_comments.user = profile
            new_comments.name = request.user
            new_comments.post = self.post_instance
            new_comments.save()
            messages.success(request, 'your comment submitted successfully', 'success')
            return redirect('blog:post-detail', self.post_instance.id)
        return redirect('blog:post-detail', self.post_instance.id)


class PostListApiView(TemplateView):
    template_name = "blog/post_list_api.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        form.instance.author = profile
        return super().form_valid(form)


class PostEditView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/post/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/post/"

# @cache_page(60)
# def test(request):
#     response = requests.get("https://5add16cb-13b5-4c3e-ac48-635ec4f8654b.mock.pstmn.io/test/delay/20")
#     return JsonResponse(response.json())

@cache_page(1200)
def test(request):
    api_key = 'c10cf61f23551c490fe69ca601a58502'
    city_name = 'Tehran'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        temperature = data['main']['temp']
        weather_description = data['weather'][0]['description']
        print(f"The temperature in {city_name} is {temperature} degrees Celsius with {weather_description}.")
        return JsonResponse(response.json())
    else:
        return HttpResponse("Failed to retrieve weather data.")

    