from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import TreeForeignKey, MPTTModel
from django.utils.text import slugify 
# Create your models here.

class Category (MPTTModel):
    
    name = models.CharField(
        verbose_name= "Category Name",
        help_text= "Required and unique",
        max_length= 255,
        unique = True
    )
    slug = models.SlugField(verbose_name= "Category slug", max_length=255, unique= True)
    parent = TreeForeignKey("self", on_delete= models.CASCADE, null = True, blank = True)
    is_active = models.BooleanField(default= True)
    
    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = _("Category")    
        verbose_name_plural = _("Categories")    
        
    def get_absolute_url(self):
        return reverse("store:category_detail", args=[self.slug])  
        
    def __str__(self):
        return self.name  
      
    def save(self, *args, **kwargs):  
        self.slug = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

class ProductType (models.Model):
    name = models.CharField(verbose_name=_("Product type name"), help_text= _("Required"),max_length=255, unique = True)
    is_active = models.BooleanField(default= True)    
    
    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")
        
    def __str__(self):
        return self.name 
    
class ProductSpecification (models.Model):
    name = models.CharField(verbose_name=_("Product feature name"), help_text= _("Required"),max_length=255)
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)         
    
    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
    
    def __str__(self):
        return self.name 
    
class Product (models.Model):
    product_type = models.ForeignKey(ProductType, on_delete= models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_("Title"), help_text=_("Required"), max_length=255)
    description = models.TextField(verbose_name=_("Description"), help_text=_("Not required"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(verbose_name=_("Regular price"), help_text=_("Maximum 999.9"), max_digits=5, decimal_places=2)
    discount_price = models.DecimalField(verbose_name=_("Discount price"), help_text=_("Maximum 999.9"), max_digits=5, decimal_places=2)
    is_active = models.BooleanField(verbose_name=_("Product visibility"), help_text= _("Change product visibility"), default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable= False)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        
    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title
    
    
class ProductSpecificationValue (models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(verbose_name=_("Value"), help_text=_("Product specification value (max of 255 words)"), max_length=255)
    
    
    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")
            
    def __str__ (self):
        return self.value   
    
class ProductImage (models.Model):
          
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="product_image")        
    image = models.ImageField(verbose_name=_("Image name"), help_text=_("Please add name"), max_length=255, null= True, blank=True)
    alt_text = models.CharField(verbose_name=_("Image alt text"), help_text=_("Please add alt text for image"), max_length = 255)
    is_feature = models.BooleanField(default= False)
    created_at = models.DateTimeField(auto_now_add=True, editable= False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save (self,*args, **kwargs): 
        if self.is_feature:
           t =  ProductImage.objects.filter(product = self.product, is_feature = True) 
           for p in t:
               print(p.alt_text)
           ProductImage.objects.filter(product = self.product, is_feature = True).update(is_feature = False)
           
        super().save(*args,*kwargs)

    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
 # class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(is_active=True)

# class Category (models.Model):
#     name = models.CharField(max_length=255, db_index=True)
#     slug = models.SlugField(max_length=255, unique=True)
    
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'category'   
#         verbose_name_plural = 'categories'  
        
#     def get_absolute_url(self):
#         return reverse("store:category_detail", args=[self.slug])    
    
#     def save(self, *args, **kwargs):  
#         self.slug = slugify(self.name)
#         return super(Category, self).save(*args, **kwargs)
    
#     def __str__(self):
#         return self.name
    
# class Product (models.Model):
#     category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)  
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='product_creator')  
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255, default='admin')
#     description = models.TextField(blank=True)
#     image = models.ImageField(upload_to='images/')
#     slug = models.SlugField(max_length=255, unique=True)
#     price = models.DecimalField(max_digits=4, decimal_places=2)
#     in_stock = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True) 
    
#     class Meta:
#         verbose_name_plural = 'Products'
#         ordering = ('-created',)
    
#     def get_absolute_url(self):
#         return reverse("store:product_detail", args=[self.slug])
    
#     def save(self, *args, **kwargs) :   
#         if self.slug:
#             self.slug = slugify(kwargs.pop('slug', self.slug))
#         else:
#             self.slug = slugify(self.title)
            
#         return super(Product, self).save(*args, **kwargs)
        
#     def __str__(self):
#         return self.title 