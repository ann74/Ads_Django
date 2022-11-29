from rest_framework import serializers

from ads.models import Ads, Categories
from authentication.models import User


class AdsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field='name')

    class Meta:
        model = Ads
        fields = '__all__'
