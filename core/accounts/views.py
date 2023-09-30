from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import time
from .tasks import sendEmail
import requests
from django.views import View
from .models import Profile
from .forms import ProfileForm
from django.views.generic import UpdateView

def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done Sending</h1>")


@cache_page(60)
def test(request):
    response = requests.get(
        "https://b033411-3948-4555-af18-17d55a38926.mock.pstmn.io/test/delay/3"
    )
    return JsonResponse(response.json())

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        account = Profile.objects.get(user=request.user)
        return render(request, 'accounts/profile.html', {'account':account})


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = "/accounts/profile/"