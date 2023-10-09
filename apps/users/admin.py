from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Province, UserProfile, Device


class ProvinceAdminInline(admin.ModelAdmin):
    model = Province
    fields = ['name']
    extra = 0


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ['nick_name', 'avatar', 'birthday', 'gender']
    verbose_name_plural = 'User Profile'
    inlines = [ProvinceAdminInline]


class DeviceInline(admin.StackedInline):
    model = Device
    fields = ['device_uuid', 'last_login', 'device_type', 'device_os', 'device_model', 'app_version']
    verbose_name_plural = 'Device'
    extra = 0


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': ('username', 'phone_number', 'password1', 'password2'),
                }),
    )
    list_display = ('username', 'phone_number', 'email', 'is_staff')
    search_fields = ('username__exact',)
    ordering = ('-id',)
    inlines = [UserProfileInline, DeviceInline]

    def get_search_results(self, request, queryset, search_term):
        queryset, may_have_duplicates = super().get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(phone_number=search_term_as_int)
        return queryset, may_have_duplicates


admin.site.unregister(Group)
admin.site.register(Province, ProvinceAdminInline)
admin.site.register(User, MyUserAdmin)
# admin.site.register(Site)
