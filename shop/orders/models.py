from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from products.models import Product


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True )
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return 'Status %s' % self.name

    class Meta:
        verbose_name = 'Status of order'
        verbose_name_plural = 'My Statuses of orders'


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None)
    customer_name = models.CharField(max_length=150, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=50, blank=True, null=True, default=None)
    customer_adress = models.CharField(max_length=100, blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total sum for all products in order

    def __str__(self):
        return 'Order %s %s' % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'My Orders'

    # def save(self, *args, **kwargs):
    #     price_of_prod = self.product.price
    #     self.price_of_prod = price_of_prod
    #     # self.total_sum = self.numb * price_of_prod
    #     self.total_sum = self.numb * self.price_of_prod
    #     super(ProductInOrder, self).save()


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    numb = models.IntegerField(default=1)
    price_of_prod = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0) #  price * numb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.product.name

    class Meta:
        verbose_name = 'Product in order'
        verbose_name_plural = 'My Products in order'

    def save(self, *args, **kwargs):
        price_of_prod = self.product.price
        self.price_of_prod = price_of_prod

        # self.total_sum = self.numb * price_of_prod
        self.total_sum = self.numb * self.price_of_prod

        super(ProductInOrder, self).save()

def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    total_sum_of_order = 0
    for item in all_products_in_order:
        total_sum_of_order += item.total_sum

    instance.order.total_sum = total_sum_of_order
    instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save, sender=ProductInOrder)

class ProductInCart(models.Model):
    session_key = models.CharField(max_length=150, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    numb = models.IntegerField(default=1)
    price_of_prod = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0) #  price * numb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return '%s' % self.product.name

    class Meta:
        verbose_name = 'Product in cart'
        verbose_name_plural = 'My Products in cart'

    def save(self, *args, **kwargs):
        price_of_prod = self.product.price
        self.price_of_prod = price_of_prod

        # self.total_sum = self.numb * price_of_prod
        self.total_sum = int(self.numb) * self.price_of_prod

        super(ProductInCart, self).save()
