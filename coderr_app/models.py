from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Offer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=255)
    image = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    # min_price                 --> wird im Serializer als SerializerMethodField berechnet
    # min_delivery_time         --> wird im Serializer als SerializerMethodField berechnet
    # user_details:             --> ???

    def __str__(self):
        return self.title


class OfferDetail(models.Model):
    TYPE_CHOICES = [
        ('BASIC', 'basic'),
        ('STANDARD', 'standard'),
        ('PREMIUM', 'premium')
    ]

    title = models.CharField(max_length=100)
    revision = models.IntegerField(default=-1, validators=[MinValueValidator(-1)])
    delivery_time_in_days = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    offer_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='BASIC')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')  # jedes OfferDetail gehört genau zu einem Offer! Aber ein Offer kann mehrere OfferDetails haben!
    # features  --> wird im Serializer als ListField deklariert!

    def __str__(self):
        return self.title
