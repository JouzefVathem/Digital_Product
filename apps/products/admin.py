from django.contrib import admin
from django.contrib import messages

from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportModelAdmin

from .models import Category, Product, File


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('parent', 'title', 'is_enable')}),
        (_('Create, Update'), {'fields': ('created_time', 'updated_time')}),
        (_('Optional Info'), {'classes': ('wide',), 'fields': ('description', 'avatar')}),
    )
    ordering = ('id',)
    list_display = ('id', 'title', 'display_avatar', 'parent', 'is_enable', 'created_time', 'updated_time')
    list_display_links = ('id', 'title')
    list_select_related = ('parent',)
    list_filter = ('parent', 'is_enable')
    list_per_page = 15
    search_fields = ('id', 'title', 'parent')
    search_help_text = _('Search by id, name or parent')
    date_hierarchy = 'updated_time'
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
    fields = ('id', 'title', 'file_type', 'file', 'is_enable')
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    readonly_fields = ('created_time', 'updated_time')
    inlines = (FileInlineAdmin,)
    fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('title', 'user', 'is_enable', 'categories')}),
        (_('Optional info'), {'classes': ('wide',), 'fields': ('description', 'avatar')}),
        (_('Important Dates'), {'fields': ('created_time', 'updated_time')}),
    )
    filter_horizontal = ('categories',)
    list_display = ('id', 'title', 'user', 'display_avatar', 'is_enable', 'created_time', 'updated_time')
    list_display_links = ('id', 'title')
    list_select_related = ('user',)
    list_filter = ('is_enable',)
    list_per_page = 15
    ordering = ('id',)
    search_fields = ('id', 'title', 'user')
    date_hierarchy = 'updated_time'
    actions = ('make_enable', 'make_disable')
    search_help_text = _('Search by id, title or user')
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
