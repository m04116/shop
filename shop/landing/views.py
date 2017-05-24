from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *


def landing(request):
	name = 'Medved'
	curent_day = '03.03.17'
	form = SubscriberForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		# print(form)  # в консоли принтит форму
		# print(request.POST)  # что передается в пост-запросе
		# print(form.cleaned_data)  # посмотреть все поля формыб нужен is_valid()
		# data = form.cleaned_data  # Если мы хотим посмотреть какоето поле формы
		# print(data['name'])
		new_form = form.save()
	return render(request, 'landing/index.html', locals())


def home(request):
	products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
	products_images_candies = products_images.filter(product__category__id=1)
	products_images_cakes = products_images.filter(product__category__id=2)
	return render(request, 'landing/home.html', locals())
