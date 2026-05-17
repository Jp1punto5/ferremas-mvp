/* ========================================= */
/* CAPTURAR BOTONES CATEGORIA */
/* ========================================= */

document.addEventListener(
    'DOMContentLoaded',
    () =>
    {
        const botonesCategoria =
            document.querySelectorAll(
                '.categoria-btn'
            );


        botonesCategoria.forEach(
            boton =>
            {
                boton.addEventListener(
                    'click',
                    () =>
                    {
                        const categoria =
                            boton.dataset.categoria;


                        console.log(
                            'Categoría seleccionada:',
                            categoria
                        );


                        /* ========================================= */
                        /* REDIRECCIONAR */
                        /* ========================================= */

                        window.location.href =
                            `categoria_p.html?categoria=${categoria}`;
                    }
                );
            }
        );
    }
);


/* ========================================= */
/* OBTENER PRODUCTOS DESDE API */
/* ========================================= */

async function cargarProductos()
{
    try
    {
        const respuesta = await fetch(
            'http://127.0.0.1:5000/productos'
        );

        const productos = await respuesta.json();

        console.log(productos);

        mostrarProductos(productos);
    }
    catch(error)
    {
        console.error(
            'Error al cargar productos:',
            error
        );
    }
}


/* ========================================= */
/* MOSTRAR PRODUCTOS EN HTML */
/* ========================================= */

function mostrarProductos(productos)
{
    const grid =
        document.getElementById('gridProductos');

    grid.innerHTML = '';


    productos.forEach(producto =>
    {

        if(producto.stock <= 10)
            {
                 const tarjeta = document.createElement(
                        'article'
                    );

                    tarjeta.classList.add(
                        'tarjeta-producto'
                    );


                    tarjeta.innerHTML =
                    `
                        <img
                            src="${producto.url_foto}"
                            alt="${producto.nombre}"
                            class="imagen-producto"
                        >

                        <div class="info-producto">

                            <h3>
                                ${producto.nombre}
                            </h3>

                            <p class="precio-clp">
                                $${producto.precio} CLP
                            </p>

                            <p class="precio-usd">
                                USD $0
                            </p>

                            <button class="btn-agregar">

                                <i class="fa-solid fa-plus"></i>

                                Agregar al carrito

                            </button>

                        </div>
                    `;

                    grid.appendChild(tarjeta);
            }




        
    });
}


/* ========================================= */
/* INICIAR */
/* ========================================= */

cargarProductos();