import requests
import csv

# API Key de IEEE Xplore obtenida del portal
API_KEY_IEEE = "yb8pphsyutvj7jaw8bse43dq"

# Parámetros de búsqueda
QUERY = "computational thinking"  
NUMERO_RESULTADOS_POR_SOLICITUD = 25
ARCHIVO_CSV = "articulos_ieee.csv"
TOTAL_REGISTROS = 1000

def buscar_articulos_ieee(start):
    # Endpoint de la API de IEEE Xplore
    url = "http://ieeexploreapi.ieee.org/api/v1/search/articles"
    
    # Parámetros de búsqueda
    parametros = {
        'apikey': API_KEY_IEEE,
        'querytext': QUERY,
        'max_records': NUMERO_RESULTADOS_POR_SOLICITUD,  # Número de resultados por solicitud
        'start_record': start,  # Posición inicial para paginación
        'format': 'json'  # Formato de respuesta
    }
    
    # Realizar la solicitud GET a la API
    response = requests.get(url, params=parametros)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        datos = response.json()
        resultados = datos.get('articles', [])
        return resultados
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return []

def guardar_resultados(resultados, archivo_csv):
    # Abrir el archivo CSV en modo escritura
    with open(archivo_csv, mode='a', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.writer(archivo_csv)
        
        # Escribir los resultados en el archivo CSV
        for articulo in resultados:
            titulo = articulo.get('title', 'Sin título')
            autores = articulo.get('authors', 'Autor desconocido')
            ano = articulo.get('publication_year', 'Año desconocido')
            doi = articulo.get('doi', 'Sin DOI')
            afiliaciones = articulo.get('affiliations', [])
            journal = articulo.get('publication_title', 'Sin journal')
            publisher = articulo.get('publisher', 'Sin publisher')
            tipo_producto = articulo.get('content_type', 'Sin tipo')
            citas = articulo.get('citation_count', '0')
            
            # Crear una lista de las afiliaciones separadas por comas
            afiliaciones_str = ', '.join([afiliacion.get('name', 'Afiliación desconocida') for afiliacion in afiliaciones])
            
            # Escribir la fila en el CSV
            writer.writerow([titulo, autores, ano, doi, afiliaciones_str, journal, publisher, tipo_producto, citas])

def inicializar_csv(archivo_csv):
    # Inicializar el archivo CSV con el encabezado
    with open(archivo_csv, mode='w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.writer(archivo_csv)
        # Escribir el encabezado en el archivo CSV
        writer.writerow(['Título', 'Autores', 'Año de publicación', 'DOI', 'Afiliaciones', 'Journal', 'Publisher', 'Tipo de producto', 'Citas'])

# Ejecutar la búsqueda en bloques de 25 hasta llegar a 1000 registros
inicializar_csv(ARCHIVO_CSV)
for start in range(1, TOTAL_REGISTROS + 1, NUMERO_RESULTADOS_POR_SOLICITUD):
    resultados = buscar_articulos_ieee(start)
    if resultados:
        guardar_resultados(resultados, ARCHIVO_CSV)
    else:
        print(f"No se encontraron más resultados a partir del registro {start}")
        break

print(f"Datos guardados en {ARCHIVO_CSV}")
