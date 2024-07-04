from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
from django.utils.text import slugify


class Article(models.Model):

    title = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    image = models.ImageField(blank=True)
    date = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=50, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_pk': self.pk})
    

class Categories(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
    

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now=True)
