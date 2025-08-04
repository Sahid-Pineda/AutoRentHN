import bcrypt
import pyodbc
import logging
import datetime
from .db_utils import consultar_una_fila_dict, consultar_todas_filas_dict
from .queries import QUERIES
from .db_utils import ejecutar_query, db_transaction, ejecutar_insert_retorna_id
# Modulo para manejar la logica de negocio como la autenticacion y creacion de usuarios.

logger = logging.getLogger(__name__)

def hash_password(password):
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def authenticate_user(email, password):
    result = ejecutar_query(QUERIES['get_user_by_email'], (email,),)
    if result: 
        email, password_hash, rol_id, id_user = result[0] 
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return id_user, email, rol_id
    return None

def register_user(data):
    try:
        # Primero verificamos si la persona ya existe (fuera de la transacción)
        persona_existe = ejecutar_query(
            QUERIES['check_person_exists'],
            (data['telefono'],)
        )
        if persona_existe:
            raise ValueError("Este usuario ya existe.")
        
        correo_existe = ejecutar_query(
            QUERIES['check_correo_exists'],
            (data['email'],)
        )

        if correo_existe:
            raise ValueError("El correo ya está registrado.")

        # Iniciamos la transacción
        with db_transaction() as (conn, cursor):
            # Insertar dirección
            direccion_id = ejecutar_insert_retorna_id(
                QUERIES['create_address'],
                [data['descripcion'], data['colonia_id']],
                conn=conn,
                cursor=cursor
            )

            # Insertar persona
            persona_id = ejecutar_insert_retorna_id(
                QUERIES['create_person'],
                (
                    data['primer_nombre'],
                    data['segundo_nombre'],
                    data['primer_apellido'],
                    data['segundo_apellido'],
                    data['telefono'],
                    direccion_id,
                    data['sexo']
                ),
                conn=conn,
                cursor=cursor
            )

            ejecutar_query(
                QUERIES['insert_info_fiscal'],
                (data['rtn'], 
                data['tipo_contribuyente'],
                persona_id,
                data['tipo_exoneracion']),
                conn=conn,
                cursor=cursor
            )

            # Obtener ID del rol 'Cliente'
            rol_id = ejecutar_query(
                QUERIES['get_rol_by_name'],
                ('Cliente',),
                conn=conn,
                cursor=cursor
            )[0][0]  # Asumimos que existe

            # Insertar usuario
            usuario_id = ejecutar_insert_retorna_id(
                QUERIES['create_user'],
                (
                    data['email'],
                    hash_password(data['password']),
                    persona_id,
                    rol_id
                ),
                conn=conn,
                cursor=cursor
            )

            # Insertar cliente
            ejecutar_query(
                QUERIES['insert_client'],
                (usuario_id,),
                conn=conn,
                cursor=cursor
            )


    except (ValueError, pyodbc.Error) as e:
        print(f"Error al registrar usuario: {e}")
        raise


def crear_contrato_venta(data):
    try:
        for campo in ['terminos', 'garantia']:
            if not data.get(campo):  # Si es '', None o no existe
                data[campo] = None

        # Paso 1: Insertar en Contrato
        with db_transaction() as (conn, cursor):
            contrato_id = ejecutar_insert_retorna_id(
                QUERIES['insert_contrato'],
                (
                    data['empleado_id'],
                    data['cliente_id'],
                    data['id_vehiculo'],
                    data['fecha'],
                    data['terminos'],
                    data['garantia'],
                    data['tipo_contrato'],
                    data['estado'],
                    data['firma']
                ),
                    conn=conn,
                    cursor=cursor
            )

            # Paso 2: Insertar en Contrato Venta
            ejecutar_query(
                QUERIES['insert_contrato_venta'],
                (
                    contrato_id,
                    data['monto'],
                ),
                conn=conn,
                cursor=cursor
            )

            return contrato_id
    except Exception as e:
        print(f"Error al crear contrato de venta: {e}")
        raise

def crear_contrato_alquiler(data):
    try:
        with db_transaction() as (conn, cursor):
            for campo in ['terminos', 'garantia', 'politica', 'clausulas']:
                if not data.get(campo):  # Si es '', None o no existe
                    data[campo] = None

            # Paso 1: Insertar en Contrato
            contrato_id = ejecutar_insert_retorna_id(
                QUERIES['insert_contrato'],
                (
                    data['empleado_id'],
                    data['cliente_id'],
                    data['id_vehiculo'],
                    data['fecha'],
                    data['terminos'],
                    data['garantia'],
                    data['tipo_contrato'],
                    data['estado'],
                    data['firma'],
                ),
                conn=conn,
                cursor=cursor
            )

            # Paso 2: Insertar en Contrato Venta
            ejecutar_query(
                QUERIES['insert_contrato_alquiler'],
                (
                    contrato_id,
                    data['fecha_inicio'],
                    data['fecha_fin'],
                    data['fecha_entrega_real'],
                    data['kilometraje'],
                    data['politica_combustible'],
                    data['es_tardia'],
                    data['es_extensible'],
                    data['reporte_danios'],
                    data['clausulas'],
                    data['recargo_incumplimiento'],
                ),
                conn=conn,
                cursor=cursor
            )

            return contrato_id
    except Exception as e:
        print(f"Error al crear contrato de venta: {e}")
        raise

def registrar_factura_y_pago(data):
    try:
        with db_transaction() as (conn, cursor):
            # Validar que el número de factura no esté en uso
            check_query = """
            SELECT COUNT(*) as count
            FROM DocumentoFiscal
            WHERE RangoAutorizado_id = ? AND NumeroDocumentoFiscal = ?
            """
            check_result = consultar_una_fila_dict(check_query, (data['rango_autorizado_id'], data['numero_documento_fiscal']))
            if check_result['count'] > 0:
                logger.error(f"El número de factura {data['numero_documento_fiscal']} ya está en uso")
                raise ValueError("El número de factura ya está en uso")


            # Insertar Documento Fiscal
            documento_id = ejecutar_insert_retorna_id(
            QUERIES['insert_documento_fiscal'], (
            data['contrato_id'],
            data['cai'],
            data['rango_autorizado_id'],
            data['numero_documento_fiscal'],
            1 if data['es_exonerado'] else 0,
            data['subtotal'],
            data['impuesto_total'],
            data['total'],
            data['estado'],),
            conn=conn,
            cursor=cursor
            )

            # Insertar Detalle Documento Fiscal
            ejecutar_query(
            QUERIES['insert_detalle_documento_fiscal'], (
            documento_id,
            data['vehiculo']['id_vehiculo'],
            data['descripcion'],
            data['cantidad'],
            data['precio_unitario'],
            data['impuesto_total'],
            data['total_linea'],
            ),
            conn=conn,
            cursor=cursor
            )

            # Insertar Pago Documento Fiscal
            for pago in data['pagos']:
                ejecutar_query(
                QUERIES['insert_pago_documento_fiscal'], (
                documento_id,
                pago['metodo_pago_id'],
                pago['monto'],
                pago['referencia'],
                ),
                conn=conn,
                cursor=cursor
                )
            return 1 # Si se creo factura retorna 1
    except Exception as e:
        print(f"Error al crear documento fiscal de venta: {e}")
        return 0 # Si no se creo factura retorna 0


def obtener_vehiculos_marcados(ids):
    if not ids:
        return []
    
    query = QUERIES["get_vehiculos_marcados"].format(
        placeholders = ",".join("?" for _ in ids)
    )
    return consultar_todas_filas_dict(query, ids)

def traer_cliente_id(cliente_id):
    return consultar_una_fila_dict(QUERIES['get_cliente_by_id'], (cliente_id,))

def traer_cliente_correo(correo):
    return consultar_una_fila_dict(QUERIES['get_cliente_by_correo'], (correo))

def traer_empleado(empleado_id):
    return consultar_una_fila_dict(QUERIES['get_empleado_by_id'], (empleado_id,))

def traer_departamentos(pais_id):
    return consultar_todas_filas_dict(QUERIES['obtener_departamento'], (pais_id,))

def traer_ciudades(departamento_id):
    return consultar_todas_filas_dict(QUERIES['obtener_ciudad'], (departamento_id,))

def traer_colonias(ciudad_id):
    return consultar_todas_filas_dict(QUERIES['obtener_colonia'], (ciudad_id,))

def traer_vehiculos():
    return consultar_todas_filas_dict(QUERIES['get_all_vehicles'])

def traer_vehiculos_alquiler():
    return consultar_todas_filas_dict(QUERIES['get_vehicle_by_uso_Alquiler'])

def traer_vehiculos_venta():
    return consultar_todas_filas_dict(QUERIES['get_vehicle_by_uso_Venta'])

def actualizar_estado_vehiculo(vehiculo_id):
    return ejecutar_query(QUERIES['update_disponibilidad'], vehiculo_id)

def actualizar_estado_contrato(contrato_id, usuario_modificacion):
    try:
        return ejecutar_query(QUERIES['update_estado'], ('Finalizado', usuario_modificacion, contrato_id))
    except Exception as e:
        logger.error(f"Error al actualizar estado del contrato {contrato_id}: {str(e)}")
        raise

def traer_vehiculo_id(vehiculo_id):
    return consultar_una_fila_dict(QUERIES['get_vehicle_by_id'], (vehiculo_id,))

def traer_contrato_venta_id(contrato_id):
    return consultar_una_fila_dict(QUERIES['get_contrato_venta_id'], (contrato_id,))

def traer_contrato_alquiler_id(contrato_id):
    contrato = consultar_una_fila_dict(QUERIES['get_contrato_alquiler_id'], (contrato_id,))
    if not contrato:
        logger.error(f"No se encontró contrato de alquiler con ID {contrato_id}")
        return None
    
    # Asegurar que las fechas sean objetos date/datetime
    for campo in ['FechaInicioAlquiler', 'FechaFinAlquiler', 'FechaEntregaReal']:
        if contrato.get(campo) and isinstance(contrato[campo], str):
            try:
                contrato[campo] = datetime.strptime(contrato[campo], "%Y-%m-%d").date()
            except ValueError as e:
                logger.error(f"Error al parsear fecha {campo}: {str(e)}")
                contrato[campo] = None
    
    return contrato

def traer_contrato_id(contrato_id):
    return consultar_una_fila_dict(QUERIES['contrato_tipo'], (contrato_id,))

def traer_pagos_contrato(contrato_id):
    return consultar_todas_filas_dict(QUERIES['get_pagos_contrato'], (contrato_id,))

def traer_contratos(estado=None, tipo=None, cliente=None):
    # Convierte None a una cade vacia para filtro
    estado = estado if estado is not None else ''
    tipo = tipo if tipo is not None else ''
    cliente = cliente if cliente is not None else ''
    filtro = (estado, estado, tipo, tipo, cliente, cliente)
    return consultar_todas_filas_dict(QUERIES['get_contratos'], filtro)

def obtener_metodos_pago():
    return consultar_todas_filas_dict(QUERIES['metodos_pago'])

def obtener_rangos_facturacion_disponibles():
    tipo_documento_id = 1  # Factura de venta
    return consultar_todas_filas_dict(QUERIES['rangos_facturacion'], (tipo_documento_id,))

def obtener_siguiente_numero_factura(rango):
    try:
        # Consultar el máximo NumeroDocumentoFiscal
        result = consultar_una_fila_dict(QUERIES['obtener_ultimo_numero_factura'], (rango['id_RangoAutorizado'],))
        
        if result and result['max_numero']:
            siguiente_numero = result['max_numero'] + 1
        else:
            siguiente_numero = rango['NumeroInicial']
        
        if siguiente_numero > rango['NumeroFinal']:
            logger.error(f"El rango {rango['id_RangoAutorizado']} ha alcanzado su límite de facturas")
            return None
        
        # Verificar si el número ya está en uso
        check_query = """
        SELECT COUNT(*) as count
        FROM DocumentoFiscal
        WHERE RangoAutorizado_id = ? AND NumeroDocumentoFiscal = ?
        """
        check_result = consultar_una_fila_dict(check_query, (rango['id_RangoAutorizado'], siguiente_numero))
        if check_result['count'] > 0:
            logger.error(f"El número de factura {siguiente_numero} ya está en uso")
            return None
        
        return siguiente_numero
    except Exception as e:
        logger.error(f"Error al obtener el siguiente número de factura: {str(e)}")
        return None
    
def traer_documentos_fiscales(estado=None, tipo=None, cliente=None):
    datos = []
    if estado:
        datos.append(estado)
        datos.append(estado)
    else:
        datos.append(None)
        datos.append(None)
    if tipo:
        datos.append(tipo)
        datos.append(tipo)
    else:
        datos.append(None)
        datos.append(None)
    if cliente:
        datos.append(cliente)
        datos.append(f'%{cliente}%')
    else:
        datos.append(None)
        datos.append(None)
    return consultar_todas_filas_dict(QUERIES['documentos_fiscales'], datos)