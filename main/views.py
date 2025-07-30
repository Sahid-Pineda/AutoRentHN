import os
import logging #Registra eventos (errores, advertencias, información) dureante la ejecución
from .queries import QUERIES
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from .utils import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .services import traer_cliente_id, traer_cliente_correo, traer_vehiculos, traer_empleado
from .services import crear_contrato_venta, actualizar_estado_vehiculo, crear_contrato_alquiler
from .db_utils import execute_query, get_db_connection
from .services import authenticate_user, register_user, traer_departamentos, traer_ciudades, traer_colonias
from .services import traer_vehiculo_id, traer_vehiculos, traer_vehiculos_alquiler, traer_vehiculos_venta

# Create your views here.

ruta_terminos_venta = os.path.join(settings.BASE_DIR, 'main' ,'templates' ,'contratos', 'textos_legales', 'terminos_venta.txt')
ruta_terminos_alquiler = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'terminos_alquiler.txt')
ruta_garantia = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'garantia_vehiculo.txt')
ruta_politica = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'politica_combustible.txt')
ruta_clausulas = os.path.join(settings.BASE_DIR, 'main' ,'templates' , 'contratos', 'textos_legales', 'clausulas.txt')

def home_view(request):
    vehiculos = traer_vehiculos()
    return render(request, 'vista_principal/home.html', {'vehiculos': vehiculos})

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
            return render(request, 'vista_principal/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'vista_principal/login.html')

@login_required
def admin_view(request):
    return render(request, 'usuarios/admin_home.html')

@login_required
def cliente_view(request):
    ids = request.session.get("vehiculos_marcados", [])
    marcados = [] # Vehiculos Marcados

    if ids:
        placeholders = ",".join("?" for _ in ids)
        query = f"""
        SELECT  v.id_Vehiculo AS id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
            v.VIN AS vin, v.Motor AS motor, v.MatriculaPlaca AS placa, 
            tv.nombreTipo AS tipo_nombre, tv.descripcion AS tipo_descripcion, 
            uv.descripcion AS uso_descripcion, v.PrecioVenta AS precio_de_venta, 
            v.PrecioAlquiler AS precio_de_alquiler, v.Estado AS estado, 
            v.TipoCombustible AS tipo_de_combustible,
            v.Url_Vehiculo AS url_vehiculo, v.KilometrajeActual AS Kilometraje,
            v.UltimoMantenimiento AS Ultimo_Mantenimiento
        FROM Vehiculo v
        INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
        INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
        INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
        INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
        WHERE v.id_Vehiculo IN ({placeholders})
    """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, ids)
        columns = [col[0] for col in cursor.description]
        marcados = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()

    return render(request, "usuarios/cliente_home.html", {"marcados": marcados,})

@login_required
def empleado_view(request):
    return render(request, 'usuarios/empleado_home.html')

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
                    return render(request, 'vista_principal/register.html', {'error': f'ID inválido para {valor}'})
            else:
                data[valor] = None

        register_user(data)
        return redirect('login')

    return render(request, 'vista_principal/register.html', {
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

def contrato_venta_view(request):
    return render(request, 'contratos/contrato_venta_exito.html')

def contrato_alquiler_view(request):
    return render(request, 'contratos/contrato_alquiler_exito.html')

def obtener_datos_sesion():
    pass

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


logger = logging.getLogger(__name__)
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
            vehiculo_id = request.POST.get("vehiculo_id")
            if not vehiculo_id:
                messages.error(request, "Debes seleccionar un vehículo")
            else:
                request.session["vehiculo_id"] = vehiculo_id
                return redirect(f"{reverse('contrato_venta_view')}?paso=3")
        
        vehiculos = traer_vehiculos_venta()
        return render(request, "contratos/contrato_venta_vehiculo.html", {"vehiculos": vehiculos})

    def manejar_paso_3():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("vehiculo_id")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_venta_view')}?paso=1")

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
            "vehiculo": traer_vehiculo_id(request.session.get("vehiculo_id")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_venta_view')}?paso=1")

        if request.method == "POST":
            try:
                data = {
                    "cliente_id": request.session["cliente_id"],
                    "vehiculo_id": request.session["vehiculo_id"],
                    "empleado_id": request.session.get("user_id"),
                    "fecha": request.POST.get("fecha"),
                    "terminos": terminos_venta,
                    "garantia": garantia,
                    "tipo_contrato": "Venta",
                    "estado": "Activo",  # Valor por defecto
                    "firma": 1 if request.POST.get("firma") == "on" else 0,
                    "monto": float(request.POST.get("monto", 0)),
                }
                
                crear_contrato_venta(data)
                actualizar_estado_vehiculo(data['vehiculo_id'])
                
                # Limpiar solo las keys usadas
                for key in ["cliente_id", "vehiculo_id", "empleado_id"]:
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

#Gestion Contratos
"""@login_required
def contrato_venta_view(request):
    terminos_venta, terminos_alquiler, garantia = leer_archivos_terminos_y_garantia()
    paso = int(request.GET.get('paso', 1))

    if paso == 1:
        if request.method == "POST":
            correo = request.POST.get("correo")
            cliente = traer_cliente_correo(correo)
            if cliente:
                request.session["cliente_id"] = cliente["id_cliente"]
                request.session["cliente_correo"] = cliente["correo"]
                return redirect("/contrato/?paso=2")
            else:
                return render(request, "contratos/contrato_venta_cliente.html", {'error': 'Cliente no encontrado'})
        return render(request, "contratos/contrato_venta_cliente.html")

    elif paso == 2:
        if request.method == "POST":
            vehiculo_id = request.POST.get("vehiculo_id")
            print("DEBUG vehiculo_id recibido:", vehiculo_id)
            if vehiculo_id:
                request.session["vehiculo_id"] = vehiculo_id
                return redirect("/contrato/?paso=3")
        vehiculos = traer_vehiculos_venta()
        return render(request, "contratos/contrato_venta_vehiculo.html", {"vehiculos": vehiculos})

    elif paso == 3:

        cliente_id = request.session.get("cliente_id")
        vehiculo_id = request.session.get("vehiculo_id")
        usuario_id = request.session.get("user_id")

        cliente = traer_cliente_id(cliente_id)
        vehiculo = traer_vehiculo(vehiculo_id)
        empleado_info = traer_empleado(usuario_id)

        if not all([cliente, vehiculo, empleado_info]):
            return redirect("/contrato/?paso=1")

        request.session["empleado_id"] = empleado_info["id_empleado"]

        if request.method == "POST":
            if request.POST.get("acepto_terminos") == "on":
                return redirect("/contrato/?paso=4")
                #request.session["terminos"] = terminos_venta
                #request.session["garantia"] = garantia
            else:
                return render(request, "contratos/contrato_venta_formulario.html", {
                    "cliente": cliente,
                    "vehiculo": vehiculo,
                    "terminos": terminos_venta,
                    "garantia": garantia,
                    "error": "Debes aceptar los términos para continuar"
                })

        return render(request, "contratos/contrato_venta_confirmar.html", {
            "cliente": cliente,
            "vehiculo": vehiculo,
            "empleado": empleado_info,
            "terminos": terminos_venta,
            "garantia": garantia,
        })

    elif paso == 4:
        cliente_id = request.session.get("cliente_id")
        vehiculo_id = request.session.get("vehiculo_id")
        usuario_id = request.session.get("user_id")

        cliente = traer_cliente_id(cliente_id)
        vehiculo = traer_vehiculo(vehiculo_id)
        empleado_info = traer_empleado(usuario_id)
        
        if request.method == "POST":
            try:
                data = {
                    "cliente_id": request.session["cliente_id"],
                    "vehiculo_id": request.session["vehiculo_id"],
                    "empleado_id": request.session.get("empleado_id"),
                    "fecha": request.POST.get("fecha"),
                    "terminos": terminos_venta,
                    "garantia": garantia,
                    "tipo_contrato": request.POST.get("tipo_contrato"),
                    "estado": request.POST.get("estado"),
                    "firma": 1 if request.POST.get("firma") == "on" else 0,
                    "monto": request.POST.get("monto")
                }
                print("Datos del contrato a insertar:", data)
                crear_contrato_venta(data)
                actualizar_estado_vehiculo(data['vehiculo_id'])
                request.session.flush()
                return redirect("contrato_exito")
            except Exception as e:
                print("ERROR: 0", e)
                return render(request, "contratos/contrato_venta_formulario.html", {
                    "cliente": cliente,
                    "vehiculo": vehiculo,
                    "empleado": empleado_info,
                })
        return render(request, "contratos/contrato_venta_formulario.html", {
        "cliente": cliente,
        "vehiculo": vehiculo,
        "empleado": empleado_info,
        })
    return redirect("/contrato/?paso=1")
"""

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
            vehiculo_id = request.POST.get("vehiculo_id")
            if not vehiculo_id:
                messages.error(request, "Debes seleccionar un vehículo")
            else:
                request.session["vehiculo_id"] = vehiculo_id
                return redirect(f"{reverse('contrato_alquiler_view')}?paso=3")
        
        vehiculos = traer_vehiculos_alquiler()
        return render(request, "contratos/contrato_alquiler_vehiculo.html", {"vehiculos": vehiculos})
    
    def manejar_paso_3():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("vehiculo_id")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_venta_view')}?paso=1")

        if request.method == "POST":
            if request.POST.get("acepto_terminos") != "on":
                messages.error(request, "Debes aceptar los términos para continuar")
                return render(request, "contratos/contrato_alquiler_confirmar.html", {
                    **sesion_datos, # **desempaquetador de diccionarios
                    "terminos": terminos_alquiler,
                    "garantia": garantia,
                })
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=4")
        
        return render(request, "contratos/contrato_alquiler_confirmar.html", {
            **sesion_datos,
            "terminos": terminos_alquiler,
            "garantia": garantia,
        })

    def manejar_paso_4():
        # Validar datos de sesión
        sesion_datos = {
            "cliente": traer_cliente_id(request.session.get("cliente_id")),
            "vehiculo": traer_vehiculo_id(request.session.get("vehiculo_id")),
            "empleado": traer_empleado(request.session.get("user_id")),
        }
        
        if not all(sesion_datos.values()):
            messages.error(request, "Datos incompletos. Comienza nuevamente.")
            return redirect(f"{reverse('contrato_alquiler_view')}?paso=1")

        if request.method == "POST":
            try:
                data = {
                    "cliente_id": request.session["cliente_id"],
                    "vehiculo_id": request.session["vehiculo_id"],
                    "empleado_id": request.session.get("user_id"),
                    "fecha": request.POST.get("fecha"),
                    "terminos": terminos_alquiler,
                    "garantia": garantia,
                    "tipo_contrato": "Alquiler",
                    "estado": "Activo",
                    "firma": 1 if request.POST.get("firma") == "on" else 0,
                    "fecha_inicio": request.POST.get["fecha_inicio"],
                    "fecha_fin": request.POST.get["fecha_fin"],
                    "fecha_entrega_real": request.POST.get["fecha_entrega_real"],
                    "kilometraje": request.POST.get["kilometraje"],
                    "politica_combustible": politica,
                    "es_tardia": 1 if request.POST.get("es_tardia") == "on" else 0,
                    "es_extensible": 1 if request.POST.get("es_extensible") == "on" else 0,
                    "reporte_danios": request.POST.get("reporte_danios"),
                    "clausulas": clausulas,
                    "recargo_incumplimiento": float(request.POST.get("recargo_incumplimiento", 0)),
                }
                
                crear_contrato_alquiler(data)
                actualizar_estado_vehiculo(data['vehiculo_id'])
                
                # Limpiar solo las keys usadas
                for key in ["cliente_id", "vehiculo_id", "empleado_id"]:
                    request.session.pop(key, None)
                
                messages.success(request, "Contrato creado exitosamente")
                return redirect("contrato_exito")
            
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
    
    return manejadores.get(paso, lambda: redirect(f"{reverse('contrato_alquiler_view')}?paso=1"))()

"""@login_required
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
    })"""