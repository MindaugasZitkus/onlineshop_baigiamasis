from .models import Product, Order, OrderItem, Customer

import json


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except json.JSONDecodeError:
        cart = {}

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for item_id, item_data in cart.items():
        try:
            quantity = item_data.get('quantity', 0)
            if quantity > 0:
                cartItems += quantity

                product = Product.objects.get(id=item_id)
                total = product.price * quantity

                order['get_cart_total'] += total
                order['get_cart_items'] += quantity

                item = {
                    'id': product.id,
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.photoURL
                    },
                    'quantity': quantity,
                    'digital': product.digital,
                    'get_total': total,
                }

                items.append(item)

                if not product.digital:
                    order['shipping'] = True
        except Product.DoesNotExist:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.lines.all()  # naudoti "lines" o ne  "line_set"
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

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item['id'])
        quantity = item['quantity'] if item['quantity'] > 0 else -1 * item['quantity']

        OrderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=quantity,
        )

    return customer, order
