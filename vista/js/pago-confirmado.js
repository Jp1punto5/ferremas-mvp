/* ========================================= */
/* CONFIRMACIÓN DE PAGO - JAVASCRIPT */
/* ========================================= */

/**
 * Obtener URL base dinámicamente
 * Funciona tanto con file:// como con http://
 */
function obtenerUrlBase() {
    if (window.location.protocol === 'file:') {
        return 'http://127.0.0.1:5003/vista';
    }
    return window.location.origin + '/vista';
}

/**
 * Construir URL absoluta para navegación
 * @param {string} pagina - Nombre de la página (ej: catalogo_p.html)
 * @returns {string} URL absoluta
 */
function construirUrlPagina(pagina) {
    if (window.location.protocol === 'file:') {
        return `http://127.0.0.1:5003/vista/${pagina}`;
    }
    return `/vista/${pagina}`;
}

/**
 * Inicializar la página cuando carga
 */
async function inicializarPaginaConfirmacion() {
    console.log("📄 Inicializando página de confirmación...");
    
    // Obtener token de la URL
    const params = new URLSearchParams(window.location.search);
    const tokenWs = params.get('token_ws');

    console.log("🔍 Token recibido:", tokenWs ? "Sí" : "No");

    if (!tokenWs) {
        mostrarErrorSinToken();
        return;
    }

    // Mostrar spinner
    mostrarSpinner();

    // Confirmar pago
    try
    {
        const resultadoCompra = await confirmarPagoWebpay(tokenWs);

        if(resultadoCompra.estado === "AUTHORIZED")
        {
            mostrarExito(resultadoCompra);
        }
        else
        {
            mostrarError(resultadoCompra);
        }
        

    } catch (error)
    {
        console.error(error);
    }

}

/**
 * Mostrar spinner mientras se confirma el pago
 */
function mostrarSpinner() {
    const spinner = document.getElementById('spinner');
    if (spinner) {
        spinner.style.display = 'block';
    }
}

/**
 * Ocultar spinner
 */
function ocultarSpinner() {
    const spinner = document.getElementById('spinner');
    if (spinner) {
        spinner.style.display = 'none';
    }
}

/**
 * Mostrar éxito del pago
 * @param {Object} datos - Datos del pago confirmado
 */
function mostrarExito(datos) {
    console.log("✅ Pago exitoso", datos);

    ocultarSpinner();

    // Mostrar contenedor de resultado
    const resultadoContainer = document.getElementById('resultadoContainer');
    if (resultadoContainer) {
        resultadoContainer.style.display = 'block';
    }

    // Mostrar sección de éxito
    const exitoContainer = document.getElementById('exitoContainer');
    if (exitoContainer) {
        exitoContainer.style.display = 'block';
    }

    // Ocultar sección de error
    const errorContainer = document.getElementById('errorContainer');
    if (errorContainer) {
        errorContainer.style.display = 'none';
    }

    // Llenar detalles
    const detalles = {
        detalleOrden: datos.orden || '-',
        detalleMonto: `$${parseInt(datos.monto || 0).toLocaleString('es-CL')}`,
        detalleCodigoRespuesta: datos.codigo_respuesta || '-',
        detalleAutorizacion: datos.autorizacion || '-',
        detalleFecha: new Date().toLocaleString('es-AR')
    };

    for (const [id, valor] of Object.entries(detalles)) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = valor;
        }
    }

    // Guardar en sessionStorage
    sessionStorage.setItem('pagoProcesado', JSON.stringify(datos));

    // Limpiar carrito
    sessionStorage.removeItem('carrito');

    // Actualizar botones con URLs correctas
    actualizarUrlsBotones();
}

/**
 * Mostrar error del pago
 * @param {Object} datos - Datos del error
 */
function mostrarError(datos) {
    console.log("❌ Pago rechazado", datos);

    ocultarSpinner();

    // Mostrar contenedor de resultado
    const resultadoContainer = document.getElementById('resultadoContainer');
    if (resultadoContainer) {
        resultadoContainer.style.display = 'block';
    }

    // Mostrar sección de error
    const errorContainer = document.getElementById('errorContainer');
    if (errorContainer) {
        errorContainer.style.display = 'block';
    }

    // Ocultar sección de éxito
    const exitoContainer = document.getElementById('exitoContainer');
    if (exitoContainer) {
        exitoContainer.style.display = 'none';
    }

    // Llenar detalles del error
    const detalles = {
        errorOrden: datos.orden || 'No se recibió token de Webpay',
        errorCodigo: datos.codigo_respuesta || 'Token no encontrado',
        errorMensaje: 'El pago no fue procesado correctamente'
    };

    for (const [id, valor] of Object.entries(detalles)) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = valor;
        }
    }

    // Mostrar mensaje de error
    const mensajeError = document.getElementById('mensajeError');
    if (mensajeError) {
        mensajeError.style.display = 'block';
    }

    // Actualizar botones con URLs correctas
    actualizarUrlsBotones();
}

/**
 * Mostrar error cuando no hay token
 */
function mostrarErrorSinToken() {
    console.log("⚠️ No se recibió token de Webpay");

    ocultarSpinner();

    // Mostrar contenedor de resultado
    const resultadoContainer = document.getElementById('resultadoContainer');
    if (resultadoContainer) {
        resultadoContainer.style.display = 'block';
    }

    // Mostrar sección de error
    const errorContainer = document.getElementById('errorContainer');
    if (errorContainer) {
        errorContainer.style.display = 'block';
    }

    // Llenar detalles
    const elemento = document.getElementById('errorMensaje');
    if (elemento) {
        elemento.textContent = 'No se recibió confirmación de Webpay. Es posible que hayas cancelado el pago.';
    }

    // Mostrar mensaje
    const mensajeError = document.getElementById('mensajeError');
    if (mensajeError) {
        mensajeError.style.display = 'block';
    }

    // Actualizar botones
    actualizarUrlsBotones();
}

/**
 * Actualizar URLs de los botones para funcionar tanto con file:// como http://
 */
function actualizarUrlsBotones() {
    // Botón Seguir Comprando (en éxito)
    const btnExito = document.querySelector('#exitoContainer .btn-exito');
    if (btnExito) {
        btnExito.href = construirUrlPagina('catalogo_p.html');
        btnExito.addEventListener('click', (e) => {
            e.preventDefault();
            window.location.href = construirUrlPagina('catalogo_p.html');
        });
    }

    // Botón Volver al Catálogo (en error)
    const btnsError = document.querySelectorAll('#errorContainer .btn-confirmacion');
    btnsError.forEach(btn => {
        if (btn.textContent.includes('Catálogo')) {
            btn.href = construirUrlPagina('catalogo_p.html');
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = construirUrlPagina('catalogo_p.html');
            });
        } else if (btn.textContent.includes('Carrito')) {
            btn.href = construirUrlPagina('carrito.html');
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                window.location.href = construirUrlPagina('carrito.html');
            });
        }
    });
}

/**
 * Descargar comprobante como archivo de texto
 */
function descargarComprobante() {
    const datos = JSON.parse(sessionStorage.getItem('pagoProcesado') || '{}');
    
    if (!datos.orden) {
        mostrarAlerta('No hay datos de pago para descargar',"warning");
        return;
    }

    const contenido = `
╔════════════════════════════════════════════════════════════╗
║          FERREMAS - COMPROBANTE DE PAGO                    ║
╚════════════════════════════════════════════════════════════╝

Fecha: ${new Date().toLocaleString('es-AR')}

═══════════════════════════════════════════════════════════════

DETALLES DEL PAGO:

  Número de Orden:        ${datos.orden || '-'}
  Monto Pagado:           $${parseInt(datos.monto || 0).toLocaleString('es-CL')}
  Código de Respuesta:    ${datos.codigo_respuesta || '-'}
  Código de Autorización: ${datos.autorizacion || '-'}

═══════════════════════════════════════════════════════════════

¡Gracias por tu compra!

Para más información, visita: www.ferremas.cl
Correo de soporte: soporte@ferremas.cl
    `.trim();

    // Crear blob y descargar
    const blob = new Blob([contenido], { type: 'text/plain;charset=utf-8' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `comprobante-${datos.orden}.txt`;
    document.body.appendChild(link);
    link.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(link);

    console.log("✅ Comprobante descargado");
}

/**
 * Ejecutar cuando el DOM esté listo
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log("🚀 DOM cargado, inicializando confirmación...");
    inicializarPaginaConfirmacion();
});
