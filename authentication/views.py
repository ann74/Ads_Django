from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from Ads_Django import settings
from authentication.models import Location, User
from authentication.serializers import LocationSerializer, UserSerializer


# GET, POST, PUT, PATCH and DELETE for Location
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# GET and POST for Users
class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# GET for one user, PUT, PATCH and DELETE
class UserDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# Класс для вывода пользователей м количеством опубликованных объявлений у каждого
class UserAdsDetailView(View):
    def get(self, request):
        user_qs = User.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))
        paginator = Paginator(user_qs, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        response = {
            "items": list({
                              'id': user.id,
                              'username': user.username,
                              'first_name': user.first_name,
                              'last_name': user.last_name,
                              'role': user.role,
                              'age': user.age,
                              'locations': list(map(str, user.locations.all())),
                              'total_ads': user.total_ads
                          } for user in page_obj),
            "page": page_number,
            "total": paginator.count,
            "per_page": settings.TOTAL_ON_PAGE
        }

        return JsonResponse(response)
