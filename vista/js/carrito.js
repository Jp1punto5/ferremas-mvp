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
    const tituloCompraTotal = document.getElementById("tituloCompraTotal");

    if (carrito.length === 0)
    {

        
        const mostrarAside =
        document.getElementById(
            "resumenCompra"
        );

         mostrarAside.style.display =
        "none";
        tituloCompraTotal.style.display = "none";
        mostrarAlerta("No hay productos en el carrito","error");
        
        return;
    }
    

    tituloCompraTotal.style.display = carrito.length > 0 ? "block" : "none";

    mostrarUsuarioLogeado();
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

    mostrarResumenCompra();
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
                item.cantidad > 0
        );
    }


    guardarCarrito(carrito);

    actualizarContadorCarrito();


    /* RECARGAR VISTA */

    listarProductosCarrito();


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



    mostrarAlerta(
        'Producto eliminado',
        'warning'
    );
}


/* ========================================= */
/* MOSTRAR RESUMEN COMPRA */
/* ========================================= */

function mostrarResumenCompra()
{

    const carrito =
        obtenerCarrito();


    const aside =
        document.getElementById(
            'resumenCompra'
        );
    
    const mostrarAside = document.getElementById("resumenCompra");
     mostrarAside.style.display = carrito.length > 0 ? "block" : "none";
    

    /* ========================================= */
    /* CALCULAR TOTAL */
    /* ========================================= */

    let total = 0;
    /* ========================================= */
    /* VALIDAR USUARIO LOGEADO */
    /* ========================================= */

    const usuarioLogeado =
        JSON.parse(
            sessionStorage.getItem(
                'usuarioLogeado'
            )
        );


 

    carrito.forEach(
        producto =>
        {
            total +=
                producto.precio *
                producto.cantidad;
        }
    );
    /* ========================================= */
    /* APLICAR DESCUENTO */
    /* ========================================= */
        let descuento = 0;
        console.log("total= ",total);
        console.log(typeof total);

        if(usuarioLogeado)
        {
            descuento = Number(total) * 0.10;

            total = Number(total) - descuento;
        }

    const totalFormateado =
        total.toLocaleString(
            'es-CL'
        );


    /* ========================================= */
    /* HTML */
    /* ========================================= */

    aside.innerHTML =
    `
        <h2>
            Total a Pagar
        </h2>


        <div class="valor-total">

            $${totalFormateado}

        </div>
                ${
                    usuarioLogeado
                    ?
                    `
                        <p class="descuento-aplicado">

                            Descuento cliente:
                            -$${descuento.toLocaleString('es-CL')}

                        </p>
                    `
                    :
                    ''
                }

        <div class="botones-pago">

            <button class="btn-webpay">

                <i class="fa-solid fa-credit-card"></i>

                Pagar con tarjeta

            </button>


            <button class="btn-transferencia">

                <i class="fa-solid fa-building-columns"></i>

                Transferencia

            </button>


            ${
                usuarioLogeado
                ?
                `
                    <button class="btn-logout">

                        <i class="fa-solid fa-right-from-bracket"></i>

                        Cerrar sesión

                    </button>
                `
                :
                `
                    <button class="btn-login">

                        <i class="fa-solid fa-user"></i>

                        Iniciar sesión

                    </button>
                `
            }

        </div>
    `;


    /* ========================================= */
    /* BOTON LOGIN */
    /* ========================================= */

    const botonLogin =
        document.querySelector(
            '.btn-login'
        );


    if(botonLogin)
    {
        botonLogin.addEventListener(
            'click',
            () =>
            {
                document.getElementById(
                    'modalLogin'
                ).classList.remove(
                    'oculto'
                );
            }
        );
    }

    /* ========================================= */
    /* BOTON CERRAR SESION */
    /* ========================================= */

    const botonLogout =
        document.querySelector(
            '.btn-logout'
        );


    if(botonLogout)
    {
        botonLogout.addEventListener(
            'click',
            cerrarSesion
        );
    }


}

/* ========================================= */
/* CERRAR SESION */
/* ========================================= */

function cerrarSesion()
{

    sessionStorage.removeItem(
        'usuarioLogeado'
    );


    mostrarAlerta(
        'Sesión cerrada',
        'success'
    );


    /* ========================================= */
    /* RECARGAR COMPONENTES */
    /* ========================================= */

    mostrarResumenCompra();

    mostrarUsuarioLogeado();
}