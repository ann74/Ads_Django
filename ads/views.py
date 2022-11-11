import json

from django.core.paginator import Paginator
from django.db.models import ProtectedError, Count, Q
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from Ads_Django import settings
from ads.models import Ads, Categories, AdsEncoder, CatEncoder, Users, UsersEncoder, Location


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# Общий класс для отображения списка объявлений, категорий и пользователей, с пагинацией
class ModelListView(ListView):
    encoder = None

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

        return JsonResponse(response, safe=False, encoder=self.encoder)


# Общий класс для отображения одного объявления, категории и пользователя
class ModelDetailView(DetailView):
    encoder = None

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse(ad, safe=False, encoder=self.encoder)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)
        ad = Ads.objects.create(
            name=ad_data['name'],
            author_id=ad_data['author_id'],
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            category_id=ad_data['category_id'],
        )

        return JsonResponse(ad, safe=False, encoder=AdsEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Categories
    fields = ['name']

    def post(self, request, *args, **kwargs):
        cat_data = json.loads(request.body)
        cat = Categories.objects.create(name=cat_data['name'])

        return JsonResponse(cat, safe=False, encoder=CatEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = Users
    fields = ['username', 'password', 'first_name', 'last_name', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)
        user = Users.objects.create(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password=user_data['password'],
            role=user_data['role'],
            age=user_data['age'],
        )
        for loc in user_data['locations']:
            loc_obj, created = Location.objects.get_or_create(name=loc)
            user.locations.add(loc_obj)
            user.save()

        return JsonResponse(user, safe=False, encoder=UsersEncoder)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'price', 'description', 'is_published', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        self.object.name = ad_data['name']
        self.object.price = ad_data['price']
        self.object.description = ad_data['description']
        self.object.is_published = ad_data['is_published']
        self.object.category_id = ad_data['category_id']
        self.object.save()

        return JsonResponse(self.object, safe=False, encoder=AdsEncoder)


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


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = Users
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)
        self.object.username = user_data['username']
        self.object.first_name = user_data['first_name']
        self.object.last_name = user_data['last_name']
        self.object.password = user_data['password']
        self.object.age = user_data['age']

        for loc in user_data['locations']:
            loc_obj, created = Location.objects.get_or_create(name=loc)
            self.object.locations.add(loc_obj)
            self.object.save()

        return JsonResponse(self.object, safe=False, encoder=UsersEncoder)


# Общий класс для удаления объявления, категории и пользователя
@method_decorator(csrf_exempt, name='dispatch')
class ModelDeleteView(DeleteView):
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return JsonResponse({"status": "ok"}, status=200)
        except ProtectedError:
            return JsonResponse({"status": "Not deleted"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse(self.object, safe=False, encoder=AdsEncoder)


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
                              'locations': list(user.locations.all().values_list("name", flat=True)),
                              'total_ads': user.total_ads
                          } for user in page_obj),
            "page": page_number,
            "total": paginator.count,
            "per_page": settings.TOTAL_ON_PAGE
        }

        return JsonResponse(response)
