from django.test import TestCase

# Create your tests here.
import pyodbc

try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost,1433;"
        "DATABASE=AutoRentHN;"
        "UID=sa;"
        "PWD=MyStrongP@ssw0rd!;"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    version = cursor.fetchone()
    print(f"Conexión exitosa ✅ - Versión del servidor: {version[0]}")

except pyodbc.Error as e:
    print(f"Error al conectar a la base de datos ❌: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
