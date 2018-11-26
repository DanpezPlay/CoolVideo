# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.
class Usuario(models.Model):
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    apellidoP = models.CharField(max_length=50)
    apellidoM = models.CharField(max_length=50)
    codigoVerificacion = models.CharField(max_length=6)
    verificado = models.BooleanField(default=False)
    creado = models.DateTimeField(default=timezone.now())
    editado = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return '{}'.format(self.nombre + ' ' + self.apellidoP + ' ' + self.apellidoM)

class Publicacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=255)
    creado = models.DateTimeField(default=timezone.now())
    editado = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return '{}'.format(self.titulo)

class ArchivoPublicacion(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    archivo = models.FileField(null=True,blank=True)

    def __str__(self):
        return '{}'.format(self.pk)