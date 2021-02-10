from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):

    def _create_user(self, mobile_number, email, password, **extra_fields):
        """
        Create and save a user with the given mobile_number, email, and password.
        """
        if not mobile_number:
            raise ValueError('The given mobile_number must be set')
        email = self.normalize_email(email)
        user = self.model(mobile_number=mobile_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(mobile_number, email, password, **extra_fields)

    def create_superuser(self, mobile_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(mobile_number, email, password, **extra_fields)


class User(AbstractUser):
    last_name = models.NOT_PROVIDED
    username = models.NOT_PROVIDED
    mobile_number = models.CharField(verbose_name=_("Mobile Number"), max_length=128,
                                     blank=False, null=False, unique=True)
    sur_name = models.CharField(_('last name'), max_length=150, blank=True)

    USERNAME_FIELD = 'mobile_number'

    objects = CustomUserManager()
