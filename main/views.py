import os
import logging #Registra eventos (errores, advertencias, información) dureante la ejecución
from datetime import datetime
from .queries import QUERIES
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .utils import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .services import traer_cliente_id, traer_cliente_correo, traer_vehiculos, traer_empleado
from .services import crear_contrato_venta, actualizar_estado_vehiculo, crear_contrato_alquiler
from .db_utils import ejecutar_query
from .services import authenticate_user, register_user
from .services import traer_departamentos, traer_ciudades, traer_colonias
from .services import traer_vehiculo_id, traer_vehiculos, traer_vehiculos_alquiler, traer_vehiculos_venta, obtener_vehiculos_marcados

# Create your views here.
logger = logging.getLogger(__name__)

ruta_terminos_venta = os.path.join(settings.BASE_DIR, 'main' ,'templates' ,'contratos', 'textos_legales', 'terminos_venta.txt')
ruta_terminos_alquiler = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'terminos_alquiler.txt')
ruta_garantia = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'garantia_vehiculo.txt')
ruta_politica = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'politica_combustible.txt')
ruta_clausulas = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'clausulas.txt')

def home_view(request):
    vehiculos = traer_vehiculos()
    return render(request, 'vista_principal/home.html', {'vehiculos': vehiculos, 'show_particles': True})

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
                empleado = traer_empleado(id_usuario)
                if empleado:
                    request.session['empleado_id'] = empleado['id_empleado']
                return redirect('empleado_view')
        else:
            return render(request, 'vista_principal/login.html', {'error': 'Credenciales inválidas', 'show_particles': True})
    return render(request, 'vista_principal/login.html', {'show_particles': True})

@login_required
def admin_view(request):
    return render(request, 'usuarios/admin_home.html')

@login_required
def cliente_view(request):
    ids = request.session.get("vehiculos_marcados", [])
    marcados = obtener_vehiculos_marcados(ids)
    return render(request, 'usuarios/cliente_home.html', {
        "marcados": marcados,
        'show_particles': True
        })

@login_required
def empleado_view(request):
    return render(request, 'usuarios/empleado_home.html', {'show_particles': True})

@login_required
def cliente_venta_view(request):
    vehiculos = traer_vehiculos_venta()
    return render(request, 'usuarios/cliente_venta.html', {'vehiculos': vehiculos})

@login_required
def cliente_alquiler_view(request):
    vehiculos = traer_vehiculos_alquiler()
    return render(request, 'usuarios/cliente_alquiler.html', {'vehiculos': vehiculos})

@login_required
def auto_view(request, id_vehiculo):
    vehiculo = traer_vehiculo_id(id_vehiculo)
    # Verificar si está marcado
    marcados = request.session.get("vehiculos_marcados", [])
    ya_marcado = id_vehiculo in marcados

    return render(request, "vehiculos/visualizar_auto.html", {
        "vehiculo": vehiculo,
        "ya_marcado": ya_marcado,
    })

def marcar_vehiculo(request, id_vehiculo):
    if "vehiculos_marcados" not in request.session:
        request.session["vehiculos_marcados"] = []
        
    if id_vehiculo not in request.session["vehiculos_marcados"]:
        request.session["vehiculos_marcados"].append(id_vehiculo)
        request.session.modified = True
    return redirect("cliente_view")

def desmarcar_vehiculo(request, id_vehiculo):
    marcados = request.session.get("vehiculos_marcados", [])

    if id_vehiculo in marcados:
        marcados.remove(id_vehiculo)
        request.session["vehiculos_marcados"] = marcados

    return redirect("cliente_view")

@login_required
def logout_view(request):
    request.session.flush()  # Elimina todos los datos de la sesión
    return redirect('home')

def register_view(request):
    # Obtener datos para el formulario de registro
    colonias = ejecutar_query(QUERIES['get_all_colonias'])
    ciudades = ejecutar_query(QUERIES['get_all_ciudades'])
    departamentos = ejecutar_query(QUERIES['get_all_departamentos'])
    paises = ejecutar_query(QUERIES['get_all_paises'])
    #tipo_exoneracion = execute_query(QUERIES['get_all_tipo_exoneracion'])

    # Convertir los resultados a diccionarios para el template
    colonias= [{'colonia_id': c[0], 'nombre': c[1]} for c in colonias]
    ciudades = [{'ciudad_id': c[0], 'nombre': c[1]} for c in ciudades]
    departamentos = [{'departamento_id': d[0], 'nombre': d[1]} for d in departamentos]
    paises = [{'pais_id': p[0], 'nombre': p[1]} for p in paises]
    #tipo_exoneracion = [{'tipo_exoneracion_id': t[0], 'nombre': t[1]} for t in tipo_exoneracion]
    
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
                    return render(request, 'vista_principal/register.html', {'error': f'ID inválido para {valor}'})
            else:
                data[valor] = None
        try:
            register_user(data)
            return redirect('login')
        except ValueError as ve:
            return render(request, 'vista_principal/register.html', {
            'colonias': colonias,
            'ciudades': ciudades,
            'departamentos': departamentos,
            'paises': paises,
            'show_particles': True,
            'error_mensaje': str(ve),
            })

    return render(request, 'vista_principal/register.html', {
        'colonias': colonias,
        'ciudades': ciudades,
        'departamentos': departamentos,
        'paises': paises,
        'show_particles': True
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

def contrato_creado_venta(request):
    return render(request, 'contratos/contrato_venta_exito.html')

def contrato_creado_alquiler(request):
    return render(request, 'contratos/contrato_alquiler_exito.html')

def leer_archivos_terminos_y_garantia_venta():
    with open(ruta_terminos_venta, "r", encoding="utf-8") as f:
        terminos_venta = f.read()
    with open(ruta_garantia, "r", encoding="utf-8") as f:
        garantia = f.read()
    return terminos_venta, garantia

def leer_archivos_terminos_y_garantia_alquiler():
    with open(ruta_terminos_alquiler, "r", encoding="utf-8") as f:
        terminos_alquiler = f.read()
    with open(ruta_garantia, "r", encoding="utf-8") as f:
        garantia = f.read()
    with open(ruta_politica, "r", encoding="utf-8") as f:
        politica = f.read()
    with open(ruta_clausulas, "r", encoding="utf-8") as f:
        clausulas = f.read()
    return terminos_alquiler, garantia, politica, clausulas

# Vista para crear un Contrato Venta
@login_required
def contrato_venta_view(request):
    terminos_venta, garantia = leer_archivos_terminos_y_garantia_venta()
    paso = int(request.GET.get('paso', 1))

    # Manejadores para cada paso
    def manejar_paso_1():
        if request.method == "POST":
            correo = request.POST.get("correo", "").strip()
            if not correo:
                messages.error(request, "El correo es obligatorio")
                return render(request, "contratos/contrato_venta_cliente.html")
            
            cliente = traer_cliente_correo(correo)
            if not cliente:
                messages.error(request, "Cliente no encontrado")
                return render(request, "contratos/contrato_venta_cliente.html")
            
            request.session["cliente_id"] = cliente["id_cliente"]
            request.session["cliente_correo"] = cliente["correo"]
            return redirect(f"{reverse('contrato_venta_view')}?paso=2")
        
        return render(request, "contratos/contrato_venta_cliente.html")

    def manejar_paso_2():
        if request.method == "POST":
            id_vehiculo = request.POST.get("id_vehiculo")
            if not id_vehiculo:
                messages.error(request, "Debes seleccionar un vehículo")
            else:
                request.session["id_vehiculo"] = id_vehiculo
                return redirect(f"{reverse('contrato_venta_view')}?paso=3")
        
        vehiculos = traer_vehiculos_venta()
        return render(request, "contratos/contrato_venta_vehiculo.html", {"vehiculos": vehiculos})

    def manejar_paso_3():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("id_vehiculo")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_venta_view')}?paso=4")

        if request.method == "POST":
            if request.POST.get("acepto_terminos") != "on":
                messages.error(request, "Debes aceptar los términos para continuar")
                return render(request, "contratos/contrato_venta_confirmar.html", {
                    **sesion_datos, # **desempaquetador de diccionarios
                    "terminos": terminos_venta,
                    "garantia": garantia,
                })
            return redirect(f"{reverse('contrato_venta_view')}?paso=4")
        
        return render(request, "contratos/contrato_venta_confirmar.html", {
            **sesion_datos,
            "terminos": terminos_venta,
            "garantia": garantia,
        })

    def manejar_paso_4():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("id_vehiculo")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_venta_view')}?paso=1")

        if request.method == "POST":
            try:
                data = {
                    "cliente_id": request.session["cliente_id"],
                    "id_vehiculo": request.session["id_vehiculo"],
                    "empleado_id": request.session.get("user_id"),
                    "fecha": datetime.now(),
                    "terminos": terminos_venta,
                    "garantia": garantia,
                    "tipo_contrato": "Venta",
                    "estado": request.POST.get("estado"),
                    "firma": 1 if request.POST.get("firma") == "on" else 0,
                    "monto": float(request.POST.get("monto", 0)),
                }
                
                crear_contrato_venta(data)
                actualizar_estado_vehiculo(data['id_vehiculo'])
                
                # Limpiar solo las keys usadas
                for key in ["cliente_id", "id_vehiculo", "empleado_id"]:
                    request.session.pop(key, None)
                
                messages.success(request, "Contrato creado exitosamente")
                return redirect("contrato_exito_venta")
            
            except Exception as e:
                logger.error(f"Error al crear contrato: {str(e)}", exc_info=True)
                messages.error(request, "Error interno al procesar el contrato")
                return render(request, "contratos/contrato_venta_formulario.html", sesion_datos)
        
        return render(request, "contratos/contrato_venta_formulario.html", sesion_datos)

    # Router de pasos
    manejadores = {
        1: manejar_paso_1,
        2: manejar_paso_2,
        3: manejar_paso_3,
        4: manejar_paso_4,
    }
    
    return manejadores.get(paso, lambda: redirect(f"{reverse('contrato_venta_view')}?paso=1"))()

# Vista para crear un Contrato Alquiler
@login_required
def contrato_alquiler_view(request):
    terminos_alquiler, garantia, politica, clausulas = leer_archivos_terminos_y_garantia_alquiler()
    paso = int(request.GET.get('paso', 1))
    
    # Manejadores para cada paso
    def manejar_paso_1():
        if request.method == "POST":
            correo = request.POST.get("correo", "").strip()
            if not correo:
                messages.error(request, "El correo es obligatorio")
                return render(request, "contratos/contrato_alquiler_cliente.html")
            
            cliente = traer_cliente_correo(correo)
            if not cliente:
                messages.error(request, "Cliente no encontrado")
                return render(request, "contratos/contrato_alquiler_cliente.html")
            
            request.session["cliente_id"] = cliente["id_cliente"]
            request.session["cliente_correo"] = cliente["correo"]
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=2")
        
        return render(request, "contratos/contrato_alquiler_cliente.html")

    def manejar_paso_2():
        if request.method == "POST":
            id_vehiculo = request.POST.get("id_vehiculo")
            if not id_vehiculo:
                messages.error(request, "Debes seleccionar un vehículo")
            else:
                request.session["id_vehiculo"] = id_vehiculo
                return redirect(f"{reverse('contrato_alquiler_view')}?paso=3")
        
        vehiculos = traer_vehiculos_alquiler()
        return render(request, "contratos/contrato_alquiler_vehiculo.html", {"vehiculos": vehiculos})
    
    def manejar_paso_3():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("id_vehiculo")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=1")

        if request.method == "POST":
            if request.POST.get("acepto_terminos") != "on":
                messages.error(request, "Debes aceptar los términos para continuar")
                return render(request, "contratos/contrato_alquiler_confirmar.html", {
                    **sesion_datos, # **desempaquetador de diccionarios
                    "terminos": terminos_alquiler,
                    "garantia": garantia,
                    "politica": politica,
                    "clausula": clausulas
                })
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=4")
        
        return render(request, "contratos/contrato_alquiler_confirmar.html", {
            **sesion_datos,
            "terminos": terminos_alquiler,
            "garantia": garantia,
            "politica": politica,
            "clausula": clausulas
        })

    def manejar_paso_4():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("id_vehiculo")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=1")

        if request.method == "POST":
            try:
                fecha_inicio = datetime.strptime(request.POST.get("fecha_inicio"), "%Y-%m-%d")
                fecha_fin = datetime.strptime(request.POST.get("fecha_fin"), "%Y-%m-%d")
                # fecha_entrega_real_raw = request.POST.get("fecha_entrega_real")
                # fecha_entrega_real = datetime.strptime(fecha_entrega_real_raw, "%Y-%m-%d")

                data = {
                    "cliente_id": request.session["cliente_id"],
                    "id_vehiculo": request.session["id_vehiculo"],
                    "empleado_id": request.session.get("user_id"),
                    "fecha": datetime.now(),
                    "terminos": terminos_alquiler,
                    "garantia": garantia,
                    "tipo_contrato": "Alquiler",
                    "estado": request.POST.get("estado"),
                    "firma": 1 if request.POST.get("firma") == "on" else 0,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin,
                    # "fecha_entrega_real": fecha_entrega_real,
                    "kilometraje": int(request.POST.get("kilometraje", 0)),
                    "politica_combustible": politica,
                    # "es_tardia": 1 if request.POST.get("es_tardia") == "on" else 0,
                    "es_extensible": 1 if request.POST.get("es_extensible") == "on" else 0,
                    "reporte_danios": request.POST.get("reporte_danios"),
                    "clausulas": clausulas,
                    "recargo_incumplimiento": float(request.POST.get("recargo_incumplimiento", 0)),
                }
                
                crear_contrato_alquiler(data)
                actualizar_estado_vehiculo(data['id_vehiculo'])
                
                # Limpiar solo las keys usadas
                for key in ["cliente_id", "id_vehiculo", "empleado_id"]:
                    request.session.pop(key, None)
                
                messages.success(request, "Contrato creado exitosamente")
                return redirect("contrato_exito_alquiler")
            
            except Exception as e:
                logger.error(f"Error al crear contrato: {str(e)}", exc_info=True)
                messages.error(request, "Error interno al procesar el contrato")
                return render(request, "contratos/contrato_alquiler_formulario.html", sesion_datos)
        
        return render(request, "contratos/contrato_alquiler_formulario.html", sesion_datos)

    # Router de pasos
    manejadores = {
        1: manejar_paso_1,
        2: manejar_paso_2,
        3: manejar_paso_3,
        4: manejar_paso_4,
    }
    
    return manejadores.get(paso, lambda: redirect(f"{reverse('contrato_alquiler_view')}?paso=1"))()