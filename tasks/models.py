from django.db import models
from django.contrib.auth.models import User

##Se crear el modelo de la tabla master de tareas
class Task(models.Model):
    title = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True)
    important = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " by " + self.user.username
