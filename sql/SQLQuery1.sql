USE AutoRentHN;

SELECT * FROM Usuario;
SELECT * FROM Persona;
SELECT * FROM RolUsuario;
SELECT * FROM Vehiculo;
SELECT * FROM TipoVehiculo;
SELECT * FROM Marca;
SELECT * FROM Modelo;
SELECT * FROM UsoVehiculo;
SELECT * FROM ParqueoVehiculo;
SELECT * FROM Proveedor;
SELECT * FROM HorarioTrabajo;
SELECT * FROM Departamento;
SELECT * FROM Empleado;
SELECT * FROM Contrato;
SELECT * FROM ContratoVenta;
SELECT * FROM Empleado WHERE id_Empleado = 1;

SELECT * FROM Usuario u
LEFT JOIN Cliente c ON c.Usuario_id = u.id_Usuario
WHERE u.Correo = 'diego@example.com';

SELECT 
    c.id_Cliente AS id_cliente,
    p.PrimerNombre AS Nombre, 
    p.PrimerApellido AS Apellido
FROM Cliente c
INNER JOIN Usuario u ON c.Usuario_id = u.id_Usuario
INNER JOIN Persona p ON u.Persona_id = p.id_Persona
WHERE c.id_Cliente = 1;

ALTER TABLE Contrato DROP COLUMN RecargoIncumplimiento;
ALTER TABLE ContratoAlquiler
ADD RecargoIncumplimiento DECIMAL(13,2) NOT NULL DEFAULT 0.00;
GO

SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
  tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
  v.PrecioVenta, v.Estado
FROM Vehiculo v
INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
WHERE uv.descripcion = 'Venta' AND Disponibilidad = 1;

SELECT 
p.PrimerNombre AS Nombre, 
p.PrimerApellido AS Apellido,
e.id_Empleado AS id_Empleado
FROM Empleado e
INNER JOIN Usuario u ON e.Usuario_id = u.id_Usuario
INNER JOIN Persona p ON u.Persona_id = p.id_Persona
WHERE u.id_Usuario = 2;

SELECT 
p.PrimerNombre AS Nombre, 
p.PrimerApellido AS Apellido,
c.id_Cliente AS id_Cliente
FROM Cliente c
INNER JOIN Usuario u ON c.Usuario_id = u.id_Usuario
INNER JOIN Persona p ON u.Persona_id = p.id_Persona
WHERE u.id_Usuario = 1;

SELECT 
    c.id_Cliente,
    p.PrimerNombre,
    p.SegundoNombre,
    p.PrimerApellido,
    p.SegundoApellido,
    u.Correo,
    p.Telefono,
    p.Direccion_id
FROM Cliente c
INNER JOIN Usuario u ON c.Usuario_id = u.id_Usuario
INNER JOIN Persona p ON u.Persona_id = p.id_Persona
WHERE u.Correo = 'diego@example.com';

SELECT id_Usuario, Correo, Contrasenia, Rol_id FROM Usuario WHERE Correo = 'diego@example.com';

SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS año, 
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
           v.PrecioAlquiler, v.Estado
    FROM Vehiculo v
    JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    JOIN Marca ma ON m.Marca_id = ma.id_Marca
    JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE uv.descripcion = 'Alquiler' AND Disponibilidad = 1;

SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS año,
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
           v.PrecioVenta, v.Estado
    FROM Vehiculo v
    JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    JOIN Marca ma ON m.Marca_id = ma.id_Marca
    JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE uv.descripcion = 'Venta' AND Disponibilidad = 1;

--INSERT INTO Vehiculo VALUES(7, 2018, '3G1BE6SM7JS601472', '1.5L I4 Turbo', 'HNX-4127', 1, 310000.00, 950.00, 1, 'Usado', 'Gasolina', 1, 1, 1);
--(4, 2019, '3HGGK5H57KM701893', '1.5L I4', 'HNP-2211', 1, 330000.00, 0, 2, 'Usado', 'Gasolina', 2, 2, 1),
--(8, 2022, '1G1FB1RX9N0104733', '2.3L EcoBoost', 'HNR-1189', 1, 870000.00, 0, 1, 'Nuevo', 'Gasolina', 2, 1, 1),
--(2, 2021, '3TMCZ5AN5MM374185', '3.5L V6', 'HNT-7854', 1, 790000.00, 2500.00, 3, 'Nuevo', 'Diésel', 2, 2, 1),
--(3, 2017, '19XFC2F5XHE045379', '1.5L I4 Turbo', 'HNM-6348', 1, 235000.00, 850.00, 1, 'Usado', 'Gasolina', 2, 2, 1);

SELECT  v.id_Vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
		v.VIN AS vin, v.Motor AS motor, v.MatriculaPlaca AS placa, 
		tv.nombreTipo AS tipo_nombre, tv.descripcion AS tipo_descripcion, 
		uv.descripcion AS uso_descripcion, v.PrecioVenta AS precio_de_venta, 
		v.PrecioAlquiler AS precio_de_alquiler, v.Estado AS estado, 
		v.TipoCombustible AS tipo_de_combustible
    FROM Vehiculo v
    JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    JOIN Marca ma ON m.Marca_id = ma.id_Marca
    JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE v.id_Vehiculo = 11;

SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS anio, 
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion, v.PrecioVenta,
           v.PrecioAlquiler, v.Estado
    FROM Vehiculo v
    JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    JOIN Marca ma ON m.Marca_id = ma.id_Marca
    JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE Disponibilidad = 1;