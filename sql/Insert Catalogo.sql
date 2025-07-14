USE AutoRentHN;
GO

--Agregando Datos para los catalogos
INSERT INTO RolUsuario (Nombre, Descripcion) VALUES
('Administrador', 'Usuario con permisos completos'),
('Cliente', 'Usuario que alquila o compra vehículos'),
('Empleado', 'Usuario que gestiona operaciones');
GO

INSERT INTO UsoVehiculo (Descripcion) VALUES
('Alquiler'),
('Venta');
GO

INSERT INTO HorarioTrabajo (Dia, HoraInicio, HoraFin) VALUES
('Lunes', '08:00:00', '17:00:00'),
('Sábado', '09:00:00', '13:00:00');
GO

INSERT INTO Marca (Nombre) VALUES
('Toyota'),
('Honda'),
('Ford'),
('Chevrolet');
GO

INSERT INTO TipoVehiculo (NombreTipo, Descripcion) VALUES
('Sedán', 'Vehículo de cuatro puertas para uso urbano'),
('SUV', 'Vehículo utilitario deportivo'),
('Camioneta', 'Vehículo de carga ligera');
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
('Blanco');
GO

INSERT INTO TipoSeguro (Nombre, Disponibilidad) VALUES
('Cobertura Total', 'Disponible'),
('Cobertura Parcial', 'Disponible');
GO

INSERT INTO MetodoPago (Nombre) VALUES
('Efectivo'),
('Tarjeta de Crédito'),
('Transferencia Bancaria');
GO

INSERT INTO TipoExoneracion (Descripcion) VALUES
('Exoneración Diplomática'),
('Exoneración por Discapacidad'),
('Sin Exoneración');
GO

INSERT INTO Pais (Nombre, Codigo_Pais) VALUES
('Honduras', 'HN');
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
('La Ceiba Centro', 1),
('Trujillo Centro', 2),
('Comayagua Norte', 3),
('Santa Rosa Este', 4),
('San Pedro Sula Sur', 5),
('Choluteca Centro', 6),
('Yuscarán Norte', 7),
('Tegucigalpa Centro', 8),
('Puerto Lempira', 9),
('La Esperanza Oeste', 10),
('Roatán Sur', 11),
('La Paz Centro', 12),
('Gracias Norte', 13),
('Ocotepeque Este', 14),
('Juticalpa Centro', 15),
('Santa Bárbara Sur', 16),
('Nacaome Norte', 17),
('El Progreso Centro', 18);
GO

INSERT INTO Permiso (Nombre, Descripcion) VALUES
('Seleccionar Vehiculo', 'Permite seleccionar un vehiculo'),
('Crear Contrato', 'Permite crear nuevos contratos'),
('Editar Vehículo', 'Permite modificar información de vehículos');
GO
