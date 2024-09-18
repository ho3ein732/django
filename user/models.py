from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('ایمیل را لطفا وارد کنید')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is False:
            raise ValueError('erorr')
        if extra_fields.get('error') is False:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    date_of_birth = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    Photo = models.ImageField(upload_to='gallery/user-photo', blank=True, null=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  #

    objects = UserManager()


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
