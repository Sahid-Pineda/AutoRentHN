# Modulo para manejar las consultas a la base de datos

QUERIES = {
    # Consultas relacionadas con Direccion
    # Pais, Departamento, Ciudad, Colonia ya estan creadas en la base de datos
    'create_address': "INSERT INTO Direccion (Descripcion, Colonia_id) VALUES (?, ?)",
    'get_all_colonias': "SELECT * FROM Colonia",
    'get_all_ciudades': "SELECT * FROM Ciudad",
    'get_all_departamentos': "SELECT * FROM Departamento",
    'get_all_paises': "SELECT * FROM Pais",

    'obtener_departamento': "SELECT id_Departamento AS id, Nombre AS nombre FROM Departamento WHERE Pais_id = ?",
    'obtener_ciudad': "SELECT id_Ciudad AS id, Nombre AS nombre FROM Ciudad WHERE Departamento_id = ?",
    'obtener_colonia': "SELECT id_Colonia AS id, Nombre AS nombre FROM Colonia WHERE Ciudad_id = ?",

    # Consultas relacionadas con Persona
    "create_person":"INSERT INTO Persona (PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Telefono, Direccion_id, Sexo) VALUES (?, ?, ?, ?, ?, ?, ?)",
    
    # Consultas relacionadas con Usuario
    "get_user_name_by_id": "SELECT nombre FROM Usuario WHERE id_Usuario = ?",
    "get_user_by_email": "SELECT id_Usuario, Correo, Contrasenia, Rol_id FROM Usuario WHERE Correo = ?",
    "create_user": "INSERT INTO Usuario (Correo, Contrasenia, Persona_id, Rol_id) VALUES (?, ?, ?, ?)",
    "get_rol_by_name":"SELECT id_RolUsuario FROM RolUsuario WHERE Nombre = ?",

    # Consultas relacionadas con Cliente
    "insert_client": "INSERT INTO Cliente (Usuario_id) VALUES (?)",
    "get_all_clients": "SELECT * FROM Cliente",
    "get_cliente_by_id": """
    SELECT 
    p.PrimerNombre AS Nombre, 
    p.PrimerApellido AS Apellido,
    c.id_Cliente AS id_cliente
    FROM Cliente c
    INNER JOIN Usuario u ON c.Usuario_id = u.id_Usuario
    INNER JOIN Persona p ON u.Persona_id = p.id_Persona
    WHERE c.id_Cliente = ?;
    """,
    "get_cliente_by_correo": """
    SELECT 
    c.id_Cliente AS id_cliente,
    p.PrimerNombre,
    p.SegundoNombre,
    p.PrimerApellido,
    p.SegundoApellido,
    u.Correo AS correo,
    p.Telefono,
    p.Direccion_id
    FROM Cliente c
    INNER JOIN Usuario u ON c.Usuario_id = u.id_Usuario
    INNER JOIN Persona p ON u.Persona_id = p.id_Persona
    WHERE u.Correo = ?;
    """,

    "insert_tipo_exoneracion": "INSERT INTO TipoExoneracion (Descripcion) VALUES (?)",
    'get_tipo_exoneracion_by_id': "SELECT TipoExoneracion_id FROM TipoExoneracion WHERE TipoExoneracion_id = ?",
    'get_all_tipo_exoneracion': "SELECT * FROM TipoExoneracion",

    # Consultas relacionadas con Empleado
    "get_empleado_by_id": """
    SELECT 
    p.PrimerNombre AS Nombre, 
    p.PrimerApellido AS Apellido,
    e.id_Empleado AS id_Empleado
    FROM Empleado e
    INNER JOIN Usuario u ON e.Usuario_id = u.id_Usuario
    INNER JOIN Persona p ON u.Persona_id = p.id_Persona
    WHERE u.id_Usuario = ?;
    """,
 
    # Consultar para Contrato
    'insert_contrato': """
        INSERT INTO Contrato (Vendedor_id, Cliente_id, Vehiculo_id, FechaContrato, TerminosCondiciones, GarantiaRequerida, TipoContrato, EstadoContrato, FirmaCliente)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    'insert_contrato_venta': """
        INSERT INTO ContratoVenta (id_Contrato, FechaVenta, Monto)
        VALUES (?, GETDATE(), ?)
    """,
    'insert_contrato_alquiler': """
    INSERT INTO ContratoAlquiler (id_Contrato, FechaInicioAlquiler, FechaFinAlquiler, FechaEntregaReal, KilometrajePermitido, PoliticaCombustible, EsTardia, EsExtensible, ReporteDanios, Clausulas, RecargoIncumplimiento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    
    #Consultas para Vehiculos
    'get_vehicle_by_marca': """
    SELECT
        ma.Marca_id AS id_Marca, ma.Nombre AS Nombre
    FROM Modelo mo
    INNER JOIN Marca ma ON mo.Marca_id = ma.id_Marca
    WHERE mo.id_Marca = ?
    """,

    "get_all_vehicles": """
    SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS anio, 
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion, v.PrecioVenta,
           v.PrecioAlquiler, v.Estado,
           v.Url_Vehiculo AS url_vehiculo
    FROM Vehiculo v
    INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
    INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE Disponibilidad = 1
    """,

    "get_vehicle_by_uso_Alquiler": """
    SELECT v.id_vehiculo AS id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS año, 
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
           v.PrecioAlquiler, v.Estado,
           v.Url_Vehiculo AS url_vehiculo
    FROM Vehiculo v
    INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
    INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE uv.descripcion = 'Alquiler' AND Disponibilidad = 1
    """,

    "get_vehicle_by_uso_Venta": """
    SELECT v.id_vehiculo AS id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
           v.PrecioVenta, v.Estado,
           v.Url_Vehiculo AS url_vehiculo
    FROM Vehiculo v
    INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
    INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE uv.descripcion = 'Venta' AND Disponibilidad = 1
    """,

    "update_disponibilidad": """
    UPDATE Vehiculo SET Disponibilidad = 0 WHERE id_Vehiculo = ?;
    """,

    "get_vehicle_by_id": """
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
	WHERE v.id_Vehiculo = ?;
    """,
}