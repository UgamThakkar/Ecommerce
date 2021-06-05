import json
from .models import Product, Customer, Order, OrderItem, ShippingAddress

def cookieCart(request):
    #in django if we want to obtain the cookies of any variable that we set to collect the cookies for us in the browser
    #back to our backend then we use var name = request.cookies['name of var that was set to obtain cookies for us in the browser']
    try: 
        cart = json.loads(request.COOKIES['cart']) #here we get the cookies from our front end which are in string format and convert them into pyth dict
    except:
        cart = {}
    print('Cart:',cart)
    
    items=[]
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    #process for creating an order for an anonymous user is here below:
    for i in cart:


        try:  #in this try block because if the user adds some product in his cart and that product doest not exist in our database then he might face an error.

            cartItems += cart[i]['quantity'] #updates the value on the cart icon for the user that is not logged in.obtains all the items and loops through them and passess it into the cartitems variable   
            
            product = Product.objects.get(id=i)  #started the process to create the order for anonymous user. first we get the product and store it in 'product' then the total price is by calculating the quantity of the product currently in var 'product'
            
            total = (product.price * cart[i]['quantity'])
            
            order['get_cart_total'] += total #this will add the total price of our product to the overall total of our cart
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL,
                },
                'quantity': cart[i]["quantity"],
                'get_total':total

            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        
        except:
            pass

    return {'cartItems':cartItems, 'order':order, 'items':items}    


def cartData(request):
    if request.user.is_authenticated:    #checks if user is logged in or not.
        customer = request.user.customer #gets the logged in user using request.user and as we have a one to one relationship of customer and user we can obtain the customer using this way.
        order, created = Order.objects.get_or_create(customer=customer, complete=False)   #get or create function first tries to obtain the objects created if no objects are found then it creates an object.
        items = order.orderitem_set.all()  #all the child objects(here:orderitems) can be accessed using the parent object(here:order).
        cartItems = order.get_cart_items #updating the item count at the cart icon of our nav bar


    else: #cond for anonymous user.
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']   
        order = cookieData['order']   
        items = cookieData['items']
         #updating the item count at the cart icon of our nav bar
    return {'cartItems':cartItems, 'order':order, 'items':items}    


def guestOrder(request, data):
    
    print("user not logged in") 
    print("COOKIES:", request.COOKIES)   
    name = get(data['form']['name'])
    email = get(data['form']['email'])

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(

        email = email,

)
    customer.name = name
    customer.save()

#create order for the customer not logged in
    order = Order.objects.create(
        customer = customer,
        complete = False,
)

    for item in items:   
    #refers to line 32 in utils .py whole item dict and inside that product dict
    #looping through the items obtained above on line 78 
        product = Product.objects.get(id=item['product']['id'])
    #so to create and order item checkout our models.py OrderItem model there we have attributes product and order attached to the model Product and Order 
    #so to create an order we need to have those relations of product and order

        orderItem = OrderItem.objects.create(
    #for every iteration it will create and orderitem and it will refer to model OrderItem 
    # and it will attach it to the the product above in this loop and the order var above this loop because the OrderItem model needs a relationship of model Product and Order to create an orderitem
            product=product,
            order=order,
            quantity=item['quantity']
    )

    return customer, order