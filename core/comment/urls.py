from django.urls import path, include
from . import views


app_name = "comment"

urlpatterns = [
    path("register/<int:post_id>/", views.Comment_register_view, name="register"),
]
