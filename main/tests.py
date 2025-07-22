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

import bcrypt

#Para encriptar contraseñas para guardar manual en la BD
password = "A123"
# bcrypt necesita el password en bytes
password_bytes = password.encode('utf-8')

# Generar salt y luego hashear
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password_bytes, salt)

print("\n" + hashed.decode())  # Esto es lo que se guarda en la DB

#Para comparar contraseñas
hashed = b"$2b$12$tsTNYcVEuzoOCGrhw7iT..kKncmupNbdGYCOcK07QvjCrasqIHg3m"
password = b"MiContraP@ssw0rd!"

if bcrypt.checkpw(password, hashed):
    print("\n" + "La contraseña es correcta")
else:
    print("\n" + "Contraseña incorrecta")
