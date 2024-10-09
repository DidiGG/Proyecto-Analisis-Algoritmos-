import requests
from bs4 import BeautifulSoup
import csv

# Agregar el User-Agent para simular un navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

# URL de búsqueda en SAGE con el término deseado
QUERY = "computational thinking"
SEARCH_URL = f"https://journals.sagepub.com/action/doSearch?AllField={QUERY}"

# Realizar la solicitud GET a la página de resultados con headers
response = requests.get(SEARCH_URL, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Solicitud exitosa")
else:
    print(f"Error en la solicitud: {response.status_code}")

# Archivo CSV donde se guardarán los resultados
ARCHIVO_CSV = "articulos_sage.csv"

def obtener_metadatos_sage():
    # Realizar la solicitud GET a la página de resultados
    response = requests.get(SEARCH_URL)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Abrir el archivo CSV en modo escritura
        with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv)
            
            # Escribir el encabezado en el archivo CSV
            writer.writerow(['Título', 'Autores', 'Año de publicación', 'DOI', 'Journal'])

            # Extraer los artículos de la página (ajusta el selector CSS según la estructura de SAGE)
            articulos = soup.find_all('div', class_='searchResultItem')
            
            for articulo in articulos:
                titulo = articulo.find('span', class_='hlFld-Title').text if articulo.find('span', class_='hlFld-Title') else 'Sin título'
                autores = articulo.find('span', class_='hlFld-ContribAuthor').text if articulo.find('span', class_='hlFld-ContribAuthor') else 'Autor desconocido'
                ano = articulo.find('span', class_='publication-date').text if articulo.find('span', class_='publication-date') else 'Año desconocido'
                doi = articulo.find('a', class_='SFX').get('href') if articulo.find('a', class_='SFX') else 'Sin DOI'
                journal = articulo.find('span', class_='citation-source').text if articulo.find('span', class_='citation-source') else 'Journal desconocido'
                
                # Escribir la fila en el CSV
                writer.writerow([titulo, autores, ano, doi, journal])
                
        print(f"Datos guardados en {ARCHIVO_CSV}")
    else:
        print(f"Error en la solicitud: {response.status_code}")

# Ejecutar la función para obtener los metadatos de SAGE
obtener_metadatos_sage()
