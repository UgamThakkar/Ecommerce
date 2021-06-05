from django.shortcuts import render
from .models import Product, Order, OrderItem, Customer, ShippingAddress
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .utils import cookieCart, cartData,guestOrder
from .filters import ProductFilter


#get_or_create explained on line 73 to 76
# Create your views here.
#in order to use any of the attribute/variables/properties of the views created here we first need to pass them to the context dict in order to use them in our html pages and elsewhere. 
def store(request):

    data = cartData(request)
    cartItems = data['cartItems']   
            
    #so this right here is going to get all our products and then pass them into our context dict to render them on our store.html
    products = Product.objects.all() #to render the defined products in the database we need to first import all models from models.py and then we can render them on our page.

    myFilter = ProductFilter(request.GET, queryset = products) 
    products = myFilter.qs
    context = {'products':products,'cartItems':cartItems, 'myFilter':myFilter}
    return render(request, 'store/store.html', context)

# def get_context_data(self, *args, **kwargs):

#     search_input = self.reques.GET.get('search-area')
#     products = Product.objects.all()
    
#     if search_input:
#         context['products'] = context['products'].filter(name__icontains=search_input)

    

   



def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']   
    order = data['order']   
    items = data['items']
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset = products)
    products = myFilter.qs
            
            
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems,
        'myFilter':myFilter,
    }
    return render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']   
    order = data['order']   
    items = data['items']
            

    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'store/checkout.html', context)



def updateItem(request): 
    #logic for change in the quantity of the products added to the cart on the cart.html page
    #this will update the cart when the user clicks the add to cart and will return a json response back.

    data = json.loads(request.body)  #the updateitem url in cart.js will post the data to this function or send the data from the frontend to this url to the backend

    productId = data['productId']

    action = data['action']

    print('Action:', action)
    print('productid:', productId)

    customer = request.user.customer #this gets the logged in customer 
    product = Product.objects.get(id=productId) #this gets the id of the product we want to add to the cart
    order, created = Order.objects.get_or_create(customer=customer, complete=False)   #get or create function first tries to obtain the objects created if not objects found then it creates an object.
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    #explanation of get_create is given by dennis in his vid Adding Items to Cart without Registering a Account | eCommerce Website
    #time frame 11:57 or here it is.
    # in the statement order, created = Order.objects.get_or_create(customer=customer, complete=False) what get_or_create does here that   
    #if we dont have an order with the attribute/prop of customer=customer and com=false than create it and if we do have the order with the property of cust=cust then find it and set the value of our order var to that.


    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()    

    return JsonResponse('Item added', safe=False)


#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body) #parse the data
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

         
    else:
        customer, order = guestOrder(request, data)
        
        

    total = float(data['form']['total']) #obtains the total price of products from frontend
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order=order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],

        )

    return JsonResponse('Payment complete', safe=False)

 
def dashboard(request):
    customer = Customer.objects.all()
    context = {
        'customer':customer,
    }
    return render(request, 'store/dashboard.html', context)

