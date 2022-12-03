from rest_framework import permissions

from ads.models import AdsSelection
from authentication.models import User


class AdUpdateDeletePermission(permissions.BasePermission):
    message = 'Update an delete ad can only author or moderator or admin'

    def has_permission(self, request, view):
        if request.user.role in ('moderator', 'admin') or\
                request.user == AdsSelection.objects.get(id=view.kwargs['pk']).author:
            return True
        return False

class SelectionUpdateDeletePermission(permissions.BasePermission):
    message = 'Update an delete slection can only owner'

    def has_permission(self, request, view):
        if request.user == AdsSelection.objects.get(id=view.kwargs['pk']).owner:
            return True
        return False
