from django.contrib import admin
from django.contrib import messages

from django.utils.translation import gettext_lazy as _

from .models import Package, Subscription

from import_export.admin import ImportExportModelAdmin


@admin.register(Package)
class PackageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': (('title', 'is_enable'),)}),
        (_('Package Info'), {'classes': ('wide',), 'fields': ('description', 'avatar')}),
        (_('Optional Info'), {'classes': ('wide',), 'fields': ('sku', 'price', 'duration')}),
        (_('Create, Update'), {'fields': ('created_time', 'updated_time')}),
    )
    ordering = ('duration', )
    list_display = ('id', 'title', 'photo', 'sku', 'is_enable', 'price', 'duration', 'created_time', 'updated_time')
    list_display_links = ('id', 'title')
    list_filter = ('is_enable',)
    list_per_page = 15
    search_fields = ('id', 'title', 'user')
    date_hierarchy = 'updated_time'
    actions = ('make_enable', 'make_disable')
    verbose_name_plural = 'Packages'
    search_help_text = _('Search by id, title or user')

    @admin.action(description='Enable selected Packages')
    def make_enable(self, request, queryset):
        enabled_count = len(queryset.filter(is_enable=False))
        if enabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{enabled_count} of the disable Packages enabled.')

            Package.make_enable(queryset)

    @admin.action(description='Disable selected Packages')
    def make_disable(self, request, queryset):
        disabled_count = len(queryset.filter(is_enable=True))
        if disabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{disabled_count} of the enable Packages disabled.')

            Package.make_disable(queryset)


@admin.register(Subscription)
class SubscriptionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time',)
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': (('user', 'package'),)}),
        (_('Expire Time'), {'fields': ('created_time', 'expire_time')}),
    )
    ordering = ('expire_time',)
    list_display = ('id', 'created_time', 'expire_time', 'user', 'package')
    list_display_links = ('id', 'created_time', 'expire_time')
    list_filter = ('user', 'package')
    list_select_related = ('user', 'package')
    list_per_page = 15
    search_fields = ('id', 'user', 'package')
    date_hierarchy = 'expire_time'
    verbose_name_plural = 'Subscriptions'
    search_help_text = _('Search by id, user or package')
