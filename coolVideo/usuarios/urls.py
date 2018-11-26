from django.conf.urls import url
from . import views
app_name = 'usuarios'

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^registro/$', views.registro, name='registro'),
    url(r'^verification/(?P<code>\w+)/$', views.verification, name='verification'),

    url(r'^home/(?P<upk>\w+)/$', views.home, name='home'),
    url(r'^crearPost/(?P<upk>\w+)/$', views.crearPost, name='crearPost'),
    url(r'^perfil/(?P<upk>\w+)/$', views.perfil, name='perfil'),
    url(r'^busqueda/(?P<upk>\w+)/$', views.busqueda, name='busqueda'),
    url(r'^eliminarPost/(?P<upk>\w+)&(?P<ppk>\w+)/$', views.eliminarPost, name='eliminarPost'),
]
