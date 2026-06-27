# Pruebas de Software - Ferremas MVP

Esta carpeta contiene los archivos utilizados para validar el correcto funcionamiento del sistema **Ferremas-MVP**, incluyendo pruebas unitarias, de integración, Mock, carga y estrés.

## Requisitos

Antes de ejecutar cualquiera de las pruebas, asegúrese de:

1. Clonar el repositorio.
2. Crear y activar el entorno virtual.
3. Instalar las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

---

## Pruebas Unitarias

Las pruebas unitarias verifican el funcionamiento individual de las funciones del módulo de productos.

Ejecutar:

```bash
python -m unittest test.test_productos
```

---

## Pruebas de Integración

Las pruebas de integración validan la comunicación entre la aplicación Flask y la base de datos SQLite.

Ejecutar:

```bash
python -m unittest test.test_integracion
```

---

## Pruebas Mock

Las pruebas Mock simulan la respuesta del servicio de Webpay sin necesidad de levantar **Ferremas-API** ni establecer una conexión con servicios externos.

Para ejecutarlas, abrir en un navegador el archivo ubicado en:

```text
vista/test_mock_webpay.html
```

El archivo permite ejecutar dos escenarios:

* **Pago exitoso:** Simula una respuesta satisfactoria del servicio Webpay.
* **Pago con error:** Simula una respuesta de error del servicio Webpay.

---

## Pruebas de Carga

Antes de ejecutar esta prueba, asegúrese de que el servidor **Ferremas-MVP** se encuentre en ejecución.

Ejecutar:

```bash
python test/test_carga.py
```

---

## Pruebas de Estrés

Antes de ejecutar esta prueba, asegúrese de que el servidor **Ferremas-MVP** se encuentre en ejecución.

Ejecutar:

```bash
python test/test_estres.py
```

> **Nota:** La prueba de estrés somete al servidor a una carga elevada de solicitudes concurrentes. Debido a que la aplicación utiliza el servidor de desarrollo de Flask, es esperable que bajo una carga extrema el servidor alcance su límite de capacidad y comience a rechazar nuevas conexiones.
