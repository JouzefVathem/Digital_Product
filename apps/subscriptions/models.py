from django.db import models
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from thumbnails.fields import ImageField

from utils.validators import validate_sku


class Package(models.Model):
    title = models.CharField(_("title"), max_length=50)
    sku = models.CharField(_("stock keeping unit"), max_length=20,
                           help_text=_("Unique identifier for the package"), validators=[validate_sku], db_index=True)
    description = models.TextField(_("description"), blank=True)
    avatar = ImageField(_('avatar'), upload_to='Packages/', blank=True, null=True, pregenerated_sizes=['small'])
    is_enable = models.BooleanField(_("is enable"), default=True)
    price = models.PositiveIntegerField(_("price"))
    # gateways = models.ManyToManyField('payments.Gateway')
    duration = models.DurationField(_("duration"), blank=True, null=True)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        db_table = 'packages'
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

    @admin.display(description='avatar')
    def photo(self):
        try:
            original_url = self.avatar.url
            small_url = self.avatar.thumbnails.small.url

            return format_html(
                f'<a href="{original_url}" target="_blank"> <img src="{small_url}" width=50 style="border-radius:50%; '
                f'border: 3px solid gray; padding: 5px"/> </a>')

        except ValueError:
            return format_html(
                '<strong style="color: whitesmoke; padding: 5px; border-radius: 5px; '
                'background-color: #990100b5">⚠️ avatar not set !!! </strong>')

    @staticmethod
    def make_enable(queryset):
        queryset.filter(is_enable=False).update(is_enable=True)

    @staticmethod
    def make_disable(queryset):
        queryset.filter(is_enable=True).update(is_enable=False)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', related_name='%(class)s', on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name='%(class)s', on_delete=models.CASCADE)
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    expire_time = models.DateTimeField(_("expire time"), blank=True, null=True)

    class Meta:
        db_table = 'subscriptions'
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def __str__(self):
        return str(self.user.username) + ", " + str(self.package.title)
