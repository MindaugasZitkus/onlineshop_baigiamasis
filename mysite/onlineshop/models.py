from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
import json



# Create your models here.

class Status(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(to=User, verbose_name="Vartotojas", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Vardas", max_length=200, null=True)
    email = models.CharField(verbose_name="el.paštas", max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name="Produkto pavadinimas", max_length=200)
    price = models.FloatField(verbose_name="Kaina")
    digital = models.BooleanField(default=False, null=True, blank=True)
    # image = models.ImageField(verbose_name="Nuotrauka", null=True, blank=True)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="products", null=True, blank=True)
    description = HTMLField(verbose_name="Aprašymas", null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def photoURL(self):
        try:
            url = self.photo.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)
    complete = models.BooleanField(verbose_name="užbaigta", default=False)
    transaction_id = models.CharField(verbose_name="pavedimo id", max_length=100, null=True)
    status = models.ForeignKey(to="Status", verbose_name="Būsena", on_delete=models.SET_NULL, null=True)

    def total(self):
        total = 0
        lines = self.lines.all()
        for line in lines:
            total += line.sum()
        return total

    def __str__(self):
        return f"{self.customer}, {self.date_ordered}, {self.status} "

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(to=Product, verbose_name="Produktas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True, related_name="lines")
    quantity = models.IntegerField(verbose_name="Kiekis", default=0, null=True, blank=True)
    date_added = models.DateTimeField(verbose_name="Pridėjimo data", auto_now_add=True)

    def sum(self):
        return self.product.price * self.quantity

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total




class ShippingAddress(models.Model):
    customer = models.ForeignKey(to=Customer, verbose_name="Klientas", on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(to=Order, verbose_name="Užsakymas", on_delete=models.SET_NULL, null=True)
    address = models.CharField(verbose_name="Adresas", max_length=200, null=False)
    city = models.CharField(verbose_name="Miestas", max_length=200, null=False)
    state = models.CharField(verbose_name="Valstybė", max_length=200, null=False)
    zipcode = models.CharField(verbose_name="Pašto kodas", max_length=200, null=False)
    date_added = models.DateTimeField(verbose_name="Užsakymo data", auto_now_add=True)

    def __str__(self):
        return self.address


def cookieCart(request):
    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if (cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.imageURL}, 'quantity': cart[i]['quantity'],
                    'digital': product.digital, 'get_total': total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=(item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']),
            # negative quantity = freebies
        )
    return customer, order






# from django.conf import settings
#
# class Cart(object):
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get(settings.CART_SESSION_ID)
#
#         if not cart:
#             cart = self.session[settings.CART_SESSION_ID] = {}
#
#         self.cart = cart
#
#     def __iter__(self):
#         for p in self.cart.keys():
#             self.cart[str(p)]['product'] = Product.objects.get(pk=p)
#
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())
#
#     def save(self):
#         self.session[settings.CART_SESSION_ID] = self.cart
#         self.session.modified = True
#
#     def add(self, product_id, quantity = 1, update_quantity=False):
#         product_id = str(product_id)
#
#         if product_id not in self.cart:
#             self.cart[product_id] = {'quantity':1, 'id': product_id}
#
#         if update_quantity:
#             self.cart[product_id]['quantity'] += int(quantity)
#
#             if self.cart[product_id]['quantity'] == 0:
#                 self.remove(product_id)
#
#         self.save()
#
#     def remove(self, product_id):
#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()

