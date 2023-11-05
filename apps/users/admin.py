from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Province, UserProfile, Device


@admin.register(Province)
class ProvinceAdminInline(admin.ModelAdmin):
    model = Province
    list_display = ('id', 'name', 'is_valid')
    ordering = ('name',)
    fields = ('name', 'is_valid')
    extra = 0


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('id', 'nick_name', 'display_avatar', 'gender', 'province')
    verbose_name_plural = 'User Profile'
    ordering = ('id',)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fields = ('nick_name', 'avatar', 'birthday', 'gender')
    verbose_name_plural = 'User Profile'
    inlines = (ProvinceAdminInline,)


class DeviceInline(admin.StackedInline):
    model = Device
    fields = ('device_uuid', 'last_login', 'device_type', 'device_os', 'device_model', 'app_version')
    verbose_name_plural = 'Device'
    extra = 0


@admin.register(User)
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
    list_display = ('id', 'username', 'phone_number', 'email', 'is_staff', 'is_active')
    search_fields = ('username__exact',)
    ordering = ('id',)
    inlines = (UserProfileInline, DeviceInline)

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
