from django.db import models
from user.models import User
from product.models import Stock
# Create your models here.


class Status(models.Model):
    choices = (
        ('تایید سفارش', 'تایید سفارش'),
        ('در انتظار پرداخت', 'در انتظار پرداخت'),
        ('رد شده', 'رد شده')
    )

    name = models.CharField(max_length=30, choices=choices)

    def __str__(self):
        return self.name


class Copen(models.Model):
    copen_code = models.CharField(max_length=200)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    validity = models.DateTimeField()
    until = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.copen_code} until {self.until}'


class GatewayPayment(models.Model):
    name = models.CharField(max_length=200)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + self.amount


class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice')
    copen = models.OneToOneField(Copen, on_delete=models.CASCADE, related_name='invoice') # برای اینکه به هر فاکتور
    # بتوانند یک کوپن تخفیف بزنند
    status = models.OneToOneField(Status, on_delete=models.CASCADE, related_name='invoice')
    total_price =    models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"invoice id  {self.id} - {self.user.username}"


class PaymentType(models.Model):
    name = models.CharField(max_length=200)
    invoice = models.ForeignKey(Invoice, related_name='types', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(default=0)


class InvoiceLog(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='logs', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log {self.id} - Invoice {self.invoice.id}"