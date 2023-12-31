from django.contrib import admin

from .models import Gateway, Payment


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_enable')
    actions = ('make_enable', 'make_disable')

    def make_enable(self, request, queryset):
        Gateway.make_enable(queryset)

    make_enable.short_description = "Enable selected Gateways"

    def make_disable(self, request, queryset):
        Gateway.make_disable(queryset)

    make_disable.short_description = "Disable selected Gateways"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'gateway', 'price', 'status', 'phone_number', 'created_time')
    list_filter = ('status', 'gateway', 'package')
    search_fields = ('user_username', 'phone_number')
