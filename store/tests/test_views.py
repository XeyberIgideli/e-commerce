from django.test import TestCase 
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Category, Product

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')      
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                               slug='django-beginners', price='20.00', image='django')
        
    def test_product_detail_url(self): 
        response = self.c.get(
            reverse('store:product_detail', args=['django-beginners']))
        self.assertEqual(response.status_code, 200)
        
    def test_url_allowed_host(self):
        response = self.c.get('', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
            