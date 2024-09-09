from django.db import models
from user.models import User
from django.utils.text import slugify

# Create your models here.


class BlogCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(max_length=200,  null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} for {self.author.username}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/blog')
    title = models.CharField(max_length=200, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='gallery')

    def __str__(self):
        return self.title if self.title else f'image {self.id} for {self.blog.title}'


class Tags(models.Model):
    name = models.CharField(max_length=200)
    blogs = models.ManyToManyField(Blog, related_name='tags')
    # چون هر مدل شاید چند تگ داشته باشه و هر تگ میتونه برای چند مدل باشه
    slug = models.SlugField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'tag: {self.name} at {self.created}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogComment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    comment = models.TextField()
    whiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.whiter} at {self.created}'
