from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view
from .views import login_view, logout_view
from .views import register_view
from .views import obtener_departamento, obtener_ciudad, obtener_colonia
from .views import admin_view, cliente_view, empleado_view
from .views import cliente_venta_view, cliente_alquiler_view
from .views import auto_view
from .views import contrato_venta_view, contrato_alquiler_view, contrato_venta_view, contrato_alquiler_view
from .views import marcar_vehiculo, desmarcar_vehiculo
from .views import contrato_venta_view, contrato_alquiler_view, contrato_creado_venta, contrato_creado_alquiler
from .views import facturacion_venta, factura_venta_creada, facturacion_alquiler
from .views import seleccionar_contratos


urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    path('admin/', admin_view, name='admin_view'),
    path('cliente/', cliente_view, name='cliente_view'),
    path('empleado/', empleado_view, name='empleado_view'),
    path('cliente/venta', cliente_venta_view, name='cliente_venta_view'),
    path('cliente/alquiler', cliente_alquiler_view, name='cliente_alquiler_view'),

    path('contrato/', contrato_venta_view, name='contrato_venta_view'),
    path('contrato-exito-venta/', contrato_creado_venta, name='contrato_exito_venta'),
    path('contrato-alquiler/', contrato_alquiler_view, name='contrato_alquiler_view'),
    path('contrato-exito-alquiler/', contrato_creado_alquiler, name='contrato_exito_alquiler'),
    
    
    path('facturacion/Venta/', facturacion_venta, name='factura_venta'),
    path('facturacion-venta-exito/', factura_venta_creada, name='factura_venta_exito'),
    
    path('facturacion/Alquiler/', facturacion_alquiler, name='factura_alquiler'),

    #path('facturacion-alquiler-exito/', factura_alquiler_creada, name='factura_alquiler_exito'),
    #path('facturacion-venta/seleccionar/', seleccionar_contratos, name='seleccionar_contrato_factura'),

    path('seleccionar-contratos/', seleccionar_contratos, name='seleccionar_contratos'),

    path('auto/<int:id_vehiculo>/', auto_view, name='auto'),
    path("marcar/<int:id_vehiculo>/", marcar_vehiculo, name="marcar_vehiculo"),
    path("desmarcar/<int:id_vehiculo>/", desmarcar_vehiculo, name="desmarcar_vehiculo"),

    # url js
    path('api/obtener-departamento/', obtener_departamento, name='obtener-departamento'),
    path('api/obtener-ciudad/', obtener_ciudad, name='obtener-ciudad'),
    path('api/obtener-colonia/', obtener_colonia, name='obtener-colonia'),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

"""
Toyota Corolla 2023 ROJO
Toyota Tacoma 2022 ROJO
Honda Civic 2023 BLANCO
Honda Fit 2021 NEGRO
Nissan Sentra 2022 BLANCO
Nissan Frontier 2021 BLANCO
Ford Focus 2020 AZUL
Ford Mustang 2022 AZUL

1 admin
2 cliente
3 empleado
"""