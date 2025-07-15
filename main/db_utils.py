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
        return None
    except pyodbc.Error as e:
        print(f"Error en la consulta: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def fetch_one_dict(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        columns = [column[0] for column in cursor.description]
        row = cursor.fetchone()
        if row:
            return dict(zip(columns, row))
        return None
    except pyodbc.Error as e:
        print(f"Error al obtener un registro: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

def execute_insert(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        row = cursor.fetchone()
        columns = [column[0] for column in cursor.description]
        return dict(zip(columns, row))
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
        print(f"Ejecutando consulta: {query} con parámetros: {params}")        
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

