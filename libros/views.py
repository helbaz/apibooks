# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from usuarios.models import *
from .forms import *
# Create your views here.


def view_index(request):
    libros = Libros.objects.all()
    ultimos_capitulos = Capitulos.objects.all().order_by('fecha_creacion')
    context = {'titulo': 'Inici | Apibooks, la teva pàgina de llibres', 'libros': libros, 'capitulos': ultimos_capitulos}
    if request.user.is_authenticated():
        usuario = Usuarios.objects.get(usuario=request.user)
        print usuario
        context['user'] = usuario
        print 'esta logeado'
    else:
        'no esta logeado'
    return render(request, 'index.html', context)


@login_required()
def view_publicar(request):
    form = formPublicar(request.POST, request.FILES)
    usuario = Usuarios.objects.get(usuario=request.user)
    context = {'title': 'Publicar', 'form': form, 'user': usuario}
    print 'entra en publicar'
    if request.method == 'POST':
        print 'es post'
        if form.is_valid():
            print 'crea el libro'
            titulo = form.cleaned_data.get('titulo').encode('utf-8')
            descripcion = form.cleaned_data.get('descripcion').encode('utf-8')
            generos = form.cleaned_data.get('generos')
            imagen_perfil = form.cleaned_data.get('imagen_perfil')
            print imagen_perfil
            libro = Libros(titulo=titulo, descripcion=descripcion, imagen_perfil=request.FILES.get('imagen_perfil'), autor=usuario)
            libro.save()
            for genero in generos:
                print genero
                libro.generos.add(genero)
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'publicar.html', context)
