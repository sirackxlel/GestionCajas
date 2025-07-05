# Instrucciones de Instalación

Este proyecto es una aplicación web basada en Django para gestionar cajas y entidades. A continuación se describen los pasos para ponerla en marcha en un entorno local.

## Requisitos previos

- Python 3.10 o superior
- Git
- `virtualenv` (opcional pero recomendado)

## Instalación

1. **Clonar el repositorio**

```bash
git clone <URL-del-repositorio>
cd GestionCajas
```

2. **Crear un entorno virtual (opcional)**

```bash
python3 -m venv env
source env/bin/activate  # En Windows usar `env\Scripts\activate`
```

3. **Instalar las dependencias**

```bash
pip install -r requirements.txt
```

4. **Aplicar las migraciones**

```bash
python manage.py migrate
```

5. **(Opcional) Crear un superusuario para el panel de administración**

```bash
python manage.py createsuperuser
```

6. **Ejecutar el servidor de desarrollo**

```bash
python manage.py runserver
```

El sitio estará disponible en `http://127.0.0.1:8000/`.

## Notas adicionales

- La base de datos por defecto es SQLite y se crea automáticamente en `db.sqlite3`.
- Las plantillas se encuentran en la carpeta `templates`.
- Para desplegar en producción, asegúrate de configurar las variables de entorno adecuadas y el servidor web de tu elección.