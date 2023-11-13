import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils import timezone
from django.utils.html import format_html
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, send_mail, UserManager
from django.contrib import admin

from thumbnails.fields import ImageField


# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
#         """
#         Creates and saves a User with given username, email and password.
#         """
#         now = timezone.now()
#         if not username:
#             raise ValueError('The given username must be set')
#         username = str(username).lower()
#         email = self.normalize_email(email)
#         user = self.model(username=username, email=email,
#                           is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now,
#                           date_joined=now, **extra_fields)
#         if not extra_fields.get('no_password'):
#             user.set_password(password)
#
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, username=None, email=None, phone_number=None, password=None, **extra_fields):
#         if username is None:
#             if email:
#                 username = email.split('@', 1)[0]
#             if phone_number:
#                 username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
#             while User.objects.filter(username=username).exists():
#                 username += str(random.randint(10, 99))
#
#         return self._create_user(username, email, password, False, False, **extra_fields)
#
#     def create_superuser(self, username, email, password, **extra_fields):
#         return self._create_user(username, email, password, True, True, **extra_fields)
#
#     def get_by_phone_number(self, phone_number):
#         return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with admin-compliant permissions.

    Username Password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=32, unique=True, help_text=_('Required. 32 characters or '
                                                                                       'fewer starting with a '
                                                                                       'Lowercase letter. @/./+/-/_ '
                                                                                       'only.'),
                                validators=[
                                    validators.RegexValidator(r'^[a-z][a-z0-9_\.]+$',
                                                              _('Enter a valid username. '
                                                                'This value must contain only Lowercase letter, '
                                                                'numbers and @/./+/-/_ characters.'),
                                                              'invalid'),
                                ],
                                error_messages={
                                    'unique': _("A user with this username already exists."),
                                }
                                )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(_('phone number'), null=True, blank=True, unique=True,
                                          validators=[
                                              validators.RegexValidator(r'^989[0-3,9]\d{8}$',
                                                                        'Enter a valid mobile number.', 'invalid'),
                                          ],
                                          error_messages={
                                              'unique': _("A user with this phone number already exists."),
                                          }
                                          )
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as active. '
                                                'Unselect this instead of deleting accounts.'))
    avatar = ImageField(_('avatar'), upload_to='User/', blank=True, null=True, pregenerated_sizes=['small'])
    nick_name = models.CharField(_('nick name'), max_length=150, blank=True)
    gender = models.BooleanField(_('gender'), help_text=_('female is No, male is Yes, Unknown is unset'), null=True,
                                 blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(_('last seen date'), null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @admin.display(description='avatar')
    def display_avatar(self):
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

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    @classmethod
    def get_active_users(cls):
        """
        Returns all users that are active.
        """
        return cls.objects.filter(is_active=True)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_logged_in_user(self):
        """
        Returns True if it has actually logged in with valid credentials.
        """
        return self.phone_number is not None or self.email is not None

    def get_nickname(self):
        return self.nick_name if self.nick_name else self.username

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == "":
            self.email = None
        super().save(*args, **kwargs)


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android'),
    )

    user = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUID'), default=uuid.uuid4)
    last_login = models.DateTimeField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(_('device os'), max_length=20, blank=True)
    device_model = models.CharField(_('device model'), max_length=20, blank=True)
    app_version = models.CharField(_('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')

    def save(self, *args, **kwargs):
        if not self.device_uuid:
            self.device_uuid = uuid.uuid4()
        super().save(*args, **kwargs)


class Province(models.Model):
    name = models.CharField(max_length=50)
    Description = models.TextField(blank=True, null=True)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def make_valid(queryset):
        queryset.filter(is_valid=False).update(is_valid=True)

    @staticmethod
    def make_invalid(queryset):
        queryset.filter(is_valid=True).update(is_valid=False)

    def __str__(self):
        return self.name
