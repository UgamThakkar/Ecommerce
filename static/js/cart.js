var updateBtns = document.getElementsByClassName('update-cart') /*we have a for loop in our store.html where for each product add to cart button is displayed so this variable updateBtns
gets all the buttons displayed for all the products on our home page by the class name we have given it update-cart(update-cart is class name giuen by us everything before it in store.html is bootstrap 5 class names*/
for(var i=0; i<updateBtns.length; i++){ /*now here what is happening is that we are looping through the all the buttons that are displayed for the product on our store.html
    and then we are waiting for an event i.e. click as soon as customer clicks the button i.e. add to cart button of some product for the first time, 
    we take the id of the product that we have defined in our database and then we print it out on the console and add to cart means that add the item to the cart right
    so action here is to add and we print that out too.*/
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user)
        if (user=== 'AnonymousUser'){
            console.log("not logged in")
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)

        }
    })
}

//this function will update the value of cart for anonymous user
function addCookieItem(productId, action){
    console.log("user is not logged in")
    if (action =='add'){ //checks if the user clicked on add to cart button 
        if(cart[productId] == undefined) { //checks that our cart has a productid or not and if not that it will create one
            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action =='remove'){
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0){
            console.log('remove item')
            delete cart[productId]
        }
    }
    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()//reloads our website
}



//this function will update the value of the cart for authenticated user
function updateUserOrder(productId, action){
    console.log('user is logged in sending data')  /*whenever we are using post method in django with fetch api or we need to post or send data to the backend then we need the csrf token for security mechanisms 
                                                     without that it wont work*/ 
    var url = '/update_item/' //this is the url where we want to send/post our data
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:' , data)
        location.reload()
    })
}