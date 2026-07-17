from locust import HttpUser, task, between


# ============================================================
# ESCENARIO L1 — CARGA NORMAL
# Simula usuarios navegando el catalogo de forma tranquila.
# Patron: mezcla de listado, categoria y detalle con tiempo
# de espera realista entre peticiones.
# Comando:
#   python -m locust -f test/locustfile.py --headless -u 50 -r 5
#     --run-time 90s --host http://127.0.0.1:5002
#     --csv test/resultados/run_L1 FerremasCargarUser
# ============================================================

class FerremasCargarUser(HttpUser):
    """
    Carga normal: simula uso tipico del catalogo por usuarios reales.
    Espera entre 1 y 3 segundos entre peticiones (comportamiento humano).
    """
    wait_time = between(1.0, 3.0)

    @task(5)
    def listar_productos(self):
        self.client.get("/productos", name="CARGA - GET /productos")

    @task(3)
    def listar_categoria(self):
        self.client.get(
            "/productos/categoria/Herramientas",
            name="CARGA - GET /productos/categoria/<categoria>",
        )

    @task(2)
    def detalle_producto(self):
        self.client.get("/productos/HER001", name="CARGA - GET /productos/<codigo>")


# ============================================================
# ESCENARIO E1 — ESTRES: CATALOGO
# Simula muchos usuarios concurrentes navegando el catalogo
# con esperas minimas para forzar el limite del servidor.
# Comando:
#   python -m locust -f test/locustfile.py --headless -u 200 -r 20
#     --run-time 90s --host http://127.0.0.1:5002
#     --csv test/resultados/run_E1 FerremasEstres1User
# ============================================================

class FerremasEstres1User(HttpUser):
    """
    Estres 1 (catalogo): alta concurrencia sobre endpoints de listado.
    Espera minima entre peticiones para saturar el servidor.
    """
    wait_time = between(0.1, 0.5)

    @task(7)
    def listar_productos(self):
        self.client.get("/productos", name="ESTRES1 - GET /productos")

    @task(3)
    def listar_categoria(self):
        self.client.get(
            "/productos/categoria/Herramientas",
            name="ESTRES1 - GET /productos/categoria/<categoria>",
        )


# ============================================================
# ESCENARIO E2 — ESTRES: FLUJO CHECKOUT
# Simula el flujo completo de un usuario: ver catalogo, ver
# detalle de producto, luego iniciar y confirmar pago Webpay.
# Combina endpoints de BD + Webpay para maxima presion.
# Comando:
#   python -m locust -f test/locustfile.py --headless -u 350 -r 30
#     --run-time 90s --host http://127.0.0.1:5002
#     --csv test/resultados/run_E2 FerremasEstres2User
# ============================================================

class FerremasEstres2User(HttpUser):
    """
    Estres 2 (checkout): simula flujo completo de compra a maxima presion.
    Combina endpoints de productos + Webpay (init + commit).
    """
    wait_time = between(0.05, 0.3)

    @task(4)
    def listar_productos(self):
        self.client.get("/productos", name="ESTRES2 - GET /productos")

    @task(3)
    def detalle_producto(self):
        self.client.get("/productos/HER001", name="ESTRES2 - GET /productos/<codigo>")

    @task(2)
    def webpay_init(self):
        payload = {
            'buy_order': 'ORD_STRESS',
            'session_id': 'SESS_STRESS',
            'amount': 12000,
            'return_url': 'http://127.0.0.1:5003/pago-confirmado'
        }
        self.client.post("/crear-pago", json=payload, name="ESTRES2 - POST /crear-pago")

    @task(1)
    def dolar(self):
        self.client.get("/dolar", name="ESTRES2 - GET /dolar")


# ============================================================
# CLASE ORIGINAL (compatibilidad — ejecuta los 3 endpoints base)
# ============================================================

class FerremasApiUser(HttpUser):
    """
    Escenario base original: mezcla de los 3 endpoints principales.
    Usar para comparacion con resultados anteriores (u=50 y u=350).
    """
    wait_time = between(0.1, 0.8)

    @task(6)
    def listar_productos(self):
        self.client.get("/productos", name="GET /productos")

    @task(3)
    def listar_herramientas(self):
        self.client.get(
            "/productos/categoria/Herramientas",
            name="GET /productos/categoria/<categoria>",
        )

    @task(1)
    def obtener_producto(self):
        self.client.get("/productos/HER001", name="GET /productos/<codigo>")

