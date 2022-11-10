import json

from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView

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
            author_id=ad_data['author'],
            price=ad_data['price'],
            description=ad_data['description'],
            is_published=ad_data['is_published'],
            category_id=ad_data['category'],
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
