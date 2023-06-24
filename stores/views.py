from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from . models import *
from django.core.paginator import Paginator
from django.db.models import Q

from django.contrib import messages
from . forms import CheckoutForm
from django.conf import settings


# Create your views here.
def index(request):
    sliders = Slider.objects.all()
    categorys = Category.objects.all().order_by('-created_at')[:4]
    products = Products.objects.all().order_by('-created_at')[:4]

    context = {
        'sliders' : sliders,
        'categorys': categorys,
        'products': products
    }
    return render(request, 'stores/index.html', context)


def stores(request):
    products = Products.objects.all().order_by('-created_at')
    # Paginate products
    paginator = Paginator(products,8)
    page_number = request.GET.get('page')
    page_list = paginator.get_page(page_number)
    context = {
        'products': products,
        'paginator': page_list
    }
    return render(request, 'stores/stores.html', context)

def store(request, id):
    product = Products.objects.get(id = id)

    context ={
        'product': product
    }

    return render(request, 'stores/store.html', context)

def category(request, id):
    category = Products.objects.all().filter(category = id)

    context = {
        'category': category
    }
    return render(request, 'stores/category.html', context)

def search(request):
    getkword = request.GET.get('kword')

    product = Products.objects.filter(Q(title__icontains = getkword) | Q(text__icontains = getkword) )
    context = {
        'products': product
    }
    return render(request, 'stores/search.html', context)

def add_to_cart(request, id):

    cart_product = Products.objects.get(id = id)

    cart_id = request.session.get('cart_id', None)

    if cart_id:
        cart_item = get_object_or_404(Cart, id = cart_id)

        if request.user.is_authenticated:
            cart_item.profile = request.user.profile
            cart_item.save()

        this_product_in_cart = cart_item.cartproduct_set.filter(product = cart_product)
        if this_product_in_cart.exists():
            cartproduct = this_product_in_cart.last()
            cartproduct.quantity += 1
            cartproduct.subtotal += cart_product.price
            cartproduct.save()
            cart_item.total += cart_product.price
            cart_item.save()

        else:
            cartproduct = CartProduct.objects.create(cart = cart_item, product = cart_product, quantity = 1, subtotal = cart_product.price)
            cart_item.total += cart_product.price
            cart_item.save()

    else:
        cart_item = Cart.objects.create(total = 0)
        request.session['cart_id'] = cart_item.id
        cartproduct = CartProduct.objects.create(cart = cart_item, product = cart_product, quantity = 1, subtotal = cart_product.price)
        cart_item.total += cart_product.price
        cart_item.save()
    messages.success(request, 'Item added to cart Cart')
    return redirect('stores')

def myCart(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id:
        cart_item = Cart.objects.get(id = cart_id)

        if request.user.is_authenticated:
            cart_item.profile = request.user.profile
            cart_item.save()
        # check or assign cart to registered user
        if request.user.is_authenticated and request.user.profile:
            cart_item.profile = request.user.profile
            cart_item.save()
    else:
        cart_item = None

    context = {
        'cart': cart_item
    }

    return render(request, 'stores/myCart.html', context)

def manageCart(request, id):
    # get the cart
    cart_obj = CartProduct.objects.get(id = id)
    cart = cart_obj.cart

    # get the clicked action
    action = request.GET.get('action')

    if (action == 'inc'):
        cart_obj.quantity += 1
        cart_obj.subtotal += cart_obj.product.price
        cart_obj.save()
        cart.total += cart_obj.product.price
        cart.save()
        messages.success(request, 'Item quantity increased in Cart')

    elif(action == 'dcr'):
        cart_obj.quantity -= 1
        cart_obj.subtotal -= cart_obj.product.price
        cart_obj.save()
        cart.total -= cart_obj.product.price
        cart.save()
        if(cart_obj.quantity == 0):
            cart_obj.delete()
            cart.save()
        messages.success(request, 'Item quantity reduced in Cart')

    elif(action == 'rmv'):
        cart.total -= cart_obj.subtotal
        cart.save()
        cart_obj.delete()
        messages.success(request, 'Item removed from cart Cart')
    return redirect('myCart')

def checkout(request):
    cart_id = request.session.get('cart_id', None)
    cart_item = Cart.objects.get(id = cart_id)

    form = CheckoutForm()

    # check authentication and authorisation
    if request.user.is_authenticated and request.user.profile:
        pass
    else:
        return redirect('/user/login/?next=/checkout/')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            form = form.save(commit = False)
            form.cart = cart_item
            form.amount = cart_item.total
            form.subtotal = cart_item.total
            form.discount = 0
            paymentmethod = form.payment_method
            del request.session['cart_id']
            form.save()

            order = form.id
            if paymentmethod == 'paystack':
                return redirect('payment', id = order)
    
    context = {
        'form': form,
        'cart': cart_item
    }
    return render(request, 'stores/checkout.html', context,)

def payment(request, id):
    orders = Order.objects.get(id = id)
    context = {
        'order': orders,
        'paystack': settings.PAYSTACK_PUBLIC_KEY

    }

    return render(request, 'stores/payment.html', context)

def verify_payment(request: HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Order, ref = ref)
    verified = payment.verify_payment()

    if verified:
        messages.success(request, 'verification successful')
    else:
        messages.success(request, 'verification failed')
    return redirect('dashboard')