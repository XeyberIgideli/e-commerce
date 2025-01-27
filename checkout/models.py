from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class DeliveryOptions (models.Model):
    
    DELIVERY_CHOICES = [
        ('STD', 'Standard Delivery'),
        ('EXP', 'Express Delivery'),
        ('SDD', 'Same Day Delivery'),
        ('NDD', 'Next Day Delivery'),
    ]
    
    name = models.CharField(verbose_name=_("delivery_name"),max_length=100, help_text = _("Required") )
    price = models.DecimalField(verbose_name=_("delivery_price"),max_digits=5, decimal_places=2, help_text = _("Maximum 999.99"))
    method = models.CharField(verbose_name=_("delivery_method"),choices=DELIVERY_CHOICES, max_length=100, default= "STD")
    delivery_time = models.CharField(verbose_name=_("delivery_time"),max_length=150, help_text = _("Required")) 
    delivery_window = models.CharField(verbose_name=_("delivery_window"),help_text=_("Required"),max_length=255)
    order = models.IntegerField(verbose_name=_("list_order"), help_text=_("Required"), default=0)
    is_active = models.BooleanField(default = True)
    
    
    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.name