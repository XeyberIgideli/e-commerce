from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)

class Category (models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'   
        verbose_name_plural = 'categories'  
        
    def get_absolute_url(self):
        return reverse("store:category_detail", args=[self.slug])    
    
    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Product (models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')  
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True) 
    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])
    
    def save(self, *args, **kwargs): 
        if self.slug:
            self.slug = slugify(kwargs.pop('slug', self.slug))
        else:
            self.slug = slugify(self.title)
        return super(Product, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title 