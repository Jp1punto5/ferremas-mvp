/**
 * INTEGRACIÓN DE DIVISAS
 * Obtiene la tasa de cambio CLP/USD desde API de Ferremas
 * y actualiza automáticamente los precios en USD de todos los productos
 */

// ========================================
// OBTENER TASA DE CAMBIO
// ========================================

async function obtenerTasaCambio() {
    /**
     * Obtiene la tasa de cambio CLP/USD desde API de ferremas-api
     * Utiliza mindicador.cl como fuente oficial de datos de divisas en Chile
     * 
     * Returns:
     *   Object: { exito: boolean, tasa: number, fecha: string, error?: string }
     */
    const PRIMARY = 'http://127.0.0.1:5002/dolar';
    const MOCK = 'http://127.0.0.1:5050/api/dolar';

    async function _fetchUrl(url) {
        const r = await fetch(url);
        if (!r.ok) throw new Error(`Error HTTP: ${r.status}`);
        const d = await r.json();
        if (d.error) throw new Error(d.error || 'Error en respuesta');
        return d;
    }

    try {
        // Intentar la URL primaria (ferremas-api)
        let datos = null;
        try {
            const respuesta = await _fetchUrl(PRIMARY);
            datos = respuesta;
            console.log("Usando ferremas-api para tasa de cambio");
        } catch (errPrimary) {
            console.warn('ferremas-api no disponible o dio error, usando mock:', errPrimary.message);
            // Intentar el mock
            const respuestaMock = await _fetchUrl(MOCK);
            datos = respuestaMock;
        }

        // Compatibilidad: mindicador.cl y nuestro mock retornan estructura con 'serie' o con {valor, fecha}
        let tasaCambio = null;
        let fecha = null;
        if (datos.serie && datos.serie.length) {
            tasaCambio = datos.serie[0].valor || datos.serie[0].valor || datos.serie[0].valor;
            fecha = datos.serie[0].fecha;
        } else if (datos.valor) {
            tasaCambio = datos.valor;
            fecha = datos.fecha || new Date().toISOString();
        } else if (datos[0] && datos[0].valor) {
            tasaCambio = datos[0].valor;
            fecha = datos[0].fecha || new Date().toISOString();
        } else if (datos.serie && datos.serie[0] && datos.serie[0].valor) {
            tasaCambio = datos.serie[0].valor;
            fecha = datos.serie[0].fecha;
        }

        if (!tasaCambio) throw new Error('No se pudo leer tasa de cambio de la respuesta');

        console.log(`✅ Tasa de cambio obtenida: 1 CLP = ${tasaCambio} USD (${fecha})`);
        return {
            exito: true,
            tasa: tasaCambio,
            fecha: fecha,
            origen: 'externo'
        };
    } catch (error) {
        console.error('❌ Error obteniendo tasa de cambio:', error);
        return {
            exito: false,
            tasa: null,
            error: error.message,
            fecha: new Date().toISOString()
        };
    }
}


// ========================================
// ACTUALIZAR PRECIOS EN BD
// ========================================

async function actualizarPreciosUSD(tasaCambio) {
    /**
     * Envía la tasa de cambio al servidor para actualizar todos los precios USD
     * 
     * Args:
     *   tasaCambio (number): Tasa de cambio CLP a USD
     *   
     * Returns:
     *   Object: { exito: boolean, mensaje: string, productosActualizados?: number }
     */
    try {
        const respuesta = await fetch(
            'http://127.0.0.1:5002/actualizar-precios-usd',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tasa_cambio: tasaCambio
                })
            }
        );
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP: ${respuesta.status}`);
        }
        
        const datos = await respuesta.json();
        
        console.log(`✅ Precios actualizados: ${datos.productos_actualizados} productos`);
        
        return {
            exito: true,
            mensaje: datos.mensaje,
            productosActualizados: datos.productos_actualizados,
            tasaCambioUsada: datos.tasa_cambio_usada
        };
    } catch (error) {
        console.error('❌ Error actualizando precios:', error);
        return {
            exito: false,
            mensaje: `Error: ${error.message}`,
            productosActualizados: 0
        };
    }
}


// ========================================
// ACTUALIZAR PRECIO INDIVIDUAL
// ========================================

async function actualizarPrecioIndividual(codigoProducto, tasaCambio) {
    /**
     * Actualiza el precio USD de un producto específico
     * 
     * Args:
     *   codigoProducto (string): Código del producto
     *   tasaCambio (number): Tasa de cambio CLP a USD
     *   
     * Returns:
     *   Object: { exito: boolean, mensaje: string, producto?: Object }
     */
    try {
        const respuesta = await fetch(
            `http://127.0.0.1:5002/actualizar-precio-usd/${codigoProducto}`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    tasa_cambio: tasaCambio
                })
            }
        );
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP: ${respuesta.status}`);
        }
        
        const datos = await respuesta.json();
        
        console.log(`✅ Precio de ${codigoProducto} actualizado a USD ${datos.producto.precio_usd}`);
        
        return {
            exito: true,
            mensaje: datos.mensaje,
            producto: datos.producto
        };
    } catch (error) {
        console.error(`❌ Error actualizando precio de ${codigoProducto}:`, error);
        return {
            exito: false,
            mensaje: `Error: ${error.message}`
        };
    }
}


// ========================================
// FLUJO AUTOMÁTICO
// ========================================

async function sincronizarPrecios() {
    /**
     * Ejecuta el flujo completo:
     * 1. Obtiene tasa de cambio desde ferremas-api
     * 2. Actualiza precios de todos los productos en BD
     * 
     * Se ejecuta automáticamente al cargar la página
     * 
     * Returns:
     *   Object: { exito: boolean, tasaCambio: number, productosActualizados: number }
     */
    console.log('🔄 Iniciando sincronización de precios...');
    
    // Paso 1: Obtener tasa de cambio desde API de ferremas
    const tasaResult = await obtenerTasaCambio();
    if (!tasaResult.exito) {
        console.error('❌ No se pudo obtener la tasa de cambio');
        return {
            exito: false,
            tasaCambio: null,
            productosActualizados: 0,
            error: tasaResult.error
        };
    }
    
    // Paso 2: Actualizar todos los precios en ferremas-mvp
    const updateResult = await actualizarPreciosUSD(tasaResult.tasa);
    
    console.log('✅ Sincronización completada');
    
    return {
        exito: updateResult.exito,
        tasaCambio: tasaResult.tasa,
        productosActualizados: updateResult.productosActualizados,
        fecha: tasaResult.fecha
    };
}


// ========================================
// EJECUCIÓN AUTOMÁTICA
// ========================================

// Ejecutar sincronización cuando el documento esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', sincronizarPrecios);
} else {
    sincronizarPrecios();
}

// Ejecutar cada 30 minutos para mantener precios actualizados
// Cambiar el valor (en milisegundos) para ajustar la frecuencia
setInterval(sincronizarPrecios, 1800000);  // 30 minutos

