# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import *
from usuarios.models import *
# Create your views here.

def index(request):
    libros = Libros.objects.all()
    ultimos_capitulos = Capitulos.objects.all().order_by()
    context = {'titulo': 'Inici | Apibooks, la teva pàgina de llibres', 'libros': libros}
    return render(request, 'index.html', context)