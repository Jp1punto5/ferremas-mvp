import threading
import requests
import time

URL = "http://127.0.0.1:5003/productos"

def prueba():
    requests.get(URL)

inicio = time.time()

hilos = []

for i in range(100):

    hilo = threading.Thread(target=prueba)

    hilo.start()

    hilos.append(hilo)

for hilo in hilos:
    hilo.join()

fin = time.time()

print(f"Tiempo total: {fin-inicio:.2f} segundos")