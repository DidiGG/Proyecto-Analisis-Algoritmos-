import os

# Directorio donde están los archivos (usando raw string para evitar problemas de escape)
directorio = r'C:\Users\didie\OneDrive\Documents\GitHub\Proyecto-Analisis-Algoritmos-\Bases de datos Algoritmos\ScienceDirect'

# Nombre del archivo de salida
archivo_unificado = 'ScienDirec_unificado.txt'

# Abrir el archivo de salida en modo de escritura
with open(archivo_unificado, 'w', encoding='utf-8') as outfile:  # Forzar codificación a UTF-8
    # Iterar sobre todos los archivos en el directorio
    for filename in os.listdir(directorio):
        if filename.endswith('.txt'):  # Procesar solo archivos .txt
            ruta_archivo = os.path.join(directorio, filename)
            with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as infile:
                # Escribir el contenido del archivo al archivo unificado
                outfile.write(infile.read())
                # Opcional: Añadir un salto de línea entre archivos
                outfile.write("\n")

print(f'Archivos unificados en {archivo_unificado}')
