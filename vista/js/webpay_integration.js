/* ========================================= */
/* WEBPAY INTEGRATION */
/* ========================================= */

/**
 * Obtener URL de retorno después del pago
 * Funciona tanto con file:// como con http://
 */
function obtenerUrlRetorno() {
    if (window.location.protocol === 'file:') {
        return 'http://127.0.0.1:5003/vista/pago-confirmado.html';
    }
    return `${window.location.origin}/pago-confirmado`;
}

/**
 * Procesa el pago con Webpay
 * - Obtiene el total del carrito
 * - Genera IDs únicos para la orden y sesión
 * - Envía la solicitud a la API
 * - Redirige a Webpay o muestra error
 */
async function procesarPagoWebpay() {
    try {
        // Obtener datos del carrito
        const carrito = obtenerCarrito();
        
        if (carrito.length === 0) {
            mostrarAlerta("El carrito está vacío", "error");
            return;
        }

        // Calcular total
        let total = carrito.reduce((acum, item) => acum + (item.precio * item.cantidad), 0);
        
        // Aplicar descuento si hay usuario logeado
        const usuarioLogeado = JSON.parse(sessionStorage.getItem('usuarioLogeado'));
        if (usuarioLogeado) {
            total = total * 0.9; // 10% de descuento
        }

        // Generar IDs únicos
        const numeroOrden = `ORD-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
        const sessionId = `SESS-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

        // URL de retorno (función mejorada que funciona con file:// y http://)
        const returnUrl = obtenerUrlRetorno();

        console.log("📤 Enviando solicitud a Webpay...");
        console.log({
            buy_order: numeroOrden,
            session_id: sessionId,
            amount: Math.round(total),
            return_url: returnUrl
        });

        // Llamar API de ferremas-api
        const response = await fetch('http://127.0.0.1:5002/crear-pago', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                buy_order: numeroOrden,
                session_id: sessionId,
                amount: Math.round(total),
                return_url: returnUrl
            })
        });

        const data = await response.json();

        if (!response.ok) {
            console.error("❌ Error de API:", data);
            mostrarAlerta(`Error: ${data.error || 'Error desconocido'}`, "error");
            return;
        }

        if (data.token && data.url) {
            console.log("✅ Token recibido:", data.token);
            console.log("🔗 Redirigiendo a Webpay...");

            // Guardar datos de la transacción en sessionStorage para referencias futuras
            sessionStorage.setItem('transaccionWebpay', JSON.stringify({
                numeroOrden,
                sessionId,
                total: Math.round(total),
                token: data.token,
                timestamp: new Date().toISOString()
            }));

            // Redirigir a Webpay
            window.location.href = `${data.url}?token_ws=${data.token}`;
        } else {
            console.error("❌ Respuesta inválida:", data);
            mostrarAlerta("Error al iniciar el pago con Webpay", "error");
        }

    } catch (error) {
        console.error("❌ Error al procesar pago:", error);
        mostrarAlerta(`Error de conexión: ${error.message}`, "error");
    }
}

/**
 * Confirma el pago cuando Webpay redirecciona
 * Se debe llamar en la página de confirmación
 */
async function confirmarPagoWebpay(tokenWs) {
    try {
        console.log("📤 Confirmando pago con token:", tokenWs);

        const formData = new FormData();
        formData.append('token_ws', tokenWs);

        const response = await fetch('http://127.0.0.1:5002/confirmar', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        console.log("📥 Respuesta de confirmación:", data);

        return data;

    } catch (error) {
        console.error("❌ Error al confirmar pago:", error);
        return { success: false, error: error.message };
    }
}
