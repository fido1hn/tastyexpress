from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to="customer/avatars/", blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payement_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last4 = models.CharField(max_length=255, blank=True)

    def __str__(self) -> str:
        return self.user.get_full_name()
