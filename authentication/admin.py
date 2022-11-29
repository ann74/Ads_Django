from django.contrib import admin

from authentication.models import User, Location


class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'role']
    list_display_links = ['username']
    search_fields = ['username']


admin.site.register(User, UsersAdmin)
admin.site.register(Location)
