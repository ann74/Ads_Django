from django.contrib import admin

from ads.models import Ads, Categories, Users, Location

class AdsAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'price', 'is_published']
    list_display_links = ['name']
    search_fields = ['name']


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role']
    list_display_links = ['username']
    search_fields = ['username']


admin.site.register(Ads, AdsAdmin)
admin.site.register(Categories)
admin.site.register(Users, UsersAdmin)
admin.site.register(Location)
