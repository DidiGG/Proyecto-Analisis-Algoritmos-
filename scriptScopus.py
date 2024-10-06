import requests
import csv

# API Key de Scopus obtenida del portal de Elsevier
API_KEY_SCOPUS = "a0a6aa8a0b2b39d9fbca3ab31f59d9b2"

# Parámetros de búsqueda
QUERY = "computational thinking"  
NUMERO_RESULTADOS = 10
START = 0

# Nombre del archivo CSV donde se guardarán los resultados
ARCHIVO_CSV = "articulos_scopus.csv"

def buscar_articulos_scopus():
    # Endpoint de la API de Scopus
    url = "https://api.elsevier.com/content/search/scopus"
    
    # Parámetros de búsqueda
    parametros = {
        'query': QUERY,
        'count': NUMERO_RESULTADOS,  # Número de resultados por solicitud
        'start': START,  # Posición inicial para paginación
        'apikey': API_KEY_SCOPUS,  # Tu API Key
        'httpAccept': 'application/json'  # Formato de respuesta
    }
    
    # Realizar la solicitud GET a la API
    response = requests.get(url, params=parametros)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        datos = response.json()
        resultados = datos.get('search-results', {}).get('entry', [])
        
        # Abrir el archivo CSV en modo escritura
        with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            
            # Escribir el encabezado en el archivo CSV
            writer.writerow(['Título', 'Autores', 'Año de publicación', 'DOI', 'Afiliaciones'])
            
            # Iterar sobre los artículos y escribir los datos en el archivo CSV
            for articulo in resultados:
                titulo = articulo.get('dc:title', 'Sin título')
                autores = articulo.get('dc:creator', 'Autor desconocido')
                ano = articulo.get('prism:coverDate', 'Año desconocido')
                doi = articulo.get('prism:doi', 'Sin DOI')
                afiliaciones = articulo.get('affiliation', [])
                
                # Crear una lista de las afiliaciones separadas por comas
                lista_afiliaciones = [afiliacion.get('affilname', 'Afiliación desconocida') for afiliacion in afiliaciones]
                afiliaciones_str = ', '.join(lista_afiliaciones)
                
                # Escribir la fila en el CSV
                writer.writerow([titulo, autores, ano, doi, afiliaciones_str])
                
        print(f"Datos guardados en {ARCHIVO_CSV}")
    else:
        print(f"Error en la solicitud: {response.status_code}")

# Ejecutar la búsqueda de forma automática y guardar los resultados en CSV
buscar_articulos_scopus()
