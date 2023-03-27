from django.contrib import admin

from .models import User
from reviews.models import (Title, Category, Genre,
                            GenreTitle, Comment, Review)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'role')
    search_fields = ('username', 'role',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
