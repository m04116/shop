from django.db import models

class Subscriber(models.Model):
	email = models.EmailField()
	name = models.CharField(max_length=150)

	def __str__(self):
		try:
			return self.name
		except:
			return '%s' % self.id

	class Meta:
		verbose_name = 'MySubscriber'
		verbose_name_plural = 'A lot of Subscribers'
