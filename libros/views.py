# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict
from .models import *
from usuarios.models import *
from .forms import *


# Create your views here.

def view_redirect_index(request):
    return HttpResponseRedirect(reverse('index'))


# view de la pàgina index
def view_index(request):
    # agafo tots els llibres i utilitzo el paginator per fer un paginador
    libros = Libros.objects.all()
    ultimos_capitulos = Capitulos.objects.all().order_by('-fecha_creacion')
    paginator = Paginator(ultimos_capitulos, 8)
    page = request.GET.get('page', '1')
    try:
        caps = paginator.page(page)
    except:
        caps = paginator.page(1)
    context = {'titulo': 'Inici | Apibooks, la teva pàgina de llibres', 'libros': libros,
               'capitulos': caps}
    if request.user.is_authenticated():
        usuario = Usuarios.objects.get(usuario=request.user)
        print usuario
        context['user'] = usuario
        print 'esta logeado'
    else:
        'no esta logeado'

    return render(request, 'index.html', context)


# view per crear llibres
@login_required()
def view_publicar(request):
    form = formPublicar(request.POST, request.FILES)
    usuario = Usuarios.objects.get(usuario=request.user)
    context = {'titulo': 'Publicar llibre | Apibooks, la teva pàgina de llibres', 'form': form, 'user': usuario}
    print 'entra en publicar'
    # si es post crearà el llibre si tot està be (form.is_valid())
    if request.method == 'POST':
        print 'es post'
        if form.is_valid():
            print 'crea el libro'
            titulo = form.cleaned_data.get('titulo').encode('utf-8')
            descripcion = form.cleaned_data.get('descripcion').encode('utf-8')
            generos = form.cleaned_data.get('generos')
            imagen_perfil = form.cleaned_data.get('imagen_perfil')
            print imagen_perfil
            print request.FILES
            libro = Libros(titulo=titulo, descripcion=descripcion, imagen_perfil=imagen_perfil, autor=usuario)
            libro.save()
            for genero in generos:
                print genero
                libro.generos.add(genero)
            return HttpResponseRedirect(reverse('libros'))
    return render(request, 'admin/nuevolibro.html', context)


# view per veure els meus llibres
@login_required()
def view_libros(request):
    usuario = Usuarios.objects.get(usuario=request.user)
    libros = Libros.objects.filter(autor=usuario)
    context = {'titulo': 'Els meus llibres | Apibooks, la teva pàgina de llibres', 'libros': libros, 'user': usuario}
    return render(request, 'admin/libros.html', context)


# view per afegir un capítol
@login_required()
def view_nuevo_cap(request, libro_id):
    form = formCapitulo(request.POST)
    usuario = Usuarios.objects.get(usuario=request.user)
    libro = Libros.objects.get(pk=libro_id)
    siguiente_n_cap = Capitulos.objects.filter(libro_id=libro_id).order_by("num_capitulo").last()
    # si aquest llibre ja te capítols m'ha agafara el següent número, en cas contrari agafara 1
    # en cas contrari 'siguiente_n_cap' serà 1
    if siguiente_n_cap:
        siguiente_n_cap = siguiente_n_cap.num_capitulo + 1
    else:
        siguiente_n_cap = 1
    context = {'titulo': 'Afegir capítol | Apibooks, la teva pàgina de llibres', 'libro': libro, 'user': usuario,
               'form': form, 'siguiente': siguiente_n_cap}
    # si es post crearà el capítol si tot està be (form.is_valid()) i només si soc el autor
    if request.method == 'POST' and libro.autor == usuario:
        if libro.autor == usuario:
            print 'es mi libro'
            if form.is_valid():
                print 'form ok'
                titulo = form.cleaned_data.get('titulo').encode('utf-8')
                num_capitulo = form.cleaned_data.get('num_capitulo')
                contenido = request.POST.get('contenido')
                print num_capitulo
                Capitulos.objects.create(titulo=titulo, num_capitulo=num_capitulo, contenido=contenido,
                                         libro_id=libro_id)
                return HttpResponseRedirect(reverse('libros'))
            else:
                print form.errors
        else:
            return HttpResponseRedirect(reverse('index'))
    return render(request, 'admin/nuevocap.html', context)


# view per editar un capítol
@login_required()
def view_editar_cap(request, capitulo_id):
    usuario = Usuarios.objects.get(usuario=request.user)
    cap = Capitulos.objects.get(pk=capitulo_id)
    form = formEditarCapitulo(request.POST, instance=cap)
    # si es post editarà el capítol si tot està be (form.is_valid()) i només si soc el autor
    if request.method == 'POST':
        if cap.libro.autor == usuario:
            print 'es mi libro'
            if form.is_valid():
                print 'form ok'
                titulo = form.cleaned_data.get('titulo').encode('utf-8')
                num_capitulo = form.cleaned_data.get('num_capitulo')
                contenido = request.POST.get('contenido')
                cap.titulo = titulo
                cap.num_capitulo = num_capitulo
                cap.contenido = contenido
                cap.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                print form.errors
        else:
            return HttpResponseRedirect(reverse('index'))
    context = {'titulo': 'Editar capítol | Apibooks, la teva pàgina de llibres', 'user': usuario, 'cap': cap,
               'form': form}
    return render(request, 'admin/editarcap.html', context)


# view per borrar un llibre
@login_required()
def view_borrar_libro(request, libro_id):
    usuario = Usuarios.objects.get(usuario=request.user)
    libro = Libros.objects.get(pk=libro_id)
    libros = Libros.objects.filter(autor=usuario)
    # borro el llibre si soc el autor
    if libro.autor == usuario:
        print libro.titulo + " - eliminado"
        Libros.objects.get(pk=libro_id).delete()
    context = {'titulo': 'Borrar llibre | Apibooks, la teva pàgina de llibres', 'libros': libros, 'user': usuario}
    return HttpResponseRedirect(reverse('libros'))


# view per mostrà la llista de capítols d'un llibre
@login_required()
def view_capitulos(request, libro_id):
    usuario = Usuarios.objects.get(usuario=request.user)
    libro = Libros.objects.get(pk=libro_id)
    # si no soc el autor del llibre em rediregirà al index
    if libro.autor != usuario:
        return HttpResponseRedirect(reverse('index'))
    caps = Capitulos.objects.filter(libro_id=libro_id)
    titulo = "Capítols de {0} | Apibooks, la teva pàgina de llibres".format(libro.titulo)
    context = {'titulo': titulo, 'libro': libro, 'user': usuario, 'caps': caps}
    return render(request, 'admin/listacaps.html', context)


# view per borrar un capítol
@login_required()
def view_borrar_cap(request, capitulo_id):
    usuario = Usuarios.objects.get(usuario=request.user)
    cap = Capitulos.objects.get(pk=capitulo_id)
    # borro el capítol si soc el autor
    if cap.libro.autor == usuario:
        Capitulos.objects.get(pk=capitulo_id).delete()
    return HttpResponseRedirect(reverse('lista_caps', args=(cap.libro.id,)))


# view per veure la pàgina del llibre
def view_front_libro(request, libro_id):
    if request.user.is_authenticated:
        usuario = Usuarios.objects.get(usuario=request.user)
    else:
        usuario = None
    libro = Libros.objects.get(pk=libro_id)
    caps = Capitulos.objects.filter(libro_id=libro_id).order_by('num_capitulo')
    ultimo_cap = None
    # si el llibre té 1 o més capítols, agafarà el últim per mostrar-lo
    if caps.count() > 0:
        ultimo_cap = Capitulos.objects.filter(libro_id=libro_id).order_by('-num_capitulo')[0]
    titulo = '{0} | Apibooks, la teva pàgina de llibres'.format(libro.titulo)
    context = {'titulo': titulo, 'libro': libro, 'user': usuario, 'caps': caps, 'ultimo_cap': ultimo_cap}
    return render(request, 'front/libro.html', context)


# view per veure un capítol d'un llibre
def view_fron_cap(request, libro_id, num_cap):
    libro = Libros.objects.get(pk=libro_id)
    # si he iniciat sessió i segueixo el llibre actualitzo l'es dades de la taula
    if request.user.is_authenticated:
        usuario = Usuarios.objects.get(usuario=request.user)
        libro_seguido = LibrosSeguidos.objects.filter(libro=libro, usuario=usuario)
        if libro_seguido.count() > 0:
            libro_seguido = LibrosSeguidos.objects.get(libro=libro, usuario=usuario)
            libro_seguido.ultimo_capitulo = num_cap
            libro_seguido.ultima_visita = timezone.now()
            libro_seguido.save()

    else:
        usuario = None
    cap = Capitulos.objects.filter(libro_id=libro_id, num_capitulo=num_cap)
    caps = Capitulos.objects.filter(libro_id=libro_id)
    cap_anterior = None
    cap_siguiente = None
    # si aquest capítol no existeix em retorna al index
    if cap.count() == 0:
        return HttpResponseRedirect(reverse('index'))
    cap = Capitulos.objects.get(libro_id=libro_id, num_capitulo=num_cap)
    # em dona el següent capítol i l'anterior
    try:
        cap_siguiente = \
            Capitulos.objects.filter(libro_id=libro_id, num_capitulo__gt=num_cap).exclude(
                num_capitulo=num_cap).order_by(
                'num_capitulo')[0]
    except:
        cap_siguiente = None
    try:
        cap_anterior = \
            Capitulos.objects.filter(libro_id=libro_id, num_capitulo__lt=num_cap).exclude(
                num_capitulo=num_cap).order_by(
                '-num_capitulo')[0]
    except:
        cap_anterior = None
    titulo = 'Capitulo {0}: {1} | Apibooks, la teva pàgina de llibres'.format(cap.num_capitulo, cap.titulo)
    context = {'titulo': titulo, 'libro': libro, 'user': usuario, 'cap': cap, 'siguiente': cap_siguiente,
               'anterior': cap_anterior, 'lista_caps': caps}
    return render(request, 'front/capitulo.html', context)

# view per seguir un llibre
@login_required()
def view_seguir(request):
    usuario = Usuarios.objects.get(usuario=request.user)
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    libro_id = request.GET.get('libro', None)
    num_cap = request.GET.get('cap', '0')
    # si no em donen el id del llibre per get retorno al index
    if libro_id is None:
        return HttpResponseRedirect(reverse('index'))
    libro = Libros.objects.filter(pk=libro_id)
    # comprovo que existeix el llibre
    if libro.count() > 0:
        libro = Libros.objects.get(pk=libro_id)
    else:
        return HttpResponseRedirect(reverse('index'))
    libro_seguido = LibrosSeguidos.objects.filter(libro=libro, usuario=usuario).count()
    dict = {}
    # si segueixo el llibre el deixo de seguir
    if libro_seguido == 1:
        LibrosSeguidos.objects.get(libro=libro, usuario=usuario).delete()
        dict = {"result": 'Ya no sigo el libro {0}'.format(libro.titulo), "type": "2"}
    # en cas contrari segueixo el llibre
    else:
        LibrosSeguidos.objects.create(libro=libro, usuario=usuario, ultimo_capitulo=int(num_cap))
        dict = {"result": 'Sigo el libro {0}'.format(libro.titulo), "type": "1"}
    # retorno el diccionari com un fitxer JSON
    return HttpResponse(json.dumps(dict), content_type='aplication/json')

# view per comprova si segueixo un llibre
@login_required()
def view_seguir_status(request):
    usuario = Usuarios.objects.get(usuario=request.user)
    if request.method != 'GET':
        return HttpResponseRedirect(reverse('index'))
    libro_id = request.GET.get('libro', None)
    num_cap = request.GET.get('cap', '0')
    if libro_id is None:
        return HttpResponseRedirect(reverse('index'))
    libro = Libros.objects.filter(pk=libro_id)
    if libro.count() > 0:
        libro = Libros.objects.get(pk=libro_id)
    else:
        return HttpResponseRedirect(reverse('index'))
    libro_seguido = LibrosSeguidos.objects.filter(libro=libro, usuario=usuario).count()
    dict = {}
    if libro_seguido == 1:
        libro_seguido = LibrosSeguidos.objects.get(libro=libro, usuario=usuario)
        dict = {"result": 'Sigo el libro {0}'.format(libro.titulo), "type": "1",
                "ultimo_cap": libro_seguido.ultimo_capitulo, "ultima_visita": str(libro_seguido.ultima_visita)}
    else:
        dict = {"result": 'No sigo el libro {0}'.format(libro.titulo), "type": "2"}
    return HttpResponse(json.dumps(dict), content_type='aplication/json')


def view_buscador(request):
    if request.user.is_authenticated:
        usuario = Usuarios.objects.get(usuario=request.user)
    else:
        usuario = None
    context = {'titulo': 'Cercador | Apibooks, la teva pàgina de llibres', 'user': usuario}
    if request.GET.get('genere'):
        context['libros'] = Libros.objects.filter(generos__nombre=request.GET.get('genere'))
    return render(request, 'front/buscador.html', context)

# view del cercador
def view_api_buscador(request):
    # type es qué busca (titol llibre, titol capítol, autor o nom del gènere)
    type = request.GET.get("type")
    # q es el text de la búsqueda
    query = request.GET.get("q")
    libros = None
    br = False
    dict = {}
    libros_id = []
    i = 0
    if type == "titulo_libro":
        libros = Libros.objects.filter(titulo__contains=query)
    elif type == "titulo_cap":
        libros = Capitulos.objects.filter(titulo__contains=query)
    elif type == "genero":
        libros = Libros.objects.filter(generos__nombre__contains=query)
    elif type == "autor":
        libros = Libros.objects.filter(autor__nickname__contains=query)
    else:
        dict = {"result": "Bad request"}
        # en cas de que modifiquin el html i fiquin un tipus de busqueda que no busco res
        # br = bad request
        br = True
    if not br:
        for libro in libros:
            if type == "titulo_cap":
                libro = libro.libro
            pasa = True
            if libro.id in libros_id:
                pasa = False
            if pasa:
                dict[str(i)] = {"titulo": libro.titulo, "portada": libro.imagen_perfil.url, "libro_id": libro.id}
            libros_id.append(libro.id)
            i += 1
    return HttpResponse(json.dumps(dict), content_type='aplication/json')

# view per editar un llibre
@login_required()
def view_editar_libro(request, libro_id):
    libro = Libros.objects.get(pk=libro_id)
    formulario = formEditarLibro(request.POST, request.FILES, instance=libro)

    usuario = Usuarios.objects.get(usuario=request.user)
    context = {'titulo': 'Editar llibre | Apibooks, la teva pàgina de llibres', 'form': formulario, 'user': usuario,
               'libro': libro}
    # si no soc l'autor retorna a l'index
    if libro.autor != usuario:
        return HttpResponseRedirect(reverse('index'))
    # si es post i el formulari està be edita el llibre
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect(reverse('libros'))
    return render(request, 'admin/editarlibro.html', context)
