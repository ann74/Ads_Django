from django.contrib.auth.models import User
from django.urls import path
from ads import views
from ads.models import Ads, AdsEncoder, Categories, CatEncoder, Users, UsersEncoder

urlpatterns = [
    path('', views.index),
    path('ad/', views.ModelListView.as_view(model=Ads, encoder=AdsEncoder)),
    path('cat/', views.ModelListView.as_view(model=Categories, encoder=CatEncoder)),
    path('user/', views.ModelListView.as_view(model=Users, encoder=UsersEncoder)),
    path('ad/<int:pk>/', views.ModelDetailView.as_view(model=Ads, encoder=AdsEncoder)),
    path('cat/<int:pk>/', views.ModelDetailView.as_view(model=Categories, encoder=CatEncoder)),
    path('user/<int:pk>/', views.ModelDetailView.as_view(model=Users, encoder=UsersEncoder)),
    path('ad/create/', views.AdsCreateView.as_view()),
    path('cat/create/', views.CatCreateView.as_view()),
    path('user/create/', views.UserCreateView.as_view()),
    path('ad/<int:pk>/update/', views.AdsUpdateView.as_view()),
    path('cat/<int:pk>/update/', views.CatUpdateView.as_view()),
    path('user/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('ad/<int:pk>/delete/', views.ModelDeleteView.as_view(model=Ads)),
    path('cat/<int:pk>/delete/', views.ModelDeleteView.as_view(model=Categories)),
    path('user/<int:pk>/delete/', views.ModelDeleteView.as_view(model=Users)),
    path('ad/<int:pk>/upload_image/', views.AdsImageView.as_view()),
    path('user/Z/', views.UserAdsDetailView.as_view()),
]
