/* ========================================= */
/* INICIAR */ 
actualizarContadorCarrito();
listarProductosCarrito();       

/* ========================================= */
/* OBTENER CARRITO */
/* ========================================= */

function obtenerCarrito()
{
    return JSON.parse(
        sessionStorage.getItem(
            'carrito'
        )
    ) || [];
}


/* ========================================= */
/* GUARDAR CARRITO */
/* ========================================= */

function guardarCarrito(carrito)
{
    sessionStorage.setItem(
        'carrito',
        JSON.stringify(carrito)
    );
}


/* ========================================= */
/* AGREGAR PRODUCTO */
/* ========================================= */

function agregarProducto(producto)
{
    let carrito =
        obtenerCarrito();


    const productoExistente =
        carrito.find(
            item =>
                item.codigo_producto ===
                producto.codigo_producto
        );


    /* ========================================= */
    /* PRODUCTO YA EXISTE */
    /* ========================================= */

    if (productoExistente)
    {

        /* VALIDAR STOCK */

        if (
            productoExistente.cantidad <
            producto.stock
        )
        {
            productoExistente.cantidad++;
        }
        else
        {
            mostrarAlerta(
                'Stock máximo alcanzado',"warning"
            );

            return;
        }

    }
    else
    {

        /* AGREGAR NUEVO */

        carrito.push({

            codigo_producto:
                producto.codigo_producto,

            nombre:
                producto.nombre,

            precio:
                producto.precio_cl,

            precio_usd:
                producto.precio_usd,

            stock:
                producto.stock,

            url_foto:
                producto.url_foto,

            cantidad: 1
        });

        mostrarAlerta("Producto agregado al carrito","success");
    }


    guardarCarrito(carrito);

    actualizarContadorCarrito();

    console.log(carrito);
}


/* ========================================= */
/* ACTUALIZAR CONTADOR */
/* ========================================= */

function actualizarContadorCarrito()
{
    const carrito =
        obtenerCarrito();


    const total =
        carrito.reduce(
            (acumulador, item) =>
                acumulador + item.cantidad,
            0
        );


    const contador =
        document.getElementById(
            'contador-carrito'
        );


    if (contador)
    {
        contador.textContent = total;
    }
}
 
/* ========================================= */
/* LISTAR PRODUCTOS CARRITO */
/* ========================================= */

function listarProductosCarrito()
{

    const carrito =
        obtenerCarrito();


    const grid =
        document.getElementById(
            'gridProductos'
        );


    grid.innerHTML = '';


    /* ========================================= */
    /* CARRITO VACIO */
    /* ========================================= */

    if (carrito.length === 0)
    {

        mostrarAlerta("No hay productos en el carrito","error");

        return;
    }


    /* ========================================= */
    /* RECORRER PRODUCTOS */
    /* ========================================= */

    carrito.forEach(
        producto =>
        {

            const subtotal =
                producto.precio *
                producto.cantidad;


            const precioFormateado =
                producto.precio.toLocaleString(
                    'es-CL'
                );


            const subtotalFormateado =
                subtotal.toLocaleString(
                    'es-CL'
                );


            const tarjeta =
                document.createElement(
                    'article'
                );


            tarjeta.classList.add(
                'tarjeta-carrito'
            );


            tarjeta.innerHTML =
            `
                <img
                    src="${producto.url_foto}"
                    alt="${producto.nombre}"
                    class="imagen-carrito"
                >


                <div class="info-carrito">

                    <h3>
                        ${producto.nombre}
                    </h3>


                    <p>
                        Cantidad:
                        <strong>
                            x${producto.cantidad}
                        </strong>
                    </p>


                    <p>
                        Precio unitario:
                        <strong>
                            $${precioFormateado}
                        </strong>
                    </p>


                    <p class="subtotal">
                        Subtotal:
                        <strong>
                            $${subtotalFormateado}
                        </strong>
                    </p>


                    <div class="acciones-carrito">

                        <button class="btn-restar">

                            <i class="fa-solid fa-minus"></i>

                        </button>


                        <button class="btn-eliminar">

                            <i class="fa-solid fa-trash"></i>

                        </button>

                    </div>

                </div>
            `;


                    /* ========================================= */
                    /* BOTON RESTAR */
                    /* ========================================= */

                    tarjeta.querySelector(
                        '.btn-restar'
                    ).addEventListener(
                        'click',
                        () =>
                        {
                            descontarProducto(
                                producto.codigo_producto
                            );
                        }
                    );


                    /* ========================================= */
                    /* BOTON ELIMINAR */
                    /* ========================================= */

                    tarjeta.querySelector(
                        '.btn-eliminar'
                    ).addEventListener(
                        'click',
                        () =>
                        {
                            eliminarProducto(
                                producto.codigo_producto
                            );
                        }
                    );


            console.log(tarjeta);
            grid.appendChild(
                tarjeta
            );
        }
    );
}



/* ========================================= */
/* DESCONTAR PRODUCTO */
/* ========================================= */

function descontarProducto(
    codigoProducto
)
{

    let carrito =
        obtenerCarrito();


    const producto =
        carrito.find(
            item =>
                item.codigo_producto ===
                codigoProducto
        );


    if (!producto)
    {
        return;
    }


    producto.cantidad--;


    /* ========================================= */
    /* ELIMINAR SI LLEGA A 0 */
    /* ========================================= */

    if (producto.cantidad <= 0)
    {
        carrito =
            carrito.filter(
                item =>
                    item.codigo_producto !==
                    codigoProducto
            );
    }


    guardarCarrito(carrito);

    actualizarContadorCarrito();


    /* RECARGAR VISTA */

    listarProductosCarrito();

    actualizarTotalCompra();
}


/* ========================================= */
/* ELIMINAR PRODUCTO */
/* ========================================= */

function eliminarProducto(
    codigoProducto
)
{

    let carrito =
        obtenerCarrito();


    carrito =
        carrito.filter(
            item =>
                item.codigo_producto !==
                codigoProducto
        );


    guardarCarrito(carrito);

    actualizarContadorCarrito();


    /* RECARGAR */

    listarProductosCarrito();

    actualizarTotalCompra();


    mostrarAlerta(
        'Producto eliminado',
        'warning'
    );
}