from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import *
from .forms import CartContactForm


def add_to_cart(request):
    return_dict = dict()
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()
    print(request.POST)
    data = request.POST
    product_id = data.get('product_id')
    nmb = data.get('nmb')
    is_delete = data.get('is_delete')

    if is_delete == 'true':
    # if is_delete:
        ProductInCart.objects.filter(id=product_id).update(is_active=False)
    else:
        new_product, created = ProductInCart.objects.get_or_create(session_key=session_key, 
                                                                   is_active=True, 
                                                                   product_id=product_id, 
                                                                   defaults={'numb': nmb})
        if not created:
            print('not created')
            new_product.numb += int(nmb)
            new_product.save(force_update=True)

    products_in_cart = ProductInCart.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_cart.count()

    return_dict['products_total_nmb'] = products_total_nmb
    return_dict['products'] = list()

    for item in products_in_cart:
        product_dict = dict()
        product_dict['name'] = item.product.name
        product_dict['price_per_item'] = item.price_of_prod
        product_dict['nmb'] = item.numb
        product_dict['id'] = item.id
        return_dict['products'].append(product_dict)

    print('###')
    ret = JsonResponse(return_dict)
    print(ret.content)

    return JsonResponse(return_dict)



def cart(request):
    session_key = request.session.session_key
    products_in_cart = ProductInCart.objects.filter(session_key=session_key, 
                                                    is_active=True, 
                                                    order__isnull=True)

    form = CartContactForm(request.POST or None)

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            print('form is ok')
            data = request.POST
            name = data.get('name', 'default')
            # phone_number = data.phone_number
            phone_number = data['phone_number']
            user, created = User.objects.get_or_create(
                username=phone_number, 
                defaults={'first_name': name})

            order = Order.objects.create(user=user, 
                                         customer_name=name, 
                                         customer_phone=phone_number,
                                         status_id=1)



            for name, value in data.items():
                if name.startswith('product_in_cart_'):
                    product_in_cart_id = name.split('product_in_cart_')[1]
                    product_in_cart = ProductInCart.objects.get(id=product_in_cart_id)
                    product_in_cart.numb = int(value)
                    product_in_cart.order = order
                    product_in_cart.save(force_update=True)
                    
                    ProductInOrder.objects.create(product=product_in_cart.product, 
                                                  numb=product_in_cart.numb,
                                                  price_of_prod=ProductInCart.price_of_prod,
                                                  total_sum=ProductInCart.total_sum,
                                                  order=order)

        else:
            print('form is not ok')

    return render(request, 'orders/cart.html', locals())
