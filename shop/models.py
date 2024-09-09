from django.db import models
from user.models import User


# Create your models here.


class Shop(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Shop')
    description = models.TextField()
    phone = models.CharField(max_length=11)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} is the manage of {self.name}'

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['-updated_at']),
        ]
        verbose_name = 'Shop'
        verbose_name_plural = 'Shops'


class ShopWallet(models.Model):
    shop = models.OneToOneField(Shop, related_name='wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=200)

    def __str__(self):
        return f'wallet of {self.shop.name}'

    class Meta:
        ordering = ['amount']
        indexes = [
            models.Index(fields=['-amount'])
        ]


class ShopWalletLog(models.Model):
    wallet = models.ForeignKey(ShopWallet, related_name='log', on_delete=models.CASCADE)
    transactions_time = models.DateTimeField(auto_now_add=True)
    transactions_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'transaction {self.transactions_time} - {self.transactions_type} for {self.wallet}'

    class Meta:
        ordering = ['-transactions_time']

        verbose_name = "shop wallet log"
        verbose_name_plural = "shop wallet logs"


class ShopGallery(models.Model):
    image = models.ImageField(upload_to='gallery/shop')
    title = models.CharField(max_length=200, blank=True, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.title} for {self.shop.name}'
