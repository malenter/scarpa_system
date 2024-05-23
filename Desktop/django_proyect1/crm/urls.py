"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path ,include
from usuairo import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
	path('',views.home,name='inicio'),
    path('inicio/',views.inicio,name='home'),
    path('singup/',views.singnup,name='singup'),
    path('sigint/',views.siging,name='sigint'),
    path('clientes/',views.clientes,name='clientes'),
    path('clientes/create/',views.create_clientes,name='create_clientes'),
    path('logaut/',views.signaout,name='logaut'),
    path('clientes/<int:cliente_id>/', views.task_detail, name='modificar_cliente'),
    path('clientes/<int:cliente_id>/delete', views.delete_task, name='delete_task'),
	path('clientes/<int:cliente_id>/send', views.mi_vista_muestrario, name='send_email'),
	path('clientes/<int:cliente_id>/encuesta', views.mi_vista_email_encuesta, name='send_email_encuesta'),
	path('encuesta/<int:cliente_id>/', views.encuesta_view, name='encuesta'),
    path('gracias_encuesta/', views.gracias_encuesta, name='gracias_encuesta'),
    path('zapato/',views.Zapatos,name='zapato'),
    path('zapato/create/',views.crear_Zapatos,name='create_zapato'),
	path('zapato/<int:Zapato_id>/',views.Zapato_detail,name='Zapato_detail'),
	path('zapato/<int:Zapato_id>/delete/',views.delete_zapato,name='zapato_delete'),
	path('facturas/',views.facturas,name='facturas'),
	path('facturas/create/',views.create_factura,name='create_clientes'),
	path('facturas/<int:factura_id>/',views.factura_detail,name='factura_detail'),
	path('facturas/<int:factura_id>/delete/',views.delete_factura,name='factura_delete'),
	path('facturas/<int:factura_id>/send', views.mi_vista_email, name='send_email_factura'),
	path('facturas/<int:factura_id>/paga/',views.pagar_factura,name='factura_paga'),
	path('facturas/<int:factura_id>/entrega/',views.entregar_factura,name='entregar_factura'),
	path('pedidos/',views.pedidos,name='pedidos'),
	path('pedidos/create/',views.create_pedido,name='create_pedido'),
	path('pedidos/<int:pedidos_id>/',views.pedidos_detail,name='pedidos_detail'),
	path('pedidos/<int:pedidos_id>/delete',views.delete_pedido,name='delete_pedido'),
	path('clientes/search',views.busqueda_clientes,name='search_cliente'),
	path('zapato/search',views.busqueda_zapato,name='search_zapato'),
	path('pedido/search',views.busqueda_pedido,name='search_pedido'),
	path('factura/search',views.busqueda_factura,name='search_factura'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
	path('graficas/', views.plotly_ventas_mes, name='ventas_por_mes'),
	path('obtener_ciudades/', views.obtener_ciudades, name='obtener_ciudades'),
	path('profile/', views.profile, name='profile'),
	path('profile/detail', views.profile_detail, name='profile_detail'),
	path('profile/encuestas', views.encuesta_detail, name='encuesta_detail'),




]
if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)