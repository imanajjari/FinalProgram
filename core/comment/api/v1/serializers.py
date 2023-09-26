from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile
from ...models import  Comment
from blog.api.v1.serializers import PostSerializer




class CommentSerializer(serializers.ModelSerializer):
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name="get_abs_url")

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "email",
            "subject",
            "message",
            "snippet",
            "relative_url",
            "absolute_url",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["user"]

    def get_abs_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        rep["post"] = PostSerializer(
            instance.post, context={"request": request}
        ).data
        rep["post"].pop("image",None)
        rep["post"].pop("category",None)
        rep["post"].pop("snippet",None)
        rep["post"].pop("created_date",None)
        rep["post"].pop("published_date",None)
        return rep

    def create(self, validated_data):
        validated_data["user"] = Profile.objects.get(
            user__id=self.context.get("request").user.id
        )
        validated_data["name"] = Profile.objects.get(
            user=self.context.get("request").user.id
        )
        return super().create(validated_data)

