from django.urls import path
from rest_framework import routers

from ads import views


router = routers.SimpleRouter()
router.register('selection', views.AdsSelectionViewSet)

urlpatterns = [
    path('', views.index),
    path('ad/', views.AdListCreateView.as_view()),
    path('ad/<int:pk>/', views.AdDetailUpdateDeleteView.as_view()),
    path('cat/', views.CatlListView.as_view()),
    path('cat/<int:pk>/', views.CatDetailView.as_view()),
    path('cat/create/', views.CatCreateView.as_view()),
    path('cat/<int:pk>/update/', views.CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', views.CatDeleteView.as_view()),
]

urlpatterns += router.urls
