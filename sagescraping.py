from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

# Ruta al GeckoDriver
geckodriver_path = 'C:\\Users\\didie\\Downloads\\selenium\\geckodriver-v0.35.0-win64\\geckodriver.exe'

# Inicializar el driver de Firefox usando el objeto Service
service = Service(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=service)

# URL de búsqueda en SAGE
QUERY = "computational thinking"
SEARCH_URL = f"https://journals.sagepub.com/action/doSearch?AllField={QUERY}"

# Navegar a la URL de SAGE
driver.get(SEARCH_URL)

# Esperar unos segundos para que la página cargue completamente
time.sleep(5)

# Obtener los resultados de la búsqueda
articulos = driver.find_elements(By.CSS_SELECTOR, 'div.searchResultItem')

# Procesar los resultados y mostrarlos
for articulo in articulos:
    titulo = articulo.find_element(By.CSS_SELECTOR, 'span.hlFld-Title').text
    print(f"Título: {titulo}")

# Cerrar el navegador cuando termines
driver.quit()
