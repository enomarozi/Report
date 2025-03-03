from django.db import models
from django.utils.timezone import now

class OutputFiles(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	md5check = models.CharField(max_length=32, unique=True)
	date = models.DateTimeField(default=now)

	class Meta:
		db_table = 'uploads'
