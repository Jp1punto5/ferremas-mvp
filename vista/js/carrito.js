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