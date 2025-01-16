from rest_framework.serializers import ModelSerializer
from ads.models import Ads, Comment


class AdsSerializer(ModelSerializer):
    class Meta:
        model = Ads
        fields = ("title", "description", )


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
