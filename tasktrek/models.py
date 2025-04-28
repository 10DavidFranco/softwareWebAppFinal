from django.db import models

# Create your models here.

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 64)
    is_admin = models.BooleanField(default=False)
    tasks = models.CharField(max_length = 64)

class Task(models.Model):
    id = models.AutoField(primary_key = True)
    description = models.CharField(max_length = 100)
    due_date = models.DateField()
    status = models.BooleanField()

