from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.IntegerField(null=True, blank=True)
    Photo = models.ImageField(upload_to='gallery/user-photo', blank=True, null=True)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='address')
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    plague = models.CharField(max_length=10)  # دقیفا نمیدونم پلاک چند رقمه
    postal_code = models.CharField(max_length=11)  # اینم مطمعن نیستم

    def __str__(self):
        return f'{self.user.username} - {self.province} - {self.city}'


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    amount = models.DecimalField(max_digits=200, decimal_places=2)


class WalletLog(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='log')
    Transactions_time = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f'{self.wallet.user} - {self.amount} - {self.description}'


class ActivityReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity')
    description = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} at {self.time}'


class BlackList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='block')
    date_ad = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.user} is block'
