import pyodbc #Permite conectar a bases de datos compatibles con ODBC, como SQL Server.

# Modulo para manejar las conexiones y consultas a la base de datos.
# Define una función para obtener la conexión a la base de datos.
def get_db_connection():
    conn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=localhost,1433;'
        'DATABASE=AutoRentHN;'
        'UID=sa;'
        'PWD=MyStrongP@ssw0rd!'  # Remplazar por tu contraseña real
    )
    return pyodbc.connect(conn_str)

# Define una función para ejecutar consultas SQL.
def execute_query(query, params=None):
    conn = get_db_connection() # Obtiene la conexión a la base de datos.
    cursor = conn.cursor() # Crea un cursor para interactuar con la base de datos.
    try:
        if params:
            cursor.execute(query, params) 
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            return cursor.fetchall()
        conn.commit()
        return cursor.execute("SELECT @@IDENTITY").fetchone()[0]
    except pyodbc.Error as e:
        print(f"Error en la consulta: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def consultar_todas_filas_dict(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    # Obtener nombres de columnas
    columnas = [columna[0] for columna in cursor.description]

    resultados = [
        dict(zip(columnas, fila))
        for fila in cursor.fetchall()
    ]

    cursor.close()
    conn.close()
    return resultados

def consultar_una_fila_dict(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    columnas = [columna[0].lower() for columna in cursor.description]
    fila = cursor.fetchone()

    cursor.close()
    conn.close()

    if fila:
        return dict(zip(columnas, fila))
    else:
        return None


def execute_insert(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except pyodbc.Error as e:
        print(f"Error al insertar: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

# Define una función para insertar datos y obtener el ID del registro insertado.
def execute_insert_returning_id(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:       
        if params:
            cursor.execute(query + "; SELECT SCOPE_IDENTITY();", params)
        else:
            cursor.execute(query + "; SELECT SCOPE_IDENTITY();")
        cursor.nextset()
        result = cursor.fetchone()
        inserted_id = result[0]
        conn.commit()
        return int(inserted_id)
    except pyodbc.Error as e:
        print(f"Error al insertar y obtener ID: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

