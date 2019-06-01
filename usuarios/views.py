# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import render

from .models import *
from libros.models import *
from django.shortcuts import render
from .forms import *


# View per registrar usuaris
def view_registre(request):
    form = formRegistre(request.POST)
    # si ja he iniciat sessió retorno a l'index
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {'form': form, 'title': 'Registrat | Apibooks, la teva pàgina de llibres'}
    # si es post i el formulari està bé creo l'usuari
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            nom_usuari = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            nickname = form.cleaned_data.get('nickname')
            usuari = authenticate(username=nom_usuari, password=password)
            login(request, usuari)
            Usuarios.objects.create(usuario=request.user, nickname=nickname)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'usuarios/regitro.html', context)


# view per editar el nom de l'usuari i la imatge de perfil
@login_required()
def view_perfil(request):
    user = Usuarios.objects.get(usuario=request.user)
    form = formPerfil(request.POST, request.FILES, instance=user)
    context = {'form': form, 'titulo': 'Editar perfil | Apibooks, la teva pàgina de llibres', 'user': user}
    # si es post i el formulari està bé edito el perfil de l'usuari
    if request.method == 'POST':
        print form.errors
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'usuarios/perfil.html', context)

# view per veure els llibres que segueixo
@login_required()
def view_mis_libros(request):
    user = Usuarios.objects.get(usuario=request.user)
    libros_seguidos = LibrosSeguidos.objects.filter(usuario=user)
    dict = {}
    # si segueixo 1 o més llibres els fico dins d'un diccionari
    if libros_seguidos.count() > 0:
        i = 0
        for libro_seguido in libros_seguidos:
            num = Capitulos.objects.filter(libro=libro_seguido.libro).order_by("-num_capitulo")
            nuevo_cap = False
            if num.count() > 0:
                if num[0].fecha_creacion > libro_seguido.ultima_visita:
                    nuevo_cap = True
                num = num[0].num_capitulo
            else:
                num = 0
            dict[str(i)] = {"libro": libro_seguido, "num_cap": num, "titulo": libro_seguido.libro.titulo, "url_imagen": libro_seguido.libro.imagen_perfil, "nuevo_cap": nuevo_cap, "libro_id": libro_seguido.libro.id}
            i += 1
    else:
        dict = None
    context = {'titulo': 'Els meus llibres | Apibooks, la teva pàgina de llibres', 'user': user, 'libros': dict}
    return render(request, 'usuarios/biblioteca.html', context)