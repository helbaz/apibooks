# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
    context = {'titulo': 'Inici | Apibooks, la teva pàgina de llibres'}
    return render(request, 'index.html', context)