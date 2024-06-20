
from decimal import Decimal
from store.models import Product


class Basket:
    def __init__ (self, request):
        self.session = request.session
        self.copy_basket = {}
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
    
    def update (self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.basket:
            self.basket[product_id]["quantity"] += int(quantity)
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
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
        
    def display (self, product_id):
        product_total_price = int
        if str(product_id) in self.basket:
            product_total_price = self.basket[str(product_id)]['quantity'] * Decimal(self.basket[str(product_id)]['price']) 
        return {"totalprice": self.get_total_price(), "basket_quantity": self.__len__(), "product_total_price": product_total_price}        
    def save (self):
        self.session.modified = True 