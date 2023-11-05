from django.contrib import admin
from django.contrib import messages

from .models import Gateway, Payment


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'display_avatar', 'is_enable', 'updated_time')
    actions = ('make_enable', 'make_disable')
    ordering = ('id',)
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
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'package', 'gateway', 'price', 'status', 'phone_number', 'created_time', 'updated_time')
    list_filter = ('status', 'gateway', 'package')
    search_fields = ('user_username', 'phone_number')
    ordering = ('id',)
    verbose_name_plural = 'Payments'
