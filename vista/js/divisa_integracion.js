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
    try {
        const respuesta = await fetch('http://127.0.0.1:5002/dolar');
        // visualizamos la respuesta en consola (object)
        console.log("Respuesta API mindicador.cl = ", respuesta);
        
        if (!respuesta.ok) {
            throw new Error(`Error HTTP: ${respuesta.status}`);
        }
        
        const datos = await respuesta.json();
        console.log("respuesta Json = ", datos);
        
        if (datos.error) {
            throw new Error(datos.error);
        }
        
        const tasaCambio = datos.valor;
        const fecha = datos.fecha;
        
        console.log(`✅ Tasa de cambio obtenida: 1 CLP = ${tasaCambio} USD (${fecha})`);
        
        return {
            exito: true,
            tasa: tasaCambio,
            fecha: fecha,
            origen: 'mindicador.cl'
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
            'http://127.0.0.1:5003/actualizar-precios-usd',
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
            `http://127.0.0.1:5003/actualizar-precio-usd/${codigoProducto}`,
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

