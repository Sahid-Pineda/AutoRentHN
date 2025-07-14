from django.shortcuts import render, redirect
from .db_utils import execute_query, execute_insert_returning_id
from .services import hash_password, authenticate_user, register_user
from .utils import login_required
from django.http import HttpResponse
from .queries import QUERIES
import pyodbc

# Create your views here.
# El orden de trabajo es: Template -> View -> url -> service -> Query

@login_required
def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate_user(email, password)
        if user:
            id_usuario, email = user
            request.session['user_id'] = id_usuario
            request.session['user_email'] = email
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('login')

def register_view(request):
    print("POST DATA:", request.POST)
    if request.method == 'POST':
        data = {
            'primer_nombre': request.POST.get('primer_nombre'),
            'segundo_nombre': request.POST.get('segundo_nombre'),
            'primer_apellido': request.POST.get('primer_apellido'),
            'segundo_apellido': request.POST.get('segundo_apellido'),
            'telefono': request.POST.get('telefono'),
            'descripcion': request.POST.get('descripcion'),
            'colonia_id': request.POST.get('colonia_id'),
            'ciudad_id': request.POST.get('ciudad_id'),
            'departamento_id': request.POST.get('departamento_id'),
            'pais_id': request.POST.get('pais_id'),
            'tipo_exoneracion': request.POST.get('tipo_exoneracion'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }

        if not data['colonia_id']:
            return render(request, 'register.html', {'error': 'Debes seleccionar una colonia.'})

    
        # Convertir y validar IDs de los datos
        for valor in ['colonia_id', 'ciudad_id', 'departamento_id', 'pais_id', 'tipo_exoneracion']:
            if data[valor]:
                try:
                    data[valor] = int(data[valor])
                except ValueError:
                    return render(request, 'register.html', {'error': f'ID inválido para {valor}'})
            else:
                data[valor] = None

        register_user(data)
        return HttpResponse("Usuario registrado exitosamente")

    # Obtener datos para el formulario de registro
    colonias = execute_query(QUERIES['get_all_colonias'])
    ciudades = execute_query(QUERIES['get_all_ciudades'])
    departamentos = execute_query(QUERIES['get_all_departamentos'])
    paises = execute_query(QUERIES['get_all_paises'])
    tipo_exoneracion = execute_query(QUERIES['get_all_tipo_exoneracion'])

    # Convertir los resultados a diccionarios para el template
    colonias= [{'colonia_id': c[0], 'nombre': c[1]} for c in colonias]
    ciudades = [{'ciudad_id': c[0], 'nombre': c[1]} for c in ciudades]
    departamentos = [{'departamento_id': d[0], 'nombre': d[1]} for d in departamentos]
    paises = [{'pais_id': p[0], 'nombre': p[1]} for p in paises]
    tipo_exoneracion = [{'tipo_exoneracion_id': t[0], 'nombre': t[1]} for t in tipo_exoneracion]

    return render(request, 'register.html', {
        'colonias': colonias,
        'ciudades': ciudades,
        'departamentos': departamentos,
        'paises': paises,
        'tipo_exoneracion': tipo_exoneracion
    })
