"""Calculos para estimacion e intervalos de confianza en Estadistica II."""

import math
from statistics import NormalDist


class EstimacionTamanoMuestra:
    """Implementa formulas de tamano de muestra, estimacion puntual e intervalos."""

    @classmethod
    def normalizar_confianza_porcentaje(cls, nivel_confianza):
        valor_str = str(nivel_confianza).strip()
        if not valor_str:
            raise ValueError("Ingrese un nivel de confianza valido.")

        if valor_str.endswith("%"):
            valor_str = valor_str[:-1].strip()

        valor = float(valor_str)
        if valor <= 0:
            raise ValueError("El nivel de confianza debe ser mayor que 0.")

        if valor < 1:
            valor *= 100

        if valor >= 100:
            raise ValueError("El nivel de confianza debe ser menor que 100%.")

        return valor

    @classmethod
    def obtener_z(cls, nivel_confianza):
        confianza = cls.normalizar_confianza_porcentaje(nivel_confianza)
        alpha = 1 - (confianza / 100)
        probabilidad = 1 - (alpha / 2)
        return NormalDist().inv_cdf(probabilidad)

    @classmethod
    def obtener_t_critico(cls, nivel_confianza, grados_libertad):
        """Aproxima t critico bilateral usando expansion de Cornish-Fisher."""
        gl = int(grados_libertad)
        if gl <= 0:
            raise ValueError("Los grados de libertad deben ser mayores que 0.")

        z = cls.obtener_z(nivel_confianza)
        if gl > 200:
            return z

        v = float(gl)
        z3 = z**3
        z5 = z**5
        z7 = z**7

        t = z
        t += (z3 + z) / (4 * v)
        t += (5 * z5 + 16 * z3 + 3 * z) / (96 * (v**2))
        t += (3 * z7 + 19 * z5 + 17 * z3 - 15 * z) / (384 * (v**3))
        return t

    @staticmethod
    def _validar_no_negativo(valor, nombre):
        if valor < 0:
            raise ValueError(f"{nombre} no puede ser negativo.")

    @staticmethod
    def _validar_positivo(valor, nombre):
        if valor <= 0:
            raise ValueError(f"{nombre} debe ser mayor que cero.")

    @staticmethod
    def calcular_q(p):
        if p < 0 or p > 1:
            raise ValueError("p debe estar entre 0 y 1.")
        return 1 - p

    def tamano_muestra_proporcion_desconocida(self, z, p, d):
        self._validar_positivo(d, "d")
        if p < 0 or p > 1:
            raise ValueError("p debe estar entre 0 y 1.")

        q = 1 - p
        n = (z**2 * p * q) / (d**2)
        return n

    def tamano_muestra_proporcion_conocida(self, n_poblacion, z, p, d):
        self._validar_positivo(d, "d")
        self._validar_positivo(n_poblacion, "N")
        if n_poblacion <= 1:
            raise ValueError("N debe ser mayor que 1 para poblacion conocida.")
        if p < 0 or p > 1:
            raise ValueError("p debe estar entre 0 y 1.")

        q = 1 - p
        numerador = n_poblacion * (z**2) * p * q
        denominador = (d**2) * (n_poblacion - 1) + (z**2) * p * q
        return numerador / denominador

    def tamano_muestra_media_desconocida(self, z, s, d):
        self._validar_no_negativo(s, "s")
        self._validar_positivo(d, "d")
        return (z**2 * s**2) / (d**2)

    def tamano_muestra_media_conocida(self, n_poblacion, z, s, d):
        self._validar_positivo(n_poblacion, "N")
        if n_poblacion <= 1:
            raise ValueError("N debe ser mayor que 1 para poblacion conocida.")
        self._validar_no_negativo(s, "s")
        self._validar_positivo(d, "d")

        numerador = n_poblacion * (z**2) * (s**2)
        denominador = (d**2) * (n_poblacion - 1) + (z**2) * (s**2)
        return numerador / denominador

    @staticmethod
    def ajuste_perdidas(n, pe):
        if pe < 0:
            raise ValueError("El porcentaje de perdidas no puede ser negativo.")

        pe_proporcion = pe / 100 if pe > 1 else pe
        if pe_proporcion >= 1:
            raise ValueError("El porcentaje de perdidas debe ser menor que 100%.")

        return n / (1 - pe_proporcion)

    @staticmethod
    def estimacion_puntual_proporcion(x, n):
        if n == 0:
            raise ValueError("n no puede ser cero.")
        if x < 0 or n < 0:
            raise ValueError("x y n no pueden ser negativos.")
        if x > n:
            raise ValueError("x no puede ser mayor que n.")
        return x / n

    def intervalo_confianza_proporcion(self, p_hat, n, z):
        if p_hat < 0 or p_hat > 1:
            raise ValueError("p_hat debe estar entre 0 y 1.")
        self._validar_positivo(n, "n")

        error = z * math.sqrt((p_hat * (1 - p_hat)) / n)
        return p_hat - error, p_hat + error

    def intervalo_confianza_media(self, media, s, n, z):
        self._validar_no_negativo(s, "s")
        self._validar_positivo(n, "n")

        error = z * (s / math.sqrt(n))
        return media - error, media + error

    @staticmethod
    def redondear_tamano_muestra(n):
        return math.ceil(n)