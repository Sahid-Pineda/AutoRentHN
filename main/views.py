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
from .services import crear_contrato_venta, actualizar_estado_vehiculo, crear_contrato_alquiler, actualizar_estado_contrato
from .db_utils import ejecutar_query
from .services import authenticate_user, register_user
from .services import traer_departamentos, traer_ciudades, traer_colonias
from .services import traer_vehiculo_id, traer_vehiculos, traer_vehiculos_alquiler, traer_vehiculos_venta, obtener_vehiculos_marcados
from .services import traer_contrato_venta_id, traer_contrato_alquiler_id,registrar_factura_y_pago, traer_contratos, obtener_metodos_pago, obtener_rangos_facturacion_disponibles
from .services import obtener_siguiente_numero_factura, traer_contrato_id, traer_documentos_fiscales

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
    tipo_exoneracion = ejecutar_query(QUERIES['get_all_tipo_exoneracion'])

    # Convertir los resultados a diccionarios para el template
    colonias= [{'colonia_id': c[0], 'nombre': c[1]} for c in colonias]
    ciudades = [{'ciudad_id': c[0], 'nombre': c[1]} for c in ciudades]
    departamentos = [{'departamento_id': d[0], 'nombre': d[1]} for d in departamentos]
    paises = [{'pais_id': p[0], 'nombre': p[1]} for p in paises]
    tipo_exoneracion = [{'tipo_exoneracion_id': t[0], 'descripcion': t[2]} for t in tipo_exoneracion]
    
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
            'password': request.POST.get('password'),
            'rtn': request.POST.get('rtn'),
            'tipo_contribuyente': request.POST.get('tipo_contribuyente'),
            'tipo_exoneracion': request.POST.get('tipo_exoneracion_id'),
        }        
    
        # Convertir y validar IDs de los datos
        for valor in ['colonia_id', 'ciudad_id', 'departamento_id', 'pais_id', 'tipo_exoneracion']:
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
            'tipo_exoneracion': tipo_exoneracion,
            'show_particles': True,
            'error_mensaje': str(ve),
            })

    return render(request, 'vista_principal/register.html', {
        'colonias': colonias,
        'ciudades': ciudades,
        'departamentos': departamentos,
        'paises': paises,
        'tipo_exoneracion': tipo_exoneracion,
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

def factura_venta_creada(request):
    return render(request, 'facturacion/factura_venta_exito.html')

def factura_alquiler_creada(request):
    return render(request, 'facturacion/factura_alquiler_exito.html')

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
                messages.success(request, "Contrato creado satisfactoriamente.")
                actualizar_estado_vehiculo(data['id_vehiculo'])

                # Limpiar solo las keys usadas
                for key in ["cliente_id", "id_vehiculo", "empleado_id"]:
                    request.session.pop(key, None)
                
                messages.success(request, "Contrato creado exitosamente")
                return redirect(reverse("contrato_exito_venta"))
            
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
                fecha_entrega_real_raw = request.POST.get("fecha_entrega_real")
                fecha_entrega_real = datetime.strptime(fecha_entrega_real_raw, "%Y-%m-%d")

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
                    "fecha_entrega_real": fecha_entrega_real,
                    "kilometraje": int(request.POST.get("kilometraje", 0)),
                    "politica_combustible": politica,
                    "es_tardia": 1 if request.POST.get("es_tardia") == "on" else 0,
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

@login_required
def seleccionar_documentos_fiscales(request):
    estado = request.GET.get('estado', None)
    tipo = request.GET.get('tipo', None)
    cliente = request.GET.get('cliente', None)

    documentos = traer_documentos_fiscales(estado, tipo, cliente)
    
    data = {
        'documentos': documentos,
        'estado_seleccionado': estado,
        'tipo_seleccionado': tipo,
        'cliente_buscado': cliente,
        'estados_disponibles': ['Emitido', 'Anulado', 'Pendiente'],
        'tipos_disponibles': ['Alquiler', 'Venta'],
    }   
    return render(request, "facturacion/seleccionar_documento_fiscal.html", data)

@login_required
def seleccionar_contratos(request):
    if request.method == "POST":
        contrato_info = request.POST.get("contrato_info")
        if not contrato_info or "|" not in contrato_info:
            messages.error(request, "Debe seleccionar un contrato válido.")
            return redirect('seleccionar_contratos')
    
        contrato_id, tipo_contrato = contrato_info.split("|")
        
        # Validar que el contrato existe
        contrato = traer_contrato_id(contrato_id)
        if not contrato:
            messages.error(request, "El contrato seleccionado no existe.")
            return redirect('seleccionar_contratos')
            
        # Limpiar datos previos de la sesión
        request.session.pop('id_contrato', None)
        request.session.pop('tipo_contrato', None)
        
        # Almacenar en sesión
        request.session['id_contrato'] = contrato_id
        request.session['tipo_contrato'] = tipo_contrato
        
        logger.debug(f"Redirigiendo a facturación de {tipo_contrato} con ID {contrato_id}")
        
        # Redirigir según el tipo de contrato
        if tipo_contrato == "Venta":
            return redirect('factura_venta')
        elif tipo_contrato == "Alquiler":
            return redirect('factura_alquiler')
        else:
            messages.error(request, "Tipo de contrato no reconocido.")
            return redirect('seleccionar_contratos')
    
    estado = request.GET.get('estado', None)
    tipo = request.GET.get('tipo', None)
    cliente = request.GET.get('cliente', None)

    contratos = traer_contratos(estado, tipo, cliente)
    logger.debug(f"Contratos encontrados: {contratos}")
    data = {
        'contratos': contratos,
        'estado_seleccionado': estado,
        'tipo_seleccionado': tipo,
        'cliente_buscado': cliente,
        'estados_disponibles': ['Activo', 'Finalizado', 'Cancelado'],
        'tipos_disponibles': ['Alquiler', 'Venta',],
    }   
    return render(request, "facturacion/seleccionar_contrato.html", data)

@login_required
def facturacion_venta(request):
    context = {
        'factura': {
            'cliente': {
                'id': None,
                'nombre_completo': '',
                'telefono': '',
                'correo': '',
                'rtn': 'N/A'
            },
            'vehiculo': {
                'id': None,
                'marca': '',
                'modelo': '',
                'anio': '',
                'vin': '',
                'precio': 0.0
            },
            'empleado': {
                'nombre_completo': ''
            },
            'contrato': {
                'id': None,
                'tipo': '',
                'fecha': None,
                'monto': 0.0
            },
            'pagos': [],
            'calculos': {
                'subtotal': 0.0,
                'impuesto': 0.0,
                'total': 0.0,
                'cantidad': 1
            },
            'cai': '',
            'numero_documento_fiscal': ''
        }
    }

    contrato_id = request.session.get('id_contrato')
    if not contrato_id:
        logger.warning("No se encontró id_contrato en la sesión")
        messages.error(request, "No se encontró el contrato en la sesión.")
        return redirect(reverse('seleccionar_contratos'))

    try:
        contrato = traer_contrato_venta_id(contrato_id)
        if not contrato:
            logger.error(f"Contrato con ID {contrato_id} no encontrado")
            messages.error(request, "El contrato no fue encontrado.")
            return redirect(reverse('seleccionar_contratos'))

        cliente = traer_cliente_id(contrato.get('cliente_id'))
        vehiculo = traer_vehiculo_id(contrato.get('vehiculo_id'))
        empleado = traer_empleado(request.session.get('user_id'))
        metodos_pago = obtener_metodos_pago()
        rangos_facturacion = obtener_rangos_facturacion_disponibles()  # Factura de venta
        
        if not rangos_facturacion:
            logger.error("No se encontraron rangos autorizados válidos para facturación de venta")
            messages.error(request, "No se encontró un rango autorizado válido para la facturación.")
            return redirect(reverse('seleccionar_contratos'))

        if not all([cliente, vehiculo, empleado, metodos_pago, rangos_facturacion]):
            logger.error("Faltan datos relacionados al contrato")
            messages.error(request, "Error al obtener datos relacionados al contrato.")
            return redirect(reverse('seleccionar_contratos'))

        # Seleccionar rango de facturación automáticamente
        fecha_actual = datetime.now()
        rango_seleccionado = None
        for rango in rangos_facturacion:
            if (rango.get('TipoDocumento_id') == 1 and
                rango.get('FechaInicio') <= fecha_actual <= rango.get('FechaFin')):
                siguiente_numero = obtener_siguiente_numero_factura(rango)
                if siguiente_numero:
                    rango_seleccionado = rango
                    break

        if not rango_seleccionado:
            logger.error("No se encontró un rango de facturación válido")
            messages.error(request, "No hay rangos de facturación disponibles para la fecha actual.")
            return redirect(reverse('seleccionar_contratos'))

        cai = rango_seleccionado.get('CAI')
        numero_documento_fiscal = siguiente_numero

        subtotal = float(contrato.get('monto', 0))
        impuesto_total = round(subtotal * 0.15, 2) if cliente.get('tipoexoneracion_id') else 0.0
        total = subtotal + impuesto_total

        context['factura'].update({
            'cliente': {
                'id': cliente.get('cliente_id'),
                'nombre_completo': f"{cliente.get('nombre', '')} {cliente.get('segundonombre', '')} {cliente.get('apellido', '')} {cliente.get('segundoapellido', '')}".strip(),
                'telefono': cliente.get('telefono', 'N/A'),
                'correo': cliente.get('correo', 'N/A'),
                'rtn': cliente.get('rtn', 'N/A')
            },
            'vehiculo': {
                'id': vehiculo.get('id_vehiculo'),
                'marca': vehiculo.get('marca_nombre', ''),
                'modelo': vehiculo.get('modelo_nombre', ''),
                'anio': vehiculo.get('anio', ''),
                'vin': vehiculo.get('vin', ''),
                'precio': float(vehiculo.get('precio_de_venta', 0))
            },
            'empleado': {
                'nombre_completo': f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}".strip()
            },
            'contrato': {
                'id': contrato.get('id_contrato'),
                'tipo': contrato.get('tipocontrato', ''),
                'fecha': contrato.get('fecha'),
                'monto': subtotal
            },
            'pagos': metodos_pago,
            'calculos': {
                'subtotal': subtotal,
                'impuesto': impuesto_total,
                'total': total,
                'cantidad': 1
            },
            'cai': cai,
            'numero_documento_fiscal': numero_documento_fiscal
        })

        if request.method == "POST":
            try:
                cantidad = int(request.POST.get('cantidad', 1))
                precio_unitario = float(request.POST.get('precio_unitario', subtotal))
                subtotal = cantidad * precio_unitario
                impuesto = round(subtotal * 0.15, 2) if cliente.get('tipoexoneracion_id') else 0.0
                total_form = subtotal + impuesto

                data = {
                    'contrato_id': contrato_id,
                    'cliente': cliente,
                    'vehiculo': vehiculo,
                    'empleado': empleado,
                    'cai': cai,
                    'rango_autorizado_id': rango_seleccionado.get('id_RangoAutorizado'),
                    'numero_documento_fiscal': numero_documento_fiscal,
                    'es_exonerado': bool(cliente.get('tipoexoneracion_id')),
                    'estado': 'Emitido',
                    'descripcion': request.POST.get('descripcion'),
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'impuesto_total': impuesto,
                    'total_linea': subtotal,
                    'total': total_form,
                    'pagos': []
                }

                metodo_pago_ids = request.POST.getlist('metodo_pago_id')
                montos = request.POST.getlist('monto')
                referencias = request.POST.getlist('referencia')

                for metodo_id, monto, referencia in zip(metodo_pago_ids, montos, referencias):
                    if monto and float(monto) > 0:
                        data['pagos'].append({
                            'metodo_pago_id': int(metodo_id),
                            'monto': float(monto),
                            'referencia': referencia or ''
                        })

                total_pagos = sum(pago['monto'] for pago in data['pagos'])
                if abs(total_pagos - total_form) > 0.01:
                    logger.warning(f"La suma de los pagos ({total_pagos}) no coincide con el total ({total_form})")
                    messages.error(request, "La suma de los pagos no coincide con el total de la factura.")
                    context['factura']['calculos'].update({
                        'subtotal': subtotal,
                        'impuesto_total': impuesto,
                        'total': total_form,
                        'cantidad': cantidad
                    })
                    context['factura']['descripcion'] = data['descripcion']
                    return render(request, 'facturacion/facturacion_venta.html', context)

                valor = registrar_factura_y_pago(data)
                if valor == 1:
                    actualizar_estado_contrato(contrato_id, request.user.username if request.user.is_authenticated else 'system')
                    messages.success(request, "Factura generada exitosamente.")
                    return redirect('empleado_view')
                else:
                    logger.error("Error al registrar la factura")
                    messages.error(request, "Error al registrar la factura.")
                    return render(request, 'facturacion/facturacion_venta.html', context)

            except ValueError as ve:
                logger.error(f"Error en los datos del formulario: {str(ve)}")
                messages.error(request, "Los datos ingresados no son válidos. Verifique los valores numéricos.")
                return render(request, 'facturacion/facturacion_venta.html', context)

            except Exception as e:
                logger.error(f"Error al procesar factura: {str(e)}", exc_info=True)
                messages.error(request, f"Error al procesar la factura: {str(e)}")
                return render(request, 'facturacion/facturacion_venta.html', context)

        logger.debug(f"Datos preparados para el template: {context}")
        return render(request, 'facturacion/facturacion_venta.html', context)

    except Exception as e:
        logger.error(f"Error al preparar daparatos para facturación: {str(e)}", exc_info=True)
        messages.error(request, "Error al preparar datos  facturación.")
        return redirect(reverse('seleccionar_contratos'))

@login_required
def facturacion_alquiler(request):
    context = {
        'factura': {
            'cliente': {
                'id': None,
                'nombre_completo': '',
                'telefono': '',
                'correo': '',
                'rtn': 'N/A'
            },
            'vehiculo': {
                'id': None,
                'marca': '',
                'modelo': '',
                'anio': '',
                'vin': '',
                'precio': 0.0
            },
            'empleado': {
                'nombre_completo': ''
            },
            'contrato': {
                'id': None,
                'tipo': '',
                'fecha': None,
                'monto': 0.0,
                'fecha_inicio': None,
                'fecha_fin': None
            },
            'pagos': [],
            'calculos': {
                'subtotal': 0.0,
                'impuesto': 0.0,
                'total': 0.0,
                'cantidad': 1
            },
            'cai': '',
            'numero_documento_fiscal': ''
        }
    }
    
    if request.session.get('tipo_contrato') != 'Alquiler':
        messages.error(request, "Esta es una vista para contratos de alquiler")
        return redirect('seleccionar_contratos')
    
    contrato_id = request.session.get('id_contrato')
    if not contrato_id:
        logger.warning("No se encontró id_contrato en la sesión")
        messages.error(request, "No se encontró el contrato en la sesión.")
        return redirect(reverse('seleccionar_contratos'))

    try:
        contrato = traer_contrato_alquiler_id(contrato_id)
        logger.debug(f"Contrato traído: {contrato}")
        if not contrato:
            logger.error(f"Contrato con ID {contrato_id} no encontrado o no es de alquiler")
            messages.error(request, "El contrato no fue encontrado o no es de alquiler.")
            return redirect(reverse('seleccionar_contratos'))

        cliente = traer_cliente_id(contrato.get('cliente_id'))
        vehiculo = traer_vehiculo_id(contrato.get('vehiculo_id'))
        empleado = traer_empleado(request.session.get('user_id'))
        metodos_pago = obtener_metodos_pago()
        rangos_facturacion = obtener_rangos_facturacion_disponibles()

        if not all([cliente, vehiculo, empleado, metodos_pago, rangos_facturacion]):
            logger.error("Faltan datos relacionados al contrato")
            messages.error(request, "Error al obtener datos relacionados al contrato.")
            return redirect(reverse('seleccionar_contratos'))

        fecha_actual = datetime.now()
        rango_seleccionado = None
        for rango in rangos_facturacion:
            if (rango.get('TipoDocumento_id') == 1 and
                rango.get('FechaInicio') <= fecha_actual <= rango.get('FechaFin')):
                siguiente_numero = obtener_siguiente_numero_factura(rango)
                if siguiente_numero:
                    rango_seleccionado = rango
                    break

        if not rango_seleccionado:
            logger.error("No se encontró un rango de facturación válido para alquiler")
            messages.error(request, "No hay rangos de facturación disponibles para la fecha actual.")
            return redirect(reverse('seleccionar_contratos'))

        cai = rango_seleccionado.get('CAI')
        numero_documento_fiscal = siguiente_numero

        # Calcular el monto basado en el precio de alquiler y la duración
        precio_diario = float(vehiculo.get('precio_de_alquiler', 0))
        fecha_inicio = contrato.get('fechainicioalquiler')
        fecha_fin = contrato.get('fechafinalquiler')
        if fecha_inicio and fecha_fin:
            dias_alquiler = (fecha_fin - fecha_inicio).days + 1
            subtotal = precio_diario * dias_alquiler
        else:
            subtotal = precio_diario
        impuesto_total = round(subtotal * 0.18, 2) if cliente.get('tipoexoneracion_id') else 0.0
        total = subtotal + impuesto_total

        context['factura'].update({
            'cliente': {
                'id': cliente.get('cliente_id'),
                'nombre_completo': f"{cliente.get('nombre', '')} {cliente.get('segundonombre', '')} {cliente.get('apellido', '')} {cliente.get('segundoapellido', '')}".strip(),
                'telefono': cliente.get('telefono', 'N/A'),
                'correo': cliente.get('correo', 'N/A'),
                'rtn': cliente.get('rtn', 'N/A')
            },
            'vehiculo': {
                'id': vehiculo.get('id_vehiculo'),
                'marca': vehiculo.get('marca_nombre', ''),
                'modelo': vehiculo.get('modelo_nombre', ''),
                'anio': vehiculo.get('anio', ''),
                'vin': vehiculo.get('vin', ''),
                'precio': float(vehiculo.get('precio_de_alquiler', 0))
            },
            'empleado': {
                'nombre_completo': f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}".strip()
            },
            'contrato': {
                'id': contrato.get('id_contrato'),
                'tipo': contrato.get('tipocontrato', ''),
                'fecha': contrato.get('fecha'),
                'monto': subtotal,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            },
            'pagos': metodos_pago,
            'calculos': {
                'subtotal': subtotal,
                'impuesto': impuesto_total,
                'total': total,
                'cantidad': dias_alquiler if fecha_inicio and fecha_fin else 1
            },
            'cai': cai,
            'numero_documento_fiscal': numero_documento_fiscal
        })

        if request.method == "POST":
            try:
                cantidad = int(request.POST.get('cantidad', context['factura']['calculos']['cantidad']))
                precio_unitario = float(request.POST.get('precio_unitario', precio_diario))
                subtotal = cantidad * precio_unitario
                impuesto = round(subtotal * 0.18, 2) if cliente.get('tipoexoneracion_id') else 0.0
                total_form = subtotal + impuesto

                data = {
                    'contrato_id': contrato_id,
                    'cliente': cliente,
                    'vehiculo': vehiculo,
                    'empleado': empleado,
                    'cai': cai,
                    'rango_autorizado_id': rango_seleccionado.get('id_RangoAutorizado'),
                    'numero_documento_fiscal': numero_documento_fiscal,
                    'es_exonerado': bool(cliente.get('tipoexoneracion_id')),
                    'estado': 'Emitido',
                    'descripcion': request.POST.get('descripcion', f"Alquiler de vehículo {vehiculo.get('marca_nombre')} {vehiculo.get('modelo_nombre')}"),
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'subtotal': subtotal,
                    'impuesto_total': impuesto,
                    'total_linea': subtotal,
                    'total': total_form,
                    'pagos': []
                }

                metodo_pago_ids = request.POST.getlist('metodo_pago_id')
                montos = request.POST.getlist('monto')
                referencias = request.POST.getlist('referencia')

                for metodo_id, monto, referencia in zip(metodo_pago_ids, montos, referencias):
                    if monto and float(monto) > 0:
                        data['pagos'].append({
                            'metodo_pago_id': int(metodo_id),
                            'monto': float(monto),
                            'referencia': referencia or ''
                        })

                total_pagos = sum(pago['monto'] for pago in data['pagos'])
                if abs(total_pagos - total_form) > 0.01:
                    logger.warning(f"La suma de los pagos ({total_pagos}) no coincide con el total ({total_form})")
                    messages.error(request, "La suma de los pagos no coincide con el total de la factura.")
                    context['factura']['calculos'].update({
                        'subtotal': subtotal,
                        'impuesto': impuesto,
                        'total': total_form,
                        'cantidad': cantidad
                    })
                    context['factura']['descripcion'] = data['descripcion']
                    return render(request, 'facturacion/facturacion_alquiler.html', context)

                valor = registrar_factura_y_pago(data)
                if valor == 1:
                    actualizar_estado_contrato(contrato_id, request.user.username if request.user.is_authenticated else 'system')
                    messages.success(request, "Factura generada exitosamente.")
                    return redirect('empleado_view')
                else:
                    logger.error("Error al registrar la factura")
                    messages.error(request, "Error al registrar la factura.")
                    return render(request, 'facturacion/facturacion_alquiler.html', context)

            except ValueError as ve:
                logger.error(f"Error en los datos del formulario: {str(ve)}")
                messages.error(request, "Los datos ingresados no son válidos. Verifique los valores numéricos.")
                return render(request, 'facturacion/facturacion_alquiler.html', context)

            except Exception as e:
                logger.error(f"Error al procesar factura: {str(e)}", exc_info=True)
                messages.error(request, f"Error al procesar la factura: {str(e)}")
                return render(request, 'facturacion/facturacion_alquiler.html', context)

        logger.debug(f"Datos preparados para el template: {context}")
        return render(request, 'facturacion/facturacion_alquiler.html', context)

    except Exception as e:
        logger.error(f"Error al preparar datos para facturación: {str(e)}", exc_info=True)
        messages.error(request, "Error al preparar datos para facturación.")
        return redirect(reverse('seleccionar_contratos'))