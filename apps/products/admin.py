from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from PIL import Image, ImageDraw, ImageOps

from .models import Category, Product, File


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'title', 'is_enable', 'created_time')
    list_filter = ('parent', 'is_enable')
    search_fields = ('title',)
    actions = ('make_enable', 'make_disable')

    def make_enable(self, request, queryset):
        Category.make_enable(queryset)

    make_enable.short_description = "Enable selected Categories"

    def make_disable(self, request, queryset):
        Category.make_disable(queryset)

    make_disable.short_description = "Disable selected Categories"


class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ('title', 'file_type', 'file', 'is_enable')
    extra = 0


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('title', 'photo', 'is_enable', 'created_time')
    list_filter = ('is_enable',)
    search_fields = ('title',)
    filter_horizontal = ('categories',)
    inlines = (FileInlineAdmin,)
    actions = ('make_enable', 'make_disable')

    def make_enable(self, request, queryset):
        Product.make_enable(queryset)

    make_enable.short_description = "Enable selected Products"

    def make_disable(self, request, queryset):
        Product.make_disable(queryset)

    make_disable.short_description = "Disable selected Products"
