from django.db import models
from product.models import Product


# Create your models here.


class Sliders(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sliders')
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.product.name} - active: {self.is_active}'


class Banners(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='banners')
    name = models.CharField(max_length=200)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/banners')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - is active : {self.is_active}'


class Section(models.Model):
    sliders = models.ForeignKey(Sliders, related_name='sections', on_delete=models.CASCADE)
    banners = models.ForeignKey(Banners, related_name='sections', on_delete=models.CASCADE)
    sliders_image_item = models.ForeignKey('SliderImageItem', related_name='sections', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class SliderImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/slider')
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class SliderImageItem(models.Model):
    slider_image = models.ForeignKey(SliderImage, on_delete=models.CASCADE, related_name='images')
    ordering = models.ImageField(default=0)