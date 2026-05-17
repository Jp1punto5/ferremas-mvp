
document.addEventListener(
    'DOMContentLoaded',
    () =>
    {

        const parametros = new URLSearchParams(
            window.location.search
        );
        const categoria =
            parametros.get('categoria');

        document.getElementById(
            'tituloCategoria'
        ).textContent =
            categoria.toUpperCase();



        /* ========================================= */
        /* CARGAR PRODUCTOS */
        /* ========================================= */

        cargarProductosDeCategoria(
            categoria
        );

    }
);



/* ========================================= */
/* CARGAR PRODUCTOS AL CARGAR LA PÁGINA */
/* ========================================= */ 

async function cargarProductosDeCategoria(categoria)
{
    try{
        const respuesta = await fetch(
            `http://127.0.0.1:5000/productos/categoria/${categoria}`
        );
        const productos = await respuesta.json();
        console.log(productos);
        categoriaProductos(productos);
    } catch (error) {
        console.error('Error al cargar productos:', error);
    }
}

actualizarContadorCarrito();

function categoriaProductos(productos)
{
    const grid =
        document.getElementById('gridProductos');

    grid.innerHTML = '';


    productos.forEach(producto =>
    {

                 const precioFormateado = producto.precio_cl.toLocaleString('es-CL');
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
                                <h4>$${precioFormateado} CLP</h4>
                            </p>

                            <p class="precio-usd">
                                <h4>USD $${producto.precio_usd.toFixed(2)}</h4>
                            </p>

                            <p class="stock">
                                <h4>Stock: ${producto.stock}</h4>
                            </p>

                            <button class="btn-agregar">

                                <i class="fa-solid fa-plus"></i>

                                Agregar al carrito

                            </button>

                        </div>
                    `;


                        /* ========================================= */
                        /* AGREGAR AL CARRITO */
                        /* ========================================= */ 
                        tarjeta.querySelector(
                            '.btn-agregar'
                        ).addEventListener(
                            'click',
                            () =>
                            {
                                agregarProducto(producto);
                            }
                        );

                    grid.appendChild(tarjeta);
            




        
    }); 

}

