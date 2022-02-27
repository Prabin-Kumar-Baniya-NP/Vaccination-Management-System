from django.db import models

# Create your models here.
class Medical_Condition(models.Model):
    name = models.CharField("Disease/Infection Name", max_length=32)
    description = models.TextField("Description", max_length=1024)

    def __str__(self):
        return self.name