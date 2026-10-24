# Pixel art de la opción D ("El pizarrón"): personajes del cuerpo técnico, íconos de las secciones y logo.
# Elaboración propia, sin assets de terceros: cada figura se dibuja con código sobre una grilla de regiones
# (pelo, piel, buzo, pantalón...). Después cada región se sombrea sola con cuatro tonos (luz arriba a la
# izquierda: luz, base, sombra y sombra profunda, con las sombras corridas al violeta y las luces al amarillo),
# se le agrega un contorno selectivo (el color del vecino, oscurecido) y se convierte en SVG de píxeles.

import html
import math

LUZ, SOMBRA, PROFUNDA = '#fff2cc', '#2b2a55', '#1b1435'


def _mezcla(color, otro, t):
    a = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(otro[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))


def oscuro(color, t=0.3):
    return _mezcla(color, '#000000', t)


def claro(color, t=0.3):
    return _mezcla(color, '#ffffff', t)


class Lienzo:
    """Grilla de regiones: cada píxel guarda la letra de su región ('.' es transparente)."""

    def __init__(self, ancho, alto):
        self.ancho, self.alto = ancho, alto
        self.g = [['.'] * ancho for _ in range(alto)]

    def punto(self, x, y, r):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.g[y][x] = r

    def rect(self, x0, y0, x1, y1, r):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.punto(x, y, r)

    def tramos(self, filas, r):
        """filas: {y: (x0, x1)} o {y: [(x0, x1), ...]}."""
        for y, t in filas.items():
            for x0, x1 in (t if isinstance(t, list) else [t]):
                self.rect(x0, y, x1, y, r)

    def disco(self, cx, cy, radio, r):
        for y in range(self.alto):
            for x in range(self.ancho):
                if (x - cx) ** 2 + (y - cy) ** 2 <= radio ** 2:
                    self.punto(x, y, r)

    def linea(self, x0, y0, x1, y1, r, grosor=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x, y = round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)
            self.rect(x, y, x + grosor - 1, y, r)

    def girado(self, cx, cy, ancho, alto, grados, dentro):
        """Rectángulo girado: dentro(u, v) decide la región de cada píxel (u, v en el sistema del rectángulo)."""
        c, s = math.cos(math.radians(grados)), math.sin(math.radians(grados))
        for y in range(self.alto):
            for x in range(self.ancho):
                dx, dy = x + 0.5 - cx, y + 0.5 - cy
                u, v = dx * c + dy * s + ancho / 2, -dx * s + dy * c + alto / 2
                if 0 <= u < ancho and 0 <= v < alto:
                    r = dentro(u, v)
                    if r:
                        self.punto(x, y, r)


def sombrear(lz, paleta, planos=''):
    """Cuatro tonos por región: luz arriba y a la izquierda, sombra abajo y a la derecha, sombra profunda en el
    borde derecho de los tramos anchos. Las regiones de `planos` (ojos, boca, detalles chicos) van sin sombrear."""
    g = lz.g
    px = [[None] * lz.ancho for _ in range(lz.alto)]
    for y in range(lz.alto):
        x = 0
        while x < lz.ancho:
            r = g[y][x]
            if r == '.':
                x += 1
                continue
            x1 = x
            while x1 + 1 < lz.ancho and g[y][x1 + 1] == r:
                x1 += 1
            n = x1 - x + 1
            for xi in range(x, x1 + 1):
                base = paleta[r]
                if r in planos:
                    px[y][xi] = base
                    continue
                t = (xi - x) / max(1, n - 1)
                arriba = y == 0 or g[y - 1][xi] != r
                abajo = y == lz.alto - 1 or g[y + 1][xi] != r
                tono = 'base'
                if n >= 3:
                    if xi == x1 and n >= 5:
                        tono = 'profunda'
                    elif t > 0.66:
                        tono = 'sombra'
                    elif t < 0.3:
                        tono = 'luz'
                if abajo and tono in ('base', 'luz'):
                    tono = 'sombra'
                if arriba and tono == 'base':
                    tono = 'luz'
                px[y][xi] = {'base': base, 'luz': _mezcla(base, LUZ, 0.3), 'sombra': _mezcla(base, SOMBRA, 0.3),
                             'profunda': _mezcla(base, PROFUNDA, 0.5)}[tono]
            x = x1 + 1
    return px


def contornear(px, tono=0.62):
    """Contorno de 1 píxel alrededor de la figura: el color del vecino, oscurecido. Agrega 1 píxel de margen."""
    px = [[None] * (len(px[0]) + 2)] + [[None] + fila + [None] for fila in px] + [[None] * (len(px[0]) + 2)]
    alto, ancho = len(px), len(px[0])
    salida = [fila[:] for fila in px]
    for y in range(alto):
        for x in range(ancho):
            if px[y][x] is not None:
                continue
            vecinos = [px[y + dy][x + dx] for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))
                       if 0 <= y + dy < alto and 0 <= x + dx < ancho and px[y + dy][x + dx] is not None]
            if vecinos:
                salida[y][x] = _mezcla(vecinos[0], '#120c1e', tono)
    return salida


def svg(px, clase='pixel', etiqueta=''):
    """SVG de píxeles: un <rect> por tramo horizontal del mismo color."""
    alto, ancho = len(px), len(px[0])
    rects = []
    for y, fila in enumerate(px):
        x = 0
        while x < ancho:
            c = fila[x]
            if c is None:
                x += 1
                continue
            n = 1
            while x + n < ancho and fila[x + n] == c:
                n += 1
            rects.append(f'<rect x="{x}" y="{y}" width="{n}" height="1" fill="{c}"/>')
            x += n
    accesible = f'role="img" aria-label="{html.escape(etiqueta)}"' if etiqueta else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{clase}" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}" '
            f'shape-rendering="crispEdges" {accesible}>{"".join(rects)}</svg>')


# ------------------------------------------------------------------ Personajes (32 x 48, con contorno 34 x 50)
# Regiones: H pelo · S piel · N cuello · Y cejas · E ojo · W brillo del ojo · n nariz · M boca · T torso
# C cuello de la prenda · A manga · G mano · B cinturón · P pantalón · K calzado · J pierna (con short) · 1 medias
# Accesorios: Q gorra o sombrero · V visera, vincha o bandera · Z metal · X oscuro · O lente o papel · R asa
# U cuerpo del maletín · F solapa · I corbata · L bolsillo o abertura del saco · D tablero de la carpeta

PLANOS = 'EWnMYZXOLFI1'

PIEL = {'clara': '#f2c9a0', 'media': '#d9a066', 'morena': '#a8693d', 'oscura': '#6e4226', 'rosada': '#f0b898'}


def cabeza(lz, estilo):
    lz.tramos({3: (12, 19), 4: (11, 20), **{y: (10, 21) for y in range(5, 13)}, 13: (11, 20), 14: (12, 19),
               15: (13, 18)}, 'S')
    lz.rect(9, 8, 9, 10, 'S')
    lz.rect(22, 8, 22, 10, 'S')
    if estilo in ('corto', 'vincha', 'peinado'):
        lz.tramos({1: (12, 19), 2: (11, 20), 3: (10, 21), 4: (10, 21), 5: (10, 21), 6: [(10, 13), (20, 21)],
                   7: [(10, 10), (21, 21)]}, 'H')
        if estilo == 'vincha':
            lz.rect(10, 4, 21, 5, 'V')
        if estilo == 'peinado':
            lz.rect(13, 2, 13, 4, 'S')
    elif estilo == 'gorra':
        lz.tramos({1: (12, 19), 2: (11, 20), 3: (10, 21), 4: (10, 21), 5: (10, 21)}, 'Q')
        lz.rect(8, 6, 22, 6, 'V')
        lz.rect(10, 7, 21, 7, 'H')
    elif estilo == 'sombrero':
        lz.tramos({1: (12, 19), 2: (11, 20), 3: (11, 20), 4: (11, 20)}, 'Q')
        lz.rect(7, 5, 24, 6, 'V')
        lz.rect(10, 7, 10, 8, 'H')
        lz.rect(21, 7, 21, 8, 'H')
    elif estilo == 'entradas':
        lz.tramos({5: [(10, 11), (20, 21)], 6: [(10, 11), (20, 21)], 7: [(10, 10), (21, 21)]}, 'H')
        lz.rect(9, 6, 9, 7, 'H')
        lz.rect(22, 6, 22, 7, 'H')
    # Cara: cejas, ojos de 2 x 2 con brillo, nariz y boca.
    lz.rect(12, 7, 14, 7, 'Y')
    lz.rect(17, 7, 19, 7, 'Y')
    for x in (13, 17):
        lz.rect(x, 9, x + 1, 10, 'E')
        lz.punto(x + 1, 9, 'W')
    lz.punto(16, 11, 'n')
    lz.rect(15, 12, 16, 12, 'n')
    lz.rect(14, 13, 17, 13, 'M')
    lz.rect(14, 16, 17, 16, 'N')


def torso(lz, faldon=False):
    lz.tramos({17: (10, 21), 18: (8, 23), 19: (8, 23), 20: (8, 23), **{y: (9, 22) for y in range(21, 30)}}, 'T')
    lz.tramos({17: (13, 18), 18: (14, 17), 19: (15, 16)}, 'C')
    lz.rect(9, 30, 22, 30, 'B')
    if faldon:
        lz.tramos({y: (9, 22) for y in range(30, 39)}, 'T')
        lz.rect(15, 20, 16, 38, 'L')


def piernas(lz, tipo='largo'):
    lz.rect(9, 31, 22, 32, 'P')
    lz.rect(9, 33, 14, 44, 'P')
    lz.rect(17, 33, 22, 44, 'P')
    if tipo == 'short':
        lz.rect(9, 37, 14, 40, 'J')
        lz.rect(17, 37, 22, 40, 'J')
        lz.rect(9, 41, 14, 44, '1')
        lz.rect(17, 41, 22, 44, '1')
    lz.tramos({45: [(9, 14), (17, 22)], 46: [(8, 14), (17, 23)]}, 'K')


def brazo_caido(lz, lado, mano=True, hasta=29):
    x0 = 5 if lado == 'izq' else 24
    lz.rect(x0 + (1 if lado == 'izq' else 0), 18, x0 + (2 if lado == 'izq' else 1), 18, 'A')
    lz.rect(x0, 19, x0 + 2, hasta, 'A')
    if mano:
        lz.rect(x0, hasta + 1, x0 + 2, hasta + 3, 'G')


def pose(lz, nombre):
    if nombre == 'caidos':
        brazo_caido(lz, 'izq')
        brazo_caido(lz, 'der')
    elif nombre == 'cruzados':
        lz.rect(6, 18, 8, 24, 'A')
        lz.rect(23, 18, 25, 24, 'A')
        lz.rect(7, 23, 24, 25, 'A')
        lz.rect(21, 22, 23, 23, 'G')
        lz.rect(8, 25, 10, 26, 'G')
    elif nombre == 'carpeta':
        lz.rect(6, 18, 8, 25, 'A')
        lz.rect(23, 18, 25, 25, 'A')
        lz.rect(11, 19, 20, 29, 'D')
        lz.rect(12, 20, 19, 28, 'O')
        for y in (22, 24, 26):
            lz.rect(13, y, 18, y, 'X')
        lz.rect(14, 18, 17, 19, 'Z')
        lz.rect(8, 25, 11, 27, 'A')
        lz.rect(20, 25, 23, 27, 'A')
        lz.rect(10, 24, 12, 26, 'G')
        lz.rect(19, 24, 21, 26, 'G')
    elif nombre == 'cronometro':
        brazo_caido(lz, 'izq')
        lz.rect(24, 18, 26, 20, 'A')
        lz.rect(24, 11, 26, 19, 'A')
        lz.rect(24, 8, 26, 10, 'G')
        lz.disco(25, 4.5, 2.6, 'Z')
        lz.rect(24, 4, 26, 5, 'O')
        lz.punto(25, 1, 'Z')
    elif nombre == 'binoculares':
        lz.rect(6, 18, 8, 22, 'A')
        lz.rect(23, 18, 25, 22, 'A')
        lz.linea(8, 19, 10, 13, 'A', 2)
        lz.linea(22, 19, 20, 13, 'A', 2)
        lz.rect(9, 10, 11, 12, 'G')
        lz.rect(20, 10, 22, 12, 'G')
        lz.rect(11, 8, 15, 12, 'X')
        lz.rect(16, 8, 20, 12, 'X')
        lz.rect(15, 9, 16, 10, 'X')
        lz.rect(12, 9, 14, 11, 'O')
        lz.rect(17, 9, 19, 11, 'O')
        lz.punto(12, 9, 'W')
        lz.punto(17, 9, 'W')
    elif nombre == 'bolsillos':
        lz.rect(6, 18, 8, 29, 'A')
        lz.rect(23, 18, 25, 29, 'A')
        lz.rect(7, 18, 8, 18, 'A')
        lz.rect(9, 31, 11, 31, 'L')
        lz.rect(20, 31, 22, 31, 'L')
        lz.linea(8, 29, 10, 31, 'A')
        lz.linea(23, 29, 21, 31, 'A')
    elif nombre == 'maletin':
        brazo_caido(lz, 'izq')
        brazo_caido(lz, 'der')
        lz.rect(24, 33, 27, 33, 'R')
        lz.rect(24, 34, 24, 34, 'R')
        lz.rect(27, 34, 27, 34, 'R')
        lz.rect(21, 35, 30, 42, 'U')
        lz.rect(21, 37, 30, 37, 'X')
        lz.rect(25, 37, 26, 38, 'Z')


def figura(cabeza_estilo, pose_nombre, piernas_tipo='largo', faldon=False, extra=None):
    lz = Lienzo(32, 48)
    piernas(lz, piernas_tipo)
    torso(lz, faldon)
    if extra:
        extra(lz, 'debajo')
    cabeza(lz, cabeza_estilo)
    pose(lz, pose_nombre)
    if extra:
        extra(lz, 'encima')
    return lz


def paleta_base(piel, pelo, torso_c, manga, pantalon, calzado, cuello, cinturon='#2b2118', **extra):
    p = {
        'H': pelo, 'S': piel, 'N': oscuro(piel, 0.2), 'Y': oscuro(pelo, 0.25), 'E': '#1c1410', 'W': '#ffffff',
        'n': oscuro(piel, 0.2), 'M': oscuro(piel, 0.42), 'T': torso_c, 'C': cuello, 'A': manga, 'G': piel,
        'B': cinturon, 'P': pantalon, 'K': calzado, 'J': piel, '1': '#f4f1e8', 'L': oscuro(torso_c, 0.35),
    }
    p.update(extra)
    return p


def silbato(lz, capa):
    if capa == 'encima':
        lz.linea(13, 17, 15, 21, 'X')
        lz.linea(18, 17, 16, 21, 'X')
        lz.rect(15, 21, 17, 22, 'Z')


def estetoscopio(lz, capa):
    if capa == 'encima':
        lz.linea(12, 17, 12, 22, 'Z')
        lz.linea(19, 17, 19, 22, 'Z')
        lz.linea(12, 22, 15, 25, 'Z')
        lz.linea(19, 22, 16, 25, 'Z')
        lz.rect(15, 25, 16, 27, 'Z')
        lz.rect(19, 23, 21, 25, 'U')
        lz.punto(20, 23, 'V')
        lz.punto(19, 24, 'V')
        lz.punto(20, 24, 'V')
        lz.punto(21, 24, 'V')
        lz.punto(20, 25, 'V')


def traje(lz, capa):
    if capa == 'encima':
        lz.linea(12, 18, 14, 24, 'F')
        lz.linea(19, 18, 17, 24, 'F')
        lz.rect(15, 18, 16, 19, 'I')
        lz.rect(15, 20, 16, 27, 'I')


def buzo(lz, capa):
    if capa == 'encima':
        lz.rect(9, 33, 9, 44, 'V')
        lz.rect(22, 33, 22, 44, 'V')


def piloto(lz, capa):
    if capa == 'encima':
        lz.rect(9, 29, 22, 30, 'B')
        lz.linea(12, 17, 14, 21, 'F')
        lz.linea(19, 17, 17, 21, 'F')


def personaje(clave, verde='#1f6e43', crema='#efe3c2'):
    """Cada integrante del cuerpo técnico, con una pose propia. verde y crema: colores del club."""
    if clave == 'asistente':
        lz = figura('corto', 'carpeta', extra=buzo)
        p = paleta_base(PIEL['media'], '#2a1c12', verde, verde, verde, '#f4f1e8', crema, cinturon=oscuro(verde, 0.3),
                        V=crema, D='#7a4b25', O='#f4f1e8', X='#8a8f96', Z='#c9ced6')
    elif clave == 'entrenador':
        lz = figura('gorra', 'cruzados', extra=silbato)
        p = paleta_base(PIEL['clara'], '#4a3020', '#5d6673', '#5d6673', '#2f343c', '#1c1c1c', '#3d444d',
                        Q='#22427a', V='#17305c', X='#e8e2cf', Z='#c9ced6')
    elif clave == 'entrenador2':
        lz = figura('corto', 'caidos')
        p = paleta_base(PIEL['oscura'], '#141010', '#d65a1f', '#d65a1f', '#23262e', '#f4f1e8', '#f4f1e8')
    elif clave == 'preparador':
        lz = figura('vincha', 'cronometro', piernas_tipo='short')
        p = paleta_base(PIEL['morena'], '#1e1410', crema, crema, '#1d1d22', '#f4f1e8', verde, cinturon='#1d1d22',
                        V=verde, Z='#c9ced6', O='#f4f1e8')
    elif clave == 'ojeador':
        lz = figura('sombrero', 'binoculares', faldon=True, extra=piloto)
        p = paleta_base(PIEL['rosada'], '#6b4a2b', '#b89a6a', '#b89a6a', '#3b3f47', '#4a2f1c', '#8c7148',
                        cinturon='#8c7148', Q='#5b4630', V='#46362a', X='#22252b', O='#4f8fbf', F='#8c7148')
    elif clave == 'medico':
        lz = figura('entradas', 'bolsillos', faldon=True, extra=estetoscopio)
        p = paleta_base(PIEL['clara'], '#a7a9ad', '#f2f2ec', '#f2f2ec', '#2b3a67', '#1c1c1c', '#9fc3d8',
                        cinturon='#f2f2ec', Z='#5d6673', X='#2a2a2a', U='#f2f2ec', V='#3fa65a')
    elif clave == 'representante':
        lz = figura('peinado', 'maletin', extra=traje)
        p = paleta_base(PIEL['media'], '#8d8f93', '#3a3f4a', '#3a3f4a', '#3a3f4a', '#151515', '#f4f1e8',
                        cinturon='#151515', F='#262a33', I='#8c2a3a', R='#3a2414', U='#6b4423', X='#4a2f1c',
                        Z='#d9b44a')
    else:
        raise KeyError(clave)
    return contornear(sombrear(lz, p, PLANOS))


def dos(px_atras, px_adelante, corrimiento=12):
    """Dos figuras: la de atrás, un poco más oscura y corrida a la derecha."""
    alto, ancho = len(px_adelante), len(px_adelante[0]) + corrimiento
    salida = [[None] * ancho for _ in range(alto)]
    for y in range(alto):
        for x, c in enumerate(px_atras[y]):
            if c is not None:
                salida[y][x + corrimiento] = _mezcla(c, SOMBRA, 0.2)
        for x, c in enumerate(px_adelante[y]):
            if c is not None:
                salida[y][x] = c
    return salida


def svg_personaje(clave, **colores):
    if clave == 'entrenadores':
        px = dos(personaje('entrenador2', **colores), personaje('entrenador', **colores))
    else:
        px = personaje(clave, **colores)
    return svg(px, f'pixel personaje p-{clave}')


# ------------------------------------------------------------------ Íconos de las secciones (24 x 24, con contorno 26)

def _icono(clave, verde, crema):
    lz = Lienzo(24, 24)
    if clave == 'formacion':  # pizarra táctica en su atril
        lz.linea(6, 16, 3, 23, 'N', 2)
        lz.linea(17, 16, 20, 23, 'N', 2)
        lz.rect(2, 2, 21, 16, 'N')
        lz.rect(3, 3, 20, 15, 'G')
        for x0, y0, x1, y1 in ((4, 4, 19, 4), (4, 14, 19, 14), (4, 4, 4, 14), (19, 4, 19, 14), (11, 4, 11, 14),
                               (4, 7, 6, 7), (4, 11, 6, 11), (6, 7, 6, 11), (17, 7, 19, 7), (17, 11, 19, 11), (17, 7, 17, 11)):
            lz.rect(x0, y0, x1, y1, 'L')
        lz.linea(8, 6, 10, 8, 'R')
        lz.linea(10, 6, 8, 8, 'R')
        lz.rect(14, 10, 15, 11, 'O')
        p = {'N': '#7a4b25', 'G': '#2f8a45', 'L': '#e6f2e0', 'R': '#e04a3a', 'O': '#ffd23f'}
        planos = 'LRO'
    elif clave == 'plantel':  # camiseta con los colores del club
        lz.tramos({3: [(5, 9), (14, 18)], 4: (3, 20), 5: (2, 21), 6: (1, 22), 7: (1, 22), 8: (2, 21), 9: (3, 20),
                   10: [(3, 5), (6, 17), (18, 20)]}, 'V')
        lz.rect(6, 10, 17, 21, 'V')
        lz.rect(10, 3, 13, 3, 'C')
        lz.rect(11, 4, 12, 5, 'C')
        lz.rect(11, 8, 12, 21, 'C')
        p = {'V': verde, 'C': crema}
        planos = ''
    elif clave == 'entrenamiento':  # cono con franjas
        for y in range(2, 20):
            m = 1 + (y - 2) * 0.42
            lz.rect(round(11.5 - m), y, round(11.5 + m) - 1, y, 'O')
        lz.rect(round(11.5 - 3.5), 8, round(11.5 + 3.5) - 1, 9, 'W')
        lz.rect(round(11.5 - 5.6), 13, round(11.5 + 5.6) - 1, 14, 'W')
        lz.rect(2, 20, 21, 22, 'K')
        p = {'O': '#f07a1e', 'W': '#f4f1e8', 'K': '#3a3f47'}
        planos = ''
    elif clave == 'tabla':  # copa
        lz.tramos({2: (5, 18), 3: (5, 18), **{y: (6, 17) for y in range(4, 9)}, 9: (7, 16), 10: (8, 15), 11: (9, 14)}, 'Y')
        for lado in (0, 1):
            x = 2 if lado == 0 else 19
            lz.rect(x, 3, x + 2, 3, 'Y')
            lz.rect(x if lado == 0 else x + 2, 4, x if lado == 0 else x + 2, 7, 'Y')
            lz.rect(x + (1 if lado == 0 else 0), 8, x + (2 if lado == 0 else 1), 8, 'Y')
        lz.rect(11, 12, 12, 15, 'Y')
        lz.rect(8, 16, 15, 17, 'Y')
        lz.rect(6, 18, 17, 21, 'N')
        lz.rect(9, 19, 14, 20, 'W')
        lz.rect(8, 4, 8, 7, 'w')
        p = {'Y': '#f2c230', 'N': '#6b4423', 'W': '#e8d7a8', 'w': '#fff3b0'}
        planos = 'Ww'
    elif clave == 'calendario':
        lz.rect(3, 6, 20, 21, 'W')
        lz.rect(3, 3, 20, 7, 'R')
        lz.rect(7, 1, 8, 5, 'Z')
        lz.rect(15, 1, 16, 5, 'Z')
        for f in range(3):
            for c in range(4):
                lz.rect(5 + 4 * c, 10 + 3 * f, 6 + 4 * c, 11 + 3 * f, 'R' if (f, c) == (1, 2) else 'D')
        p = {'W': '#f4f1e8', 'R': '#c8443a', 'Z': '#9aa1ab', 'D': '#8a8f96'}
        planos = 'D'
    elif clave == 'noticias':  # diario
        lz.rect(2, 4, 21, 20, 'W')
        lz.rect(4, 6, 19, 7, 'D')
        lz.rect(4, 10, 10, 15, 'F')
        for y in (10, 12, 14, 16, 18):
            lz.rect(12, y, 19, y, 'd')
        lz.rect(4, 17, 10, 17, 'd')
        lz.rect(4, 19, 10, 19, 'd')
        p = {'W': '#f4f1e8', 'D': '#3a3f47', 'F': '#7fa3c4', 'd': '#8a8f96'}
        planos = 'Dd'
    elif clave == 'fichajes':  # apretón de manos: dos antebrazos en diagonal
        lz.rect(0, 11, 5, 16, 'A')
        lz.rect(18, 11, 23, 16, 'B')
        lz.rect(6, 11, 6, 16, 'W')
        lz.rect(17, 11, 17, 16, 'W')
        lz.tramos({8: (9, 14), 9: (8, 15), **{y: (7, 16) for y in range(10, 16)}, 16: (8, 15), 17: (10, 13)}, 'S')
        for x in (10, 12, 14):
            lz.rect(x, 12, x, 15, 's')
        lz.linea(8, 10, 12, 10, 's')
        p = {'A': '#2b3a67', 'B': '#c8443a', 'S': '#e0ac78', 's': '#a8703f', 'W': '#f4f1e8'}
        planos = 'sW'
    elif clave == 'ojeadores':  # binoculares
        lz.rect(4, 3, 9, 5, 'x')
        lz.rect(14, 3, 19, 5, 'x')
        lz.rect(3, 6, 10, 19, 'X')
        lz.rect(13, 6, 20, 19, 'X')
        lz.rect(10, 9, 13, 12, 'X')
        lz.disco(6.5, 15.5, 2.6, 'O')
        lz.disco(16.5, 15.5, 2.6, 'O')
        lz.punto(5, 14, 'W')
        lz.punto(15, 14, 'W')
        p = {'X': '#3a3f47', 'x': '#22252b', 'O': '#4f8fbf', 'W': '#d6ecfa'}
        planos = 'W'
    elif clave == 'contratos':  # hoja, firma y lapicera
        lz.rect(3, 2, 16, 21, 'W')
        for y in (5, 7, 9, 11, 13):
            lz.rect(5, y, 14, y, 'D')
        lz.linea(5, 18, 7, 16, 'R')
        lz.linea(7, 16, 9, 18, 'R')
        lz.linea(9, 18, 12, 16, 'R')
        lz.linea(21, 2, 13, 16, 'Q', 2)
        lz.rect(12, 17, 13, 18, 'Z')
        p = {'W': '#f4f1e8', 'D': '#8a8f96', 'R': '#1f4e9a', 'Q': '#c8443a', 'Z': '#22252b'}
        planos = 'DRZ'
    elif clave == 'caja':  # bolsa y monedas (sin billetes reales)
        lz.disco(10, 14.5, 7.2, 'G')
        lz.rect(8, 4, 12, 7, 'G')
        lz.rect(7, 7, 13, 8, 'V')
        lz.rect(7, 2, 9, 3, 'G')
        lz.rect(11, 2, 13, 3, 'G')
        for x, y in ((9, 10), (10, 10), (11, 10), (8, 11), (9, 12), (10, 13), (11, 14), (12, 15), (11, 16),
                     (10, 16), (9, 16), (10, 9), (10, 17)):
            lz.punto(x, y, 'L')
        for y in (20, 18, 16):
            lz.rect(15, y, 22, y + 1, 'Y')
            lz.rect(15, y + 1, 22, y + 1, 'y')
        p = {'G': '#4f8a4a', 'V': '#c99512', 'L': '#d9ecc8', 'Y': '#f2c230', 'y': '#b8860b'}
        planos = 'Ly'
    elif clave == 'estadio':  # entrada inclinada, con talón troquelado y muescas
        def entrada(u, v):
            if (u < 1.2 or u > 18.8) and 3.5 < v < 6.5:
                return None
            if 4.8 < u < 5.6 and int(v) % 2 == 0:
                return 'D'
            if u < 4.8:
                return 'R'
            if 7 < u < 17 and (2.5 < v < 3.5 or 6.5 < v < 7.5):
                return 'D'
            return 'T'
        lz.girado(12, 12, 20, 10, -15, entrada)
        p = {'T': '#efe0b4', 'R': '#c8443a', 'D': '#8a6d3b'}
        planos = 'D'
    elif clave == 'dirigencia':  # sede del club con su bandera
        lz.rect(12, 0, 12, 9, 'Z')
        lz.rect(13, 1, 20, 3, 'V')
        lz.rect(13, 4, 20, 5, 'C')
        lz.tramos({8: (10, 14), 9: (7, 17), 10: (4, 20), 11: (2, 22)}, 'T')
        lz.rect(3, 12, 21, 20, 'W')
        for x in (5, 9, 15, 19):
            lz.rect(x, 13, x, 19, 'c')
        lz.rect(11, 15, 13, 20, 'D')
        lz.rect(1, 21, 23, 22, 'w')
        p = {'Z': '#9aa1ab', 'V': verde, 'C': crema, 'T': '#8c2a3a', 'W': '#efe3c2', 'c': '#b8a77a', 'D': '#6b4423',
             'w': '#8a8f96'}
        planos = 'Zc'
    else:
        raise KeyError(clave)
    return contornear(sombrear(lz, p, planos), 0.7)


SECCIONES_PX = ('formacion', 'plantel', 'entrenamiento', 'tabla', 'calendario', 'noticias', 'fichajes', 'ojeadores',
                'contratos', 'caja', 'estadio', 'dirigencia')


def svg_icono(clave, verde='#1f6e43', crema='#efe3c2'):
    return svg(_icono(clave, verde, crema), f'pixel icono-px i-{clave}')


# ------------------------------------------------------------------ Logo FOBALMANAGER

LETRAS = {
    'F': ['#####', '#....', '#....', '####.', '#....', '#....', '#....'],
    'O': ['.###.', '#...#', '#...#', '#...#', '#...#', '#...#', '.###.'],
    'B': ['####.', '#...#', '#...#', '####.', '#...#', '#...#', '####.'],
    'A': ['.###.', '#...#', '#...#', '#####', '#...#', '#...#', '#...#'],
    'L': ['#....', '#....', '#....', '#....', '#....', '#....', '#####'],
    'M': ['#...#', '##.##', '#.#.#', '#.#.#', '#...#', '#...#', '#...#'],
    'N': ['#...#', '##..#', '#.#.#', '#..##', '#...#', '#...#', '#...#'],
    'G': ['.###.', '#...#', '#....', '#.###', '#...#', '#...#', '.###.'],
    'E': ['#####', '#....', '#....', '####.', '#....', '#....', '#####'],
    'R': ['####.', '#...#', '#...#', '####.', '#.#..', '#..#.', '#...#'],
}


def svg_logo(blanco='#f4f1e8', amarillo='#f2c230'):
    """FOBAL en blanco y MANAGER en amarillo: letras de 5 x 7 en negrita (cada trazo vertical, doble), en bloques
    de 2 píxeles, con contorno y sombra. Mide 175 x 21: se muestra a escala entera (1x o 2x)."""
    bloque, espacio, margen = 2, 2, 2
    texto = 'FOBALMANAGER'
    ancho = margen * 2 + len(texto) * (6 * bloque + espacio) - espacio + 3
    alto = margen * 2 + 7 * bloque + 3
    px = [[None] * ancho for _ in range(alto)]
    cara = [[None] * ancho for _ in range(alto)]
    for i, letra in enumerate(texto):
        color = blanco if i < 5 else amarillo
        x0 = margen + i * (6 * bloque + espacio)
        for fy, fila in enumerate(LETRAS[letra]):
            negrita = [c == '#' or (fx > 0 and fila[fx - 1] == '#') for fx, c in enumerate(fila + '.')]
            for fx, lleno in enumerate(negrita):
                if not lleno:
                    continue
                for dy in range(bloque):
                    for dx in range(bloque):
                        y, x = margen + fy * bloque + dy, x0 + fx * bloque + dx
                        # Dos tonos: la mitad de arriba de la letra, más clara.
                        cara[y][x] = claro(color, 0.25) if fy < 3 else color
    # Sombra proyectada (2 píxeles abajo a la derecha) y contorno oscuro.
    for y in range(alto):
        for x in range(ancho):
            if cara[y][x] is None:
                for d in (1, 2):
                    if y - d >= 0 and x - d >= 0 and cara[y - d][x - d] is not None:
                        px[y][x] = '#0b1a12'
    for y in range(alto):
        for x in range(ancho):
            if cara[y][x] is not None:
                px[y][x] = cara[y][x]
    px = contornear(px, 0.8)
    return svg(px, 'pixel logo-px', 'Fobalmanager')
