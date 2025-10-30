# 📊 GUÍA DE ARCHIVOS CSV GENERADOS

**Fecha de generación:** 30 de octubre de 2025  
**Aplicación:** StatPro - Analizador Estadístico  
**Universidad:** UMG Huehuetenango

---

## 📁 ARCHIVOS DISPONIBLES

### 1️⃣ **datos_normal_calificaciones.csv**
- **Tipo:** Distribución Normal
- **Descripción:** Calificaciones de estudiantes (0-100)
- **Parámetros:** μ = 75, σ = 12
- **Registros:** 200
- **Columnas:** `Calificacion`
- **Uso recomendado:**
  - Estadística Descriptiva → Todas las medidas
  - Inferencial → Distribución Normal
  - Gráficas: Histogramas, curva normal, regla empírica

---

### 2️⃣ **datos_normal_alturas.csv**
- **Tipo:** Distribución Normal
- **Descripción:** Alturas en centímetros
- **Parámetros:** μ = 165 cm, σ = 10 cm
- **Registros:** 150
- **Columnas:** `Altura_cm`
- **Uso recomendado:**
  - Medidas de Tendencia Central
  - Distribución Normal
  - Análisis de variabilidad

---

### 3️⃣ **datos_poisson_llamadas.csv**
- **Tipo:** Distribución de Poisson
- **Descripción:** Número de llamadas por hora en call center
- **Parámetros:** λ = 5
- **Registros:** 180
- **Columnas:** `Llamadas_Hora`
- **Uso recomendado:**
  - Distribución de Poisson
  - Eventos raros/discretos
  - Probabilidades de conteo

---

### 4️⃣ **datos_poisson_defectos.csv**
- **Tipo:** Distribución de Poisson
- **Descripción:** Defectos encontrados en control de calidad
- **Parámetros:** λ = 3
- **Registros:** 200
- **Columnas:** `Defectos`
- **Uso recomendado:**
  - Distribución de Poisson
  - Control estadístico de calidad
  - Análisis de frecuencias

---

### 5️⃣ **datos_regresion_estudio.csv**
- **Tipo:** Regresión Lineal Simple
- **Descripción:** Relación entre horas de estudio y calificación
- **Correlación:** r ≈ 0.91 (correlación muy fuerte)
- **Registros:** 100
- **Columnas:** `Horas_Estudio`, `Calificacion`
- **Uso recomendado:**
  - Regresión y Correlación
  - Análisis bivariado
  - Predicción lineal
  - Gráfica de dispersión

---

### 6️⃣ **datos_binomial_encuesta.csv**
- **Tipo:** Distribución Binomial
- **Descripción:** Respuestas correctas en encuesta de 20 preguntas
- **Parámetros:** n = 20, p = 0.65
- **Registros:** 150
- **Columnas:** `Respuestas_Correctas`
- **Uso recomendado:**
  - Distribución Binomial
  - Probabilidades de éxito/fracaso
  - Análisis de ensayos repetidos

---

### 7️⃣ **datos_completo_estudiantes.csv**
- **Tipo:** Dataset multivariable completo
- **Descripción:** Información completa de estudiantes
- **Registros:** 200
- **Columnas:**
  - `ID` → Identificador único
  - `Edad` → Edad del estudiante (18-35)
  - `Calificacion` → Calificación final (0-100)
  - `Horas_Estudio_Semanal` → Horas dedicadas por semana
  - `Faltas` → Número de faltas (Poisson)
  - `Genero` → M/F
  - `Carrera` → Ingeniería, Medicina, Derecho, Administración
- **Uso recomendado:**
  - Análisis multivariable completo
  - Tablas de frecuencia agrupadas
  - Chi-cuadrado (Género vs Carrera)
  - Regresión múltiple
  - Todos los análisis descriptivos

---

### 8️⃣ **datos_categoricos_satisfaccion.csv**
- **Tipo:** Datos categóricos para Chi-cuadrado
- **Descripción:** Satisfacción del cliente por grupo de edad
- **Registros:** 180
- **Columnas:**
  - `Edad_Grupo` → 18-25, 26-35, 36-45, 46+
  - `Satisfaccion` → Muy Insatisfecho, Insatisfecho, Neutral, Satisfecho, Muy Satisfecho
- **Uso recomendado:**
  - Prueba Chi-cuadrado de independencia
  - Tablas de contingencia 4×5
  - Análisis de asociación categórica

---

## 🎯 CÓMO USAR EN LA APLICACIÓN

### **Método 1: Cargar desde la aplicación**
1. Abre StatPro
2. En cualquier ventana de análisis, click en **"Cargar CSV"**
3. Selecciona el archivo que necesites
4. ¡Listo! Los datos se cargarán automáticamente

### **Método 2: Usar con distribuciones**
1. Estadística Inferencial → **Distribuciones**
2. Para verificar ajuste:
   - Carga `datos_normal_calificaciones.csv`
   - Calcula μ y σ de los datos
   - Compara con distribución teórica

---

## 📊 EJEMPLOS DE ANÁLISIS

### **Ejemplo 1: Distribución Normal**
```
Archivo: datos_normal_calificaciones.csv
Análisis:
1. Medidas de Tendencia Central
2. Medidas de Dispersión
3. Distribución Normal → Ingresa μ=75, σ=12
4. Ver Gráficas → Compara curva teórica vs datos reales
```

### **Ejemplo 2: Regresión**
```
Archivo: datos_regresion_estudio.csv
Análisis:
1. Correlación y Regresión
2. Variable X: Horas_Estudio
3. Variable Y: Calificacion
4. Resultado esperado: r ≈ 0.91, pendiente ≈ 4.5
```

### **Ejemplo 3: Chi-cuadrado**
```
Archivo: datos_categoricos_satisfaccion.csv
Análisis:
1. Chi-cuadrado → Prueba de Independencia
2. Variable 1: Edad_Grupo
3. Variable 2: Satisfaccion
4. Pregunta: ¿La satisfacción depende del grupo de edad?
```

---

## 🔍 VERIFICACIÓN DE DATOS

Para verificar que los datos se cargaron correctamente:

1. **Abrir en Excel/Calc:**
   - Doble click en el archivo
   - Verificar que tenga encabezados
   - Sin valores vacíos

2. **En la aplicación:**
   - Después de cargar, revisa el área de texto
   - Debe mostrar estadísticas básicas
   - Verifica número de registros

---

## 💡 TIPS

✅ **Antes de analizar:**
- Lee la descripción del archivo
- Conoce los parámetros teóricos
- Planifica qué análisis harás

✅ **Durante el análisis:**
- Compara resultados con parámetros originales
- Usa las gráficas para visualizar
- Exporta resultados importantes

✅ **Para presentaciones:**
- Usa `datos_completo_estudiantes.csv` para demos completas
- Los datos son realistas y educativos
- Fáciles de explicar en clase

---

## 🆘 SOLUCIÓN DE PROBLEMAS

**Problema:** El archivo no se carga  
**Solución:** Verifica que esté en formato CSV con comas

**Problema:** Los valores no se ven bien  
**Solución:** Asegúrate que el separador decimal sea punto (.)

**Problema:** Quiero más datos  
**Solución:** Usa el botón "Generar Datos Aleatorios" en la app

---

## 📈 ESTADÍSTICAS DE LOS ARCHIVOS

| Archivo | Tipo | Registros | Variables | Tamaño |
|---------|------|-----------|-----------|--------|
| normal_calificaciones | Continuo | 200 | 1 | 1.2 KB |
| normal_alturas | Continuo | 150 | 1 | 1.0 KB |
| poisson_llamadas | Discreto | 180 | 1 | 382 B |
| poisson_defectos | Discreto | 200 | 1 | 409 B |
| regresion_estudio | Bivariado | 100 | 2 | 1.1 KB |
| binomial_encuesta | Discreto | 150 | 1 | 462 B |
| completo_estudiantes | Multivariable | 200 | 7 | 6.3 KB |
| categoricos_satisfaccion | Categórico | 180 | 2 | 3.1 KB |

---

## 🎓 INFORMACIÓN ADICIONAL

**Creado por:** GitHub Copilot  
**Para:** Ana Paula Vásquez  
**Curso:** Estadística - UMG Huehuetenango  
**Proyecto:** StatPro - Analizador Estadístico

**¡Éxito en tus análisis estadísticos!** 📊✨
