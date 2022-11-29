from django.urls import path
from rest_framework import routers

from authentication import views

router = routers.SimpleRouter()
router.register('location', views.LocationViewSet)

urlpatterns = [
    path('', views.UserListCreateView.as_view()),
    path('<int:pk>/', views.UserDetailUpdateDeleteView.as_view()),
    path('Z/', views.UserAdsDetailView.as_view()),
]

urlpatterns += router.urls
