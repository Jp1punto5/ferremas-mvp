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
        'Compra Finalizada - Enviar comprobante de Transferencia.',
        'success'
    );


    /* ========================================= */
    /* VALIDAR USUARIO LOGEADO */
    /* ========================================= */

    const usuarioLogeado =
        JSON.parse(
            sessionStorage.getItem(
                'usuarioLogeado'
            )
        );

    /* ========================================= */
    /* PREGUNTAR SI MANTENER SESION (SOLO SI EXISTE USUARIO) */
    /* ========================================= */

    if (usuarioLogeado)
    {
        mostrarDialogoSesion();
    }
}


/* ========================================= */
/* MOSTRAR DIALOGO DE SESION */
/* ========================================= */

function mostrarDialogoSesion()
{
    const dialogo =
        document.getElementById(
            'dialogoConfirmacion'
        );

    const btnMantener =
        document.getElementById(
            'btnMantenerSesion'
        );

    const btnCerrar =
        document.getElementById(
            'btnCerrarSesion'
        );

    if (dialogo)
    {
        dialogo.classList.remove(
            'oculto'
        );
    }

    if (btnMantener)
    {
        btnMantener.addEventListener(
            'click',
            cerrarDialogo,
            { once: true }
        );
    }

    if (btnCerrar)
    {
        btnCerrar.addEventListener(
            'click',
            () =>
            {
                cerrarDialogo();
                cerrarSesionUsuario();
            },
            { once: true }
        );
    }
}


/* ========================================= */
/* CERRAR DIALOGO */
/* ========================================= */

function cerrarDialogo()
{
    const dialogo =
        document.getElementById(
            'dialogoConfirmacion'
        );

    if (dialogo)
    {
        dialogo.classList.add(
            'oculto'
        );
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
