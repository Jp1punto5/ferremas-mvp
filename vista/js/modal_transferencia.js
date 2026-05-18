/* ========================================= */
/* ABRIR MODAL TRANSFERENCIA */
/* ========================================= */

document.addEventListener(
    'DOMContentLoaded',
    () =>
    {
        const modal =
            document.getElementById(
                'modalTransferencia'
            );

        const cerrarModal =
            document.getElementById(
                'cerrarTransferencia'
            );

        /* ========================================= */
        /* CERRAR MODAL */
        /* ========================================= */

        cerrarModal.addEventListener(
            'click',
            () =>
            {
                modal.classList.add(
                    'oculto'
                );
            }
        );


        /* ========================================= */
        /* CERRAR HACIENDO CLICK AFUERA */
        /* ========================================= */

        modal.addEventListener(
            'click',
            (event) =>
            {
                if(event.target === modal)
                {
                    modal.classList.add(
                        'oculto'
                    );
                }
            }
        );


        /* ========================================= */
        /* BOTON TRANSFERENCIA REALIZADA */
        /* ========================================= */

        const btnTransferenciaRealizada =
            document.getElementById(
                'btnTransferenciaRealizada'
            );


        if (btnTransferenciaRealizada)
        {
            btnTransferenciaRealizada.addEventListener(
                'click',
                procesarTransferencia
            );
        }

    }
);


/* ========================================= */
/* PROCESAR TRANSFERENCIA */
/* ========================================= */

function procesarTransferencia()
{
    /* ========================================= */
    /* VALIDAR USUARIO LOGEADO */
    /* ========================================= */

    const usuarioLogeado =
        JSON.parse(
            sessionStorage.getItem(
                'usuarioLogeado'
            )
        );

    if (!usuarioLogeado)
    {
        mostrarAlerta(
            'Debes iniciar sesión para completar la compra',
            'warning'
        );
        return;
    }

    /* ========================================= */
    /* CERRAR MODAL */
    /* ========================================= */

    const modal =
        document.getElementById(
            'modalTransferencia'
        );

    modal.classList.add(
        'oculto'
    );


    /* ========================================= */
    /* LIMPIAR CARRITO */
    /* ========================================= */

    sessionStorage.removeItem('carrito');


    /* ========================================= */
    /* ACTUALIZAR VISTAS */
    /* ========================================= */

    actualizarContadorCarrito();
    listarProductosCarrito();


    /* ========================================= */
    /* MOSTRAR ALERTA DE EXITO */
    /* ========================================= */

    mostrarAlerta(
        'Transferencia registrada. Comprobante enviado al correo.',
        'success'
    );


    /* ========================================= */
    /* PREGUNTAR SI MANTENER SESION */
    /* ========================================= */

    mostrarDialogoSesion();
}


/* ========================================= */
/* MOSTRAR DIALOGO DE SESION */
/* ========================================= */

function mostrarDialogoSesion()
{
    const respuesta = confirm(
        '¿Deseas mantener la sesión abierta?\n\nPresiona "Aceptar" para continuar o "Cancelar" para cerrar sesión.'
    );

    if (!respuesta)
    {
        cerrarSesionUsuario();
    }
}


/* ========================================= */
/* CERRAR SESION DEL USUARIO */
/* ========================================= */

function cerrarSesionUsuario()
{
    sessionStorage.removeItem(
        'usuarioLogeado'
    );

    mostrarAlerta(
        'Sesión cerrada',
        'success'
    );

    mostrarUsuarioLogeado();
    mostrarResumenCompra();
}
