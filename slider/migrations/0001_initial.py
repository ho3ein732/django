# Generated by Django 4.2.6 on 2024-09-11 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='gallery/banners')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banners', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='SliderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='gallery/slider')),
                ('link', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sliders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sliders', to='product.product')),
            ],
        ),
        migrations.CreateModel(
            name='SliderImageItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordering', models.ImageField(default=0, upload_to='')),
                ('slider_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='slider.sliderimage')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('banners', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='slider.banners')),
                ('sliders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='slider.sliders')),
                ('sliders_image_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='slider.sliderimageitem')),
            ],
        ),
    ]
