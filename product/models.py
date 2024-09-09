from django.db import models
from shop.models import Shop
from user.models import User
from django.utils.text import slugify


# Create your models here.


class Brands(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='gallery/logos')
    web_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/categories')
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(default=0, max_digits=200, decimal_places=2)
    off = models.DecimalField(default=0, max_digits=200, decimal_places=2)
    product_stock = models.IntegerField(default=1)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    brands = models.ForeignKey(Brands, on_delete=models.SET_NULL, null=True, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    feature = models.ForeignKey('CategoryFeature', on_delete=models.CASCADE, related_name='features')
    feature_value = models.CharField(max_length=200)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.feature} : {self.feature_value} for {self.product.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.feature)


class CategoryFeature(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='features')
    slug = models.SlugField(max_length=200, blank=True, null=True)
    feature_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.feature_name} for {self.category.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.feature_name)
        super().save(*args, **kwargs)


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'comment by {self.user} on {self.product}'


class ProductTag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.tag} for {self.product}'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery/products')


class ProductLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
    action = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.action} for {self.product}'


class Color(models.Model):
    color_name = models.CharField(max_length=200)
    color_code = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.color_name} - {self.color_code}'


class Size(models.Model):
    size_name = models.CharField(max_length=200)

    def __str__(self):
        return self.size_name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.ImageField(default=0)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} - {self.color.color_name} - {self.size.size_name}'
