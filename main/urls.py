from django.urls import path
from .views import home_view
from .views import login_view, logout_view
from .views import register_view
from .views import obtener_departamento, obtener_ciudad, obtener_colonia, buscar_cliente
from .views import admin_view, cliente_view, empleado_view
from .views import cliente_venta_view, cliente_alquiler_view
from .views import auto_view
from .views import contrato_venta_view, contrato_alquiler_view, buscar_cliente

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

    path('contrato-venta/', contrato_venta_view, name='contrato_venta_view'),
    path('contrato-alquiler/', contrato_alquiler_view, name='contrato_alquiler_view'),
    

    path('auto/<int:id_vehiculo>/', auto_view, name='auto'),

    # url js
    path('api/obtener-departamento/', obtener_departamento, name='obtener-departamento'),
    path('api/obtener-ciudad/', obtener_ciudad, name='obtener-ciudad'),
    path('api/obtener-colonia/', obtener_colonia, name='obtener-colonia'),
    path('api/buscar-cliente/', buscar_cliente, name='buscar_cliente_api'),

]