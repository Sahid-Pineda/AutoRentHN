# AutoRentHN

**AutoRentHN** es una aplicación web basada en Django para la gestión de alquiler y venta de vehículos.

## Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Instrucciones de Configuración](#instrucciones-de-configuración)
- [Ejecutar el Proyecto](#ejecutar-el-proyecto)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Descripción del Proyecto
AutoRentHN está diseñado para optimizar el proceso de alquiler y venta de vehículos. Incluye funcionalidades para el registro de usuarios, gestión de catálogos de vehículos y procesamiento de transacciones. La aplicación utiliza Django como framework backend y se conecta a una base de datos (por ejemplo, SQL Server) para el almacenamiento de datos.

## Características
- Registro de usuarios con información fiscal y detalles de dirección
- Gestión de alquiler y venta de vehículos
- Integración con una base de datos relacional
- Autenticación segura de usuarios y acceso basado en roles
- Interfaz frontend responsiva para una experiencia de usuario fluida

## Requisitos Previos
Antes de configurar el proyecto, asegúrate de tener instalado lo siguiente:
- **Python** (versión 3.8 o superior)
- **Git**
- **pip** (gestor de paquetes de Python)

## Instrucciones de Configuración
Sigue estos pasos para clonar y configurar el proyecto AutoRentHN localmente:

1. **Clonar el Repositorio**  
Pasos para clonar y levantar el proyecto
Abrir terminal y ubicarse en la carpeta donde querés clonar el repo.

1. Ejecutar git clone [url_del_repositorio]

2. Entrar a la carpeta del proyecto clonado con cd nombre_del_proyecto.

3. Crear el entorno virtual con python -m venv venv.

4. Activar el entorno virtual:

     En Windows CMD: venv\Scripts\activate

5. Instalar dependencias con pip install -r requirements.txt.

> (Opcional en Django) Correr migraciones: python manage.py migrate.

6. Ejecutar el servidor con python manage.py runserver.

7. Abrir en el navegador http://127.0.0.1:8000/ y listo.
