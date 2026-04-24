from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    STOCK_CHOICES = [
        ("SAMSUNG", "삼성전자"),
        ("SKHYNIX", "SK하이닉스"),
        ("NAVER", "네이버"),
        ("KAKAO", "카카오"),
        ("TESLA", "테슬라"),
        ("APPLE", "애플"),
        ("NVIDIA", "엔비디아"),
        ("BTC", "비트코인"),
        ("ETH", "이더리움"),
    ]

    nickname = models.CharField(max_length=50)

    interest_stocks = models.CharField(
        max_length=255,
        blank=True,
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.username