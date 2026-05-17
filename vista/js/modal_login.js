/* ========================================= */
/* ABRIR MODAL LOGIN */
/* ========================================= */

document.addEventListener(
    'DOMContentLoaded',
    () =>
    {
        const modal =
            document.getElementById(
                'modalLogin'
            );


        const cerrarModal =
            document.querySelector(
                '.cerrar-modal'
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
                limpiarModalLogin();
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

                    limpiarModalLogin();

                }
            }
        );


        const btnIngresar =
        document.getElementById(
            'btnIngresar'
        );


        btnIngresar.addEventListener(
            'click',
            
            iniciarSesion
        );

    }
);


/* ========================================= */
/* LIMPIAR INPUTS MODAL LOGIN */
/* ========================================= */

function limpiarModalLogin()
{

    const inputs =
        document.querySelectorAll(
            '#modalLogin input'
        );


    inputs.forEach(
        input =>
        {
            input.value = '';
        }
    );
}



/* ========================================= */
/* LOGIN USUARIO */
/* ========================================= */

async function iniciarSesion()
{

    const correo =
        document.getElementById(
            'correoLogin'
        ).value;


    const clave =
        document.getElementById(
            'claveLogin'
        ).value;

console.log("correo: " +correo + " clave: " + clave);
    /* ========================================= */
    /* VALIDAR CAMPOS */
    /* ========================================= */

    if(
        correo.trim() === '' ||
        clave.trim() === ''
    )
    {

        mostrarAlerta(
            'Completa todos los campos',
            'warning'
        );

        return;
    }


    try
    {

        const respuesta =
            await fetch(
                'http://127.0.0.1:5000/login',
                {

                    method: 'POST',

                    headers:
                    {
                        'Content-Type':
                            'application/json'
                    },

                    body: JSON.stringify({

                        correo:
                            correo,

                        clave:
                            clave
                    })
                }
            );


        const data =
            await respuesta.json();


        if(data.success)
        {   
            sessionStorage.setItem(
            'usuarioLogeado',
            JSON.stringify(data)
          );
            mostrarUsuarioLogeado();
            mostrarAlerta(
                'Inicio de sesión exitoso',
                'success'
            );


            console.log(data);


            /* ========================================= */
            /* CERRAR MODAL */
            /* ========================================= */

            document.getElementById(
                'modalLogin'
            ).classList.add(
                'oculto'
            );


            limpiarModalLogin();
        }
        else
        {

            mostrarAlerta(
                data.mensaje,
                'error'
            );
        }

    }
    catch(error)
    {

        console.error(error);

        mostrarAlerta(
            'Error al iniciar sesión',
            'error'
        );
    }
}


/* ========================================= */
/* MOSTRAR USUARIO LOGEADO */
/* ========================================= */

function mostrarUsuarioLogeado()
{

    const usuario =
        JSON.parse(
            sessionStorage.getItem(
                'usuarioLogeado'
            )
        );


    if(!usuario)
    {
        return;
    }


    const titulo =
        document.getElementById(
            'titulo_carrito'
        );


    titulo.textContent =
        `Bienvenido: ${usuario.usuario}`;
}