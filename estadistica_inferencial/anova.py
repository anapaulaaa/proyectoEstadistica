"""Herramientas de calculo para ANOVA de 1 y 2 factores."""

from __future__ import annotations

from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy import stats


def _as_float_array(valores: Iterable[float]) -> np.ndarray:
    datos = np.asarray(list(valores), dtype=float)
    if datos.size == 0:
        raise ValueError("Cada grupo debe contener al menos un dato.")
    return datos


def _varianza_muestral(valores: np.ndarray) -> float:
    if valores.size <= 1:
        return 0.0
    return float(np.var(valores, ddof=1))


def _f_critico(alpha: float, gl_numerador: int, gl_denominador: int) -> float:
    if gl_numerador <= 0 or gl_denominador <= 0:
        return float("nan")
    return float(stats.f.ppf(1 - alpha, gl_numerador, gl_denominador))


def _p_valor_f(f_calculada: float, gl_numerador: int, gl_denominador: int) -> float:
    if not np.isfinite(f_calculada):
        return 0.0
    if gl_numerador <= 0 or gl_denominador <= 0:
        return float("nan")
    return float(stats.f.sf(f_calculada, gl_numerador, gl_denominador))


def _interpretar_decision(f_calculada: float, f_critica: float, p_valor: float, alpha: float) -> str:
    if np.isnan(f_calculada) or np.isnan(f_critica):
        return "No fue posible evaluar la prueba con los datos suministrados."

    if np.isfinite(f_calculada) and (
        f_calculada > f_critica or (not np.isnan(p_valor) and p_valor < alpha)
    ):
        return "Se rechaza H0 porque F calculada es mayor que F critica."

    return "No se rechaza H0 porque no se observa evidencia suficiente de diferencias significativas."


def anova_un_factor(grupos: Sequence[Sequence[float]], nombres_grupos: Sequence[str] | None = None, alpha: float = 0.05) -> dict:
    """Calcula una prueba ANOVA de un factor con grupos independientes."""

    datos = [_as_float_array(grupo) for grupo in grupos]
    if len(datos) < 2:
        raise ValueError("Se requieren al menos dos grupos para ANOVA de un factor.")

    nombres = list(nombres_grupos) if nombres_grupos else [f"Grupo {i + 1}" for i in range(len(datos))]
    if len(nombres) != len(datos):
        raise ValueError("La cantidad de nombres debe coincidir con la cantidad de grupos.")

    conteos = np.array([grupo.size for grupo in datos], dtype=int)
    sumas = np.array([float(grupo.sum()) for grupo in datos], dtype=float)
    medias = np.array([float(grupo.mean()) for grupo in datos], dtype=float)
    varianzas = np.array([_varianza_muestral(grupo) for grupo in datos], dtype=float)

    total_datos = np.concatenate(datos)
    media_general = float(total_datos.mean())

    sc_entre = float(np.sum(conteos * (medias - media_general) ** 2))
    sc_dentro = float(np.sum([np.sum((grupo - grupo.mean()) ** 2) for grupo in datos]))
    sc_total = float(np.sum((total_datos - media_general) ** 2))

    gl_entre = len(datos) - 1
    gl_dentro = total_datos.size - len(datos)
    gl_total = total_datos.size - 1

    cm_entre = sc_entre / gl_entre if gl_entre > 0 else float("nan")
    cm_dentro = sc_dentro / gl_dentro if gl_dentro > 0 else float("nan")
    f_calculada = cm_entre / cm_dentro if cm_dentro not in (0, 0.0) else float("inf")
    p_valor = _p_valor_f(f_calculada, gl_entre, gl_dentro)
    f_critica = _f_critico(alpha, gl_entre, gl_dentro)

    resumen = pd.DataFrame(
        {
            "Grupo": nombres,
            "Conteo": conteos,
            "Suma": np.round(sumas, 6),
            "Promedio": np.round(medias, 6),
            "Varianza": np.round(varianzas, 6),
        }
    )

    anova = pd.DataFrame(
        [
            {
                "Fuente de variacion": "Entre grupos",
                "SC": sc_entre,
                "GL": gl_entre,
                "CM": cm_entre,
                "F": f_calculada,
                "Probabilidad": p_valor,
                "Valor critico para F": f_critica,
            },
            {
                "Fuente de variacion": "Dentro de grupos",
                "SC": sc_dentro,
                "GL": gl_dentro,
                "CM": cm_dentro,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
            {
                "Fuente de variacion": "Total",
                "SC": sc_total,
                "GL": gl_total,
                "CM": np.nan,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
        ]
    )

    hipotesis = {
        "H0": "Las medias de todos los grupos son iguales.",
        "H1": "Al menos una media de grupo es diferente.",
    }
    decision = _interpretar_decision(f_calculada, f_critica, p_valor, alpha)
    conclusion = (
        f"Con alpha = {alpha:.4f}, F = {f_calculada:.6f}, F critica = {f_critica:.6f} y p = {p_valor:.6f}. {decision}"
    )

    interpretacion = (
        f"Hipotesis nula: {hipotesis['H0']}\n"
        f"Hipotesis alternativa: {hipotesis['H1']}\n"
        f"Decision estadistica: {decision}\n"
        f"Conclusión academica: {conclusion}"
    )

    datos_largos = []
    for nombre, grupo in zip(nombres, datos):
        for indice, valor in enumerate(grupo, start=1):
            datos_largos.append({"Grupo": nombre, "Observacion": indice, "Valor": float(valor)})

    return {
        "alpha": alpha,
        "hipotesis": hipotesis,
        "resumen": resumen,
        "anova": anova,
        "datos_largos": pd.DataFrame(datos_largos),
        "estadisticos": {
            "media_general": media_general,
            "sc_entre": sc_entre,
            "sc_dentro": sc_dentro,
            "sc_total": sc_total,
            "gl_entre": gl_entre,
            "gl_dentro": gl_dentro,
            "gl_total": gl_total,
            "cm_entre": cm_entre,
            "cm_dentro": cm_dentro,
            "f_calculada": f_calculada,
            "f_critica": f_critica,
            "p_valor": p_valor,
        },
        "decision": decision,
        "conclusion": conclusion,
        "interpretacion": interpretacion,
    }


def anova_dos_factores_sin_replicacion(
    matriz: Sequence[Sequence[float]],
    nombres_filas: Sequence[str] | None = None,
    nombres_columnas: Sequence[str] | None = None,
    alpha: float = 0.05,
) -> dict:
    """Calcula ANOVA de dos factores sin replicacion."""

    datos = np.asarray(matriz, dtype=float)
    if datos.ndim != 2:
        raise ValueError("La matriz debe ser bidimensional.")
    if datos.shape[0] < 2 or datos.shape[1] < 2:
        raise ValueError("Se requieren al menos 2 filas y 2 columnas.")
    if np.isnan(datos).any():
        raise ValueError("No deje celdas vacias en la matriz.")

    filas, columnas = datos.shape
    nombres_filas = list(nombres_filas) if nombres_filas else [f"Fila {i + 1}" for i in range(filas)]
    nombres_columnas = list(nombres_columnas) if nombres_columnas else [f"Columna {j + 1}" for j in range(columnas)]
    if len(nombres_filas) != filas or len(nombres_columnas) != columnas:
        raise ValueError("Los nombres de filas y columnas deben coincidir con el tamano de la matriz.")

    media_general = float(datos.mean())
    medias_filas = datos.mean(axis=1)
    medias_columnas = datos.mean(axis=0)

    sc_total = float(np.sum((datos - media_general) ** 2))
    sc_filas = float(columnas * np.sum((medias_filas - media_general) ** 2))
    sc_columnas = float(filas * np.sum((medias_columnas - media_general) ** 2))
    sc_error = float(sc_total - sc_filas - sc_columnas)

    gl_filas = filas - 1
    gl_columnas = columnas - 1
    gl_error = (filas - 1) * (columnas - 1)
    gl_total = filas * columnas - 1

    cm_filas = sc_filas / gl_filas if gl_filas > 0 else float("nan")
    cm_columnas = sc_columnas / gl_columnas if gl_columnas > 0 else float("nan")
    cm_error = sc_error / gl_error if gl_error > 0 else float("nan")

    f_filas = cm_filas / cm_error if cm_error not in (0, 0.0) else float("inf")
    f_columnas = cm_columnas / cm_error if cm_error not in (0, 0.0) else float("inf")
    p_filas = _p_valor_f(f_filas, gl_filas, gl_error)
    p_columnas = _p_valor_f(f_columnas, gl_columnas, gl_error)
    fcrit_filas = _f_critico(alpha, gl_filas, gl_error)
    fcrit_columnas = _f_critico(alpha, gl_columnas, gl_error)

    resumen_filas = pd.DataFrame(
        {
            "Fila": nombres_filas,
            "Conteo": [columnas] * filas,
            "Suma": np.round(datos.sum(axis=1), 6),
            "Promedio": np.round(medias_filas, 6),
            "Varianza": np.round(np.var(datos, axis=1, ddof=0), 6),
        }
    )
    resumen_columnas = pd.DataFrame(
        {
            "Columna": nombres_columnas,
            "Conteo": [filas] * columnas,
            "Suma": np.round(datos.sum(axis=0), 6),
            "Promedio": np.round(medias_columnas, 6),
            "Varianza": np.round(np.var(datos, axis=0, ddof=0), 6),
        }
    )

    anova = pd.DataFrame(
        [
            {
                "Fuente de variacion": "Filas",
                "SC": sc_filas,
                "GL": gl_filas,
                "CM": cm_filas,
                "F": f_filas,
                "Probabilidad": p_filas,
                "Valor critico para F": fcrit_filas,
            },
            {
                "Fuente de variacion": "Columnas",
                "SC": sc_columnas,
                "GL": gl_columnas,
                "CM": cm_columnas,
                "F": f_columnas,
                "Probabilidad": p_columnas,
                "Valor critico para F": fcrit_columnas,
            },
            {
                "Fuente de variacion": "Error",
                "SC": sc_error,
                "GL": gl_error,
                "CM": cm_error,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
            {
                "Fuente de variacion": "Total",
                "SC": sc_total,
                "GL": gl_total,
                "CM": np.nan,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
        ]
    )

    interpretacion_filas = _interpretar_decision(f_filas, fcrit_filas, p_filas, alpha)
    interpretacion_columnas = _interpretar_decision(f_columnas, fcrit_columnas, p_columnas, alpha)

    interpretacion = (
        f"Hipotesis filas: no existen diferencias entre las medias de las filas.\n"
        f"Hipotesis columnas: no existen diferencias entre las medias de las columnas.\n"
        f"Filas -> {interpretacion_filas}\n"
        f"Columnas -> {interpretacion_columnas}\n"
        f"Nota: en ANOVA de dos factores sin replicacion la interaccion no se estima por separado."
    )

    datos_largos = []
    for i, nombre_fila in enumerate(nombres_filas):
        for j, nombre_col in enumerate(nombres_columnas):
            datos_largos.append({"Fila": nombre_fila, "Columna": nombre_col, "Valor": float(datos[i, j])})

    return {
        "alpha": alpha,
        "resumen_filas": resumen_filas,
        "resumen_columnas": resumen_columnas,
        "anova": anova,
        "datos_largos": pd.DataFrame(datos_largos),
        "estadisticos": {
            "media_general": media_general,
            "sc_filas": sc_filas,
            "sc_columnas": sc_columnas,
            "sc_error": sc_error,
            "sc_total": sc_total,
            "gl_filas": gl_filas,
            "gl_columnas": gl_columnas,
            "gl_error": gl_error,
            "gl_total": gl_total,
            "cm_filas": cm_filas,
            "cm_columnas": cm_columnas,
            "cm_error": cm_error,
            "f_filas": f_filas,
            "f_columnas": f_columnas,
            "p_filas": p_filas,
            "p_columnas": p_columnas,
            "fcrit_filas": fcrit_filas,
            "fcrit_columnas": fcrit_columnas,
        },
        "conclusion": interpretacion,
        "interpretacion": interpretacion,
    }


def anova_dos_factores_con_replicacion(
    cubo: Sequence[Sequence[Sequence[float]]],
    nombres_filas: Sequence[str] | None = None,
    nombres_columnas: Sequence[str] | None = None,
    nombres_replicaciones: Sequence[str] | None = None,
    alpha: float = 0.05,
) -> dict:
    """Calcula ANOVA de dos factores con replicacion balanceada."""

    datos = np.asarray(cubo, dtype=float)
    if datos.ndim != 3:
        raise ValueError("La estructura debe ser tridimensional: filas, columnas y replicaciones.")
    if datos.shape[0] < 2 or datos.shape[1] < 2 or datos.shape[2] < 2:
        raise ValueError("Se requieren al menos 2 niveles por factor y 2 replicaciones por celda.")
    if np.isnan(datos).any():
        raise ValueError("No deje celdas vacias en los datos de replicacion.")

    filas, columnas, replicaciones = datos.shape
    nombres_filas = list(nombres_filas) if nombres_filas else [f"Factor A {i + 1}" for i in range(filas)]
    nombres_columnas = list(nombres_columnas) if nombres_columnas else [f"Factor B {j + 1}" for j in range(columnas)]
    if len(nombres_filas) != filas or len(nombres_columnas) != columnas:
        raise ValueError("Los nombres de factores no coinciden con las dimensiones de la matriz.")

    if nombres_replicaciones and len(nombres_replicaciones) != replicaciones:
        raise ValueError("Los nombres de replicaciones no coinciden con el numero de observaciones por celda.")

    media_general = float(datos.mean())
    medias_filas = datos.mean(axis=(1, 2))
    medias_columnas = datos.mean(axis=(0, 2))
    medias_celda = datos.mean(axis=2)

    sc_factor_a = float(columnas * replicaciones * np.sum((medias_filas - media_general) ** 2))
    sc_factor_b = float(filas * replicaciones * np.sum((medias_columnas - media_general) ** 2))
    sc_interaccion = float(
        replicaciones
        * np.sum((medias_celda - medias_filas[:, None] - medias_columnas[None, :] + media_general) ** 2)
    )
    sc_error = float(np.sum((datos - medias_celda[:, :, None]) ** 2))
    sc_total = float(np.sum((datos - media_general) ** 2))

    gl_factor_a = filas - 1
    gl_factor_b = columnas - 1
    gl_interaccion = (filas - 1) * (columnas - 1)
    gl_error = filas * columnas * (replicaciones - 1)
    gl_total = filas * columnas * replicaciones - 1

    cm_factor_a = sc_factor_a / gl_factor_a if gl_factor_a > 0 else float("nan")
    cm_factor_b = sc_factor_b / gl_factor_b if gl_factor_b > 0 else float("nan")
    cm_interaccion = sc_interaccion / gl_interaccion if gl_interaccion > 0 else float("nan")
    cm_error = sc_error / gl_error if gl_error > 0 else float("nan")

    f_factor_a = cm_factor_a / cm_error if cm_error not in (0, 0.0) else float("inf")
    f_factor_b = cm_factor_b / cm_error if cm_error not in (0, 0.0) else float("inf")
    f_interaccion = cm_interaccion / cm_error if cm_error not in (0, 0.0) else float("inf")

    p_factor_a = _p_valor_f(f_factor_a, gl_factor_a, gl_error)
    p_factor_b = _p_valor_f(f_factor_b, gl_factor_b, gl_error)
    p_interaccion = _p_valor_f(f_interaccion, gl_interaccion, gl_error)

    fcrit_factor_a = _f_critico(alpha, gl_factor_a, gl_error)
    fcrit_factor_b = _f_critico(alpha, gl_factor_b, gl_error)
    fcrit_interaccion = _f_critico(alpha, gl_interaccion, gl_error)

    resumen = pd.DataFrame(
        [
            {
                "Factor": f"{nombre_fila} / promedio general",
                "Conteo": columnas * replicaciones,
                "Suma": float(np.sum(datos[i, :, :])),
                "Promedio": float(medias_filas[i]),
                "Varianza": float(np.var(datos[i, :, :], ddof=0)),
            }
            for i, nombre_fila in enumerate(nombres_filas)
        ]
    )

    anova = pd.DataFrame(
        [
            {
                "Fuente de variacion": "Factor A",
                "SC": sc_factor_a,
                "GL": gl_factor_a,
                "CM": cm_factor_a,
                "F": f_factor_a,
                "Probabilidad": p_factor_a,
                "Valor critico para F": fcrit_factor_a,
            },
            {
                "Fuente de variacion": "Factor B",
                "SC": sc_factor_b,
                "GL": gl_factor_b,
                "CM": cm_factor_b,
                "F": f_factor_b,
                "Probabilidad": p_factor_b,
                "Valor critico para F": fcrit_factor_b,
            },
            {
                "Fuente de variacion": "Interaccion",
                "SC": sc_interaccion,
                "GL": gl_interaccion,
                "CM": cm_interaccion,
                "F": f_interaccion,
                "Probabilidad": p_interaccion,
                "Valor critico para F": fcrit_interaccion,
            },
            {
                "Fuente de variacion": "Error",
                "SC": sc_error,
                "GL": gl_error,
                "CM": cm_error,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
            {
                "Fuente de variacion": "Total",
                "SC": sc_total,
                "GL": gl_total,
                "CM": np.nan,
                "F": np.nan,
                "Probabilidad": np.nan,
                "Valor critico para F": np.nan,
            },
        ]
    )

    decision_a = _interpretar_decision(f_factor_a, fcrit_factor_a, p_factor_a, alpha)
    decision_b = _interpretar_decision(f_factor_b, fcrit_factor_b, p_factor_b, alpha)
    decision_interaccion = _interpretar_decision(f_interaccion, fcrit_interaccion, p_interaccion, alpha)

    significado_interaccion = (
        "La interaccion es estadisticamente significativa, por lo que el efecto de un factor depende del nivel del otro. "
        "En este caso conviene interpretar con cautela los efectos principales y dar prioridad al analisis combinado."
        if decision_interaccion.startswith("Se rechaza")
        else "No se detecta interaccion estadisticamente significativa, por lo que los efectos principales pueden interpretarse de forma independiente."
    )

    interpretacion = (
        "Hipotesis nula factor A: las medias del factor A son iguales.\n"
        "Hipotesis nula factor B: las medias del factor B son iguales.\n"
        "Hipotesis nula de interaccion: no existe interaccion entre los factores.\n\n"
        f"Factor A: {decision_a} (F = {f_factor_a:.6f}, F critica = {fcrit_factor_a:.6f}, p = {p_factor_a:.6f}).\n"
        f"Factor B: {decision_b} (F = {f_factor_b:.6f}, F critica = {fcrit_factor_b:.6f}, p = {p_factor_b:.6f}).\n"
        f"Interaccion: {decision_interaccion} (F = {f_interaccion:.6f}, F critica = {fcrit_interaccion:.6f}, p = {p_interaccion:.6f}).\n\n"
        f"Conclusion academica: {significado_interaccion}"
    )

    datos_largos = []
    for i, nombre_fila in enumerate(nombres_filas):
        for j, nombre_col in enumerate(nombres_columnas):
            for k in range(replicaciones):
                etiqueta_rep = nombres_replicaciones[k] if nombres_replicaciones else f"Rep {k + 1}"
                datos_largos.append(
                    {
                        "Factor A": nombre_fila,
                        "Factor B": nombre_col,
                        "Replicacion": etiqueta_rep,
                        "Valor": float(datos[i, j, k]),
                    }
                )

    return {
        "alpha": alpha,
        "resumen": resumen,
        "anova": anova,
        "datos_largos": pd.DataFrame(datos_largos),
        "estadisticos": {
            "media_general": media_general,
            "sc_factor_a": sc_factor_a,
            "sc_factor_b": sc_factor_b,
            "sc_interaccion": sc_interaccion,
            "sc_error": sc_error,
            "sc_total": sc_total,
            "gl_factor_a": gl_factor_a,
            "gl_factor_b": gl_factor_b,
            "gl_interaccion": gl_interaccion,
            "gl_error": gl_error,
            "gl_total": gl_total,
            "cm_factor_a": cm_factor_a,
            "cm_factor_b": cm_factor_b,
            "cm_interaccion": cm_interaccion,
            "cm_error": cm_error,
            "f_factor_a": f_factor_a,
            "f_factor_b": f_factor_b,
            "f_interaccion": f_interaccion,
            "p_factor_a": p_factor_a,
            "p_factor_b": p_factor_b,
            "p_interaccion": p_interaccion,
            "fcrit_factor_a": fcrit_factor_a,
            "fcrit_factor_b": fcrit_factor_b,
            "fcrit_interaccion": fcrit_interaccion,
        },
        "conclusion": interpretacion,
        "interpretacion": interpretacion,
    }
