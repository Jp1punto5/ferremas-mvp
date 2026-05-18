/* ========================================= */
/* MODAL REGISTRO */
/* ========================================= */

document.addEventListener(
    'DOMContentLoaded',
    () =>
    {
        const modalRegistro =
            document.getElementById(
                'modalRegistro'
            );

        const cerrarRegistro =
            document.getElementById(
                'cerrarRegistro'
            );

        const modalLogin =
            document.getElementById(
                'modalLogin'
            );

        /* ========================================= */
        /* CERRAR MODAL REGISTRO */
        /* ========================================= */

        cerrarRegistro.addEventListener(
            'click',
            () =>
            {
                modalRegistro.classList.add(
                    'oculto'
                );
                limpiarModalRegistro();
            }
        );


        /* ========================================= */
        /* CERRAR HACIENDO CLICK AFUERA */
        /* ========================================= */

        modalRegistro.addEventListener(
            'click',
            (event) =>
            {
                if(event.target === modalRegistro)
                {
                    modalRegistro.classList.add(
                        'oculto'
                    );
                    limpiarModalRegistro();
                }
            }
        );


        /* ========================================= */
        /* BOTON CREAR CUENTA */
        /* ========================================= */

        const btnCrearCuenta =
        document.getElementById(
            'btnCrearCuenta'
        );

        btnCrearCuenta.addEventListener(
            'click',
            crearCuenta
        );


        /* ========================================= */
        /* BOTON VOLVER AL LOGIN */
        /* ========================================= */

        const btnVolverLogin =
        document.getElementById(
            'btnVolverLogin'
        );

        btnVolverLogin.addEventListener(
            'click',
            () =>
            {
                modalRegistro.classList.add('oculto');
                modalLogin.classList.remove('oculto');
            }
        );

    }
);


/* ========================================= */
/* LIMPIAR INPUTS MODAL REGISTRO */
/* ========================================= */

function limpiarModalRegistro()
{
    const inputs =
        document.querySelectorAll(
            '#modalRegistro input'
        );

    inputs.forEach(
        input =>
        {
            input.value = '';
        }
    );
}


/* ========================================= */
/* CREAR CUENTA */
/* ========================================= */

async function crearCuenta()
{
    const nombre =
        document.getElementById(
            'nombreRegistro'
        ).value;

    const correo =
        document.getElementById(
            'correoRegistro'
        ).value;

    const telefono =
        document.getElementById(
            'telefonoRegistro'
        ).value;

    const password =
        document.getElementById(
            'passwordRegistro'
        ).value;

    /* ========================================= */
    /* VALIDAR CAMPOS */
    /* ========================================= */

    if(
        nombre.trim() === '' ||
        correo.trim() === '' ||
        telefono.trim() === '' ||
        password.trim() === ''
    )
    {
        mostrarAlerta(
            'Completa todos los campos',
            'warning'
        );
        return;
    }

    /* ========================================= */
    /* VALIDAR EMAIL */
    /* ========================================= */

    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexEmail.test(correo))
    {
        mostrarAlerta(
            'Ingresa un correo válido',
            'warning'
        );
        return;
    }

    /* ========================================= */
    /* VALIDAR TELEFONO */
    /* ========================================= */

    if (telefono.length < 8)
    {
        mostrarAlerta(
            'El teléfono debe tener al menos 8 dígitos',
            'warning'
        );
        return;
    }

    try
    {
        const respuesta =
            await fetch(
                'http://127.0.0.1:5000/registro',
                {
                    method: 'POST',

                    headers:
                    {
                        'Content-Type':
                            'application/json'
                    },

                    body: JSON.stringify({
                        nombre_completo: nombre,
                        correo: correo,
                        telefono: telefono,
                        password: password
                    })
                }
            );

        const data =
            await respuesta.json();

        if(data.success)
        {
            mostrarAlerta(
                data.mensaje,
                'success'
            );

            /* ========================================= */
            /* CERRAR MODAL Y LIMPIAR */
            /* ========================================= */

            document.getElementById(
                'modalRegistro'
            ).classList.add(
                'oculto'
            );

            limpiarModalRegistro();

            /* Abre automáticamente el login */
            document.getElementById(
                'modalLogin'
            ).classList.remove(
                'oculto'
            );
        }
        else
        {
            mostrarAlerta(
                data.error || data.mensaje || 'Error al crear cuenta',
                'error'
            );
        }

    }
    catch(error)
    {
        console.error(error);

        mostrarAlerta(
            'Error al crear cuenta',
            'error'
        );
    }
}
