from django.shortcuts import render, redirect
from .db_utils import execute_query, execute_insert_returning_id, execute_insert
from .services import authenticate_user, register_user, traer_departamentos, traer_ciudades, traer_colonias, traer_vehiculo, traer_vehiculos, traer_vehiculos_alquiler, traer_vehiculos_venta
from .services import traer_cliente, traer_vehiculos, traer_empleado
from .utils import login_required
from django.http import JsonResponse
from .queries import QUERIES
import pyodbc
import datetime
from decimal import Decimal

# Create your views here.
# El orden de trabajo es: Template -> View -> url -> service -> Query

def home_view(request):
    vehiculos = traer_vehiculos()
    return render(request, 'home.html', {'vehiculos': vehiculos})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate_user(email, password)
        
        if user:
            id_usuario, email, rol_id = user
            request.session['user_id'] = id_usuario
            request.session['user_email'] = email
            request.session['rol_id'] = rol_id
            if rol_id == 1:

                return redirect('admin_view')
            elif rol_id == 2:
                return redirect('cliente_view')
            elif rol_id == 3:
                return redirect('empleado_view')
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def admin_view(request):
    return render(request, 'admin_home.html')

@login_required
def cliente_view(request):
    return render(request, 'cliente_home.html')

@login_required
def cliente_venta_view(request):
    vehiculos = traer_vehiculos_venta()
    return render(request, 'cliente_venta.html', {'vehiculos': vehiculos})

@login_required
def cliente_alquiler_view(request):
    vehiculos = traer_vehiculos_alquiler()
    return render(request, 'cliente_alquiler.html', {'vehiculos': vehiculos})

@login_required
def auto_view(request, id_vehiculo):
    vehiculo = traer_vehiculo(id_vehiculo)
    return render(request, 'visualizar_auto.html', {'vehiculo': vehiculo})

@login_required
def empleado_view(request):
    return render(request, 'empleado_home.html')

@login_required
def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('home')

def register_view(request):
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
            'sexo': request.POST.get('sexo'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password')
        }        
    
        # Convertir y validar IDs de los datos
        for valor in ['colonia_id', 'ciudad_id', 'departamento_id', 'pais_id']:
            if data[valor]:
                try:
                    data[valor] = int(data[valor])
                except ValueError:
                    return render(request, 'register.html', {'error': f'ID inválido para {valor}'})
            else:
                data[valor] = None

        register_user(data)
        return redirect('login')

    return render(request, 'register.html', {
        'colonias': colonias,
        'ciudades': ciudades,
        'departamentos': departamentos,
        'paises': paises
    })

def obtener_departamento(request):
    pais_id = request.GET.get('pais_id')
    datos = traer_departamentos(pais_id)
    return JsonResponse({'departamentos': datos})

def obtener_ciudad(request):
    departamento_id = request.GET.get('departamento_id')
    datos = traer_ciudades(departamento_id)
    return JsonResponse({'ciudades': datos})

def obtener_colonia(request):
    ciudad_id = request.GET.get('ciudad_id')
    datos = traer_colonias(ciudad_id)
    return JsonResponse({'colonias': datos})

def buscar_cliente(request):
    correo = request.GET.get('correo', '')
    if not correo:
        return JsonResponse({'clientes': []})
    
    clientes = execute_query(QUERIES['get_cliente_by_correo'], (f"%{correo}%",))
    clientes_data = [
        {
            'id_cliente': c[0],
            'nombre': f"{c[1]} {c[3]}",  # Primer nombre y primer apellido
            'correo': c[5]
        } for c in clientes
    ]
    return JsonResponse({'clientes': clientes_data})


#Gestion Contratos
@login_required
def contrato_venta_view(request):
    id_usuario = request.session.get('user_id')
    empleado = traer_empleado(id_usuario)
    cliente = None
    vehiculos = traer_vehiculos()

    if request.method == 'POST':
        data = {
            'empleado_id': empleado['id_empleado'],
            'cliente_id': request.POST.get('cliente_id'),
            'vehiculo_id': request.POST.get('vehiculo_id'),
            'fecha_contrato': datetime.datetime.now().strftime('%Y-%m-%d'),
            'terminos': request.POST.get('terminos', ''),
            'garantia': request.POST.get('garantia',),
            'recargo': request.POST.get('recargo', '0'),
            'tipo_contrato': 'Venta',
            'estado': 'Pendiente',
            'firma_cliente': request.POST.get('firma_cliente', ''),
            'monto': request.POST.get('monto', '0')
        }

        # Convertir y validar enteros
        for valor in ['cliente_id', 'vehiculo_id', 'empleado_id']:
            if data[valor]:
                try:
                    data[valor] = int(data[valor])
                except ValueError:
                    return render(request, 'contrato_venta.html', {
                        'vehiculos': vehiculos,
                        'error': f'ID inválido para {valor}'
                    })

        try:
            data['monto'] = Decimal(data['monto'])
            data['recargo'] = Decimal(data['recargo'])
        except Exception as e:
            return render(request, 'contrato_venta.html', {
                'vehiculos': vehiculos,
                'error': 'Monto, garantía o recargo inválido.'
            })

        contrato_id = execute_insert_returning_id(QUERIES['insert_contrato'], (
            data['empleado_id'],  
            data['cliente_id'],   
            data['vehiculo_id'],  
            data['fecha_contrato'],
            data['terminos'],         
            data['garantia'],         
            data['recargo'],          
            data['tipo_contrato'],    
            data['estado'],           
            data['firma_cliente']     
        ))

        execute_insert(QUERIES['insert_contrato_venta'], (
            contrato_id, data['fecha_contrato'], data['monto']
        ))

        return redirect('contrato_venta_view')

    return render(request, 'contrato_venta.html', {
        'vehiculos': vehiculos,
        'cliente': cliente,
        'empleado': empleado
    })


def contrato_alquiler_view(request):
    return render(request, 'contrato_alquiler.html')