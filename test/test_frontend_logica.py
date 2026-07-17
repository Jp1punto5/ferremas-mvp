import unittest


# ============================================================
# Logica de frontend extraida para pruebas unitarias Python
# ============================================================
# Las funciones mostrarProductos() y mostrarResumenCompra() en
# vista/js/cargar_imagen.js y vista/js/carrito.js contienen
# reglas de negocio puras que no dependen del DOM.
# Se extraen aqui para validarlas con unittest sin necesitar
# un navegador ni Node.js.
# ============================================================


def filtrar_productos_visibles(productos):
    """
    Replica la logica de mostrarProductos(productos) en cargar_imagen.js.

    Solo muestra productos con stock <= 10:
        if(producto.stock <= 10) { ... renderizar ... }

    Retorna la lista de productos que serian renderizados.
    """
    return [p for p in productos if p.get('stock', 0) <= 10]


def calcular_resumen_compra(carrito, usuario_logeado=False):
    """
    Replica la logica de mostrarResumenCompra() en carrito.js.

    Calcula el total del carrito y aplica descuento del 10% si el
    usuario esta logeado:
        if(usuarioLogeado) {
            descuento = Number(total) * 0.10;
            total = Number(total) - descuento;
        }

    Retorna un dict con: total_bruto, descuento, total_final.
    """
    total_bruto = sum(
        item['precio'] * item['cantidad']
        for item in carrito
    )

    descuento = 0.0
    if usuario_logeado:
        descuento = round(total_bruto * 0.10, 2)

    total_final = round(total_bruto - descuento, 2)

    return {
        'total_bruto': total_bruto,
        'descuento': descuento,
        'total_final': total_final
    }


class TestFrontendLogica(unittest.TestCase):
    """
    Tests unitarios de logica de frontend.

    Validan las reglas de negocio implementadas en:
      - vista/js/cargar_imagen.js  (funcion mostrarProductos)
      - vista/js/carrito.js        (funcion mostrarResumenCompra)

    No requieren DOM, navegador ni Node.js. Se verifican las mismas
    reglas que el JS aplica, usando Python como motor de prueba.
    """

    # ----------------------------------------------------------
    # FL-001: mostrarProductos — solo renderiza stock <= 10
    # ----------------------------------------------------------
    def test_FL001_mostrar_productos_filtra_stock_mayor_10(self):
        print('\n=== TEST: FL-001 - mostrarProductos filtra stock > 10 ===')
        print('Logica JS: if(producto.stock <= 10) { renderizar }')

        productos = [
            {'nombre': 'Martillo',   'precio_cl': 12000, 'stock': 5},
            {'nombre': 'Taladro',    'precio_cl': 55000, 'stock': 15},
            {'nombre': 'Serrucho',   'precio_cl': 8000,  'stock': 10},
            {'nombre': 'Nivel',      'precio_cl': 4500,  'stock': 20},
        ]

        visibles = filtrar_productos_visibles(productos)
        nombres = [p['nombre'] for p in visibles]
        print('Productos enviados:', [p['nombre'] for p in productos])
        print('Productos visibles (stock <= 10):', nombres)

        self.assertIn('Martillo', nombres,  'Stock=5 debe ser visible')
        self.assertIn('Serrucho', nombres,  'Stock=10 debe ser visible (borde)')
        self.assertNotIn('Taladro', nombres, 'Stock=15 NO debe ser visible')
        self.assertNotIn('Nivel', nombres,   'Stock=20 NO debe ser visible')
        self.assertEqual(len(visibles), 2)
        print('Filtro de stock -> CUMPLE regla de negocio')

    # ----------------------------------------------------------
    # FL-002: mostrarProductos — lista vacia si todos tienen stock > 10
    # ----------------------------------------------------------
    def test_FL002_mostrar_productos_lista_vacia_si_todo_sin_stock(self):
        print('\n=== TEST: FL-002 - mostrarProductos lista vacia sin stock valido ===')
        print('Logica JS: grid.innerHTML = ""; forEach solo agrega si stock <= 10')

        productos = [
            {'nombre': 'Gato hidraulico', 'precio_cl': 90000, 'stock': 50},
            {'nombre': 'Compresor',        'precio_cl': 150000, 'stock': 30},
        ]

        visibles = filtrar_productos_visibles(productos)
        print('Productos enviados:', [p['nombre'] for p in productos])
        print('Productos visibles:', visibles)

        self.assertEqual(len(visibles), 0, 'No debe renderizar nada si todos tienen stock > 10')
        print('Grid queda vacio -> CUMPLE regla de negocio')

    # ----------------------------------------------------------
    # FL-003: mostrarResumenCompra — sin login NO aplica descuento
    # ----------------------------------------------------------
    def test_FL003_resumen_sin_login_no_aplica_descuento(self):
        print('\n=== TEST: FL-003 - mostrarResumenCompra sin usuario logeado ===')
        print('Logica JS: if(usuarioLogeado) { descuento = total * 0.10 }')
        print('Escenario: usuarioLogeado = null/false -> descuento = 0')

        carrito = [
            {'nombre': 'Martillo', 'precio': 12000, 'precio_usd': 12.8, 'cantidad': 2},
            {'nombre': 'Serrucho', 'precio': 8000,  'precio_usd': 8.5,  'cantidad': 1},
        ]

        resumen = calcular_resumen_compra(carrito, usuario_logeado=False)
        print('Carrito:', [(p['nombre'], p['cantidad']) for p in carrito])
        print('Resumen:', resumen)

        self.assertEqual(resumen['total_bruto'], 32000)
        self.assertEqual(resumen['descuento'], 0.0, 'Sin login no debe aplicar descuento')
        self.assertEqual(resumen['total_final'], 32000, 'Total final = total bruto sin descuento')
        print('Sin descuento aplicado -> CUMPLE regla de negocio')

    # ----------------------------------------------------------
    # FL-004: mostrarResumenCompra — con login aplica 10% descuento
    # ----------------------------------------------------------
    def test_FL004_resumen_con_login_aplica_descuento_10_porciento(self):
        print('\n=== TEST: FL-004 - mostrarResumenCompra con usuario logeado ===')
        print('Logica JS: descuento = Number(total) * 0.10; total = total - descuento;')

        carrito = [
            {'nombre': 'Martillo', 'precio': 12000, 'precio_usd': 12.8, 'cantidad': 2},
            {'nombre': 'Serrucho', 'precio': 8000,  'precio_usd': 8.5,  'cantidad': 1},
        ]

        resumen = calcular_resumen_compra(carrito, usuario_logeado=True)
        print('Carrito:', [(p['nombre'], p['cantidad']) for p in carrito])
        print('Resumen:', resumen)

        esperado_bruto    = 32000
        esperado_desc     = round(32000 * 0.10, 2)  # 3200.0
        esperado_final    = round(32000 - esperado_desc, 2)  # 28800.0

        self.assertEqual(resumen['total_bruto'], esperado_bruto)
        self.assertAlmostEqual(resumen['descuento'], esperado_desc, places=2,
                               msg='El descuento debe ser exactamente el 10%')
        self.assertAlmostEqual(resumen['total_final'], esperado_final, places=2,
                               msg='El total final debe ser total - 10%')
        print(f'Descuento 10% = {esperado_desc} CLP, total final = {esperado_final} CLP -> CUMPLE')


if __name__ == '__main__':
    unittest.main()
