from datetime import date

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import Location, User


def email_validator(value):
    if '@rambler.ru' in value:
        raise serializers.ValidationError('Не допустимый домен почты')


class DataValidation:
    def __init__(self, valid_age):
        self.valid_age = valid_age

    def __call__(self, value):
        if (date.today() - value).days // 365 < self.valid_age:
            raise serializers.ValidationError(f'Нельзя регистрироваться пользователям младше {self.valid_age} лет')


class UserSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(queryset=Location.objects.all(),
                                             slug_field='name',
                                             many=True, required=False)
    email = serializers.EmailField(required=False, validators=[UniqueValidator(queryset=User.objects.all()),
                                                               email_validator])
    birthday = serializers.DateField(required=False, validators=[DataValidation(9)])

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self.initial_data = self.initial_data.copy()
        self._locations = self.initial_data.pop('locations', [])
        result = super().is_valid(raise_exception=raise_exception)
        self.initial_data.update({'locations': self._locations})
        return result

    def create(self, validated_data):
        # validated_data.pop('locations')
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"])
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


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = '__all__'
