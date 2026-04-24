from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    interest_stocks = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.username