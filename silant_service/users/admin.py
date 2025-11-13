from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

class GroupAdmin(BaseGroupAdmin):
    list_display = ('name',)
    filter_horizontal = ('permissions',)

admin.site.register(Group, GroupAdmin)

User = get_user_model()

if User in admin.site._registry:
    try:
        admin.site.unregister(User)
    except admin.sites.NotRegistered:
        pass


class SilantUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_role')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('get_role',)

    def get_role(self, obj):
        return obj.get_role()
    get_role.short_description = 'Роль'

admin.site.register(User, SilantUserAdmin) # Регистрируем кастомную админку