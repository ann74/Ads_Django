from rest_framework import serializers

from ads.models import Users, Location, Ads, Categories


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    locations = serializers.SlugRelatedField(queryset=Location.objects.all(),
                                             slug_field='name',
                                             many=True, required=False)

    class Meta:
        model = Users
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._locations = self.initial_data.pop('locations', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = Users.objects.create(**validated_data)
        for loc in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(loc_obj)
        user.save()
        return user

    def save(self):
        user = super().save()
        user.locations.clear()
        for loc in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(loc_obj)
        user.save()
        return user


class AdsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(queryset=Users.objects.all(), slug_field='username')
    category = serializers.SlugRelatedField(queryset=Categories.objects.all(), slug_field='name')

    class Meta:
        model = Ads
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
