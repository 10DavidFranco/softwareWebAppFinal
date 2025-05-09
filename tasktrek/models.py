from django.db import models

# Create your models here.

class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 64)
    is_admin = models.BooleanField(default=False)
    tasks = models.CharField(max_length = 64)
    username = models.CharField(max_length = 64, default="nousername")
    password = models.IntegerField(default = 11111)

    def __str__(self):
        return f"{self.id}~{self.name}~{self.is_admin}~{self.tasks}~{self.username}~{self.password}"

class Task(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 32, default="...")
    description = models.CharField(max_length = 100)
    due_date = models.CharField(default = "")
    is_complete = models.CharField(default = "False")
    is_team = models.CharField(default="False")


    def __str__(self):
        return f"{self.id}~{self.name}~{self.description}~{self.due_date}~{self.is_complete}~{self.is_team}"

