from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin (admin.ModelAdmin):
	list_display = ['name', 'email']  # выборочное отображение полей
	# list_display = [field.name for field in Subscriber._meta.fields]  # генератор списка для всех полей
	# exclude = ['email']  # исключаем поле email
	#fields = ['name',]  # указываем какое поле(я) показывать
	# list_filter = ['name',]  # появляется колонка справа для фильтрации
	# search_fields = ['name',]  # появится поле для поиска по name

	class Meta:
		model = Subscriber


admin.site.register(Subscriber, SubscriberAdmin)
