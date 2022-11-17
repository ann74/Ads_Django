import json

from django.core.paginator import Paginator
from django.db.models import ProtectedError, Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from Ads_Django import settings
from ads.models import Ads, Categories, CatEncoder, Users, Location
from ads.serializers import UserSerializer, AdsSerializer, LocationSerializer


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# GET, POST, PUT, PATCH and DELETE for Location
class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# GET and POST for Users
class UserListCreateView(ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


# GET for one user, PUT, PATCH and DELETE
class UserDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


# GET and POST for Ads
class AdListCreateView(ListCreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get(self, request, *args, **kwargs):
        ad_category = request.GET.get('cat')
        if ad_category:
            self.queryset = self.queryset.filter(category_id=ad_category)

        ad_text = request.GET.get('text')
        if ad_text:
            self.queryset = self.queryset.filter(name__icontains=ad_text)

        ad_location = request.GET.get('location')
        if ad_location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=ad_location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')

        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(self, request, *args, **kwargs)


# GET for one ad, PUT, PATCH and DELETE
class AdDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer


# GET for categories list
class CatlListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        response = {
            "items": list(page_obj),
            "page": page_number,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, safe=False, encoder=CatEncoder)


# GET for one category
class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse(ad, safe=False, encoder=CatEncoder)


# POST for category
@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        cat = Categories.objects.create(name=cat_data['name'])

        return JsonResponse(cat, safe=False, encoder=CatEncoder)


# PATCH for category
@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Categories
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        cat_data = json.loads(request.body)
        self.object.name = cat_data['name']
        self.object.save()

        return JsonResponse(self.object, safe=False, encoder=CatEncoder)


# DLETE for category
@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return JsonResponse({"status": "ok"}, status=200)
        except ProtectedError:
            return JsonResponse({"status": "Not deleted"}, status=404)


# Класс для вывода пользователей м количеством опубликованных объявлений у каждого
class UserAdsDetailView(View):
    def get(self, request):
        user_qs = Users.objects.annotate(total_ads=Count('ads', filter=Q(ads__is_published=True)))
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
