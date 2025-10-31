# 🎯 GUÍA RÁPIDA: ¿QUÉ ARCHIVO CSV USAR EN CADA VENTANA?

## 📊 ESTADÍSTICA DESCRIPTIVA

### ✅ **Análisis Completo** (Cuadros + Tendencia)
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Por qué:** Archivo más completo con 200 registros
- **Qué verás:** Todas las medidas de tendencia central + cuadros de frecuencia

**Alternativa:** Cualquier CSV que tenga columna `Edad`

---

### ✅ **Cuadros de Frecuencia**
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Qué verás:** Frecuencia simple y agrupada (por intervalos)

---

### ✅ **Tendencia Central** (Media, Mediana, Moda)
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Qué verás:** Media, mediana, moda, media geométrica, media armónica

**Alternativas:**
- `datos_normal_calificaciones.csv` (columna: `Calificacion`)
- `datos_normal_alturas.csv` (columna: `Altura_cm`)

---

### ✅ **Medidas de Posición** (Cuartiles, Deciles, Percentiles)
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Qué verás:** Q1, Q2, Q3, D1-D9, P1-P99

---

### ✅ **Medidas de Dispersión** (Rango, Varianza, Desv. Estándar)
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Qué verás:** Rango, varianza, desv. estándar, coef. variación

---

### ✅ **Medidas de Forma** (Asimetría, Curtosis)
**Archivo recomendado:** `datos_completo_estudiantes.csv`
- **Columna requerida:** `Edad`
- ✅ Tiene la columna `Edad` ✓
- **Qué verás:** Coeficiente de asimetría, curtosis, tipo de distribución

---

## 📈 ESTADÍSTICA INFERENCIAL

### ✅ **Probabilidades Elementales**
**Archivo:** No requiere CSV
- **Cómo usar:** Define tu propio espacio muestral y eventos
- **Ejemplo:** Espacio muestral: 1,2,3,4,5,6 (dado)
- **Qué harás:** Calcular uniones, intersecciones, complementos

---

### ✅ **Teorema de Bayes**
**Archivo:** No requiere CSV
- **Cómo usar:** Ingresa manualmente P(A), P(B|A), P(B|¬A)
- **Ejemplo:** Test médico, probabilidad de enfermedad
- **Qué harás:** Calcular probabilidad condicional P(A|B)

---

### ✅ **Distribuciones de Probabilidad**

#### 📊 **Distribución Binomial**
**Archivo de referencia:** `datos_binomial_encuesta.csv`
- **Columna:** `Respuestas_Correctas`
- **Parámetros sugeridos:** n=20, p=0.65
- **Uso:** Ingresa n, p, k manualmente (no carga CSV en esta ventana)

#### 📊 **Distribución Normal**
**Archivos de referencia:**
- `datos_normal_calificaciones.csv` → μ=75, σ=12
- `datos_normal_alturas.csv` → μ=165, σ=10
- **Uso:** Ingresa μ, σ, x manualmente

#### 📊 **Distribución de Poisson**
**Archivos de referencia:**
- `datos_poisson_llamadas.csv` → λ=5
- `datos_poisson_defectos.csv` → λ=3
- **Uso:** Ingresa λ, k manualmente

---

### ✅ **Regresión y Correlación**
**Archivo recomendado:** `datos_regresion_estudio.csv`
- **Columnas requeridas:** `Horas_Estudio`, `Calificacion`
- ✅ Tiene ambas columnas ✓
- **Qué verás:**
  - Coeficiente de correlación (r ≈ 0.91)
  - Ecuación de regresión
  - 4 modelos: Lineal, Exponencial, Logarítmico, Potencial
  - Gráficas de dispersión con líneas de ajuste

**Alternativa:** `datos_completo_estudiantes.csv`
- Puedes usar: `Horas_Estudio_Semanal` vs `Calificacion`

---

### ✅ **Diagramas de Árbol**
**Archivo:** No requiere CSV
- **Cómo usar:** Ingresa número de niveles y probabilidades
- **Ejemplo:** 3 niveles → probabilidades: 0.6, 0.7, 0.5
- **Qué harás:** Ver árbol interactivo, editar probabilidades con click

---

### ✅ **Chi-Cuadrado (χ²)**
**Archivo recomendado:** `datos_categoricos_satisfaccion.csv`
- **Columnas:** `Edad_Grupo`, `Satisfaccion`
- ✅ Perfecto para tabla de contingencia ✓
- **Qué verás:** 
  - Prueba de independencia
  - ¿La satisfacción depende del grupo de edad?
  - Estadístico χ², p-valor, conclusión

**Alternativa:** `datos_completo_estudiantes.csv`
- Puedes usar: `Genero` vs `Carrera`

---

## 🎯 RESUMEN RÁPIDO

| Ventana | Archivo Principal | Columna(s) Requerida(s) |
|---------|------------------|------------------------|
| **Análisis Completo** | `datos_completo_estudiantes.csv` | `Edad` |
| **Cuadros Frecuencia** | `datos_completo_estudiantes.csv` | `Edad` |
| **Tendencia Central** | `datos_completo_estudiantes.csv` | `Edad` |
| **Posición** | `datos_completo_estudiantes.csv` | `Edad` |
| **Dispersión** | `datos_completo_estudiantes.csv` | `Edad` |
| **Forma** | `datos_completo_estudiantes.csv` | `Edad` |
| **Probabilidades** | No requiere CSV | - |
| **Bayes** | No requiere CSV | - |
| **Distribuciones** | No requiere CSV (solo referencia) | - |
| **Regresión** | `datos_regresion_estudio.csv` | `Horas_Estudio`, `Calificacion` |
| **Árboles** | No requiere CSV | - |
| **Chi-Cuadrado** | `datos_categoricos_satisfaccion.csv` | `Edad_Grupo`, `Satisfaccion` |

---

## 💡 TIPS IMPORTANTES

### ✅ Para Estadística Descriptiva:
- **Archivo estrella:** `datos_completo_estudiantes.csv`
- Tiene la columna `Edad` que necesitan TODAS las ventanas descriptivas
- 200 registros = resultados más precisos

### ✅ Para Regresión:
- **Archivo específico:** `datos_regresion_estudio.csv`
- Correlación muy fuerte (r ≈ 0.91)
- Ideal para demostrar regresión lineal

### ✅ Para Chi-Cuadrado:
- **Archivo específico:** `datos_categoricos_satisfaccion.csv`
- Variables categóricas perfectas para independencia
- 180 registros distribuidos en tabla 4×5

### ✅ Para Distribuciones:
- NO se cargan archivos CSV directamente
- Los archivos son solo REFERENCIA para obtener parámetros
- Ejemplo: Abre `datos_normal_calificaciones.csv` en Excel → calcula μ y σ → úsalos en la ventana

---

## ⚠️ ERRORES COMUNES

### ❌ "La columna 'Edad' no existe"
**Solución:** Asegúrate de usar un archivo que tenga columna `Edad`
- ✅ `datos_completo_estudiantes.csv` → SÍ tiene `Edad`
- ❌ `datos_regresion_estudio.csv` → NO tiene `Edad`

### ❌ "Selecciona dos columnas para regresión"
**Solución:** 
- Usa `datos_regresion_estudio.csv`
- O usa `datos_completo_estudiantes.csv` y selecciona 2 columnas numéricas

### ❌ "No hay suficientes datos"
**Solución:** 
- Verifica que el CSV tenga al menos 10-20 registros
- Todos los archivos generados tienen 100+ registros ✓

---

## 🚀 FLUJO DE TRABAJO RECOMENDADO

### Para una presentación completa:

1️⃣ **Cargar datos generales:**
   - Abre "Análisis Completo"
   - Carga `datos_completo_estudiantes.csv`
   - Explora todas las medidas

2️⃣ **Regresión:**
   - Abre "Regresión y Correlación"
   - Carga `datos_regresion_estudio.csv`
   - Muestra las 4 gráficas de modelos

3️⃣ **Chi-Cuadrado:**
   - Abre "Chi-Cuadrado"
   - Carga `datos_categoricos_satisfaccion.csv`
   - Prueba de independencia

4️⃣ **Distribuciones:**
   - Abre "Distribuciones"
   - Pestaña Normal → μ=75, σ=12
   - Compara con datos reales de calificaciones

---

## 📞 ¿NECESITAS AYUDA?

Si algo no funciona:
1. Verifica que el archivo esté en la carpeta `datos/`
2. Asegúrate que tenga las columnas correctas
3. Revisa que sea formato CSV (comas, no punto y coma)
4. Lee el mensaje de error (te dice qué columnas tiene el archivo)

---

**¡Éxito en tu análisis estadístico!** 📊✨

*Creado para: Ana Paula Vásquez*  
*Proyecto: StatPro - UMG Huehuetenango*
