from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import User, Province, Device

from import_export.admin import ImportExportModelAdmin


@admin.register(Province)
class ProvinceAdminInline(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_at', 'modified_at')
    fieldsets = (
        (_('Province Info'), {'fields': ('name', 'Description', 'is_valid')}),
        (_('Important Dates'), {'fields': ('created_at', 'modified_at')}),
    )
    list_display = ('id', 'name', 'is_valid', 'modified_at')
    list_display_links = ('id', 'name')
    list_filter = ('is_valid',)
    list_per_page = 15
    ordering = ('name',)
    search_fields = ('id', 'name')
    date_hierarchy = 'modified_at'
    actions = ('make_valid', 'make_invalid')
    model = Province
    extra = 0
    search_help_text = _('Search by id or name')

    @admin.action(description='Validate selected Provinces')
    def make_valid(self, request, queryset):
        enabled_count = len(queryset.filter(is_valid=False))
        if enabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{enabled_count} of the invalid Provinces made Validated.')

            Province.make_valid(queryset)

    @admin.action(description='Invalidate selected Provinces')
    def make_invalid(self, request, queryset):
        disabled_count = len(queryset.filter(is_valid=True))
        if disabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{disabled_count} of the valid Provinces made Invalidated.')

            Province.make_invalid(queryset)


class DeviceInline(admin.StackedInline):
    model = Device
    fields = ('device_uuid', 'device_type', 'device_os', 'device_model', 'app_version', 'last_login')
    verbose_name_plural = 'Devices'
    extra = 0


@admin.register(User)
class MyUserAdmin(ImportExportModelAdmin, UserAdmin):
    inlines = (DeviceInline,)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal Info'), {'fields': (('first_name', 'last_name'), 'gender', 'phone_number', 'email')}),
        (_('Profile'), {'fields': ('nick_name', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('username', 'phone_number', 'password1', 'password2'), }),
    )
    list_display = ('id', 'username', 'nick_name', 'gender', 'display_avatar', 'phone_number', 'email',
                    'is_staff', 'is_active', 'date_joined', 'last_seen')
    list_display_links = ('id', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'gender')
    list_per_page = 15
    ordering = ('id',)
    search_fields = ('id', 'username', 'first_name', 'last_name', 'nick_name', 'phone_number', 'email')
    date_hierarchy = 'last_login'
    save_on_top = True
    search_help_text = _('Search by id, username, nick name, phone number or email')

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
