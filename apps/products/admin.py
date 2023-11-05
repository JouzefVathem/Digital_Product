from django.contrib import admin
from django.contrib import messages

from import_export.admin import ImportExportModelAdmin

from .models import Category, Product, File


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent', 'title', 'photo', 'is_enable', 'created_time', 'updated_time')
    ordering = ('id',)
    list_filter = ('parent', 'is_enable')
    search_fields = ('title',)
    actions = ('make_enable', 'make_disable')
    verbose_name_plural = 'Categories'

    @admin.action(description='Enable selected Categories')
    def make_enable(self, request, queryset):
        enabled_count = len(queryset.filter(is_enable=False))
        if enabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{enabled_count} of the disable Categories enabled.')

            Category.make_enable(queryset)

    @admin.action(description='Disable selected Categories')
    def make_disable(self, request, queryset):
        disabled_count = len(queryset.filter(is_enable=True))
        if disabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{disabled_count} of the enable Categories disabled.')

            Category.make_disable(queryset)


class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ('title', 'file_type', 'file', 'is_enable')
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'photo', 'is_enable', 'created_time', 'updated_time')
    ordering = ('id',)
    list_filter = ('is_enable',)
    search_fields = ('title',)
    filter_horizontal = ('categories',)
    inlines = (FileInlineAdmin,)
    actions = ('make_enable', 'make_disable')
    verbose_name_plural = 'Products'

    @admin.action(description='Enable selected Products')
    def make_enable(self, request, queryset):
        enabled_count = len(queryset.filter(is_enable=False))
        # query_count = len(queryset)
        # if enabled_count != 0 and enabled_count == query_count:
        if enabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{enabled_count} of the disable products enabled.')

            Product.make_enable(queryset)

        # elif enabled_count != query_count:
        #     if enabled_count != 0:
        #         messages.add_message(request, messages.SUCCESS,
        #                              f'{enabled_count} of the disable products enabled.')
        #     messages.add_message(request, messages.INFO,
        #                          f'{query_count - enabled_count} of the selected products is already enable.')
        #
        #     Product.make_enable(queryset)

    @admin.action(description='Disable selected Products')
    def make_disable(self, request, queryset):
        disabled_count = len(queryset.filter(is_enable=True))
        # query_count = len(queryset)
        # if disabled_count != 0 and disabled_count == query_count:
        if disabled_count != 0:
            messages.add_message(request, messages.SUCCESS,
                                 f'{disabled_count} of the enable products disabled.')

            Product.make_disable(queryset)

        # elif disabled_count != query_count:
        #     if disabled_count != 0:
        #         messages.add_message(request, messages.SUCCESS,
        #                              f'{disabled_count} of the enable products disabled.')
        #     messages.add_message(request, messages.INFO,
        #                          f'{query_count - disabled_count} of the selected products is already disable.')
        #
        #     Product.make_disable(queryset)

