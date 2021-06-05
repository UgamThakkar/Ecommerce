from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True) #if digital=true that means we dont need to ship the item and if it is false then we need to ship it
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageURL(self): #if any of the image is not available in the database then without this function it will throw an error, so here we try to look for the image
        try:            #and if we find the correct url then we retun that url otherwise an empty string.
            url = self.image.url
        except:
            url = '' # so in case if it does not find the url for any particular image then that image will not be rendered over the prodcut but it wont cause an error on the page it will still load all other products with respective images.
        return url


   

        
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False) #it represents that if the cart is false then it is an open cart and we can continue adding items toit and if it is true tehn we neeed to create a new cart
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.transaction_id) #str(self.id)

    @property
    def shipping(self):  #logic for checking if the product is digital or not and if it is digital then we ask the user to enter the address details otherwise we simply mail them or something.
        shipping = False
        orderitems = self.orderitem_set.all() 
        for i in orderitems:
            if i.product.digital == False:  #if the item has digital = false that means it is a physical item and we need to ship it so set shipping=true
                shipping = True
        return shipping        
            

    @property
    def get_cart_total(self): #this right here will give us the total in the form of price of all the items in the cart example: if we have 3 items then the grand total of all these items will be calculated by this method and returned.
        orderitems = self.orderitem_set.all() #gets all the items ordered by the customer
        total = sum([item.get_total for item in orderitems])
        return total    

    @property
    def get_cart_items(self): #this right here will give us the total items i.e quantity or number of items in the cart.
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self): #this gives the total price of individual item example if customer selected a headphone then this will return the price of headphone along with how many headphones customer bought.
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200, null=False)
    def __str__(self):
        return self.address
 

