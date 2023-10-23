import threading
import csv


def cargar_archivo(dataset):
    with open(dataset, 'r') as archivo:
        # Leer el tamaño del problema (n)
        n = int(archivo.readline().strip())

        # Saltar una línea en blanco
        archivo.readline()

        # Leer el flujo de productos entre unidades
        flujo_productos = []
        for _ in range(n):
            flujo = list(map(int, archivo.readline().strip().split()))
            flujo_productos.append(flujo)

        # Saltar una línea en blanco
        archivo.readline()

        # Leer la matriz de distancias entre localizaciones
        matriz_distancias = []
        for _ in range(n):
            distancias = list(map(int, archivo.readline().strip().split()))
            matriz_distancias.append(distancias)

        # Devolver los datos cargados
        return n, flujo_productos, matriz_distancias

# Imprime el problema por pantalla


def archivo_save_output(filename, output):
    file_write_lock = threading.Lock()
    with file_write_lock:
        try:
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(output)
        except IOError as e:
            print(f"Error al guardar el archivo {filename}: {e}")


def save_log(filename, text):
    try:
        with open(filename, 'a') as file:
            file.write(text + "\n")
        print(f"Appended to the log file: {filename}")
    except IOError as e:
        print(f"Error while saving the file {filename}: {e}")
