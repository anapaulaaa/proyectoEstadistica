# Proyecto Final de Estadística 

Este repositorio contiene el proyecto final del curso de **Estadística**, en el cual se recopilan y aplican los principales temas estudiados durante el semestre, acompañados de ejemplos prácticos implementados en **Python**.

## Temas incluidos
1. Medidas de tendencia central (media, mediana, moda).
2. Medidas de dispersión (varianza, desviación estándar, rango).
3. Probabilidad básica.
4. Distribuciones de probabilidad (Binomial, Poisson, Normal).
5. Diagramas de probabilidad y **árboles de decisión**.

## Tecnologías y librerías usadas
- **Python 3.x**
- `matplotlib` → para visualización de gráficos.
- `pandas` → manejo de datos tabulares.
- `numpy` → operaciones numéricas.
- (Opcional) `scipy` → funciones estadísticas.

## Empaquetado
Este proyecto se puede convertir en una aplicación distribuible por plataforma con `PyInstaller`.

### Importante
No existe un único instalador que funcione nativamente en Windows y macOS al mismo tiempo. Debes generar uno por sistema operativo:
- En macOS se genera una app `.app` y, si quieres, luego la puedes comprimir en `.dmg`.
- En Windows se genera un `.exe`.

### Construcción
1. Instala dependencias:
	```bash
	pip install -r requirements.txt
	```
2. Genera el paquete en la máquina correspondiente:
	```bash
	python build_installer.py --clean
	```
	O si prefieres un solo archivo por plataforma:
	```bash
	python build_installer.py --clean --onefile
	```

### Windows
En una computadora con Windows, usa `build_windows.bat` desde la raíz del proyecto. Ese script instalará dependencias y generará `dist\StatPro.exe`.

### Archivos de salida
- macOS: `dist/StatPro.app` o `dist/StatPro`
- Windows: `dist/StatPro.exe` o carpeta `dist/StatPro/`

### Nota sobre recursos
El programa ya fue ajustado para localizar correctamente el logo, los CSV de ejemplo y la carpeta de exportación cuando se ejecuta empaquetado.

### Icono de la app
La aplicación ya usa el logo del proyecto como icono embebido:
- macOS: `assets/app.icns`
- Windows: `assets/app.ico`


### Notas
El repositorio puede ampliarse con más ejemplos y datasets.

Este proyecto se elaboró como parte del curso de Estadística, Ingeniería en Sistemas UMG Huehuetenango.

Autor:
Ana Paula Vásquez - 4to Ciclo