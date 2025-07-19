from django.urls import path
from .views import home_view
from .views import login_view, logout_view
from .views import register_view
from .views import obtener_departamento, obtener_ciudad, obtener_colonia

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # url js
    path('api/obtener-departamento/', obtener_departamento, name='obtener-departamento'),
    path('api/obtener-ciudad/', obtener_ciudad, name='obtener-ciudad'),
    path('api/obtener-colonia/', obtener_colonia, name='obtener-colonia'),
]