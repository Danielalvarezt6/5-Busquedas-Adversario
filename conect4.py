"""
Juego de conecta 4

El estado se va a representar como una lista de 42 elementos, tal que


0  1  2  3  4  5  6
7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 29 30 31 32 33 34
35 36 37 38 39 40 41

y cada elemento puede ser 0, 1 o -1, donde 0 es vacío, 1 es una ficha del
jugador 1 y -1 es una ficha del jugador 2.

Las acciones son poner una ficha en una columna, que se representa como un
número de 0 a 6.

Un estado terminal es aquel en el que un jugador ha conectado 4 fichas
horizontales, verticales o diagonales, o ya no hay espacios para colocar
fichas.

La ganancia es 1 si gana el jugador 1, -1 si gana el jugador 2 y 0 si es un
empate.

"""

import juegos_simplificado as js
import minimax

class Conecta4(js.JuegoZT2):
    def inicializa(self):
        return tuple([0 for _ in range(6 * 7)])
        
    def jugadas_legales(self, s, j):
        return (columna for columna in range(7) if s[columna] == 0)
    
    def sucesor(self, s, a, j):
        s = list(s[:])
        for i in range(5, -1, -1):
            if s[a + 7 * i] == 0:
                s[a + 7 * i] = j
                break
        return tuple(s)
    
    def ganancia(self, s):
        #Verticales
        for i in range(7):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * (j + 1)] == s[i + 7 * (j + 2)] == s[i + 7 * (j + 3)] != 0):
                    return s[i + 7 * j]
        #Horizontales
        for i in range(6):
            for j in range(4):
                if (s[7 * i + j] == s[7 * i + j + 1] == s[7 * i + j + 2] == s[7 * i + j + 3] != 0):
                    return s[7 * i + j]
        #Diagonales
        for i in range(4):
            for j in range(3):
                if (s[i + 7 * j] == s[i + 7 * j + 8] == s[i + 7 * j + 16] == s[i + 7 * j + 24] != 0):
                    return s[i + 7 * j]
                if (s[i + 7 * j + 3] == s[i + 7 * j + 9] == s[i + 7 * j + 15] == s[i + 7 * j + 21] != 0):
                    return s[i + 7 * j + 3]
        return 0
    
    def terminal(self, s):
        if 0 not in s:
            return True
        return self.ganancia(s) != 0
    
class InterfaceConecta4(js.JuegoInterface):
    def muestra_estado(self, s):
        """
        Muestra el estado del juego, se puede usar la función pprint_conecta4
        para mostrar el estado de forma más amigable

        """
        a = [' X ' if x == 1 else ' O ' if x == -1 else '   ' for x in s]
        print('\n 0 | 1 | 2 | 3 | 4 | 5 | 6')
        for i in range(6):
            print('|'.join(a[7 * i:7 * (i + 1)]))
            print('---+---+---+---+---+---+---\n')
    
    def muestra_ganador(self, g):
        """
        Muestra el ganador del juego, se puede usar " XO"[g] para mostrar el
        ganador de forma más amigable

        """
        if g != 0:
            print("Gana el jugador " + " XO"[g])
        else:
            print("Un asqueroso empate")

    def jugador_humano(self, s, j):
        print("Jugador", " XO"[j])
        jugadas = list(self.juego.jugadas_legales(s, j))
        print("Jugadas legales:", jugadas)
        jugada = None
        while jugada not in jugadas:
            jugada = int(input("Jugada: "))
        return jugada

def ordena_centro(jugadas, jugador, s=None):
    """
    Ordena las jugadas de acuerdo a la distancia al centro
    """
    return sorted(jugadas, key=lambda x: abs(x - 4))

def evalua_3con(s):
    """
    Evalua el estado s para el jugador 1
    """
    conect3 = sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == 1)
    ) - sum(
        1 for i in range(7) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * (j + 1)] 
            == s[i + 7 * (j + 2)] == -1)
    ) + sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == 1)
    ) - sum(
        1 for i in range(6) for j in range(5) 
        if (s[7 * i + j] == s[7 * i + j + 1] 
            == s[7 * i + j + 2] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j] == s[i + 7 * j + 8] 
            == s[i + 7 * j + 16] == -1)
    ) + sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == 1)
    ) - sum(
        1 for i in range(5) for j in range(4) 
        if (s[i + 7 * j + 3] == s[i + 7 * j + 9] 
            == s[i + 7 * j + 15] == -1)
    )
    promedio = conect3 / (7 * 4 + 6 * 5 + 5 * 4 + 5 * 4)
    if abs(promedio) >= 1:
        raise ValueError("Evaluación fuera de rango --> ", promedio)
    return promedio

# ---------------------------------------------------------------------------
# Precomputo de todas las líneas de 4 celdas posibles en el tablero 6×7
# ---------------------------------------------------------------------------
_VENTANAS = []
_VTIPO = []   # 'h', 'v' o 'd' (diagonal)
for _r in range(6):
    for _c in range(4):
        _VENTANAS.append(tuple(_r * 7 + _c + k for k in range(4)))
        _VTIPO.append('h')
for _c in range(7):
    for _r in range(3):
        _VENTANAS.append(tuple((_r + k) * 7 + _c for k in range(4)))
        _VTIPO.append('v')
for _r in range(3):
    for _c in range(4):
        _VENTANAS.append(tuple((_r + k) * 7 + _c + k for k in range(4)))
        _VTIPO.append('d')
for _r in range(3):
    for _c in range(3, 7):
        _VENTANAS.append(tuple((_r + k) * 7 + _c - k for k in range(4)))
        _VTIPO.append('d')

_VENTANAS_DE = {i: [] for i in range(42)}
for _idx, _v in enumerate(_VENTANAS):
    for _celda in _v:
        _VENTANAS_DE[_celda].append(_idx)

_PESO_COL = (0, 0.5, 1.0, 1.5, 1.0, 0.5, 0)


def _fila_caida(s, col):
    for i in range(5, -1, -1):
        if s[col + 7 * i] == 0:
            return i
    return -1


def evalua_ventanas(s):
    """
    Evaluación por dominancia territorial:
      - Pesos exponenciales por piezas alineadas en una ventana libre
      - Prima ×1.3 para alineaciones diagonales (más difíciles de defender)
      - Multiplicador de inmediatez: si la celda que completa la línea
        es jugable AHORA (tiene soporte), la amenaza vale mucho más
      - Bonus posicional por fichas en columnas centrales
    """
    score = 0.0
    pesos = (0, 1, 8, 80)

    for ventana, tipo in zip(_VENTANAS, _VTIPO):
        c0, c1, c2, c3 = (
            s[ventana[0]], s[ventana[1]], s[ventana[2]], s[ventana[3]]
        )
        p1 = (c0 == 1) + (c1 == 1) + (c2 == 1) + (c3 == 1)
        p2 = (c0 == -1) + (c1 == -1) + (c2 == -1) + (c3 == -1)

        if (p1 and p2) or not (p1 or p2):
            continue

        piezas, signo = (p1, 1) if p1 else (p2, -1)
        mult = 1.3 if tipo == 'd' else 1.0

        if piezas >= 2:
            for i in ventana:
                if s[i] == 0:
                    fila = i // 7
                    if fila == 5 or s[i + 7] != 0:
                        mult *= 2.5 if piezas == 3 else 1.4
                        break

        score += signo * pesos[piezas] * mult

    for i in range(42):
        if s[i]:
            score += s[i] * _PESO_COL[i % 7]

    return max(-0.999, min(0.999, score / 3500))


def ordena_consecuencias(jugadas, jugador, s):
    """
    Ordenamiento por análisis de consecuencias:
      1. Victoria inmediata  →  prioridad máxima
      2. Bloqueo de victoria rival  →  segunda prioridad
      3. Creación de amenaza propia (3 en línea libre)
      4. Bloqueo de amenaza rival
      5. Detección de trampa: si colocar aquí le regala al rival
         una celda ganadora justo arriba  →  penalización fuerte
      6. Centralidad como desempate
    """
    def _score(col):
        fila = _fila_caida(s, col)
        if fila < 0:
            return -10000
        pos = col + 7 * fila
        pts = 0.0

        s_sim = list(s)
        s_sim[pos] = jugador
        for vi in _VENTANAS_DE[pos]:
            v = _VENTANAS[vi]
            propias = sum(1 for i in v if s_sim[i] == jugador)
            rivales = sum(1 for i in v if s_sim[i] == -jugador)
            if rivales == 0:
                if propias == 4:
                    return 10000
                if propias == 3:
                    pts += 40

        s_sim[pos] = -jugador
        for vi in _VENTANAS_DE[pos]:
            v = _VENTANAS[vi]
            rivales = sum(1 for i in v if s_sim[i] == -jugador)
            propias = sum(1 for i in v if s_sim[i] == jugador)
            if propias == 0:
                if rivales == 4:
                    pts += 5000
                elif rivales == 3:
                    pts += 25

        if fila > 0:
            pos_arriba = col + 7 * (fila - 1)
            s_tr = list(s)
            s_tr[pos] = jugador
            s_tr[pos_arriba] = -jugador
            for vi in _VENTANAS_DE[pos_arriba]:
                v = _VENTANAS[vi]
                if all(s_tr[i] == -jugador for i in v):
                    pts -= 3000
                    break

        pts += (3 - abs(col - 3)) * 0.5
        return pts

    return sorted(jugadas, key=_score, reverse=True)


if __name__ == '__main__':

    cfg = {
        "Jugador 1": "Humano",      #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "Jugador 2": "Aleatorio",   #Puede ser "Humano", "Aleatorio", "Negamax", "Tiempo"
        "profundidad máxima": 5,
        "tiempo": 10,
        "ordena": ordena_consecuencias, #Puede ser None o una función f(jugadas, j, s) -> lista de jugadas ordenada
        "evalua": evalua_ventanas      #Puede ser None o una función f(estado) -> número entre -1 y 1
    }

    def jugador_cfg(cadena):
        if cadena == "Humano":
            return "Humano"
        elif cadena == "Aleatorio":
            return js.JugadorAleatorio()
        elif cadena == "Negamax":
            return minimax.JugadorNegamax(
                ordena=cfg["ordena"], d=cfg["profundidad máxima"], evalua=cfg["evalua"]
            )
        elif cadena == "Tiempo":
            return minimax.JugadorMinimaxIterativo(
                tiempo=cfg["tiempo"], ordena=cfg["ordena"], evalua=cfg["evalua"]
            )
        else:
            raise ValueError("Jugador no reconocido")

    interfaz = InterfaceConecta4(
        Conecta4(),
        jugador1=jugador_cfg(cfg["Jugador 1"]),
        jugador2=jugador_cfg(cfg["Jugador 2"])
    )

    print("El Juego del Conecta 4 ")
    print("Jugador 1:", cfg["Jugador 1"])
    print("Jugador 2:", cfg["Jugador 2"])
    print()

    interfaz.juega()
