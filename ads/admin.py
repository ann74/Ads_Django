from django.contrib import admin

from ads.models import Ads, Categories, AdsSelection


class AdsAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'price', 'is_published']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(Ads, AdsAdmin)
admin.site.register(Categories)
admin.site.register(AdsSelection)
