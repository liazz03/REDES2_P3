from django.db import models
from django.urls import reverse

class Reloj(models.Model):

    publicId = models.CharField(blank=False, max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse("reloj_detail", kwargs={"pk": self.id})

    class Meta:
        app_label = 'sysdomotic'

    def __str__(self) -> str:
        return self.publicId

class Sensor(models.Model):

    publicId = models.CharField(blank=False, max_length=50 , unique=True)
    state = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse("sensor_detail", kwargs={"pk": self.id})

    class Meta:
        app_label = 'sysdomotic'

    def __str__(self) -> str:
        return self.publicId

class Interruptor(models.Model):

    publicId = models.CharField(blank=False, max_length=50, unique=True)
    state = models.CharField(max_length=50, default='OFF')

    def get_absolute_url(self):
        return reverse("interruptor_detail", kwargs={"pk": self.id})

    class Meta:
        app_label = 'sysdomotic'

    def __str__(self) -> str:
        return self.publicId

class Regla(models.Model):

    regla = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'sysdomotic'
        
    def __str__(self) -> str:
        return self.regla
    
class Evento(models.Model):

    evento = models.CharField(max_length=100)

    class Meta:
        app_label = 'sysdomotic'
        
    def __str__(self) -> str:
        return self.evento