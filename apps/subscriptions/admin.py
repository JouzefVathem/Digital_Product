from django.contrib import admin
from django.contrib import messages

from .models import Package, Subscription


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo', 'sku', 'is_enable', 'price', 'duration', 'created_time', 'updated_time')
    ordering = ('id', )
    actions = ('make_enable', 'make_disable')

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

    make_disable.short_description = "Disable selected Packages"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'created_time', 'expire_time')
    ordering = ('expire_time',)
