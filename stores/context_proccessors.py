from . models import Category, CartProduct,Cart

def categoryss(request):
    category = Category.objects.all()

    context = {
       'categorys': category 
    }

    return context

# def cartproductss(request):
#    cart_id = request.session.get('cart_id', None)
#    if cart_id:
#         cart_item = Cart.objects.get(id = cart_id)
#         cart_products = cart_item.cartproduct_set.all()
#         num_of_products = cart_products.count()
#    else:
#        cart_item = None

#    context = {
#        'items': num_of_products
#    }

#    return context
   