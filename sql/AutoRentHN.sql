CREATE DATABASE AutoRentHN;
GO

USE AutoRentHN;
GO

--Tablas base sin dependencias

CREATE TABLE RolUsuario (
id_RolUsuario INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Descripcion TEXT
);
GO

CREATE TABLE UsoVehiculo (
id_UsoVehiculo INTEGER PRIMARY KEY IDENTITY(1,1),
Descripcion VARCHAR(100) NOT NULL
);
GO

CREATE TABLE HorarioTrabajo (
id_HorarioTrabajo INTEGER PRIMARY KEY IDENTITY(1,1),
Dia VARCHAR(30) NOT NULL,
HoraInicio TIME,
HoraFin TIME
);
GO

CREATE TABLE Marca (
id_Marca INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL
);
GO

CREATE TABLE TipoVehiculo (
id_TipoVehiculo INTEGER PRIMARY KEY IDENTITY(1,1),
NombreTipo VARCHAR(100) NOT NULL,
Descripcion TEXT
);
GO

CREATE TABLE TipoDocumento (
id_TipoDocumento INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Codigo VARCHAR(2) NOT NULL
);
GO

CREATE TABLE Color (
id_Color INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL
);
GO

CREATE TABLE TipoSeguro (
id_TipoSeguro INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Disponibilidad VARCHAR(20) NOT NULL
);
GO

CREATE TABLE MetodoPago (
id_MetodoPago INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100)
);
GO

CREATE TABLE TipoExoneracion (
id_TipoExoneracion INTEGER PRIMARY KEY IDENTITY(1,1),
Descripcion VARCHAR(100) NOT NULL
);
GO

--Tablas Ubicacion con dependencias
CREATE TABLE Pais (
id_Pais INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL UNIQUE,
Codigo_Pais VARCHAR(2) NOT NULL UNIQUE
);
GO

CREATE TABLE Departamento (
id_Departamento INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Codigo_Departamento VARCHAR(2) NOT NULL UNIQUE,
Pais_id INTEGER NOT NULL,
FOREIGN KEY (Pais_id) REFERENCES Pais(id_Pais)
);
GO

CREATE TABLE Ciudad (
id_Ciudad INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Codigo_Ciudad VARCHAR(4) NOT NULL UNIQUE,
Departamento_id INTEGER NOT NULL,
FOREIGN KEY (Departamento_id) REFERENCES Departamento(id_Departamento)
);
GO

CREATE TABLE Colonia (
id_Colonia INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Ciudad_id INTEGER NOT NULL,
FOREIGN KEY (Ciudad_id) REFERENCES Ciudad(id_Ciudad)
);
GO

CREATE TABLE Direccion (
id_Direccion INTEGER PRIMARY KEY IDENTITY(1,1),
Descripcion VARCHAR(250) NOT NULL,
Colonia_id INTEGER NOT NULL,
FOREIGN KEY (Colonia_id) REFERENCES Colonia(id_Colonia)
);
GO

CREATE TABLE Establecimiento (
id_Establecimiento INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Direccion TEXT NOT NULL,
CodigoEstablecimiento VARCHAR(12)
);
GO

--Tablas Usuario y Permisos
CREATE TABLE Persona (
id_Persona INTEGER PRIMARY KEY IDENTITY(1,1),
PrimerNombre VARCHAR(100) NOT NULL,
SegundoNombre VARCHAR(100),
PrimerApellido VARCHAR(100) NOT NULL,
SegundoApellido VARCHAR(100),
Telefono VARCHAR(20) NOT NULL,
Direccion_id INTEGER NOT NULL,
FOREIGN KEY (Direccion_id) REFERENCES Direccion(id_Direccion)
);
GO

CREATE TABLE InformacionFiscal (
id_InformacionFiscal INTEGER PRIMARY KEY IDENTITY(1,1),
RTN VARCHAR(25) NOT NULL,
TipoContribuyente VARCHAR(20),
FechaRegistro DATE DEFAULT GETDATE(),
Persona_id INTEGER NOT NULL,
FOREIGN KEY (Persona_id) REFERENCES Persona(id_Persona)
);

CREATE TABLE Usuario (
id_Usuario INTEGER PRIMARY KEY IDENTITY(1,1),
Correo VARCHAR(250) NOT NULL UNIQUE,
Contrasenia VARCHAR(250) NOT NULL,
InicioUso DATETIME,
FinUso DATETIME,
Rol_id INTEGER NOT NULL,
Persona_id INTEGER NOT NULL,
FOREIGN KEY (Persona_id) REFERENCES Persona(id_Persona),
FOREIGN KEY (Rol_id) REFERENCES RolUsuario(id_RolUsuario)
);
GO

CREATE TABLE Permiso (
id_Permiso INTEGER PRIMARY KEY IDENTITY(1,1),
Nombre VARCHAR(100) NOT NULL,
Descripcion TEXT
);
GO

CREATE TABLE RolPermiso (
id_RolPermiso INTEGER PRIMARY KEY IDENTITY(1,1),
Rol_id INTEGER NOT NULL,
Permiso_id INTEGER NOT NULL,
FOREIGN KEY (Rol_id) REFERENCES RolUsuario(id_RolUsuario),
FOREIGN KEY (Permiso_id) REFERENCES Permiso(id_Permiso)
);
GO

CREATE TABLE Empleado (
id_Empleado INTEGER PRIMARY KEY IDENTITY(1,1),
Horario_id INTEGER,
Usuario_id INTEGER NOT NULL,
Estado VARCHAR(100),
FOREIGN KEY (Horario_id) REFERENCES HorarioTrabajo(id_HorarioTrabajo),
FOREIGN KEY (Usuario_id) REFERENCES Usuario(id_Usuario)
);
GO

CREATE TABLE Cliente (
id_Cliente INTEGER PRIMARY KEY IDENTITY(1,1),
Usuario_id INTEGER NOT NULL,
TipoExoneracion_id INTEGER,
FOREIGN KEY (Usuario_id) REFERENCES Usuario(id_Usuario),
FOREIGN KEY (TipoExoneracion_id) REFERENCES TipoExoneracion(id_TipoExoneracion)
);
GO

--Tablas Gestion Vehiculos
CREATE TABLE Modelo (
id_Modelo INTEGER PRIMARY KEY IDENTITY(1,1),
Marca_id INTEGER NOT NULL,
Nombre VARCHAR(100) NOT NULL,
FOREIGN KEY (Marca_id) REFERENCES Marca(id_Marca)
);
GO

CREATE TABLE ParqueoVehiculo (
id_ParqueoVehiculo INTEGER PRIMARY KEY IDENTITY(1,1),
Lote VARCHAR(50) NOT NULL,
Referencia VARCHAR(100)
);
GO

CREATE TABLE Proveedor (
id_Proveedor INTEGER PRIMARY KEY IDENTITY(1,1),
NombreProveedor VARCHAR(100) NOT NULL,
RTN VARCHAR(20) NOT NULL,
ContactoNombre VARCHAR(100) NOT NULL,
Telefono VARCHAR(15) NOT NULL,
Correo VARCHAR(100) NOT NULL,
Direccion VARCHAR(100),
TipoProveedor VARCHAR(100) NOT NULL
);
GO

CREATE TABLE Vehiculo (
id_Vehiculo INTEGER PRIMARY KEY IDENTITY(1,1),
Modelo_id INTEGER NOT NULL,
Anio VARCHAR(4) NOT NULL,
VIN VARCHAR(17) NOT NULL,
Motor VARCHAR(100) NOT NULL,
MatriculaPlaca VARCHAR(100) NOT NULL,
Disponibilidad BIT DEFAULT 1,
PrecioVenta DECIMAL(13,2) NOT NULL,
PrecioAlquiler DECIMAL(13,2) NOT NULL,
TipoVehiculo_id INTEGER,
Estado VARCHAR(100) NOT NULL,
TipoCombustible VARCHAR(100) NOT NULL,
UsoVehiculo_id INTEGER,
ParqueoVehiculo_id INTEGER,
Proveedor_id INTEGER,
FOREIGN KEY (Modelo_id) REFERENCES Modelo(id_Modelo),
FOREIGN KEY (TipoVehiculo_id) REFERENCES TipoVehiculo(id_TipoVehiculo),	
FOREIGN KEY (UsoVehiculo_id) REFERENCES UsoVehiculo(id_UsoVehiculo),
FOREIGN KEY (ParqueoVehiculo_id) REFERENCES ParqueoVehiculo(id_ParqueoVehiculo),
FOREIGN KEY (Proveedor_id) REFERENCES Proveedor(id_Proveedor)
);
GO

CREATE TABLE CompraVehiculo (
id_CompraVehiculo INTEGER PRIMARY KEY IDENTITY(1,1),
Proveedor_id INTEGER,
Vehiculo_id INTEGER,
FechaCompra DATETIME,
CostoCompra DECIMAL(13,2) NOT NULL,
NumeroFacturaProveedor VARCHAR(100),
ComprobanteCompra VARCHAR(250),
Notas TEXT,
FOREIGN KEY (Proveedor_id) REFERENCES Proveedor(id_Proveedor),
FOREIGN KEY (Vehiculo_id) REFERENCES Vehiculo(id_Vehiculo)
);
GO

CREATE TABLE VehiculoColor (
id_VehiculoColor INTEGER PRIMARY KEY IDENTITY(1,1),
Vehiculo_id INTEGER NOT NULL,
Color_id INTEGER NOT NULL,
FOREIGN KEY (Vehiculo_id) REFERENCES Vehiculo(id_Vehiculo),
FOREIGN KEY (Color_id) REFERENCES Color(id_Color)
);
GO

CREATE TABLE Seguro (
id_Seguro INTEGER PRIMARY KEY IDENTITY(1,1),
TipoSeguro_id INTEGER,
Cobertura TEXT,
Costo DECIMAL(13,2) NOT NULL,
Vehiculo_id INTEGER,
FOREIGN KEY (TipoSeguro_id) REFERENCES TipoSeguro(id_TipoSeguro),
FOREIGN KEY (Vehiculo_id) REFERENCES Vehiculo(id_Vehiculo)
);
GO

--Tablas Contratos y Transacciones
CREATE TABLE PuntoEmision (
id_PuntoEmision INTEGER PRIMARY KEY IDENTITY(1,1),
CodigoPuntoEmision VARCHAR(3) NOT NULL,
Descripcion TEXT,
Establecimiento_id INTEGER NOT NULL,
FOREIGN KEY (Establecimiento_id) REFERENCES Establecimiento(id_Establecimiento)
);
GO

CREATE TABLE RangoAutorizado (
id_RangoAutorizado INTEGER PRIMARY KEY IDENTITY(1,1),
TipoDocumento_id INTEGER NOT NULL,
PuntoEmision_id INTEGER NOT NULL,
CAI VARCHAR(30) NOT NULL,
NumeroInicial INTEGER NOT NULL,
NumeroFinal INTEGER NOT NULL,
FechaInicio DATETIME NOT NULL,
FechaFin DATETIME NOT NULL,
FOREIGN KEY (TipoDocumento_id) REFERENCES TipoDocumento(id_TipoDocumento),
FOREIGN KEY (PuntoEmision_id) REFERENCES PuntoEmision(id_PuntoEmision)
);
GO

CREATE TABLE Contrato (
id_Contrato INTEGER PRIMARY KEY IDENTITY(1,1),
Vendedor_id INTEGER NOT NULL,
Cliente_id INTEGER NOT NULL,
Vehiculo_id INTEGER NOT NULL,
FechaContrato DATETIME DEFAULT GETDATE(),
TerminosCondiciones TEXT,
GarantiaRequerida TEXT,
RecargoIncumplimiento DECIMAL(13,2) NOT NULL,
TipoContrato VARCHAR(100) NOT NULL CHECK (TipoContrato IN ('Alquiler', 'Venta')),
EstadoContrato VARCHAR(100) NOT NULL CHECK (EstadoContrato IN ('Activo', 'Finalizado', 'Cancelado')),
FirmaCliente BIT DEFAULT 1,
FOREIGN KEY (Vehiculo_id) REFERENCES Vehiculo(id_Vehiculo),
FOREIGN KEY (Vendedor_id) REFERENCES Empleado(id_Empleado),
FOREIGN KEY (Cliente_id) REFERENCES Cliente(id_Cliente)
);
GO

CREATE TABLE ContratoAlquiler (
id_Contrato INTEGER PRIMARY KEY,
FechaInicioAlquiler DATETIME,
FechaFinAlquiler DATETIME,
FechaEntregaReal DATETIME,
KilometrajePermitido INTEGER NOT NULL,
PoliticaCombustible TEXT,
EsTardia BIT DEFAULT 1,
EsExtensible BIT DEFAULT 1,
ReporteDanios TEXT,
Clausulas TEXT,
FOREIGN KEY (id_Contrato) REFERENCES Contrato(id_Contrato),
);
GO

CREATE TABLE ContratoVenta (
id_Contrato INTEGER PRIMARY KEY,
FechaVenta DATETIME,
Monto DECIMAL(13,2) NOT NULL,
FOREIGN KEY (id_Contrato) REFERENCES Contrato(id_Contrato)
);
GO

CREATE TABLE DocumentoFiscal (
id_DocumentoFiscal INTEGER PRIMARY KEY IDENTITY(1,1),
Contrato_id INTEGER NOT NULL,
CAI VARCHAR(30) NOT NULL,
RangoAutorizado_id INTEGER NOT NULL,
NumeroDocumentoFiscal INTEGER NOT NULL,
FechaEmision DATETIME DEFAULT GETDATE(),
EsExonerado BIT DEFAULT 0,
Subtotal DECIMAL(13,2) NOT NULL,
ImpuestoTotal DECIMAL(13,2) NOT NULL,
Total Decimal(13,2) NOT NULL,
Estado VARCHAR(100) NOT NULL CHECK (Estado IN ('Emitido', 'Anulado', 'Pendiente')),
FOREIGN KEY (RangoAutorizado_id) REFERENCES RangoAutorizado(id_RangoAutorizado),
FOREIGN KEY (Contrato_id) REFERENCES Contrato(id_Contrato)
);
GO

CREATE TABLE DetalleDocumentoFiscal (
id_DetalleDocumentoFiscal INTEGER PRIMARY KEY IDENTITY(1,1),
DocumentoFiscal_id INTEGER NOT NULL,
Vehiculo_id INTEGER NOT NULL,
Descripcion VARCHAR(200) NOT NULL,
Cantidad INTEGER NOT NULL,
PrecioUnitario DECIMAL(13,2) NOT NULL,
Impuesto DECIMAL(13,2) NOT NULL,
TotalLinea DECIMAL(13,2) NOT NULL,
FOREIGN KEY (Vehiculo_id) REFERENCES Vehiculo(id_Vehiculo)
);
GO

CREATE TABLE PagoDocumentoFiscal (
id_PagoDocumentoFiscal INTEGER PRIMARY KEY IDENTITY(1,1),
DocumentoFiscal_id INTEGER NOT NULL,
MetodoPago_id INTEGER NOT NULL,
Monto DECIMAL(13,2) NOT NULL,
Referencia VARCHAR(50),
FOREIGN KEY (DocumentoFiscal_id) REFERENCES DocumentoFiscal(id_DocumentoFiscal),
FOREIGN KEY (MetodoPago_id) REFERENCES MetodoPago(id_MetodoPago)
);
GO