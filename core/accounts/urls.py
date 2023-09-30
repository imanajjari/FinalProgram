from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/edit/", views.ProfileEditView.as_view(), name="profile-edit"),
    path("", include("django.contrib.auth.urls")),
    path("send-email/", views.send_email, name="send-email"),
    path("test/", views.test, name="test"),
    # path('api/v1/',include('accounts.api.v1.urls')),
    path("api/v2/", include("djoser.urls")),
    path("api/v2/", include("djoser.urls.jwt")),
]
