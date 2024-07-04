from decimal import Decimal
from store.models import Product
from django.conf import settings

class Basket:
    def __init__ (self, request):
        self.session = request.session
        self.copy_basket = {}
        basket = self.session.get(settings.BASKET_SESSION_ID) 
    
        if settings.BASKET_SESSION_ID not in self.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
            
        self.basket = basket 
        
        if basket is not None:
            product_ids = basket.keys()
            products = Product.objects.filter(id__in = product_ids) 
        
            for product in products:
                if not product.is_active:
                    self.delete(product.id)
        
        
    def add (self, product, product_quantity):
        product_id = str(product.id)
        if product_id in self.basket:    
            self.basket[product_id]["quantity"] += product_quantity
        else:    
            self.basket[product_id] = {"price": str(product.regular_price), "quantity": int(product_quantity)} 
            
        self.save()
    
    def update (self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]["quantity"] = int(quantity)
        self.save()
        
    def __len__ (self): 
        return sum(item['quantity'] for item in self.basket.values())   
    
    def __iter__ (self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in = product_ids) 
        basket = self.basket.copy() 
        for product in products:  
            basket[str(product.id)]['product'] = product  
            
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['product_total_price'] = item['price'] * item['quantity']  
            yield item  
    
    def delete(self, product_id): 
        if str(product_id) in self.basket:
            del self.basket[str(product_id)]
            self.save()
            
    def get_total_price(self):
        subtotal = sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
        shipping = 0 if subtotal == 0 else 11.50
        return subtotal + Decimal(shipping)
        
    def display (self, product_id):
        product_total_price = int
        if str(product_id) in self.basket:
            product_total_price = self.basket[str(product_id)]['quantity'] * Decimal(self.basket[str(product_id)]['price']) 
        return {"totalprice": self.get_total_price(), "basket_quantity": self.__len__(), "product_total_price": product_total_price}        

    def save (self):
        self.session.modified = True 
        
    def clear(self, product_id):
        self.delete(product_id)
        self.save()    