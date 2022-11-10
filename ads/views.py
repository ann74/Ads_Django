import json

from django.db.models import ProtectedError
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ads, Categories, AdsEncoder, CatEncoder


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = [ad for ad in self.object_list]

        return JsonResponse(response, safe=False, encoder=AdsEncoder)


class CatListView(ListView):
    model = Categories

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        response = [cat for cat in self.object_list]

        return JsonResponse(response, safe=False, encoder=CatEncoder)


class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse(ad, safe=False, encoder=AdsEncoder)


class CatDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        try:
            cat = self.get_object()
        except Http404:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse(cat, safe=False, encoder=CatEncoder)


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
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Categories
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        try:
            super().delete(request, *args, **kwargs)
            return JsonResponse({"status": "ok"}, status=200)
        except ProtectedError:
            return JsonResponse({"result": "Not deleted"}, status=404)


