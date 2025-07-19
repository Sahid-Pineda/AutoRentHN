import bcrypt
import pyodbc
import hashlib
from .db_utils import execute_query, execute_insert, execute_insert_returning_id, consultar_todas_filas_dict
from .queries import QUERIES

# Modulo para manejar la logica de negocio como la autenticacion y creacion de usuarios.

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def authenticate_user(email, password):
    result = execute_query(QUERIES['get_user_by_email'], (email,))
    if result: 
        id_user, email, password_hash = result[0] 
        if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return id_user, email
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
                direccion_id
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

        tipo_exoneracion_id = int(data['tipo_exoneracion'])
        execute_insert(
            QUERIES['insert_client'],
            (
                usuario_id,
                tipo_exoneracion_id
            )
        )
    except (ValueError, pyodbc.Error) as e:
        print(f"Error al registrar usuario: {e}")
        raise

def traer_departamentos(pais_id):
    return consultar_todas_filas_dict(QUERIES['obtener_departamento'], (pais_id,))

def traer_ciudades(departamento_id):
    return consultar_todas_filas_dict(QUERIES['obtener_ciudad'], (departamento_id,))

def traer_colonias(ciudad_id):
    return consultar_todas_filas_dict(QUERIES['obtener_colonia'], (ciudad_id,))