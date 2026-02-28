from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.name