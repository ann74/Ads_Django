from rest_framework import serializers

from ads.models import Ads, Categories, AdsSelection
from authentication.models import User


class AdsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field='name')

    class Meta:
        model = Ads
        fields = '__all__'


class AdsSelectionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdsSelection
        fields = ('id', 'name')


class AdsSelectionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    items = AdsSerializer(many=True)

    class Meta:
        model = AdsSelection
        fields = '__all__'


class AdsSelectionUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    items = serializers.PrimaryKeyRelatedField(queryset=Ads.objects.all(), many=True, required=False)

    class Meta:
        model = AdsSelection
        fields = '__all__'
