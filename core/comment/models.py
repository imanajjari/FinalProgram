from django.db import models
from accounts.models import User
from blog.models import Post
from django.urls import reverse
from accounts.models import Profile



# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='ucomments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='pcomments')
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    approved = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date',]

    def __str__(self):
        return f'{self.name}'

    def get_snippet(self):
        return self.message[0:30]

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:comment-detail", kwargs={"pk": self.pk})

