from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import User


# Определим описание для встраивания в админку
class ProfileInlined(admin.TabularInline):
    model = User
    can_delete = False


# Определим новый вид UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInlined,)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

# Перерегистрируем UserAdmin
# Это позволит использовать админку с дополнительными полями вместо штатной
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
