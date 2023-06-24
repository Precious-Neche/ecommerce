from django.db import models
from users.models import Profile
import secrets
from . paystack import Paystack
# Create your models here.

class Slider(models.Model):

    title = models.CharField(max_length=50)
    text = models.TextField()
    image = models.ImageField( upload_to= 'slider')
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
       return self.title
    

class Category(models.Model):

    title = models.CharField(max_length=50)
    text = models.TextField()
    image = models.ImageField( upload_to= 'slider')
    created_at = models.DateTimeField(auto_now_add= True)

    def __str__(self):
       return self.title

    

class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField( upload_to= 'slider')
    created_at = models.DateTimeField(auto_now_add= True)
    stock = models.PositiveIntegerField()
    def __str__(self):
        return self.title


class Cart(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null = True, blank = True)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    def __str__(self):
        return f'{self.total} - '
    

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    subtotal = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    def __str__(self):
       return f'Cart- {self.cart.id}'

    
ORDER_STATUS = (
    ("completed", "completed"),
    ("pending","pending"),
    ("cancelled", "cancelled"),
)

PAYMENT_METHOD = (
    ("paystack", "paystack"),
    ("transfer","transfer"),
    
)

class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null = True)
    order_by = models.CharField(max_length=255)
    shipping_address = models.TextField()
    mobile = models.CharField(max_length=50)
    email = models.EmailField()
    discount = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    order_status = models.CharField(max_length=255, choices = ORDER_STATUS, null= True)
    payment_method = models.CharField(max_length=255, choices= PAYMENT_METHOD, null=True, default = 'paystack')
    payment_complete = models.BooleanField(default= False, null= True)
    ref = models.CharField(max_length=255, null = True)


    def __str__(self):
        return f'{self.amount} :: {str(self.id)}'
    
    # ref generate
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            obj_with_sm_ref = Order.objects.filter(ref = ref)
            if not obj_with_sm_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_value(self):
        return self.amount * 100
    

    # verify payment
    def verify_payment(self):
        paystack = Paystack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.payment_complete = True
            self.save()
        if self.payment_complete:
            return True
        return False


    
    