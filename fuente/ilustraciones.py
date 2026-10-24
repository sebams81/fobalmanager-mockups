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


# Opción D: la cancha a tiza sobre el pizarrón, con marcas de táctica (X, O y flechas) en tiza amarilla.
_MARCAS_O = [(300, 130), (520, 610), (770, 175), (880, 430), (430, 470), (150, 560)]
_MARCAS_X = [(220, 330), (610, 250), (700, 520), (960, 640), (360, 615), (835, 95), (120, 140), (980, 300)]
_FLECHAS = ['M260 400 Q420 290 560 380', 'M640 150 Q780 50 905 175', 'M300 655 Q500 560 700 645',
            'M470 220 Q560 110 690 205', 'M160 250 Q230 470 330 520', 'M760 600 Q900 520 960 390']


def pizarron_tiza(vertical=False, sufijo=''):
    """Pizarrón de la opción D: líneas de cal a tiza y marcas de táctica. vertical: la cancha del celular."""
    def p(x, y):
        return (y, x) if vertical else (x, y)

    def mover(d):
        partes = d.replace('M', '').replace('Q', ' ').split()
        n = [float(v) for v in partes]
        pts = [p(n[i], n[i + 1]) for i in range(0, len(n), 2)]
        return f'M{pts[0][0]:g} {pts[0][1]:g} Q{pts[1][0]:g} {pts[1][1]:g} {pts[2][0]:g} {pts[2][1]:g}'

    marcas = ''.join(f'<circle class="tiza-o" cx="{p(x, y)[0]:g}" cy="{p(x, y)[1]:g}" r="16"/>' for x, y in _MARCAS_O)
    for x, y in _MARCAS_X:
        cx, cy = p(x, y)
        marcas += f'<path class="tiza-x" d="M{cx - 14:g} {cy - 14:g}l28 28M{cx + 14:g} {cy - 14:g}l-28 28"/>'
    marcas += ''.join(f'<path class="tiza-flecha" d="{mover(d)}" marker-end="url(#punta{sufijo})"/>' for d in _FLECHAS)
    ancho, alto = (720, 1090) if vertical else (1090, 720)
    clase = 'tiza-svg vertical' if vertical else 'tiza-svg apaisada'
    return (f'<svg class="{clase}" viewBox="0 0 {ancho} {alto}" preserveAspectRatio="xMidYMid meet" aria-hidden="true" focusable="false">'
            f'<defs><filter id="tiza{sufijo}" x="-5%" y="-5%" width="110%" height="110%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" result="ruido"/>'
            '<feDisplacementMap in="SourceGraphic" in2="ruido" scale="3" result="movido"/>'
            '<feTurbulence type="fractalNoise" baseFrequency="2.4" numOctaves="1" seed="3" result="grano"/>'
            '<feColorMatrix in="grano" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.75" result="mascara"/>'
            '<feComposite in="movido" in2="mascara" operator="in"/></filter>'
            f'<marker id="punta{sufijo}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto">'
            '<path d="M0 0L10 5 0 10" fill="none" stroke="#f2d64b" stroke-width="2"/></marker></defs>'
            f'<g filter="url(#tiza{sufijo})"><g class="tiza-lineas">{_lineas_cancha(1050, 680, vertical)}</g>'
            f'<g class="tiza-marcas">{marcas}</g></g></svg>')
