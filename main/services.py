import bcrypt
import pyodbc
from .db_utils import consultar_una_fila_dict, execute_query, execute_insert, execute_insert_returning_id, consultar_todas_filas_dict
from .queries import QUERIES

# Modulo para manejar la logica de negocio como la autenticacion y creacion de usuarios.

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def authenticate_user(email, password):
    result = execute_query(QUERIES['get_user_by_email'], (email,))
    if result: 
        id_user, email, password_hash, rol_id = result[0] 
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return id_user, email, rol_id
    return None

def register_user(data):
    try:
        direccion_id = execute_insert_returning_id(
            QUERIES['create_address'],
            (
                data['descripcion'],
                data['colonia_id']
            )
        )

        persona_id = execute_insert_returning_id(
            QUERIES['create_person'],
            (
                data['primer_nombre'],
                data['segundo_nombre'],
                data['primer_apellido'],
                data['segundo_apellido'],
                data['telefono'],
                direccion_id,
                data['sexo']
            )
        )

        rol_id = execute_query(
            QUERIES['get_rol_by_name'],
            (
                'Cliente',
            )
        )[0][0]  # Asumiendo que el rol 'Cliente' siempre existe

        usuario_id = execute_insert_returning_id(
            QUERIES['create_user'],
            (
                data['email'],
                hash_password(data['password']),
                persona_id,
                rol_id
            )
        )

        execute_insert(
            QUERIES['insert_client'],
            (
                usuario_id,
            )
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
        contrato_id = execute_insert_returning_id(
            QUERIES['insert_contrato'],
            (
                data['empleado_id'],
                data['cliente_id'],
                data['vehiculo_id'],
                data['fecha'],
                data['terminos'],
                data['garantia'],
                data['tipo_contrato'],
                data['estado'],
                data['firma'],
            )
        )

        # Paso 2: Insertar en Contrato Venta
        execute_insert(
            QUERIES['insert_contrato_venta'],
            (
                contrato_id,
                data['monto'],
            )
        )

        return contrato_id
    except Exception as e:
        print(f"Error al crear contrato de venta: {e}")
        raise

def crear_contrato_alquiler(data):
    try:
        for campo in ['terminos', 'garantia', 'politica', 'clausulas']:
            if not data.get(campo):  # Si es '', None o no existe
                data[campo] = None

        # Paso 1: Insertar en Contrato
        contrato_id = execute_insert_returning_id(
            QUERIES['insert_contrato'],
            (
                data['empleado_id'],
                data['cliente_id'],
                data['vehiculo_id'],
                data['fecha'],
                data['terminos'],
                data['garantia'],
                data['tipo_contrato'],
                data['estado'],
                data['firma'],
            )
        )

        # Paso 2: Insertar en Contrato Venta
        execute_insert(
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
            )
        )

        return contrato_id
    except Exception as e:
        print(f"Error al crear contrato de venta: {e}")
        raise

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
    return execute_insert(QUERIES['update_disponibilidad'], vehiculo_id)

def traer_vehiculo(vehiculo_id):
    return consultar_una_fila_dict(QUERIES['get_vehicle_by_id'], (vehiculo_id,))
