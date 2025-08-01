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

SELECT v.id_vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, Anio AS a�o, 
           tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
           v.PrecioAlquiler, v.Estado
    FROM Vehiculo v
    JOIN Modelo m ON v.Modelo_id = m.id_Modelo
    JOIN Marca ma ON m.Marca_id = ma.id_Marca
    JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
    JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
	WHERE uv.descripcion = 'Alquiler' AND Disponibilidad = 1;

INSERT INTO Vehiculo VALUES(7, 2018, '3G1BE6SM7JS601472', '1.5L I4 Turbo', 'HNX-4127', 1, 310000.00, 950.00, 1, 'Usado', 'Gasolina', 1, 1, 1),
(4, 2019, '3HGGK5H57KM701893', '1.5L I4', 'HNP-2211', 1, 330000.00, 0, 2, 'Usado', 'Gasolina', 2, 2, 1),
(8, 2022, '1G1FB1RX9N0104733', '2.3L EcoBoost', 'HNR-1189', 1, 870000.00, 0, 1, 'Nuevo', 'Gasolina', 2, 1, 1),
(2, 2021, '3TMCZ5AN5MM374185', '3.5L V6', 'HNT-7854', 1, 790000.00, 2500.00, 3, 'Nuevo', 'Di�sel', 2, 2, 1),
(3, 2017, '19XFC2F5XHE045379', '1.5L I4 Turbo', 'HNM-6348', 1, 235000.00, 850.00, 1, 'Usado', 'Gasolina', 2, 2, 1);

--SELECT  v.id_Vehiculo, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
--		v.VIN AS vin, v.Motor AS motor, v.MatriculaPlaca AS placa, 
--		tv.nombreTipo AS tipo_nombre, tv.descripcion AS tipo_descripcion, 
--		uv.descripcion AS uso_descripcion, v.PrecioVenta AS precio_de_venta, 
--		v.PrecioAlquiler AS precio_de_alquiler, v.Estado AS estado, 
--		v.TipoCombustible AS tipo_de_combustible,
--        v.Url_Vehiculo AS url_vehiculo, v.KilometrajeActual AS Kilometraje,
--		v.UltimoMantenimiento AS Ultimo_Mantenimiento
--    FROM Vehiculo v
--    INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
--    INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
--    INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
--    INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
--	WHERE v.id_Vehiculo = ?;

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
GO

--�Cruce de datos?
--CREATE OR ALTER VIEW VistaVehiculosDetallados AS 
--SELECT 
--    v.id_vehiculo,
--    m.nombre AS marca_nombre,
--    mo.nombre AS modelo_nombre,
--    v.anio,
--    v.vin,
--    v.motor,
--    v.MatriculaPlaca,
--    t.NombreTipo AS tipo_nombre,
--    t.descripcion AS tipo_descripcion,
--    uv.Descripcion AS uso_vehiculo,
--    v.PrecioVenta,
--    v.PrecioAlquiler,
--    v.Estado,
--	v.Disponibilidad,
--	v.ParqueoVehiculo_id,
--	v.Proveedor_id,
--    v.TipoCombustible,
--	v.Url_Vehiculo,
--	v.KilometrajeActual,
--	v.UltimoMantenimiento
--FROM Vehiculo v
--INNER JOIN Modelo mo ON v.Modelo_id = mo.id_modelo
--INNER JOIN Marca m ON mo.id_Modelo = m.id_marca
--INNER JOIN TipoVehiculo t ON v.TipoVehiculo_id = t.id_TipoVehiculo
--INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo;
--GO

--SELECT * FROM [VistaVehiculosDetallados];

--ALTER TABLE Vehiculo
--ADD Url_Vehiculo VARCHAR(255),
--KilometrajeActual INTEGER DEFAULT 0,
--UltimoMantenimiento DATE;

--DELETE FROM Vehiculo;

--INSERT INTO ParqueoVehiculo (Lote, Referencia) VALUES
--('Lote C3', 'Zona lateral'),
--('Lote D4', 'Cerca de oficinas');
--GO

--INSERT INTO Proveedor (NombreProveedor, RTN, ContactoNombre, Telefono, Correo, Direccion, TipoProveedor) VALUES
--('Distribuidora CarMax', '08011990123459', 'Juan P?rez', '504-9666-4321', 'juan@carmax.com', 'San Pedro Sula', 'Importador'),
--('AutoParts HN', '08011990123460', 'Laura Mart?nez', '504-9555-6789', 'laura@autoparts.com', 'La Ceiba', 'Repuestos');
--GO

--INSERT INTO Vehiculo (Modelo_id, Anio, VIN, Motor, MatriculaPlaca, Disponibilidad, PrecioVenta, PrecioAlquiler, TipoVehiculo_id, Estado, TipoCombustible, UsoVehiculo_id, ParqueoVehiculo_id, Proveedor_id, Url_Vehiculo, KilometrajeActual, UltimoMantenimiento) VALUES
--(1, '2023', '1HGCM82633A123456', '1.8L I4 DOHC 16V VVT-i', 'HND1234', 1, 250000.00, 150.00, 1, 'Nuevo', 'Gasolina', 1, 1, 1, 'img/vehiculos/ToyotaCorolla2023.png', 5000, '2025-06-01'),
--(3, '2022', '2HGFC2F59KH512345', '2.0L I4 DOHC 16V i-VTEC', 'HND5678', 1, 230000.00, 180.00, 1, 'Nuevo', 'Gasolina', 2, 2, 1, 'img/vehiculos/ToyotaTacoma2022.png', 0, '2025-05-15'),
--(2, '2023', '5TFAX5GN4JX123456', '2.7L DOHC 16-Valve 4-Cylinder', 'TOY4321', 1, 320000.00, 200.00, 3, 'Nuevo', 'Gasolina', 1, 2, 1, 'img/vehiculos/HondaCivic2023.png', 3000, '2025-07-01'),
--(4, '2021', '3CZRU5H57MM123456', '1.5L I4 DOHC 16V', 'HON8765', 1, 210000.00, 95.00, 1, 'Usado', 'Gasolina', 2, 1, 1, 'img/vehiculos/HondaFit2021.png', 0, '2025-04-20'),
--(5, '2022', '1N4AL3AP8JC123456', '2.0L I4 DOHC 16V', 'NIS2580', 1, 250000.00, 150.00, 1, 'Nuevo', 'Gasolina', 1, 2, 1, 'img/vehiculos/NissanSentra2022.png', 3000, '2025-06-10'),
--(6, '2021', '1N6BD0CT6HN123456', '2.5L DOHC 4-Cylinder', 'NIS3579', 1, 220000.00, 120.00, 3, 'Usado', 'Diesel', 2, 1, 1, 'img/vehiculos/NissanFrontier2021.png', 0, '2025-03-30'),
--(7, '2020', '1FADP3F2XGL123456', '2.0L I4 Ti-VCT', 'FOR1357', 1, 190000.00, 110.00, 1, 'Usado', 'Gasolina', 1, 2, 1, 'img/vehiculos/FordFocus2020.png', 45000, '2025-02-15'),
--(8, '2022', '1FA6P8TH5L5123456', '2.3L EcoBoost I4 Turbo', 'FOR8642', 1, 360000.00, 250.00, 2, 'Nuevo', 'Gasolina', 2, 1, 1, 'img/vehiculos/ForMustang2022.png', 0, '2025-06-25');
--GO