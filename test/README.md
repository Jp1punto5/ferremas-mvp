

Para testear las pruebas unitarias se utilizaron las de productos.

para esto se debe lenvantar el entorno virtual y posterior a eso ejecutar el siguiente codigo en la terminal.

python -m unittest test.test_productos


Para realizar las pruebas de integración, se debe seguir el mismo esquema que antes pero ejecutando esto:

python -m unittest test.test_integracion

Para las pruebas o test de Mock del webpay para mensaje exitoso o de error, se debe abrir el archivo HTML
test_mock_webpay.html