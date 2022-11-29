from django.urls import path

from ads import views


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
