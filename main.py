# Importar la interfaz gráfica
from interfaz_grafica import main as gui_main

def main_consola():
    """Versión original para consola"""
    from cargar_datos import importar_csv
    from analisis_estadistico import calcular_tendencia_central, generar_dfs, generar_dfsvai
    from graficas import graficar_tendencia, graficar_frecuencia
    from exportar_resultados import exportar_resultados

    # Cargar datos
    ruta = 'datos/datos.csv'
    datos = importar_csv(ruta)

    if datos is not None:
        # Calcular medidas estadísticas
        tendencia = calcular_tendencia_central(datos['Edad'])

        # Generar cuadros estadísticos
        dfs = generar_dfs(datos['Edad'])
        dfsvai = generar_dfsvai(datos['Edad'])

        # Mostrar resultados
        print("\nMedidas de Tendencia Central:")
        print(tendencia)

        print("\nCuadro de Frecuencia Simple:")
        print(dfs)

        print("\nCuadro de Frecuencia Agrupada con Intervalos:")
        print(dfsvai)

        # Graficar
        graficar_tendencia(datos['Edad'])
        graficar_frecuencia(dfs, 'simple')
        graficar_frecuencia(dfsvai, 'agrupada')

        # Exportar resultados a CSV
        exportar_resultados(tendencia, dfs, dfsvai)
        
        print("\n¡Análisis completado! Los resultados se han exportado a la carpeta 'datos'.")
    else:
        print("Error: No se pudo cargar el archivo 'datos/datos.csv'")
        print("Asegúrate de que el archivo existe y está en la carpeta 'datos'.")

def main():
    """Ejecutar interfaz gráfica por defecto"""
    print("Iniciando Analizador Estadístico - Interfaz Gráfica...")
    gui_main()

if __name__ == "__main__":
    main()
