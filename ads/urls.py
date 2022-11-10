from django.urls import path
from ads import views

urlpatterns = [
    path('', views.index),
    path('ad/', views.AdsListView.as_view()),
    path('cat/', views.CatListView.as_view()),
    path('ad/<int:pk>/', views.AdsDetailView.as_view()),
    path('cat/<int:pk>/', views.CatDetailView.as_view()),
    path('ad/create/', views.AdsCreateView.as_view()),
    path('cat/create/', views.CatCreateView.as_view()),
    path('ad/<int:pk>/update/', views.AdsUpdateView.as_view()),
    path('cat/<int:pk>/update/', views.CatUpdateView.as_view()),
    path('ad/<int:pk>/delete/', views.AdsDeleteView.as_view()),
    path('cat/<int:pk>/delete/', views.CatDeleteView.as_view()),
]