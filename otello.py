"""
Juego de Otello

Tablero de 8x8, cada cuadrito vale 0 (vacía), 1 (negra/X) o -1 (blanca/O).
Se inicia el juego con 4 fichas en el centro y mueven primero las negras.

La jugada consiste en poner una ficha de tu color de modo que "encierres"
fichas del rival en línea recta (horizontal, vertical o diagonal).
Las fichas encerradas se voltean a tu color.
Si no puedes mover, pasas. Si ambos pasan, se acabó el juego.
Gana quien tenga más fichas al final.

tablero:
 0  1  2  3  4  5  6  7
 8  9 10 11 12 13 14 15
16 17 18 19 20 21 22 23
24 25 26 27 28 29 30 31
32 33 34 35 36 37 38 39
40 41 42 43 44 45 46 47
48 49 50 51 52 53 54 55
56 57 58 59 60 61 62 63
"""

import juegos_simplificado as js

# las 8 direcciones en las que se puede voltear una ficha
DIRS = [(-1, -1), (-1, 0), (-1, 1),
         ( 0, -1),          ( 0, 1),
         ( 1, -1), ( 1, 0), ( 1, 1)]


def volteos(s, pos, j):
    """
    regresa la lista de posiciones que se voltean si el jugador j pone ficha en pos.
    s: estado del tablero
    pos: posición de la ficha
    j: jugador
    """
    fila, columna = divmod(pos, 8)
    resultado = []
    for df, dc in DIRS:
        temp = []
        f, c = fila + df, columna  + dc
        while 0 <= f < 8 and 0 <= c < 8:
            idx = f * 8 + c
            if s[idx] == -j:
                temp.append(idx)
            elif s[idx] == j:
                resultado.extend(temp)
                break
            else:
                break
            f += df
            c += dc
    return resultado


def movimientos(s, j):
    """cuadritos vacíos donde el jugador j puede colocar ficha (voltea al menos una)."""
    return [i for i in range(64) if s[i] == 0 and volteos(s, i, j)]
