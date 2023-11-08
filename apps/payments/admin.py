from django.contrib import admin
from django.contrib import messages

from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Gateway, Payment


@admin.register(Gateway)
class GatewayAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('title', 'is_enable')}),
        (_('Create, Update'), {'classes': ('wide',), 'fields': ('created_time', 'updated_time')}),
        (_('Optional info'), {'classes': ('wide',), 'fields': ('description', 'avatar')}),
    )
    ordering = ('title',)
    list_display = ('id', 'title', 'display_avatar', 'is_enable', 'updated_time')
    list_display_links = ('id', 'title')
    list_filter = ('is_enable',)
    list_per_page = 15
    search_fields = ('id', 'title')
    date_hierarchy = 'updated_time'
    actions = ('make_enable', 'make_disable')
    search_help_text = _('Search by id or title')
    verbose_name_plural = 'Gateways'

    @admin.action(description='Enable selected Gateways')
    def make_enable(self, request, queryset):
        enabled_count = len(queryset.filter(is_enable=False))
        if enabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{enabled_count} of the disable Gateways enabled.')

            Gateway.make_enable(queryset)

    @admin.action(description='Disable selected Gateways')
    def make_disable(self, request, queryset):
        disabled_count = len(queryset.filter(is_enable=True))
        if disabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{disabled_count} of the enable Gateways disabled.')

            Gateway.make_disable(queryset)


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        (_('Payment Info'), {'classes': ('wide',), 'fields': ('user', 'package', 'gateway')}),
        (_('Payment Info'), {'classes': ('wide',), 'fields': ('created_time', 'updated_time')}),
        (_('User Auth'), {'classes': ('wide',), 'fields': ('device_uuid', 'token', 'phone_number', 'consumed_code')}),
    )
    ordering = ('-updated_time',)
    list_display = (
        'id', 'updated_time', 'user', 'package', 'gateway', 'price', 'status', 'phone_number', 'created_time')
    list_display_links = ('id', 'updated_time')
    list_select_related = ('user', 'package', 'gateway')
    list_filter = ('status', 'gateway', 'package')
    list_per_page = 15
    search_fields = ('id', 'user_username', 'phone_number', 'price')
    date_hierarchy = 'updated_time'
    verbose_name_plural = 'Payments'
    search_help_text = _('Search by id, user, phone number or price')
