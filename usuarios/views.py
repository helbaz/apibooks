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


# View para registrar usuarios
def view_registre(request):
    form = formRegistre(request.POST)
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    context = {'form': form, 'title': 'Registrat | Apibooks, la teva pàgina de llibres'}
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
    return render(request, 'regitro.html', context)

@login_required()
def view_perfil(request):
    user = Usuarios.objects.get(usuario=request.user)
    form = formPerfil(request.POST, request.FILES, instance=user)
    context = {'form': form, 'title': 'Editar perfil | Apibooks, la teva pàgina de llibres', 'user': user}
    if request.method == 'POST':
        print 'es post'
        print form.errors
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'perfil.html', context)