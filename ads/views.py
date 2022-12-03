import json

from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.http import JsonResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from Ads_Django import settings
from ads.models import Ads, Categories, CatEncoder, AdsSelection
from ads.permissions import AdUpdateDeletePermission, SelectionUpdateDeletePermission
from ads.serializers import AdsSerializer, AdsSelectionListSerializer, AdsSelectionDetailSerializer, AdsSelectionUpdateSerializer


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


# GET and POST for Ads
class AdListCreateView(ListCreateAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        else:
            return []

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

    def post(self, request, *args, **kwargs):
        request.data.update(author=request.user)
        return super().post(request, *args, **kwargs)


# GET for one ad, PUT, PATCH and DELETE
class AdDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Ads.objects.all()
    serializer_class = AdsSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [AdUpdateDeletePermission()]
        else:
            return []


# GET, POST, PUT, PATCH and DELETE for AdsSelection
class AdsSelectionViewSet(ModelViewSet):
    queryset = AdsSelection.objects.all()
    serializer_class = AdsSelectionUpdateSerializer


    def get_permissions(self, *args, **kwargs):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), SelectionUpdateDeletePermission()]
        elif self.action in ['retrieve', 'create']:
            return [IsAuthenticated()]
        else:
            return []

    def list(self, request, *args, **kwargs):
        self.serializer_class = AdsSelectionListSerializer
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = AdsSelectionDetailSerializer
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data.update(owner=request.user)
        return super().create(request, *args, **kwargs)


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
