import requests
import csv
import time

# API Key de Scopus obtenida del portal de Elsevier
API_KEY_SCOPUS = "a0a6aa8a0b2b39d9fbca3ab31f59d9b2"

# Parámetros de búsqueda
QUERY = "computational thinking"
NUMERO_RESULTADOS_POR_PAGINA = 25  # Máximo permitido por solicitud en Scopus es 25
TOTAL_RESULTADOS_DESEADOS = 1000  # Ajusta este número si necesitas más o menos
ARCHIVO_CSV = "articulos_scopus_ordenados.csv"

def buscar_articulos_scopus():
    # Endpoint de la API de Scopus
    url = "https://api.elsevier.com/content/search/scopus"
    
    articulos_list = []
    total_descargados = 0
    start = 0
    
    while total_descargados < TOTAL_RESULTADOS_DESEADOS:
        # Parámetros de búsqueda con paginación
        parametros = {
            'query': QUERY,
            'count': NUMERO_RESULTADOS_POR_PAGINA,  # Número de resultados por solicitud
            'start': start,  # Posición inicial para paginación
            'apikey': API_KEY_SCOPUS,  # Tu API Key
            'httpAccept': 'application/json'  # Formato de respuesta
        }
        
        # Realizar la solicitud GET a la API
        response = requests.get(url, params=parametros, timeout=30)
        
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            datos = response.json()
            resultados = datos.get('search-results', {}).get('entry', [])
            
            if not resultados:
                print("No se encontraron más resultados.")
                break
            
            # Iterar sobre los artículos y organizar los datos
            for articulo in resultados:
                # Recolectar información
                titulo = articulo.get('dc:title', 'Sin título')
                autores = articulo.get('dc:creator', 'Autor desconocido').split(",")[0]  # Primer autor
                ano = articulo.get('prism:coverDate', 'Año desconocido')
                tipo = articulo.get('subtypeDescription', 'Tipo desconocido')  # Tipo de producto
                afiliacion = articulo.get('affiliation', [])
                afiliacion_primer_autor = afiliacion[0].get('affilname', 'Afiliación desconocida') if afiliacion else 'Afiliación desconocida'
                journal = articulo.get('prism:publicationName', 'Journal desconocido')
                publisher = articulo.get('dc:publisher', 'Publisher desconocido')
                citaciones = articulo.get('citedby-count', 0)  # Citaciones
                base_datos = 'Scopus'  # Scopus es la base de datos
                
                # Agregar los datos recolectados a la lista
                articulos_list.append({
                    'primer_autor': autores,
                    'ano': ano,
                    'tipo': tipo,
                    'afiliacion_primer_autor': afiliacion_primer_autor,
                    'journal': journal,
                    'publisher': publisher,
                    'base_datos': base_datos,
                    'citaciones': int(citaciones)
                })
                
                total_descargados += 1
                if total_descargados >= TOTAL_RESULTADOS_DESEADOS:
                    break
            
            # Actualizar el parámetro de paginación
            start += NUMERO_RESULTADOS_POR_PAGINA
            
            # Pausa para no sobrecargar la API
            time.sleep(1)
            
        else:
            print(f"Error en la solicitud: {response.status_code}")
            break
    
    # Ordenar la lista por los criterios especificados
    articulos_ordenados = sorted(articulos_list, key=lambda x: (x['primer_autor'], x['ano'], x['tipo'], x['citaciones']), reverse=False)
    
    # Guardar los datos ordenados en el archivo CSV
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.writer(archivo_csv)
        
        # Escribir el encabezado en el archivo CSV
        writer.writerow(['Primer Autor', 'Año', 'Tipo de Producto', 'Afiliación del Primer Autor', 'Journal', 'Publisher', 'Base de Datos', 'Citaciones'])
        
        # Escribir los datos ordenados en el archivo CSV
        for articulo in articulos_ordenados:
            writer.writerow([articulo['primer_autor'], articulo['ano'], articulo['tipo'], articulo['afiliacion_primer_autor'], articulo['journal'], articulo['publisher'], articulo['base_datos'], articulo['citaciones']])
    
    print(f"Datos ordenados guardados en {ARCHIVO_CSV}")

# Ejecutar la búsqueda y guardar los resultados ordenados
buscar_articulos_scopus()


