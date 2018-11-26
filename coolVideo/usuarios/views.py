# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from usuarios.models import *
from django.utils import timezone
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.conf import settings
import os

tipoImagenes = ['bmp', 'gif', 'jpg', 'jpeg', 'tif', 'tiff', 'png', 'svg']

def stringRandom(longitud):
    dict = 'qwertyuiopasdfghjklñzxcvbnmQWERTYUIOPASDFGHJKLÑZXCVBNM0123456789'
    tam = len(dict)-1

    while True:

        code = ''

        for x in range(longitud):
            code += dict[random.randint(0,tam)]

        if not Usuario.objects.filter(codigoVerificacion=code).exists():
            return code

# Create your views here.
def login(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        if Usuario.objects.filter(email=email).exists():
            usuario = Usuario.objects.get(email=email)
            if usuario.password == password:
                if usuario.verificado:
                    contexto = {
                        'response':'success', 'type':'El usuario existe, la contraseña es correcta y esta verificado.',
                        'usuario':usuario
                    }
                    return redirect('usuarios:home', upk = usuario.pk)
                else:
                    contexto = {
                        'response':'error', 'type':'El usuario no esta verificado, por favor hazlo desde el link enviado a tu correo.'
                    }
            else:
                contexto = {
                    'response': 'error',
                    'type': 'Contraseña incorrecta, favor de verificarla.'
                }
        else:
            contexto = {
                'response': 'error',
                'type': 'El ususario no existe, verifica el correo o registrate.'
            }

        return render(request, 'login.html', contexto)

    elif request.method == 'GET':
        return render(request, 'login.html')


def registro(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        apellidoP = request.POST.get('apellidoP')
        apellidoM = request.POST.get('apellidoM')

        if Usuario.objects.filter(email=email).exists():
            contexto = {
                'response': 'error',
                'type': 'El correo actualmente esta registrado, inicie sesion o registre un correo diferente.'
            }
        else:
            code = stringRandom(6)

            newUser = Usuario(
                email=email,
                password=password,
                nombre=nombre,
                apellidoP=apellidoP,
                apellidoM=apellidoM,
                codigoVerificacion=code
            )

            url = 'http://coolvideo.tk/verification/' + code + '/'

            newUser.save()

            send_mail(
                'Codigo de verificacion - CoolVideo',
                'Hola, bienvenido a CoolVideo, para completar tu registro solo falta un paso mas, debes activar tu cuenta accediendo al siguiente link: \n' + url,
                'verificacion@coolvideo.com',
                [email],
                fail_silently=False
            )

            contexto = {
                'response': 'success',
                'type': 'Usuario creado con exito, se ha enviado un correo electronico para su verificacion.'
            }

        return render(request, 'registro.html', contexto)

    elif request.method == 'GET':
        return render(request, 'registro.html')

def verification(request, code):
    if request.method == 'GET':
        if Usuario.objects.filter(codigoVerificacion=code).exists():
            usuario = Usuario.objects.get(codigoVerificacion=code)

            if usuario.verificado:
                contexto = {
                    'response': 'success',
                    'description': 'El ususario ya fue activado anteriormente.'
                }
            else:
                usuario.verificado = True
                usuario.save()

                contexto = {
                    'response': 'success',
                    'description': 'El ususario ha sido activado exitosamente.'
                }
        else:
            contexto = {
                'response': 'error',
                'description': 'No existe ningun ususario con ese codigo de verificacion.'
            }

        return render(request, 'activacion.html', contexto)

def home(request, upk):
    # return HttpResponse(settings.MEDIA_ROOT)

    usuario = Usuario.objects.get(pk=upk)


    publicaciones = []
    archivoPublicacion = ArchivoPublicacion.objects.all().order_by('-pk')
    for archivo in archivoPublicacion:
        data = {}
        data['usuario'] = archivo.publicacion.usuario.nombre + ' ' + archivo.publicacion.usuario.apellidoP + ' ' + archivo.publicacion.usuario.apellidoM
        data['titulo'] = archivo.publicacion.titulo
        data['descripcion'] = archivo.publicacion.descripcion
        data['creado'] = archivo.publicacion.creado
        data['archivo'] = archivo.archivo

        isIMG = False
        for extension in tipoImagenes:
            if extension in archivo.archivo.name.lower():
                isIMG = True

        if isIMG:
            data['tipoArchivo'] = 'imagen'
        else:
            data['tipoArchivo'] = 'noImagen'

        publicaciones.append(data)

    contexto = {'usuario':usuario, 'publicaciones':publicaciones}

    return render(request, 'home.html', contexto)

def crearPost(request, upk):

    usuario = Usuario.objects.get(pk=upk)
    titulo = request.POST.get('tituloP')
    descripcion = request.POST.get('descripcionP')
    archivo = request.FILES.get('archivoP')

    publicacion = Publicacion(
        usuario=usuario,
        titulo=titulo,
        descripcion=descripcion
    )
    publicacion.save()

    archivoP = ArchivoPublicacion(
        publicacion=publicacion,
        archivo=archivo
    )

    archivoP.save()

    return redirect('usuarios:home', upk=usuario.pk)

def perfil(request, upk):
    usuario = Usuario.objects.get(pk=upk)
    publicaciones = ArchivoPublicacion.objects.filter(publicacion__usuario=usuario).order_by('-pk')

    contexto = {'usuario':usuario, 'publicaciones':publicaciones, 'numeroPublicaciones':len(publicaciones)}

    return render(request, 'perfil.html', contexto)

def busqueda(request, upk):
    usuario = Usuario.objects.get(pk=upk)
    contexto = {'usuario':usuario}

    if request.method == 'POST':
        palabrasOrg = request.POST.get('palabras')
        palabras = palabrasOrg.split(' ')

        publicaciones = []
        query = ArchivoPublicacion.objects.all().order_by('-pk')
        for q in query:
            for palabra in palabras:
                palabra = palabra.upper()
                if palabra in (q.publicacion.titulo).upper() or palabra in (q.publicacion.descripcion).upper() or palabra in (q.publicacion.usuario.nombre).upper() or palabra in (q.publicacion.usuario.apellidoP).upper() or palabra in (q.publicacion.usuario.apellidoM).upper():
                    data = {}
                    data['usuario'] = q.publicacion.usuario.nombre + ' ' + q.publicacion.usuario.apellidoP + ' ' + q.publicacion.usuario.apellidoM
                    data['titulo'] = q.publicacion.titulo
                    data['descripcion'] = q.publicacion.descripcion
                    data['creado'] = q.publicacion.creado
                    data['archivo'] = q.archivo

                    isIMG = False
                    for extension in tipoImagenes:
                        if extension in q.archivo.name.lower():
                            isIMG = True

                    if isIMG:
                        data['tipoArchivo'] = 'imagen'
                    else:
                        data['tipoArchivo'] = 'noImagen'

                    publicaciones.append(data)

        contexto['publicaciones'] = publicaciones
        contexto['busquedaAplicada'] = palabrasOrg

    return render(request, 'busqueda.html', contexto)

def eliminarPost(request, upk, ppk):
    usuario = Usuario.objects.get(pk=upk)
    archivoP = ArchivoPublicacion.objects.get(pk=ppk)

    publicacion = Publicacion.objects.get(pk=archivoP.publicacion.pk)
    urlArchivo = '/home/coolVideo/media/' + archivoP.archivo.name

    publicacion.delete()
    archivoP.delete()
    os.remove(urlArchivo)

    return redirect('usuarios:perfil', upk=usuario.pk)

