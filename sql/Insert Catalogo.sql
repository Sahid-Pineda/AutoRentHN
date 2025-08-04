USE AutoRentHN;
GO

--Agregando Datos para los catalogos
INSERT INTO RolUsuario (Nombre, Descripcion) VALUES
('Administrador', 'Usuario con permisos completos'),
('Cliente', 'Usuario que alquila o compra vehículos'),
('Empleado', 'Usuario que gestiona operaciones');
GO

INSERT INTO UsoVehiculo (Descripcion, Activo) VALUES
('Alquiler', 1),
('Venta', 1);
GO

INSERT INTO HorarioTrabajo (Dia, HoraInicio, HoraFin) VALUES
('Lunes', '08:00:00', '17:00:00'),
('Sábado', '09:00:00', '13:00:00');
GO

INSERT INTO Marca (Nombre) VALUES
('Toyota'),
('Honda'),
('Nissan'),
('Ford');
GO

INSERT INTO TipoVehiculo (NombreTipo, Descripcion) VALUES
('Sedán', 'Vehículo de cuatro puertas para uso urbano'),
('SUV', 'Vehículo utilitario deportivo'),
('Camioneta', 'Vehículo de carga ligera'),
('Pik-up', 'Vehículo de carga pesada');
GO

INSERT INTO TipoDocumento (Nombre, Codigo) VALUES
('Factura', '01'),
('Nota Crédito', '06'),
('Nota Débito', '07'),
('Boleta Compra', '11');
GO

INSERT INTO Color (Nombre) VALUES
('Rojo'),
('Azul'),
('Negro'),
('Blanco'),
('Gris'),
('Plata'),
('Verde');
GO

INSERT INTO TipoSeguro (Nombre, Disponibilidad) VALUES
('Cobertura Total', 'Disponible'),
('Cobertura Parcial', 'Disponible'),
('Cobertura Básica', 'Disponible'),
('Seguro Premiun', 'No Disponible');
GO

INSERT INTO MetodoPago (Nombre) VALUES
('Cheque'),
('Efectivo'),
('Tarjea de Débito'),
('Tarjeta de Crédito'),
('Transferencia Bancaria');
GO

INSERT INTO TipoExoneracion (Codigo, Descripcion) VALUES
('00', 'Sin Exoneración'),
('01', 'Exoneración por Ley'),
('02', 'Exoneración Diplomática'),
('03', 'Exoneración por Discapacidad');
GO

INSERT INTO Pais (Nombre, Codigo_Pais) VALUES
('Honduras', 'HND');
GO

INSERT INTO Departamento (Nombre, Codigo_Departamento, Pais_id) VALUES
('Atlántida', '01', 1),
('Colón', '02', 1),
('Comayagua', '03', 1),
('Copán', '04', 1),
('Cortés', '05', 1),
('Choluteca', '06', 1),
('El Paraíso', '07', 1),
('Francisco Morazán', '08', 1),
('Gracias a Dios', '09', 1),
('Intibucá', '10', 1),
('Islas de la Bahía', '11', 1),
('La Paz', '12', 1),
('Lempira', '13', 1),
('Ocotepeque', '14', 1),
('Olancho', '15', 1),
('Santa Bárbara', '16', 1),
('Valle', '17', 1),
('Yoro', '18', 1);
GO

INSERT INTO Ciudad (Nombre, Codigo_Ciudad, Departamento_id) VALUES
('La Ceiba', '0101', 1),               -- Atlántida
('Trujillo', '0201', 2),               -- Colón
('Comayagua', '0301', 3),              -- Comayagua
('Santa Rosa de Copán', '0401', 4),    -- Copán
('San Pedro Sula', '0501', 5),         -- Cortés
('Choluteca', '0601', 6),              -- Choluteca
('Yuscarán', '0701', 7),               -- El Paraíso
('Tegucigalpa', '0801', 8),            -- Francisco Morazán
('Puerto Lempira', '0901', 9),         -- Gracias a Dios
('La Esperanza', '1001', 10),          -- Intibucá
('Roatán', '1101', 11),                -- Islas de la Bahía
('La Paz', '1201', 12),                -- La Paz
('Gracias', '1301', 13),               -- Lempira
('Nueva Ocotepeque', '1401', 14),      -- Ocotepeque
('Juticalpa', '1501', 15),             -- Olancho
('Santa Bárbara', '1601', 16),         -- Santa Bárbara
('Nacaome', '1701', 17),               -- Valle
('Yoro', '1801', 18);                  -- Yoro
GO

INSERT INTO Colonia (Nombre, Ciudad_id) VALUES
-- La Ceiba, Atlántida (0101)
('Colonia El Centro', 1),
('Barrio Ingles', 1),
('Colonia San José', 1),

-- Trujillo, Colón (0201)
('Barrio Cristales', 2),
('Colonia Santa Fe', 2),
('Barrio El Centro', 2),

-- Comayagua, Comayagua (0301)
('Barrio La Caridad', 3),
('Colonia San Jorge', 3),
('Barrio El Centro', 3),

-- Santa Rosa de Copán, Copán (0401)
('Barrio El Calvario', 4),
('Colonia Las Flores', 4),
('Barrio San Vicente', 4),

-- San Pedro Sula, Cort�s (0501)
('Colonia Palmira', 5),
('Barrio Guamilito', 5),
('Colonia El Carmen', 5),

-- Choluteca, Choluteca (0601)
('Barrio El Centro', 6),
('Colonia San José', 6),
('Barrio La Merced', 6),

-- Yuscarán, El Paraíso (0701)
('Barrio El Calvario', 7),
('Colonia El Porvenir', 7),
('Barrio El Centro', 7),

-- Tegucigalpa, Francisco Morazán (0801)
('Colonia Palmira', 8),
('Barrio La Hoya', 8),
('Colonia Las Colinas', 8),

-- Puerto Lempira, Gracias a Dios (0901)
('Barrio El Centro', 9),
('Colonia 15 de Septiembre', 9),
('Barrio La Mosquitia', 9),

-- La Esperanza, Intibucá (1001)
('Barrio El Calvario', 10),
('Colonia San Juan', 10),
('Barrio El Centro', 10),

-- Roatán, Islas de la Bahía (1101)
('Colonia Los Fuertes', 11),
('Barrio Coxen Hole', 11),
('Colonia Sandy Bay', 11),

-- La Paz, La Paz (1201)
('Barrio El Centro', 12),
('Colonia San José', 12),
('Barrio El Calvario', 12),

-- Gracias, Lempira (1301)
('Barrio El Centro', 13),
('Colonia San Sebastián', 13),
('Barrio La Merced', 13),

-- Nueva Ocotepeque, Ocotepeque (1401)
('Colonia El Campo', 14),
('Barrio El Centro', 14),
('Colonia 1ro de Mayo', 14),

-- Juticalpa, Olancho (1501)
('Barrio El Centro', 15),
('Colonia San Francisco', 15),
('Barrio La Hoya', 15),

-- Santa Bárbara, Santa Bárbara (1601)
('Barrio El Calvario', 16),
('Colonia San José', 16),
('Barrio El Centro', 16),

-- Nacaome, Valle (1701)
('Barrio El Tamarindo', 17),
('Colonia San Antonio', 17),
('Barrio El Centro', 17),

-- Yoro, Yoro (1801)
('Barrio El Centro', 18),
('Colonia El Porvenir', 18),
('Barrio La Trinidad', 18);
GO

INSERT INTO Permiso (Nombre, Descripcion) VALUES
('Seleccionar Vehiculo', 'Permite seleccionar un vehículo'),
('Crear Contrato', 'Permite crear nuevos contratos'),
('Editar Vehículo', 'Permite modificar información de vehículos');
GO

INSERT INTO Modelo (Marca_id, Nombre) VALUES
(1, 'Corolla'),
(1, 'Tacoma'),
(2, 'Civic'),
(2, 'Fit'),
(3,'Sentra'),
(3,'Frontier'),
(4,'Focus'),
(4,'Mustang');
GO

INSERT INTO ParqueoVehiculo (Lote, Referencia) VALUES
('Lote A1', 'Cerca de entrada principal'),
('Lote B2', 'Zona trasera'),
('Lote C3', 'Zona lateral'),
('Lote D4', 'Cerca de oficinas');
GO

INSERT INTO Proveedor (NombreProveedor, RTN, ContactoNombre, Telefono, Correo, Direccion, TipoProveedor) VALUES
('Importadora AutoHN', '08011990123458', 'Ana Gómez', '504-9777-1234', 'contacto@autohn.com', 'Tegucigalpa', 'Distribuidor'),
('Distribuidora CarMax', '08011990123459', 'Juan Pérez', '504-9666-4321', 'juan@carmax.com', 'San Pedro Sula', 'Importador'),
('AutoParts HN', '08011990123460', 'Laura Martínez', '504-9555-6789', 'laura@autoparts.com', 'La Ceiba', 'Repuestos');
GO

INSERT INTO Vehiculo (Modelo_id, Anio, VIN, Motor, MatriculaPlaca, Disponibilidad, PrecioVenta, PrecioAlquiler, TipoVehiculo_id, Estado, TipoCombustible, UsoVehiculo_id, ParqueoVehiculo_id, Proveedor_id, Url_Vehiculo, KilometrajeActual, UltimoMantenimiento) VALUES
(1, '2023', '1HGCM82633A123456', '1.8L I4 DOHC 16V VVT-i', 'HND1234', 1, 250000.00, 150.00, 1, 'Nuevo', 'Gasolina', 1, 1, 1, 'img/vehiculos/ToyotaCorolla2023.png', 5000, '2025-06-01'),
(3, '2022', '2HGFC2F59KH512345', '2.0L I4 DOHC 16V i-VTEC', 'HND5678', 1, 230000.00, 180.00, 1, 'Nuevo', 'Gasolina', 2, 2, 1, 'img/vehiculos/HondaCivic2023.png', 0, '2025-05-15'),
(2, '2023', '5TFAX5GN4JX123456', '2.7L DOHC 16-Valve 4-Cylinder', 'TOY4321', 1, 320000.00, 200.00, 3, 'Nuevo', 'Gasolina', 1, 2, 1, 'img/vehiculos/ToyotaTacoma2022.png', 3000, '2025-07-01'),
(4, '2021', '3CZRU5H57MM123456', '1.5L I4 DOHC 16V', 'HON8765', 1, 210000.00, 95.00, 1, 'Usado', 'Gasolina', 2, 1, 1, 'img/vehiculos/HondaFit2021.png', 0, '2025-04-20'),
(5, '2022', '1N4AL3AP8JC123456', '2.0L I4 DOHC 16V', 'NIS2580', 1, 250000.00, 150.00, 1, 'Nuevo', 'Gasolina', 1, 2, 1, 'img/vehiculos/NissanSentra2022.png', 3000, '2025-06-10'),
(6, '2021', '1N6BD0CT6HN123456', '2.5L DOHC 4-Cylinder', 'NIS3579', 1, 220000.00, 120.00, 3, 'Usado', 'Diesel', 2, 1, 1, 'img/vehiculos/NissanFrontier2021.png', 0, '2025-03-30'),
(7, '2020', '1FADP3F2XGL123456', '2.0L I4 Ti-VCT', 'FOR1357', 1, 190000.00, 110.00, 1, 'Usado', 'Gasolina', 1, 2, 1, 'img/vehiculos/FordFocus2020.png', 45000, '2025-02-15'),
(8, '2022', '1FA6P8TH5L5123456', '2.3L EcoBoost I4 Turbo', 'FOR8642', 1, 360000.00, 250.00, 2, 'Nuevo', 'Gasolina', 2, 1, 1, 'img/vehiculos/ForMustang2022.png', 0, '2025-06-25');
GO

INSERT INTO Establecimiento (Nombre, Direccion, CodigoEstablecimiento) VALUES
('AutoRentHN Sucursal Principal', 'Avenida Principal, Boulevard Fuerzas Armadas, Tegucigalpa', '001');
GO

INSERT INTO PuntoEmision (CodigoPuntoEmision, Descripcion, Establecimiento_id) VALUES
('001', 'Punto Emisión Principal', 1);
GO

INSERT INTO RangoAutorizado (TipoDocumento_id, PuntoEmision_id, CAI, NumeroInicial, NumeroFinal, FechaInicio, FechaFin) VALUES
(1, 1, 'CAI-001-2025', 1000, 1999, '2025-01-01', '2025-12-31'),
(2, 1, 'CAI-002-2025', 2000, 2999, '2025-01-01', '2025-12-31'),
(3, 1, 'CAI-003-2025', 3000, 3999, '2025-01-01', '2025-12-31'),
(4, 1, 'CAI-004-2025', 4000, 4999, '2025-01-01', '2025-12-31');
GO

--Insert de un Empleado
INSERT INTO Direccion (Descripcion, Colonia_id) VALUES
('Calle Principal', 1),
('Dos cuadras al norte de la iglesia', 4);
GO

INSERT INTO Persona (PrimerNombre, SegundoNombre, PrimerApellido, SegundoApellido, Telefono, Direccion_id, Sexo) VALUES
('María', 'Luisa', 'Rodríguez', 'López', '504-9888-5678', 1, 'F'),
('Diego', 'Armando', 'Maradona', NULL, '504-9877-2301', 2, 'M');
GO

INSERT INTO Usuario (Correo, Contrasenia, InicioUso, FinUso, Rol_id, Persona_id) VALUES
('maria.rodriguez@autorent.com', '$2b$12$nzzYw0fr6xOQW5nRmFaIf.ITseX4JZyV0fA7uspb/PlUclIMPYMt.', '2025-07-11', NULL, 3, 1),
('diego.maradona@autorent.com', '$2b$12$og0Rc8tLPLCgRM76gZsvB.J3ArH1Zt21lGs461K2sw3vtrncoMRhe', '2025-04-16', NULL, 3, 2);
GO

INSERT INTO Empleado (Horario_id, Usuario_id, Estado) VALUES
(1, 1, 'Activo'),
(1, 2, 'Activo');
GO


SELECT * FROM Colonia;
SELECT * FROM Direccion;
SELECT * FROM Persona;
SELECT * FROM Usuario;
SELECT * FROM Cliente;
SELECT * FROM Empleado;
SELECT * FROM InformacionFiscal;

SELECT * FROM Marca;
SELECT * FROM Modelo;
SELECT * FROM Vehiculo;
SELECT * FROM UsoVehiculo;
SELECT * FROM TipoVehiculo;
SELECT * FROM ParqueoVehiculo;
SELECT * FROM Proveedor;
SELECT * FROM Vehiculo;
SELECT * FROM Proveedor;
SELECT * FROM Contrato;
SELECT * FROM ContratoVenta;
SELECT * FROM Direccion;

DELETE FROM Cliente;
DELETE FROM Empleado;
DELETE FROM Usuario;
DELETE FROM Persona;
DELETE FROM Direccion;
DELETE FROM Colonia;


SELECT v.id_vehiculo AS vehiculo_id, ma.nombre AS marca_nombre, m.nombre AS modelo_nombre, v.Anio AS anio,
    tv.descripcion AS tipo_descripcion, uv.descripcion AS uso_descripcion,
    v.PrecioVenta, v.Estado,
    v.Url_Vehiculo AS url_vehiculo
FROM Vehiculo v
INNER JOIN Modelo m ON v.Modelo_id = m.id_Modelo
INNER JOIN Marca ma ON m.Marca_id = ma.id_Marca
INNER JOIN TipoVehiculo tv ON v.TipoVehiculo_id = tv.id_TipoVehiculo
INNER JOIN UsoVehiculo uv ON v.UsoVehiculo_id = uv.id_UsoVehiculo
WHERE uv.descripcion = 'Venta' AND Disponibilidad = 1



SELECT * FROM InformacionFiscal;
SELECT * FROM ContratoVenta;
SELECT * FROM ContratoAlquiler;
SELECT * FROM Contrato;
SELECT * FROM Vehiculo;
SELECT * FROM ContratoAlquiler WHERE id_Contrato = 1;

DELETE FROM ContratoAlquiler WHERE id_Contrato = 2011;
DELETE FROM ContratoAlquiler WHERE id_Contrato = 2012;
DELETE FROM ContratoAlquiler WHERE id_Contrato = 2013;
DELETE FROM ContratoVenta WHERE id_Contrato = 2014;
DELETE FROM ContratoVenta WHERE id_Contrato = 2015;
DELETE FROM ContratoVenta WHERE id_Contrato = 2016;
DELETE FROM ContratoVenta WHERE id_Contrato = 2006;
DELETE FROM Contrato WHERE id_Contrato = 2009;
DELETE FROM Contrato WHERE id_Contrato = 2010;
DELETE FROM Contrato WHERE id_Contrato = 2011;
DELETE FROM Contrato WHERE id_Contrato = 2012;
DELETE FROM Contrato WHERE id_Contrato = 2013;
DELETE FROM Contrato WHERE id_Contrato = 2014;
DELETE FROM Contrato WHERE id_Contrato = 2015;
DELETE FROM Contrato WHERE id_Contrato = 2016;

UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 1;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 2;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 3;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 4;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 5;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 6;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 7;
UPDATE Vehiculo SET Disponibilidad = 1 WHERE id_Vehiculo = 8;

UPDATE Vehiculo SET Url_Vehiculo = 'img/vehiculos/HondaCivic2023.png' WHERE id_Vehiculo = 2 ;
UPDATE Vehiculo SET Url_Vehiculo = 'img/vehiculos/ToyotaTacoma2022.png' WHERE id_Vehiculo = 3 ;

WITH Duplicados AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY Nombre, Ciudad_id ORDER BY id_Colonia) as fila
  FROM Colonia
)
DELETE FROM Duplicados
WHERE fila > 1;
