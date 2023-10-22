import logging

from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from thumbnails.fields import ImageField


class Category(models.Model):
    parent = models.ForeignKey('self', verbose_name=_('parent'), blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(_('Name'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = ImageField(_('avatar'), upload_to='categories/', blank=True)
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    @staticmethod
    def make_enable(queryset):
        queryset.filter(is_enable=False)
        queryset.update(is_enable=True)

    @staticmethod
    def make_disable(queryset):
        queryset.filter(is_enable=True)
        queryset.update(is_enable=False)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(_('title'), max_length=50)
    description = models.TextField(_('description'), blank=True)
    avatar = ImageField(_('avatar'), upload_to='products/', blank=True, null=True, pregenerated_sizes=['small'])
    is_enable = models.BooleanField(_('is enable'), default=True)
    categories = models.ManyToManyField('Category', verbose_name=_('categories'), blank=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'products'
        verbose_name = _('product')
        verbose_name_plural = _('Products')

    # @property
    # def photo(self):
    #     return format_html('<a href={} target="_blank"><img src={} width="50" style="border-radius:2rem" /></a>'
    #                        .format(self.avatar.thumbnails.small.url, self.avatar.thumbnails.small.url))

    # @property
    @admin.display(description='avatar')
    def photo(self):
        the_small_url = self.avatar.thumbnails.small.url
        # logger = logging.getLogger('avatar thumbnails small url')
        # handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        # logger.info(self.avatar.thumbnails.small.url)
        return format_html(
            f'<a href="{self.avatar.url}" target="_blank"> '
            f'<img src="{the_small_url}" width=50 style="border-radius:2rem; object-fit:contain"/> </a>')

    @staticmethod
    def make_enable(queryset):
        queryset.filter(is_enable=False)
        queryset.update(is_enable=True)

    @staticmethod
    def make_disable(queryset):
        queryset.filter(is_enable=True)
        queryset.update(is_enable=False)

    def __str__(self):
        return self.title


class File(models.Model):
    FILE_AUDIO = 1
    FILE_VIDEO = 2
    FILE_PDF = 3
    FILE_TYPES = (
        (FILE_AUDIO, _('Audio')),
        (FILE_VIDEO, _('Video')),
        (FILE_PDF, _('PDF')),
    )

    product = models.ForeignKey('Product', verbose_name=_('product'), related_name='files', on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=50)
    file_type = models.PositiveSmallIntegerField(_('file type'), choices=FILE_TYPES)
    file = models.FileField(_('file'), upload_to='files/%Y/%m/%d/')
    is_enable = models.BooleanField(_('is enable'), default=True)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)

    class Meta:
        db_table = 'files'
        verbose_name = _('file')
        verbose_name_plural = _('files')

    def __str__(self):
        return self.title
