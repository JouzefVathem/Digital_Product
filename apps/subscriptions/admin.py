from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Package, Subscription


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'sku', 'is_enable', 'price', 'duration')
    actions = ('make_enable', 'make_disable')

    def make_enable(self, request, queryset):
        Package.make_enable(queryset)

    make_enable.short_description = "Enable selected Packages"

    def make_disable(self, request, queryset):
        Package.make_disable(queryset)

    make_disable.short_description = "Disable selected Packages"

    # def dt(self):
    #     queryset = self.objects.filter()
    #     self.make_enable(queryset)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'created_time', 'expire_time')
