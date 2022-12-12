from django.contrib import admin
from user.models import UserModel


class Users(admin.ModelAdmin):
    list_display = ('id', 'username')
    list_display_links = ('id', )
    search_fields = ('username',)
    list_per_page = 20


admin.site.register(UserModel, Users)
