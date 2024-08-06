from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import time


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, verifyToken=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), verifyToken=verifyToken)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    verifyToken = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class ShortenedLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to user
    original_url = models.URLField()
    short_url = models.URLField()
    custom_alias = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.custom_alias


class Clicks(models.Model):
    url = models.ForeignKey(
        ShortenedLink, on_delete=models.CASCADE
    )  # Link to shortened link
    clicked_at = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=100)  # Device type (e.g., desktop, mobile)
    browser = models.CharField(max_length=100)  # Browser name
    country = models.CharField(max_length=100)  # Country code
    owner_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.country)


class forgotTokens(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    forgotToken = models.CharField(max_length=100)
    expire_at = models.IntegerField(default=time.time() + 1800)
