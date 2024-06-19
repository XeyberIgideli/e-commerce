
from decimal import Decimal
from store.models import Product


class Basket:
    def __init__ (self, request):
        self.session = request.session
        basket = self.session.get('bkey')
        
        if "bkey" not in self.session:
            basket = self.session['bkey'] = {}
        self.basket = basket 
        
        
    def add (self, product, product_quantity):
        product_id = str(product.id)
        if product_id in self.basket:    
            self.basket[product_id]["quantity"] += product_quantity
        else:    
            self.basket[product_id] = {"price": str(product.price), "quantity": int(product_quantity)}
            
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
            item['total_price'] = item['price'] * item['quantity']
            yield item  
    def save (self):
        self.session.modified = True 