# Canchas en SVG para la maqueta: líneas reglamentarias a escala, pintadas por cada tema con las variables
# --cancha-* de temas.css. Las ilustraciones dibujadas a mano se reemplazaron por íconos (fuente/iconos.py).

# Medidas reglamentarias a escala: 10 unidades = 1 m, cancha de 105 x 68.

def _lineas_cancha(largo, ancho, vertical):
    """Líneas de cal de una cancha de largo x ancho (en unidades), apaisada o vertical, con 20 de margen."""
    def p(x, y):  # x a lo largo de la cancha, y a lo ancho
        return (y, x) if vertical else (x, y)

    def ruta(puntos):
        return 'M' + ' L'.join(f'{a:g} {b:g}' for a, b in (p(x, y) for x, y in puntos))

    m, L, A = 20, largo, ancho
    medio_a = m + A / 2
    trazos = [ruta([(m, m), (m + L, m), (m + L, m + A), (m, m + A), (m, m)]),
              ruta([(m + L / 2, m), (m + L / 2, m + A)])]
    for lado in (0, 1):
        def x(d):
            return m + d if lado == 0 else m + L - d
        trazos.append(ruta([(x(0), medio_a - 201.5), (x(165), medio_a - 201.5), (x(165), medio_a + 201.5), (x(0), medio_a + 201.5)]))
        trazos.append(ruta([(x(0), medio_a - 91.5), (x(55), medio_a - 91.5), (x(55), medio_a + 91.5), (x(0), medio_a + 91.5)]))
        trazos.append(ruta([(x(0), medio_a - 36.6), (x(-12), medio_a - 36.6), (x(-12), medio_a + 36.6), (x(0), medio_a + 36.6)]))
        a1, a2 = p(x(165), medio_a - 73.1), p(x(165), medio_a + 73.1)
        barrido = (1 if lado == 0 else 0) ^ (1 if vertical else 0)
        trazos.append(f'M{a1[0]:g} {a1[1]:g}A91.5 91.5 0 0 {barrido} {a2[0]:g} {a2[1]:g}')
    centro = p(m + L / 2, medio_a)
    penales = [p(m + 110, medio_a), p(m + L - 110, medio_a)]
    puntos = ''.join(f'<circle class="cal-punto" cx="{cx:g}" cy="{cy:g}" r="5"/>' for cx, cy in [centro] + penales)
    return (''.join(f'<path class="cal" d="{d}"/>' for d in trazos)
            + f'<circle class="cal" cx="{centro[0]:g}" cy="{centro[1]:g}" r="91.5"/>' + puntos)


def cancha_apaisada():
    """Cancha apaisada (menú C y portada): arco propio a la izquierda, rival a la derecha."""
    franjas = ''.join(f'<rect class="franja" x="{20 + i * 105}" y="20" width="105" height="680"/>' for i in range(0, 10, 2))
    return (f'<svg class="cancha-svg" viewBox="0 0 1090 720" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<rect class="cesped" x="0" y="0" width="1090" height="720"/>{franjas}'
            f'{_lineas_cancha(1050, 680, False)}</svg>')


def cancha_vertical():
    """Cancha de la formación: el equipo propio ataca hacia arriba."""
    franjas = ''.join(f'<rect class="franja" x="20" y="{20 + i * 105}" width="680" height="105"/>' for i in range(0, 10, 2))
    return (f'<svg class="cancha-svg" viewBox="0 0 720 1090" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            f'<rect class="cesped" x="0" y="0" width="720" height="1090"/>{franjas}'
            f'{_lineas_cancha(1050, 680, True)}</svg>')
