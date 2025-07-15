# Modulo para manejar las consultas a la base de datos

QUERIES = {
    # Consultas relacionadas con Direccion
    # Pais, Departamento, Ciudad, Colonia ya estan creadas en la base de datos
    'create_address': "INSERT INTO Direccion (Descripcion, Colonia_id) VALUES (?, ?)",
    'get_all_colonias': "SELECT * FROM Colonia",
    'get_all_ciudades': "SELECT * FROM Ciudad",
    'get_all_departamentos': "SELECT * FROM Departamento",
    'get_all_paises': "SELECT * FROM Pais",

    'get_ubicaciones':
    """
    SELECT 
	ci.id_Ciudad AS ciudad_id, ci.Nombre AS ciudad_nombre,
	d.id_Departamento AS departamento_id, d.Nombre AS departamento_nombre,
	p.id_Pais AS pais_id, p.Nombre AS pais_nombre
    FROM Colonia c
    JOIN Ciudad ci ON c.Ciudad_id = ci.id_Ciudad
    JOIN Departamento d ON ci.Departamento_id = d.id_Departamento
    JOIN Pais p ON d.Pais_id = p.id_Pais
    WHERE c.id_Colonia = ?;
    """,

    # Consultas relacionadas con Persona
    "create_person":"INSERT INTO Persona (PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Telefono, Direccion_id) VALUES (?, ?, ?, ?, ?, ?)",
    
    # Consultas relacionadas con Usuario
    "get_user_name_by_id": "SELECT nombre FROM Usuario WHERE id_Usuario = ?",
    "get_user_by_email": "SELECT id_Usuario, Correo, Contrasenia FROM Usuario WHERE Correo = ?",
    "create_user": "INSERT INTO Usuario (Correo, Contrasenia, Persona_id, Rol_id) VALUES (?, ?, ?, ?)",
    "get_rol_by_name":"SELECT id_RolUsuario FROM RolUsuario WHERE Nombre = ?",

    # Consultas relacionadas con Cliente
    "insert_client": "INSERT INTO Cliente (Usuario_id, TipoExoneracion_id) VALUES (?, ?)",
    "get_all_clients": "SELECT * FROM Cliente",
    "get_client_by_id": "SELECT * FROM Cliente WHERE id_Cliente = ?",

    "insert_tipo_exoneracion": "INSERT INTO TipoExoneracion (Descripcion) VALUES (?)",
    'get_tipo_exoneracion_by_id': "SELECT TipoExoneracion_id FROM TipoExoneracion WHERE TipoExoneracion_id = ?",
    'get_all_tipo_exoneracion': "SELECT * FROM TipoExoneracion",
}