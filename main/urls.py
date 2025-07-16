from django.urls import path
from .views import home_view
from .views import login_view, logout_view
from .views import register_view
from .views import get_ubicacion

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),

    # url js
    path('api/get_ubicacion/', get_ubicacion, name='get_ubicacion'),
]