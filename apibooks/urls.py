"""apibooks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from libros.views import *
from usuarios.views import *
from django.contrib.auth import views as auth_views


from libros.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', view_redirect_index, name='redirect_index'),
    url(r'^home$', view_index, name='index'),
    url(r'^registre$', view_registre, name='registre'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'index'}, name='sortir'),
    url(r'^login/$', auth_views.login,
    {'template_name': 'usuarios/login.html', 'redirect_authenticated_user': True, 'extra_context': {'titulo': 'Inicia '
                                                                                                              'sessio'}}, name='login'),
    url(r'^perfil$', view_perfil, name='perfil'),
    # url(r'^publicar$', view_publicar, name='publicar'),
    url(r'^publicar$', view_publicar, name='nuevo_libro'),
    url(r'^llibres/$', view_libros, name='libros'),
    url(r'^nou-capitol/(?P<libro_id>[0-9]+)$', view_nuevo_cap, name='nuevo_cap'),
    url(r'^borrar-llibre/(?P<libro_id>[0-9]+)$', view_borrar_libro, name='borrar_libro'),
    url(r'^llibre/(?P<libro_id>[0-9]+)/capitols$', view_capitulos, name="lista_caps"),
    url(r'^capitol/(?P<capitulo_id>[0-9]+)/borrar$', view_borrar_cap, name='borrar_cap'),
    url(r'^capitol/(?P<capitulo_id>[0-9]+)/editar$', view_editar_cap, name='editar_cap'),
    url(r'^llibre/(?P<libro_id>[0-9]+)$', view_front_libro, name='ver_libro'),
    url(r'^llibre/(?P<libro_id>[0-9]+)/(?P<num_cap>[0-9]+)$', view_fron_cap, name='ver_cap'),
    url(r'^llibre/seguir$', view_seguir, name='seguir_libro'),
    url(r'^llibre/seguir/status$', view_seguir_status, name='seguir_libro_status'),
    url(r'^biblioteca$', view_mis_libros, name='biblioteca'),
    url(r'^cercador$', view_buscador, name='buscador'),
    url(r'^cercador/cerca$', view_api_buscador, name='api_buscador'),
    url(r'^llibres/(?P<libro_id>[0-9]+)/editar$', view_editar_libro, name='editar_libro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
