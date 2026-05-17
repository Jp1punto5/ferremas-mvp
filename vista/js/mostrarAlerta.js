/* ========================================= */
/* MOSTRAR ALERTA */
/* ========================================= */

function mostrarAlerta(
    mensaje,
    tipo = 'success'
)
{

    const contenedor =
        document.getElementById(
            'contenedor-alertas'
        );


    /* ========================================= */
    /* CREAR ALERTA */
    /* ========================================= */

    const alerta =
        document.createElement('div');


    alerta.classList.add(
        'alerta-popup'
    );


    alerta.classList.add(
        `alerta-${tipo}`
    );


    /* ========================================= */
    /* ICONOS */
    /* ========================================= */

    let icono = '';


    if (tipo === 'success')
    {
        icono =
            'fa-circle-check';
    }

    else if (tipo === 'warning')
    {
        icono =
            'fa-triangle-exclamation';
    }

    else if (tipo === 'error')
    {
        icono =
            'fa-circle-xmark';
    }


    /* ========================================= */
    /* HTML ALERTA */
    /* ========================================= */

    alerta.innerHTML =
    `
        <i class="fa-solid ${icono}"></i>

        <span>
            ${mensaje}
        </span>
    `;


    /* ========================================= */
    /* AGREGAR */
    /* ========================================= */

    contenedor.appendChild(
        alerta
    );


    /* ========================================= */
    /* MOSTRAR ANIMACION */
    /* ========================================= */

    setTimeout(
        () =>
        {
            alerta.classList.add(
                'mostrar-alerta'
            );
        },
        50
    );


    /* ========================================= */
    /* OCULTAR */
    /* ========================================= */

    setTimeout(
        () =>
        {
            alerta.classList.remove(
                'mostrar-alerta'
            );


            setTimeout(
                () =>
                {
                    alerta.remove();
                },
                300
            );

        },
        3000
    );
}