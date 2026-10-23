# Genera las seis páginas HTML de la maqueta a partir de los datos ficticios de este archivo.
# Uso: python fuente/generar.py   (desde la raíz del repo; solo biblioteca estándar).
# El relato (fuente/relato.json) usa frases tal cual de la crónica del juego, con nombres ficticios.

import html
import json
import math
import random
from pathlib import Path

from ilustraciones import ESCENA, PATRONES, cancha_apaisada, cancha_vertical, objeto

RAIZ = Path(__file__).resolve().parent.parent
e = html.escape

# ---------------------------------------------------------------- Mundo ficticio

LIGA = '2ª División'
ETAPA = 'Primera rueda'
FECHA = 12
FECHAS = 38  # ida y vuelta entre 20 clubes
# El próximo rival lo dirige otro manager: el local (nosotros) eligió el horario (RN-170, RN-745).
MANAGER_RIVAL = 'el_flaco_ojeda'
HORARIO = 'sábado 21 h'
MI_CLUB = 'TAM'
RIVAL = 'CAL'

# sigla, nombre, color 1, color 2, diseño del escudo
CLUBES = [
    ('TAM', 'Atlético Tamarisco', '#1f6e43', '#efe3c2', 'chevron'),
    ('CAL', 'Unión Calandria', '#1b1b1b', '#f2c230', 'cuartos'),
    ('FAR', 'Sportivo Faro Viejo', '#1d4e6b', '#e8d7a8', 'circulo'),
    ('MOL', 'Deportivo Molinos del Sur', '#a8452c', '#c9c9c9', 'punta'),
    ('BAR', 'Juventud Barranca Azul', '#6fb7d9', '#6b1f2f', 'mitad'),
    ('MEM', 'Social Puerto Membrillo', '#6b1f3a', '#d9a62b', 'chevron'),
    ('CEI', 'Estrella de Villa Ceibo', '#e07b28', '#1d2547', 'circulo'),
    ('LOM', 'Defensores de Loma Chata', '#2a9d8f', '#1b1b1b', 'punta'),
    ('LEC', 'Club Lechuzas del Norte', '#6b4a2b', '#f0e2c0', 'cuartos'),
    ('CRU', 'Atlético Cruce Alegre', '#5b3a8c', '#f08a24', 'mitad'),
    ('PAS', 'Unidos de Paso Hondo', '#6b7a2b', '#f2d03b', 'circulo'),
    ('PAM', 'Sporting Pampa Brava', '#4a5560', '#e8735a', 'punta'),
    ('SAU', 'Atlético Sauce Chico', '#6cc5b0', '#6b1f2f', 'cuartos'),
    ('BAH', 'Deportivo Bahía Mansa', '#2a4fa0', '#ef8a6b', 'mitad'),
    ('CLA', 'Juventud Cañada Larga', '#d9a62b', '#3a3f45', 'chevron'),
    ('PMO', 'Club Social Piedra Mora', '#9b87c4', '#1b1b1b', 'circulo'),
    ('ARR', 'Sportivo Arroyo Manso', '#e89a7a', '#1f4a35', 'punta'),
    ('MON', 'Unión Vecinal Monte Bravo', '#7a1f2b', '#d0d0d0', 'cuartos'),
    ('TRA', 'Atlético Tranvía Viejo', '#e6e04a', '#4a2c6b', 'mitad'),
    ('CEV', 'Defensores de Cerro Ventoso', '#8a8f96', '#9acd32', 'chevron'),
]
CLUB = {c[0]: c for c in CLUBES}

ESCALA = ['nulo', 'malo', 'bajo', 'insuficiente', 'aceptable', 'cumplidor', 'bueno', 'destacado', 'excelente', 'fenómeno', 'crack']
ESTADOS = ['malo', 'insuficiente', 'aceptable', 'bueno', 'excelente']  # condición, frescura, ritmo y moral fuera del partido
ATRIBUTOS = {
    'Físicos': ['Velocidad', 'Explosión', 'Resistencia', 'Fuerza', 'Potencia', 'Salto', 'Reacción'],
    'Técnicos': ['Precisión', 'Pase', 'Gambeta', 'Control', 'Cabezazo', 'Marca', 'Quite', 'Pelota parada'],
    'Mentales': ['Visión', 'Anticipo', 'Ubicación', 'Temple'],
    'Personalidad': ['Agresividad', 'Obediencia', 'Liderazgo', 'Profesionalismo'],
}
# Atributos que pesan por puesto: suben el perfil del jugador.
PICOS = {
    'ARQ': ['Reacción', 'Salto', 'Ubicación', 'Temple'],
    'LD': ['Velocidad', 'Resistencia', 'Marca', 'Quite'],
    'LI': ['Velocidad', 'Resistencia', 'Marca', 'Quite'],
    'CDD': ['Fuerza', 'Salto', 'Cabezazo', 'Marca', 'Anticipo'],
    'CDI': ['Fuerza', 'Salto', 'Cabezazo', 'Quite', 'Ubicación'],
    'VC': ['Pase', 'Quite', 'Ubicación', 'Visión', 'Resistencia'],
    'INTD': ['Pase', 'Control', 'Resistencia', 'Visión'],
    'INTI': ['Pase', 'Control', 'Visión', 'Pelota parada'],
    'ED': ['Velocidad', 'Explosión', 'Gambeta', 'Control'],
    'EI': ['Velocidad', 'Gambeta', 'Explosión', 'Precisión'],
    'SD': ['Gambeta', 'Control', 'Precisión', 'Visión'],
    'ENG': ['Visión', 'Pase', 'Control', 'Pelota parada'],
    'DC': ['Precisión', 'Cabezazo', 'Fuerza', 'Temple'],
}
NOMBRE_PUESTO = {
    'ARQ': 'arquero', 'LD': 'lateral derecho', 'LI': 'lateral izquierdo', 'CDD': 'central derecho',
    'CDI': 'central izquierdo', 'VC': 'volante central', 'INTD': 'volante interno derecho',
    'INTI': 'volante interno izquierdo', 'ED': 'extremo derecho', 'EI': 'extremo izquierdo',
    'SD': 'segundo delantero', 'ENG': 'enganche', 'DC': 'delantero centro',
}
VECINOS = {
    'ARQ': [], 'LD': ['CDD', 'ED'], 'LI': ['CDI', 'EI'], 'CDD': ['CDI', 'LD'], 'CDI': ['CDD', 'LI'],
    'VC': ['INTD', 'CDD'], 'INTD': ['VC', 'ED'], 'INTI': ['VC', 'ENG'], 'ED': ['EI', 'INTD'],
    'EI': ['ED', 'SD'], 'SD': ['DC', 'ENG'], 'ENG': ['SD', 'INTI'], 'DC': ['SD'],
}
LINEAS = [
    ('Arqueros', ['ARQ']),
    ('Defensores', ['LD', 'CDD', 'CDI', 'LI']),
    ('Volantes', ['VC', 'INTD', 'INTI', 'ENG']),
    ('Delanteros', ['ED', 'EI', 'SD', 'DC']),
]

# puesto, nombre, edad, condición, frescura, ritmo, moral, contrato, habilidades
PLANTEL = [
    ('ARQ', 'Gervasio Toledo', 31, 3, 4, 3, 3, '1 año', ['atajapenales']),
    ('ARQ', 'Mateo Grigera', 22, 3, 4, 1, 2, '2 años', []),
    ('ARQ', 'Lucio Benavídez', 18, 2, 4, 1, 3, '3 años', []),
    ('LD', 'Martín Echagüe', 27, 3, 3, 3, 3, '1 año y medio', []),
    ('LD', 'Lucas Peralta Ruiz', 20, 3, 4, 1, 1, 'medio año', []),
    ('CDD', 'Lisandro Bermúdez', 29, 4, 3, 3, 2, '2 años', []),
    ('CDD', 'Thiago Olmedo', 24, 3, 4, 2, 3, '1 año', []),
    ('CDI', 'Facundo Arrieta', 26, 3, 3, 3, 3, '2 años y medio', []),
    ('CDI', 'Nehuén Saravia', 19, 2, 4, 1, 3, '3 años', []),
    ('LI', 'Bruno Escalada', 25, 3, 2, 3, 3, '1 año', []),
    ('LI', 'Valentín Cejas', 23, 3, 4, 2, 2, '1 año y medio', []),
    ('VC', 'Hernán Aráoz', 32, 2, 3, 3, 4, 'medio año', ['pateador de penales']),
    ('VC', 'Gonzalo Quevedo', 24, 3, 4, 2, 3, '2 años', []),
    ('INTD', 'Ezequiel Iriondo', 28, 3, 3, 3, 2, '1 año', []),
    ('INTD', 'Ramón Aldao', 30, 2, 4, 1, 1, 'medio año', []),
    ('INTI', 'Santino Ferrando', 21, 4, 3, 3, 4, '3 años', []),
    ('ENG', 'Franco Valdivieso', 26, 3, 4, 2, 3, '1 año y medio', []),
    ('ED', 'Lautaro Ortúzar', 23, 4, 3, 4, 4, '2 años', []),
    ('ED', 'Dylan Pereyra Sosa', 18, 3, 4, 1, 4, '3 años', []),
    ('EI', 'Joaquín Medrano', 27, 3, 3, 3, 3, '1 año', []),
    ('EI', 'Emiliano Sosa Rivero', 22, 3, 4, 2, 3, '2 años', []),
    ('SD', 'Tomás Ibarguren', 25, 3, 4, 2, 2, '1 año', []),
    ('DC', 'Ignacio Ugarteche', 29, 3, 3, 4, 4, '1 año y medio', []),
    ('DC', 'Benicio Albarracín', 20, 3, 4, 2, 3, '2 años y medio', []),
]
ONCE = ['Gervasio Toledo', 'Martín Echagüe', 'Lisandro Bermúdez', 'Facundo Arrieta', 'Bruno Escalada',
        'Hernán Aráoz', 'Ezequiel Iriondo', 'Santino Ferrando', 'Lautaro Ortúzar', 'Joaquín Medrano',
        'Ignacio Ugarteche']
BANCO = ['Mateo Grigera', 'Thiago Olmedo', 'Valentín Cejas', 'Gonzalo Quevedo', 'Ramón Aldao',
         'Emiliano Sosa Rivero', 'Benicio Albarracín']
PIZARRA_433 = [
    ('Ataque', ['EI', 'DC', 'ED']),
    ('Medio', ['INTI', 'VC', 'INTD']),
    ('Defensa', ['LI', 'CDI', 'CDD', 'LD']),
    ('Arco', ['ARQ']),
]

INSTRUCCIONES = [
    ('actitud', 'Actitud', [('arriesgar_poco', 'Arriesgar poco'), ('jugarlo_parejo', 'Jugarlo parejo'), ('ir_al_frente', 'Ir al frente')], 'jugarlo_parejo'),
    ('donde', '¿Dónde los esperamos?', [('arriba', 'Apretarlos arriba'), ('mitad', 'En mitad de cancha'), ('atras', 'Meterse atrás')], 'mitad'),
    ('salida', '¿Cómo la sacamos?', [('abajo', 'Por abajo'), ('al5', 'Pelota al pie del 5'), ('pelotazo', 'Pelotazo')], 'al5'),
    ('ataque', '¿Por dónde atacamos?', [('afuera', 'Por afuera'), ('adentro', 'Por adentro'), ('al9', 'Buscar al 9')], 'afuera'),
]

# --------------------------------------------------------------- Tabla simulada

def simular_tabla():
    """Todos contra todos (método del círculo) con resultados al azar y semilla fija: la tabla siempre cierra."""
    rng = random.Random(1990)
    siglas = [c[0] for c in CLUBES]
    n = len(siglas)
    rueda = list(range(n))
    fechas = []
    for f in range(n - 1):
        cruces = [(rueda[i], rueda[n - 1 - i]) for i in range(n // 2)]
        fechas.append([(a, b) if f % 2 == 0 else (b, a) for a, b in cruces])
        rueda = [rueda[0]] + [rueda[-1]] + rueda[1:-1]
    fuerza = {i: 1.0 + 0.6 * (n - i) / n for i in range(n)}

    def goles(l):
        # Poisson por el método de Knuth.
        k, lim, p = 0, math.exp(-l), rng.random()
        while p > lim:
            k += 1
            p *= rng.random()
        return k

    # El índice 0 es mi club; el rival de la fecha 12 es el índice que la rueda le asigna.
    rival_idx = next(b if a == 0 else a for a, b in fechas[FECHA - 1] if 0 in (a, b))
    orden = [MI_CLUB] + [s for s in siglas if s not in (MI_CLUB, RIVAL)]
    orden.insert(rival_idx, RIVAL)
    nombre = {i: orden[i] for i in range(n)}
    fila = {s: dict(pj=0, g=0, e=0, p=0, gf=0, gc=0, ult=[]) for s in siglas}
    partidos_mios = []
    resultados = []  # por fecha jugada: (local, goles, visitante, goles)
    for f in range(FECHA - 1):
        resultados.append([])
        for a, b in fechas[f]:
            ga = goles(0.95 * fuerza[a] + 0.25)
            gb = goles(0.85 * fuerza[b])
            for yo, gy, go_ in ((a, ga, gb), (b, gb, ga)):
                r = fila[nombre[yo]]
                r['pj'] += 1
                r['gf'] += gy
                r['gc'] += go_
                res = 'G' if gy > go_ else 'E' if gy == go_ else 'P'
                r[{'G': 'g', 'E': 'e', 'P': 'p'}[res]] += 1
                r['ult'].append(res)
            resultados[-1].append((nombre[a], ga, nombre[b], gb))
            if 0 in (a, b):
                partidos_mios.append((nombre[a], ga, nombre[b], gb))
    # En la maqueta, el partido de la fecha 12 lo jugamos de local (elegimos el horario, RN-170).
    proxima = [(MI_CLUB, RIVAL) if MI_CLUB in (nombre[a], nombre[b]) else (nombre[a], nombre[b]) for a, b in fechas[FECHA - 1]]
    tabla = sorted(fila.items(), key=lambda kv: (-(3 * kv[1]['g'] + kv[1]['e']), -(kv[1]['gf'] - kv[1]['gc']), -kv[1]['gf'], kv[0]))
    return tabla, partidos_mios, resultados, proxima


TABLA, PARTIDOS_MIOS, RESULTADOS, PROXIMA = simular_tabla()
POSICION = {s: i + 1 for i, (s, _) in enumerate(TABLA)}


def zona(pos):
    if pos <= 3:
        return 'ascenso', '▲', 'Ascenso directo'
    if pos <= 11:
        return 'octogonal', '◆', 'Octogonal por el cuarto ascenso'
    if pos >= 17:
        return 'descenso', '▼', 'Descenso'
    return None, '', ''

# --------------------------------------------------------------- Jugadores

def ficha_de(j):
    puesto, nombre = j[0], j[1]
    rng = random.Random(nombre)
    atributos = {}
    for categoria, lista in ATRIBUTOS.items():
        for a in lista:
            base = rng.choice([3, 4, 4, 5, 5, 5, 6])
            if a in PICOS.get(puesto, []):
                base = rng.choice([6, 6, 7, 7, 8])
            if categoria == 'Personalidad':
                base = rng.choice([3, 4, 5, 6, 7])
            if puesto == 'ARQ' and categoria == 'Técnicos' and a not in ('Pase', 'Pelota parada'):
                base = rng.choice([1, 2, 2, 3])
            atributos[a] = ESCALA[base]
    puestos = [(puesto, 'natural')] + [(v, rng.choice(['competente', 'incómodo'])) for v in VECINOS[puesto][:2]]
    altura = rng.randint(184, 194) if puesto in ('ARQ', 'CDD', 'CDI', 'DC') else rng.randint(167, 183)
    contextura = rng.choice(['delgado', 'normal', 'normal', 'robusto'])
    pierna = 'izquierda' if puesto in ('LI', 'EI', 'INTI', 'CDI') and rng.random() < 0.7 else rng.choice(['derecha', 'derecha', 'derecha', 'izquierda'])
    return atributos, puestos, altura, contextura, pierna


JUGADOR = {j[1]: j for j in PLANTEL}


def apellido(nombre):
    partes = nombre.split(' ')
    return ' '.join(partes[1:])

# --------------------------------------------------------------- Piezas comunes

ICONOS = {
    'club': '<path d="M5 4h14v8c0 5-3.5 8-7 9-3.5-1-7-4-7-9z"/><path d="M5 9h14"/>',
    'plantel': '<path d="M8 3 3 6l2 4 2-1v12h10V9l2 1 2-4-5-3c-1 2-2.5 3-4 3S9 5 8 3z"/>',
    'previa': '<path d="M3 4h18v13H3z"/><path d="m8 21 4-4 4 4"/><path d="m6 8 2 2m0-2-2 2"/><path d="M15 9.5a1.5 1.5 0 1 0 .01 0"/><path d="M9 13c2 1 4 0 5.5-2"/>',
    'partido': '<path d="M4 9h16v11H4z"/><path d="m7 9 10-5"/><path d="M9 12a2.5 2.5 0 1 0 .01 0"/><path d="M14 13h3m-3 3h3"/>',
    'tabla': '<path d="M4 5h16M4 10h16M4 15h16M4 20h16"/><path d="M9 5v15"/>',
    'pausa': '<path d="M8 5v14M16 5v14"/>',
    'ritmo': '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    'cambio': '<path d="M4 8h13l-3-3m6 11H7l3 3"/>',
    'opinion': '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8m-8 3h5"/>',
}


def icono(nombre):
    return f'<svg class="icono" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-{nombre}"/></svg>'


def sprite():
    simbolos = ''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONOS.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{PATRONES}{simbolos}</svg>'


_escudos = [0]


def escudo(sigla, clase='escudo'):
    """Escudo inventado: forma de escudo con dos colores y un diseño geométrico simple."""
    _, nombre, c1, c2, diseno = CLUB[sigla]
    _escudos[0] += 1
    cid = f'e{_escudos[0]}'
    forma = 'M3 3h34v19c0 11-8 18-17 21C11 40 3 33 3 22z'
    figuras = {
        'chevron': f'<path d="M0 14 20 30 40 14v10L20 40 0 24z" fill="{c2}"/>',
        'cuartos': f'<path d="M20 0h20v22H20zM0 22h20v24H0z" fill="{c2}"/>',
        'circulo': f'<circle cx="20" cy="21" r="9" fill="{c2}"/>',
        'punta': f'<path d="M0 26h40v20H0z" fill="{c2}"/><path d="M20 8l3 6h-6z" fill="{c2}"/>',
        'mitad': f'<path d="M0 0h40v15H0z" fill="{c2}"/>',
    }
    return (
        f'<svg class="{clase}" viewBox="0 0 40 46" role="img" aria-label="Escudo de {e(nombre)}">'
        f'<clipPath id="{cid}"><path d="{forma}"/></clipPath>'
        f'<g clip-path="url(#{cid})"><rect width="40" height="46" fill="{c1}"/>{figuras[diseno]}</g>'
        f'<path d="{forma}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="2"/></svg>'
    )


# Fuentes alojadas en el sitio (licencia OFL, ver fuentes/LICENCIAS.md): se carga solo la del tema activo.
TEMAS = ('retro', 'diario', 'moderno', 'pizarra')
FUENTES = {tema: f'css/fuentes-{tema}.css' for tema in TEMAS}

SCRIPT_TEMA = (
    '(function(){var T=' + json.dumps(list(TEMAS)) + ',F=' + json.dumps(FUENTES) + ',t=null;'
    'try{var q=new URLSearchParams(location.search).get("tema");if(T.indexOf(q)>=0){t=q;localStorage.setItem("fm-tema",q)}'
    'else{t=localStorage.getItem("fm-tema")}}catch(x){}'
    'if(T.indexOf(t)<0){t=T[Math.floor(Math.random()*T.length)];try{localStorage.setItem("fm-tema",t)}catch(x){}}'
    'document.documentElement.dataset.tema=t;var c={};'
    'window.fmFuentes=function(k){if(c[k])return;c[k]=1;var l=document.createElement("link");l.rel="stylesheet";l.href=F[k];document.head.appendChild(l)};'
    'window.fmFuentes(t)})();'
)

PANTALLAS = [
    ('club', 'club.html', 'Club', 'Inicio del club'),
    ('plantel', 'plantel.html', 'Plantel', 'Plantel'),
    ('previa', 'previa.html', 'Previa', 'Previa y táctica'),
    ('partido', 'partido.html', 'Partido', 'Partido en vivo'),
    ('tabla', 'tabla.html', 'Tabla', 'Tabla de posiciones'),
]

DESCRIPCIONES = {
    'club': 'Lo que pasa en el club esta semana: dirigencia, prensa, vestuario y la próxima fecha.',
    'plantel': 'Tus jugadores: quién está para jugar, quién viene falto de fútbol y quién va al banco.',
    'previa': 'Formación, indicaciones y pateadores, antes de que ruede la pelota.',
    'partido': 'El relato minuto a minuto. Los cambios entran cuando se corta el juego.',
    'tabla': 'Quién sube, quién entra al octogonal y quién ya mira para abajo.',
}


def selector_tema():
    opciones = ''.join(
        f'<label><input type="radio" name="tema" value="{v}">{t}</label>'
        for v, t in (('retro', 'Retro'), ('diario', 'Diario'), ('moderno', 'Moderno'), ('pizarra', 'Pizarra'))
    )
    return f'<fieldset class="selector-tema"><legend>Estilo visual</legend>{opciones}</fieldset>'


def barra_maqueta(portada):
    volver = '<span>Fobalmanager</span>' if portada else '<a href="index.html">← Portada</a>'
    return (
        '<div class="barra-maqueta">'
        f'<p class="aviso">{volver}<strong>Maqueta: diseño ilustrativo, sin funciones</strong></p>'
        f'{selector_tema()}</div>'
    )


def encabezado_club():
    _, nombre, c1, c2, _ = CLUB[MI_CLUB]
    return (
        f'<header class="club" style="--club-1:{c1};--club-2:{c2}">{escudo(MI_CLUB)}'
        f'<div><p class="nombre">{e(nombre)}</p>'
        f'<p class="contexto">{LIGA} · {ETAPA} · Fecha {FECHA} de {FECHAS} · {POSICION[MI_CLUB]}°</p></div>'
        '<a class="marca" href="index.html">Fobalmanager</a></header>'
    )


def navegacion(activa):
    actual = ' aria-current="page"'
    items = ''.join(
        f'<li><a href="{archivo}"{actual if clave == activa else ""}>{icono(clave)}<span>{corto}</span></a></li>'
        for clave, archivo, corto, _ in PANTALLAS
    )
    return f'<nav class="pantallas" aria-label="Pantallas de la maqueta"><ul>{items}</ul></nav>'


def pie(extra=''):
    return (
        '<footer class="pie">'
        '<span>Todo es ficticio: clubes, jugadores, dirigentes, medios, estadios y resultados.</span>'
        f'{extra}<a href="#" data-opinion>Dar mi opinión</a>'
        '</footer>'
    )


def pagina(archivo, titulo, cuerpo, activa=None, clase_body='', antes_de_main='', menu=None):
    """activa: pantalla resaltada en la navegación; None es la portada. menu: 'a' o 'b' en las páginas de menú."""
    portada = activa is None and menu is None
    if menu:
        # El menú ya es la navegación: no lleva la barra de pantallas.
        cabecera = encabezado_club()
    else:
        cabecera = '' if portada else encabezado_club() + navegacion(activa)
    otra = {'b': ('menu-c.html', 'Ver la opción C: La pizarra'), 'c': ('menu-b.html', 'Ver la opción B: La oficina del técnico')}
    extra_pie = f'<a href="{otra[menu][0]}">{otra[menu][1]} →</a>' if menu in otra else ''
    doc = f'''<!doctype html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titulo)} · Fobalmanager (maqueta)</title>
<meta name="description" content="Maqueta visual de Fobalmanager, un manager de fútbol en el navegador. Diseño ilustrativo, sin funciones.">
<script>{SCRIPT_TEMA}</script>
<link rel="stylesheet" href="css/temas.css">
<link rel="stylesheet" href="css/base.css">
</head>
<body class="{clase_body}" style="--club-1:{CLUB[MI_CLUB][2]};--club-2:{CLUB[MI_CLUB][3]}">
{sprite()}
{barra_maqueta(portada)}
{cabecera}
{antes_de_main}
<main id="contenido">
{cuerpo}
</main>
{pie(extra_pie)}
<div class="aviso-maqueta" id="estado-maqueta" role="status" aria-live="polite"></div>
<script src="js/maqueta.js" defer></script>
</body>
</html>
'''
    (RAIZ / archivo).write_text(doc, encoding='utf-8', newline='\n')


def seccion(titulo, cuerpo, volanta='', clase='', etiqueta='section', ident=''):
    v = f'<span class="volanta">{e(volanta)}</span>' if volanta else ''
    i = f' id="{ident}"' if ident else ''
    return f'<{etiqueta} class="seccion {clase}"{i}><header>{v}<h2>{e(titulo)}</h2></header>{cuerpo}</{etiqueta}>'


def club_con_escudo(sigla, corto=False):
    nombre = CLUB[sigla][1]
    return f'<span class="club-celda">{escudo(sigla, "escudo-chico")}<span>{e(nombre)}</span></span>'

# --------------------------------------------------------------- Portada


def portada():
    tarjetas = ''.join(
        f'<li class="seccion"><a href="{archivo}">{icono(clave)}<div><h3>{e(largo)}</h3><p>{e(DESCRIPCIONES[clave])}</p></div></a></li>'
        for clave, archivo, _, largo in PANTALLAS
    )
    menus = ''.join(
        f'<li class="seccion"><a href="{archivo}"><span class="muestra-menu">{dibujo}</span>'
        f'<div><span class="volanta">{volanta}</span><h3>{e(titulo)}</h3><p>{e(texto)}</p></div></a></li>'
        for archivo, dibujo, volanta, titulo, texto in (
            ('menu-b.html', objeto('pizarron'), 'Opción B', 'La oficina del técnico',
             'Cada sección es un objeto de tu oficina: el pizarrón, el teléfono, el diario, la agenda, la carpeta del plantel…'),
            ('menu-c.html', cancha_apaisada(), 'Opción C', 'La pizarra',
             'La cancha a tiza: el próximo partido arriba y cada sección es una ficha parada en su línea, como un equipo.'),
        )
    )
    comparar = f'''<section class="comparar-menus" aria-labelledby="t-menus">
<h2 id="t-menus">El menú principal: propuestas en evaluación</h2>
<p class="suave">Todavía no elegimos. Mirá las propuestas y contanos con cuál te quedarías.</p>
<ul class="tarjetas-menu" role="list">{menus}</ul></section>'''
    opinion = (
        '<div class="opinion">'
        '<p>Probá los cuatro estilos y decinos cuál te gusta y qué le falta. En el fútbol todos opinan; acá te lo pedimos.</p>'
        f'<a class="boton principal" href="#" data-opinion>{icono("opinion")}Dar mi opinión</a>'
        '<span class="pendiente" data-opinion-pendiente>[Link del formulario pendiente: se completa en js/maqueta.js]</span>'
        '</div>'
    )
    cuerpo = f'''
<h1 class="wordmark">Fobalmanager</h1>
<p class="bajada">Fobalmanager es un manager de fútbol que se juega en el navegador: armás el plantel, das las indicaciones y seguís el partido relatado minuto a minuto, como por la radio.</p>
<p class="bajada">Un juego de largo aliento en un fútbol inventado. Si jugaste a PC Fútbol o a Hattrick, te va a resultar familiar.</p>
{opinion}
{comparar}
<h2 class="titulo-pantallas">Las pantallas</h2>
<ul class="tarjetas-pantalla" role="list">{tarjetas}</ul>
{opinion}
<p class="aclaracion">PC Fútbol y Hattrick son marcas de sus respectivos titulares. Fobalmanager es un proyecto independiente, sin relación, patrocinio ni aval de ellos; se nombran solo como referencia.</p>
'''
    pagina('index.html', 'Portada', cuerpo, clase_body='portada')

# --------------------------------------------------------------- Inicio del club


def mini_tabla():
    pos = POSICION[MI_CLUB]
    desde = max(0, min(pos - 3, len(TABLA) - 5))
    filas = ''
    for i, (s, r) in enumerate(TABLA[desde:desde + 5], start=desde + 1):
        mio = ' class="mio"' if s == MI_CLUB else ''
        filas += f'<tr{mio}><td class="n">{i}</td><td>{club_con_escudo(s)}</td><td class="n">{r["pj"]}</td><td class="n"><b>{3 * r["g"] + r["e"]}</b></td></tr>'
    return (
        '<table class="mini-tabla"><thead><tr><th class="n" scope="col"><abbr title="Posición">#</abbr></th>'
        '<th scope="col">Club</th><th class="n" scope="col"><abbr title="Partidos jugados">PJ</abbr></th>'
        f'<th class="n" scope="col"><abbr title="Puntos">Pts</abbr></th></tr></thead><tbody>{filas}</tbody></table>'
        '<p><a href="tabla.html">Ver la tabla completa</a></p>'
    )


def racha(ultimos):
    texto = {'G': 'ganado', 'E': 'empatado', 'P': 'perdido'}
    items = ''.join(f'<li class="{r}"><span aria-hidden="true">{r}</span><span class="sr">{texto[r]}</span></li>' for r in ultimos)
    return f'<ol class="racha" aria-label="Últimos cinco partidos, del más viejo al más reciente">{items}</ol>'


def pantalla_club():
    l, gl, v, gv = PARTIDOS_MIOS[-1]
    ultimo = f'Fecha {FECHA - 1}: {CLUB[l][1]} {gl}, {CLUB[v][1]} {gv}.'
    proximo = seccion(
        'Próximo partido',
        f'''<div class="duelo"><span class="equipo">{escudo(MI_CLUB)}{e(CLUB[MI_CLUB][1])}</span><span class="vs">vs</span>
<span class="equipo">{escudo(RIVAL)}{e(CLUB[RIVAL][1])}</span></div>
<ul class="datos"><li><b>Se juega el {HORARIO}</b>, de local en el Estadio del Bajo</li><li>Manager rival: {e(MANAGER_RIVAL)} · {LIGA}, fecha {FECHA}</li>
<li class="suave">Último partido: {e(ultimo)}</li></ul>
<a class="boton principal ancho" href="previa.html">Preparar el partido</a>''',
        volanta=f'Fecha {FECHA}', clase='destacada proximo',
    )
    novedades = seccion(
        'Novedades',
        '''<ul class="novedades">
<li><span class="volanta">Dirigencia</span><p>La comisión directiva pide prudencia con los gastos y entrar al octogonal. «En ese orden», aclaró el tesorero.</p></li>
<li><span class="volanta">Prensa</span><p>«En Calandria hay prima por ganarnos», asegura El Eco de Tamarisco. No dice quién la paga.</p></li>
<li><span class="volanta">Vestuario</span><p>Ugarteche pidió patear los penales. Aráoz, el pateador designado, no dijo nada: se quedó media hora más practicando.</p></li>
</ul>''',
        volanta='Esta semana', ident='novedades',
    )
    dirigencia = seccion(
        'Lo que pide la dirigencia',
        '''<dl class="objetivos"><dt>Objetivo principal</dt><dd>Terminar 11° o mejor: como mínimo, jugar el octogonal</dd>
<dt>Objetivo secundario</dt><dd>Bajar el promedio de edad del plantel</dd></dl>''',
        volanta='Temporada', ident='dirigencia',
    )
    tabla = seccion('Así estamos', mini_tabla(), volanta=LIGA)
    forma = seccion(
        'Últimos cinco',
        racha(dict(TABLA)[MI_CLUB]['ult'][-5:]) + '<p class="suave" style="margin-top:.75rem">Reputación del manager: <b>conocido</b> en el país.</p>',
        volanta='Racha',
    )
    cuerpo = f'''<h1 class="titulo-pantalla">Inicio del club</h1>
{proximo}
<div class="grilla"><div>{novedades}{dirigencia}</div><div>{tabla}{forma}</div></div>'''
    pagina('club.html', 'Inicio del club', cuerpo, 'club', 'club-pantalla')

# --------------------------------------------------------------- Plantel

# Dorsales con la numeración clásica (1 arquero, 5 volante central, 9 centrodelantero, 10 enganche).
DORSALES = {
    'Gervasio Toledo': 1, 'Mateo Grigera': 12, 'Lucio Benavídez': 25, 'Martín Echagüe': 4, 'Lucas Peralta Ruiz': 14,
    'Lisandro Bermúdez': 2, 'Thiago Olmedo': 13, 'Facundo Arrieta': 6, 'Nehuén Saravia': 22, 'Bruno Escalada': 3,
    'Valentín Cejas': 15, 'Hernán Aráoz': 5, 'Gonzalo Quevedo': 16, 'Ezequiel Iriondo': 8, 'Ramón Aldao': 18,
    'Santino Ferrando': 20, 'Franco Valdivieso': 10, 'Lautaro Ortúzar': 7, 'Dylan Pereyra Sosa': 27,
    'Joaquín Medrano': 11, 'Emiliano Sosa Rivero': 17, 'Tomás Ibarguren': 19, 'Ignacio Ugarteche': 9,
    'Benicio Albarracín': 21,
}
EXTRANJEROS = {'Joaquín Medrano', 'Franco Valdivieso', 'Gonzalo Quevedo'}  # cuentan para el cupo (RN-370)
LESIONADOS = {'Nehuén Saravia': 'lesionado, 2 fechas'}


def estado_celda(n, clase=''):
    palabra = ESTADOS[n]
    b = ' bajo' if n <= 1 else ''
    return f'<td class="{clase}{b}">{palabra}</td>'


def sin_tildes(texto):
    return texto.translate(str.maketrans('áéíóú', 'aeiou'))


def nivel(palabra):
    """Modo por defecto de los atributos (RN-744): la palabra con una barra de nivel, que dice lo mismo."""
    return (f'<span class="nivel" style="--n:{ESCALA.index(palabra)}"><span>{palabra}</span>'
            f'<span class="barra" aria-hidden="true"></span></span>')


def jugadores_por_linea():
    for titulo, puestos in LINEAS:
        yield titulo, [j for j in PLANTEL if j[0] in puestos]


def celda_jugador(j, con_ficha):
    puesto, nombre, edad = j[0], j[1], j[2]
    chips = ''.join(f'<span class="chip habilidad">{e(h)}</span> ' for h in j[8])
    if nombre in EXTRANJEROS:
        chips += '<span class="chip"><abbr title="extranjero: cuenta para el cupo">EXT</abbr></span> '
    if nombre in LESIONADOS:
        chips += f'<span class="chip lesion">{e(LESIONADOS[nombre])}</span> '
    if con_ficha:
        ident = 'f-' + ''.join(c for c in nombre.lower() if c.isalnum())
        nom = f'<button class="jugador-nombre" data-ficha aria-expanded="false" aria-controls="{ident}">{e(nombre)}</button>'
    else:
        nom = f'<span class="jugador-fijo">{e(nombre)}</span>'
    return (f'<span class="fila-nombre"><span class="dorsal" title="dorsal">{DORSALES[nombre]}</span>{nom}</span>'
            f'<span class="edad-mobile"><abbr title="{NOMBRE_PUESTO[puesto]}">{puesto}</abbr> · {edad} años</span>'
            f'{"<br>" + chips if chips else ""}')


def tabla_estado():
    filas = ''
    for titulo, jugadores in jugadores_por_linea():
        filas += f'<tbody><tr class="grupo"><th colspan="8" scope="colgroup">{titulo}</th></tr>'
        for j in jugadores:
            puesto, nombre, edad, cond, fres, ritmo, moral, contrato, habs = j
            ident = 'f-' + ''.join(c for c in nombre.lower() if c.isalnum())
            atributos, aptitudes, altura, contextura, pierna = ficha_de(j)
            filas += (
                f'<tr><td class="col-pc"><abbr class="sigla" title="{NOMBRE_PUESTO[puesto]}">{puesto}</abbr></td>'
                f'<td>{celda_jugador(j, True)}</td>'
                f'<td class="n col-pc">{edad}</td>'
                f'{estado_celda(cond, "col-pc")}{estado_celda(fres)}{estado_celda(ritmo, "col-pc")}{estado_celda(moral)}'
                f'<td class="col-pc">{contrato}</td></tr>'
            )
            bloques = ''
            for categoria, lista in ATRIBUTOS.items():
                filas_attr = ''.join(f'<dt>{a}</dt><dd>{nivel(atributos[a])}</dd>' for a in lista)
                bloques += f'<div><h3>{categoria}</h3><dl>{filas_attr}</dl></div>'
            aptitud = ''.join(f'<dt>{NOMBRE_PUESTO[p].capitalize()}</dt><dd>{b}</dd>' for p, b in aptitudes)
            estados = ''.join(
                f'<dt>{k}</dt><dd>{ESTADOS[v]}</dd>'
                for k, v in (('Condición', cond), ('Frescura', fres), ('Ritmo', ritmo), ('Moral', moral))
            )
            filas += (
                f'<tr class="ficha" id="{ident}" hidden><td colspan="8"><div class="ficha-cuerpo">'
                f'<div><h3>Cómo está</h3><dl class="datos-ficha">{estados}</dl></div>'
                f'<div><h3>Puestos</h3><dl class="datos-ficha">{aptitud}</dl></div>'
                f'<div class="atributos-bloque"><h3>Atributos</h3><div class="atributos">{bloques}</div></div>'
                f'<div><h3>Físico y contrato</h3><dl class="datos-ficha"><dt>Altura</dt><dd>{altura} cm</dd>'
                f'<dt>Contextura</dt><dd>{contextura}</dd><dt>Pierna hábil</dt><dd>{pierna}</dd>'
                f'<dt>Contrato</dt><dd>{contrato}</dd></dl></div>'
                '</div></td></tr>'
            )
        filas += '</tbody>'
    return f'''<table class="plantel">
<caption class="sr">Plantel de {e(CLUB[MI_CLUB][1])}: cómo está cada jugador</caption>
<thead><tr><th class="col-pc" scope="col"><abbr title="Puesto">Pto</abbr></th><th scope="col">Jugador</th>
<th class="n col-pc" scope="col">Edad</th><th class="col-pc" scope="col">Condición</th><th scope="col">Frescura</th>
<th class="col-pc" scope="col">Ritmo</th><th scope="col">Moral</th><th class="col-pc" scope="col">Contrato</th></tr></thead>
{filas}
</table>'''


def tabla_atributos(categoria, lista):
    cols = len(lista) + 2
    filas = ''
    for titulo, jugadores in jugadores_por_linea():
        filas += f'<tbody><tr class="grupo"><th colspan="{cols}" scope="colgroup">{titulo}</th></tr>'
        for j in jugadores:
            atributos = ficha_de(j)[0]
            celdas = ''.join(f'<td>{nivel(atributos[a])}</td>' for a in lista)
            filas += (f'<tr><td class="col-pc"><abbr class="sigla" title="{NOMBRE_PUESTO[j[0]]}">{j[0]}</abbr></td>'
                      f'<th class="jugador-col" scope="row">{celda_jugador(j, False)}</th>{celdas}</tr>')
        filas += '</tbody>'
    cabeza = ''.join(f'<th scope="col">{a}</th>' for a in lista)
    return f'''<div class="region-tabla" role="region" aria-label="Atributos {categoria.lower()}, se desplaza hacia el costado" tabindex="0">
<table class="plantel atributos-tabla"><caption class="sr">Atributos {categoria.lower()} del plantel</caption>
<thead><tr><th class="col-pc" scope="col"><abbr title="Puesto">Pto</abbr></th><th class="jugador-col" scope="col">Jugador</th>{cabeza}</tr></thead>
{filas}</table></div>'''


def pantalla_plantel():
    pestanas = [('estado', 'Estado', tabla_estado())] + [
        (sin_tildes(c.lower()), c, tabla_atributos(c, lista)) for c, lista in ATRIBUTOS.items()
    ]
    sin_foco = ' tabindex="-1"'
    botones = ''.join(
        f'<button role="tab" id="tp-{k}" aria-controls="pp-{k}" aria-selected="{"true" if i == 0 else "false"}"'
        f'{"" if i == 0 else sin_foco}>{t}</button>'
        for i, (k, t, _) in enumerate(pestanas)
    )
    paneles = ''.join(
        f'<div class="panel-plantel" role="tabpanel" id="pp-{k}" aria-labelledby="tp-{k}"{"" if i == 0 else " hidden"}>{contenido}</div>'
        for i, (k, _, contenido) in enumerate(pestanas)
    )
    modos = ''.join(f'<option{" selected" if i == 0 else ""}>{m}</option>' for i, m in enumerate(
        ('Palabra y barra (por defecto)', 'Solo palabra', 'Palabra y número', 'Solo número')))
    cuerpo = f'''<h1 class="titulo-pantalla">Plantel</h1>
<section class="seccion">
<p class="suave">{len(PLANTEL)} jugadores. Los estados van en palabras: malo, insuficiente, aceptable, bueno o excelente. Tocá el nombre de un jugador para ver su ficha.</p>
<div class="fila-select modo-atributos"><label for="modo-atributos">Cómo ver los atributos</label><select id="modo-atributos">{modos}</select></div>
<div class="pestanas-plantel" role="tablist" aria-label="Qué mirar del plantel" data-pestanas>{botones}</div>
{paneles}
</section>'''
    pagina('plantel.html', 'Plantel', cuerpo, 'plantel')


# --------------------------------------------------------------- Previa


def grupo_opciones(nombre, titulo, opciones, elegida, prefijo=''):
    items = ''.join(
        f'<label class="opcion"><input type="radio" name="{prefijo}{nombre}" value="{v}"{" checked" if v == elegida else ""}><span>{e(t)}</span></label>'
        for v, t in opciones
    )
    return f'<fieldset class="opciones"><legend>{e(titulo)}</legend><div class="lista">{items}</div></fieldset>'


def instrucciones(prefijo=''):
    return ''.join(grupo_opciones(n, t, o, el, prefijo) for n, t, o, el in INSTRUCCIONES)


def plan(prefijo=''):
    def select(id_, etiqueta, opciones, elegida):
        ops = ''.join(f'<option{" selected" if o == elegida else ""}>{e(o)}</option>' for o in opciones)
        return f'<div class="fila-select"><label for="{prefijo}{id_}">{e(etiqueta)}</label><select id="{prefijo}{id_}">{ops}</select></div>'

    actitudes = ['que lo decida el asistente', 'Arriesgar poco', 'Jugarlo parejo', 'Ir al frente']
    return f'''<details class="plan seccion">
<summary><span><span class="volanta">Por si acaso</span><h2>Plan de partido</h2><span class="resumen-plan">Si se cansan: cambiar al que esté muy cansado · Preferidos: 2 de 3</span></span></summary>
<div class="grilla" style="gap:.75rem">
{select('ganando', 'Si vamos ganando', actitudes, 'Arriesgar poco')}
{select('perdiendo', 'Si vamos perdiendo', actitudes, 'Ir al frente')}
{select('cansancio', 'Si se cansan, cambiar al que esté…', ['cansado', 'muy cansado', 'fundido', 'que lo decida el asistente'], 'muy cansado')}
{select('pref-def', 'Si sale un defensor, entra…', ['que lo decida el asistente', 'Thiago Olmedo', 'Valentín Cejas'], 'Thiago Olmedo')}
{select('pref-med', 'Si sale un volante, entra…', ['que lo decida el asistente', 'Gonzalo Quevedo', 'Ramón Aldao'], 'Gonzalo Quevedo')}
{select('pref-del', 'Si sale un delantero, entra…', ['que lo decida el asistente', 'Emiliano Sosa Rivero', 'Benicio Albarracín'], 'que lo decida el asistente')}
</div></details>'''


# Pelota parada (RN-743): el manager designa penales, tiros libres, córners y capitán.
PELOTA_PARADA = [
    ('penales', 'Penales', 'Hernán Aráoz'),
    ('tiros-libres', 'Tiros libres', 'Santino Ferrando'),
    ('corners', 'Córners', 'Santino Ferrando'),
    ('capitan', 'Capitán', 'Gervasio Toledo'),
]


def pantalla_previa():
    r = dict(TABLA)[RIVAL]
    contra = seccion(
        'Contra quién',
        f'''<div class="rival-previa">{escudo(RIVAL)}
<div><b>{e(CLUB[RIVAL][1])}</b><br><span class="suave">Manager: {e(MANAGER_RIVAL)} · {POSICION[RIVAL]}° en la tabla · {3 * r["g"] + r["e"]} puntos</span></div></div>
<p class="suave" style="margin:0 0 .35rem">Sus últimos cinco:</p>{racha(r["ult"][-5:])}''',
        volanta=f'Fecha {FECHA} · se juega el {HORARIO}',
    )
    formacion = grupo_opciones('formacion', 'Formación', [('442', '4-4-2 (doble 5)'), ('433', '4-3-3'), ('352', '3-5-2')], '433')
    once_por_puesto = {JUGADOR[n][0]: n for n in ONCE}
    lineas = ''
    for nombre_linea, puestos in PIZARRA_433:
        fichas = ''
        for p in puestos:
            n = once_por_puesto[p]
            fichas += f'<li class="ficha-pizarra"><span class="sigla">{p}</span><b>{e(apellido(n))}</b><span class="frescura">{ESTADOS[JUGADOR[n][4]]}</span></li>'
        lineas += f'<div class="linea-pizarra"><span class="sr">{nombre_linea}</span><ul>{fichas}</ul></div>'
    once = seccion(
        'La formación',
        f'''{formacion}<div class="cancha-formacion">{cancha_vertical()}
<div class="pizarra" role="group" aria-label="Once titular por líneas, del ataque al arco, con la frescura de cada uno">{lineas}</div></div>
<p class="suave nota-cancha">Para cambiar a alguien, tocá al titular y después al suplente.</p>''',
        volanta='Pizarra', clase='seccion-formacion',
    )
    banco_items = ''.join(
        f'<li><span class="sigla">{JUGADOR[n][0]}</span><span>{e(n)}</span><span class="suave">{ESTADOS[JUGADOR[n][4]]}</span></li>'
        for n in BANCO
    )
    banco = seccion('El banco', f'<ul class="banco">{banco_items}</ul>', volanta='Suplentes', clase='seccion-banco')
    indicaciones = seccion('Lo que les decís antes de salir', instrucciones(), volanta='Indicaciones')
    selects = ''
    for clave, etiqueta, elegido in PELOTA_PARADA:
        opciones = ['que lo decida el asistente'] + ONCE
        ops = ''.join(f'<option{" selected" if n == elegido else ""}>{e(n)}</option>' for n in opciones)
        selects += f'<div class="fila-select"><label for="pp-{clave}">{etiqueta}</label><select id="pp-{clave}">{ops}</select></div>'
    pelota = seccion('Pelota parada', f'<div class="pelota-parada">{selects}</div>', volanta='Los que patean', clase='seccion-pelota')
    cuerpo = f'''<h1 class="titulo-pantalla">Previa y táctica</h1>
{contra}
<div class="previa-cancha">{once}{banco}</div>
{pelota}
<div class="grilla"><div>{indicaciones}</div>
<div>{plan()}
<div class="a-la-cancha"><a class="boton principal ancho" href="#" data-maqueta>Listo, nos vemos el {HORARIO}</a>
<p class="suave"><a href="partido.html">Ver cómo se sigue un partido en vivo →</a></p></div></div></div>'''
    pagina('previa.html', 'Previa y táctica', cuerpo, 'previa', 'previa-pantalla')

# --------------------------------------------------------------- Partido en vivo

ETIQUETAS = {'gol': ('GOL', 'gol'), 'tarjeta': ('AMARILLA', 'amarilla'), 'cambio': ('CAMBIO', '')}

EN_CANCHA = [
    ('ARQ', 'Gervasio Toledo', 'entero', ''),
    ('LD', 'Martín Echagüe', 'cansado', ''),
    ('CDD', 'Lisandro Bermúdez', 'cansado', 'amarilla'),
    ('CDI', 'Facundo Arrieta', 'entero', ''),
    ('LI', 'Bruno Escalada', 'muy cansado', ''),
    ('VC', 'Gonzalo Quevedo', 'fresco', ''),
    ('INTD', 'Ezequiel Iriondo', 'cansado', ''),
    ('INTI', 'Santino Ferrando', 'entero', ''),
    ('ED', 'Lautaro Ortúzar', 'cansado', ''),
    ('EI', 'Joaquín Medrano', 'muy cansado', ''),
    ('DC', 'Ignacio Ugarteche', 'muy cansado', 'sale'),
]


def pantalla_partido():
    relato = json.loads((RAIZ / 'fuente' / 'relato.json').read_text(encoding='utf-8'))
    items = ''
    for l in relato:
        clase = l['clase']
        etq = ''
        if 'Gol' in l['texto'] or '¡Gol' in l['texto'] or 'GOL' in l['texto'] or '¡gol' in l['texto']:
            clase = 'gol'
        if clase in ETIQUETAS:
            t, c = ETIQUETAS[clase]
            etq = f'<span class="etiqueta {c}">{t}</span>'
        items += f'<li class="{clase}"><span class="min">{l["minuto"]}\'</span><p>{etq}{e(l["texto"])}</p></li>'

    cancha = ''
    for p, n, fres, extra in EN_CANCHA:
        tarjeta = '<span class="tarjeta-mini" role="img" aria-label="amarilla"></span>' if extra == 'amarilla' else ''
        espera = '<span class="esperando">Esperando interrupción: entra Benicio Albarracín</span>' if extra == 'sale' else ''
        cancha += f'<li><span class="sigla">{p}</span><span>{e(n)}{tarjeta}{espera}</span><span class="estado">{fres}</span></li>'
    banco = ''.join(
        f'<li><span class="sigla">{JUGADOR[n][0]}</span><span>{e(n)}</span>'
        f'<a class="boton chico" href="#" data-maqueta aria-disabled="true">{"Calentando" if n == "Benicio Albarracín" else "Que entre"}</a></li>'
        for n in BANCO if n != 'Gonzalo Quevedo'
    )
    equipo = f'''<div class="contadores"><span>Cambios: te quedan <b>4 de 5</b></span><span>Oportunidades: te quedan <b>2 de 3</b></span></div>
<h3>En la cancha</h3><ul class="lista-jugadores">{cancha}</ul>
<h3 style="margin-top:1rem">En el banco</h3><ul class="lista-jugadores">{banco}</ul>
<h3 style="margin-top:1rem">Ya salieron</h3><ul class="lista-jugadores"><li><span class="sigla">VC</span><span>Hernán Aráoz</span><span class="estado suave">reemplazado</span></li></ul>'''
    tactica = instrucciones('vivo-') + '<p class="suave">Lo que cambies rige desde la próxima jugada.</p>' + plan('vivo-')
    pl, pv = CLUB[MI_CLUB][1], CLUB[RIVAL][1]
    marcador = f'''<div class="marcador">
<div class="fila"><div class="resultado" aria-label="{e(pl)} 2, {e(pv)} 1, minuto 87">
<span aria-hidden="true">{escudo(MI_CLUB, "escudo-chico")} {MI_CLUB}</span><span class="goles" aria-hidden="true">2 - 1</span><span aria-hidden="true">{RIVAL} {escudo(RIVAL, "escudo-chico")}</span></div>
<span class="minuto" aria-hidden="true">87'</span>
<div class="controles"><a class="boton chico" href="#" data-maqueta aria-disabled="true">{icono("pausa")}<span class="sr">Pausa</span></a>
<a class="boton chico" href="#" data-maqueta aria-disabled="true">{icono("ritmo")}normal</a></div></div>
<p class="calentando">Calentando: Albarracín por Ugarteche. Entra cuando se pare la pelota.</p></div>'''
    pestanas = '''<div class="pestanas" role="tablist" aria-label="Partido">
<button role="tab" id="t-relato" aria-controls="p-relato" aria-selected="true">Relato</button>
<button role="tab" id="t-equipo" aria-controls="p-equipo" aria-selected="false" tabindex="-1">Equipo</button>
<button role="tab" id="t-tactica" aria-controls="p-tactica" aria-selected="false" tabindex="-1">Táctica</button></div>'''
    cuerpo = f'''<h1 class="sr">Partido en vivo</h1>
<div class="vivo">
<section class="seccion panel panel-relato" id="p-relato" role="tabpanel" aria-labelledby="t-relato"><header><span class="volanta">{LIGA} · Fecha {FECHA} · Estadio del Bajo</span><h2>Relato</h2></header>
<ol class="relato" role="log" aria-label="Relato del partido">{items}</ol></section>
<section class="seccion panel" id="p-equipo" role="tabpanel" aria-labelledby="t-equipo" hidden><header><span class="volanta">{e(pl)}</span><h2>Equipo</h2></header>{equipo}</section>
<section class="seccion panel" id="p-tactica" role="tabpanel" aria-labelledby="t-tactica" hidden><header><span class="volanta">Indicaciones</span><h2>Táctica</h2></header>{tactica}</section>
</div>
{pestanas}'''
    pagina('partido.html', 'Partido en vivo', cuerpo, 'partido', 'en-partido', antes_de_main=marcador)

# --------------------------------------------------------------- Tabla


ZONAS = [  # franjas de la tabla: desde, hasta, clave, símbolo, texto
    (1, 3, 'ascenso', '▲', 'Ascenso directo'),
    (4, 11, 'octogonal', '◆', 'Octogonal por el cuarto ascenso'),
    (12, 16, 'media', '', 'Mitad de tabla'),
    (17, 20, 'descenso', '▼', 'Descenso'),
]
COLUMNAS_TABLA = 11


def fichas_racha(ultimos):
    """Racha en fichas circulares G/E/P; la última, la más reciente, va marcada."""
    texto = {'G': 'ganado', 'E': 'empatado', 'P': 'perdido'}
    fichas = ''.join(
        f'<span class="{x}{" reciente" if i == len(ultimos) - 1 else ""}" title="{texto[x]}">{x}</span>'
        for i, x in enumerate(ultimos)
    )
    return f'<span class="ultimos">{fichas}</span>'


def tabla_posiciones():
    cuerpos = ''
    for desde, hasta, clave, simbolo, texto in ZONAS:
        marca = f'<span class="marca-zona" aria-hidden="true">{simbolo}</span> ' if simbolo else ''
        filas = (f'<tr class="franja-titulo"><th colspan="{COLUMNAS_TABLA}" scope="rowgroup">'
                 f'{marca}{texto} · {desde}° a {hasta}°</th></tr>')
        for i in range(desde, hasta + 1):
            s, r = TABLA[i - 1]
            tuyo = '<span class="sr"> (tu club)</span>' if s == MI_CLUB else ''
            clase = ' class="mio"' if s == MI_CLUB else ''
            filas += (
                f'<tr{clase}><td class="pos n">{i}</td>'
                f'<th class="club-col" scope="row">{club_con_escudo(s)}{tuyo}</th>'
                f'<td class="n pts-col">{3 * r["g"] + r["e"]}</td><td class="n">{r["pj"]}</td><td class="n">{r["g"]}</td>'
                f'<td class="n">{r["e"]}</td><td class="n">{r["p"]}</td><td class="n">{r["gf"]}</td><td class="n">{r["gc"]}</td>'
                f'<td class="n">{r["gf"] - r["gc"]:+d}</td><td class="col-ultimos">{fichas_racha(r["ult"][-5:])}</td></tr>'
            )
        cuerpos += f'<tbody class="zona-{clave}">{filas}</tbody>'
    cabeza = ''.join(
        f'<th class="n{" pts-col" if a == "Pts" else ""}" scope="col"><abbr title="{t}">{a}</abbr></th>'
        for a, t in (('Pts', 'Puntos'), ('PJ', 'Partidos jugados'), ('G', 'Ganados'), ('E', 'Empatados'), ('P', 'Perdidos'),
                     ('GF', 'Goles a favor'), ('GC', 'Goles en contra'), ('DG', 'Diferencia de gol'))
    )
    return f'''<div class="region-tabla" role="region" aria-label="Tabla de posiciones, se desplaza hacia el costado" tabindex="0">
<table class="posiciones"><caption class="sr">{LIGA}, después de la fecha {FECHA - 1}, por zonas</caption>
<thead><tr><th class="pos n" scope="col"><abbr title="Posición">#</abbr></th><th class="club-col" scope="col">Club</th>{cabeza}<th class="col-ultimos" scope="col">Últimos 5 <span class="reciente-nota">(→ el más reciente)</span></th></tr></thead>
{cuerpos}</table></div>'''


def fila_fixture(local, visitante, hora=None, goles=None):
    mio = MI_CLUB in (local, visitante)
    if goles is not None:
        centro = f'<span class="resultado-fx"><b>{goles[0]}</b> - <b>{goles[1]}</b></span>'
        cuando = 'Final'
    else:
        centro = '<span class="resultado-fx">vs</span>'
        cuando = hora or 'en el día'
    tuyo = '<span class="sr"> (tu partido)</span>' if mio else ''
    return (f'<li class="partido-fx{" mio" if mio else ""}"><span class="hora-fx">{e(cuando)}</span>'
            f'<span class="local-fx">{e(nombre_corto(local))}{escudo(local, "escudo-chico")}</span>{centro}'
            f'<span class="visitante-fx">{escudo(visitante, "escudo-chico")}{e(nombre_corto(visitante))}</span>{tuyo}</li>')


def fixture():
    """Agrupado por fecha y, dentro, por día. La hora solo en partidos entre managers (RN-745)."""
    # Partidos entre managers en la fecha 12: el nuestro (21 h), uno a las 18 h y uno sin horario elegido todavía.
    horarios = {PROXIMA[0]: HORARIO.split(' ', 1)[1], PROXIMA[1]: '18 h', PROXIMA[2]: 'Horario a definir por el local'}
    proxima = ''.join(fila_fixture(l, v, horarios.get((l, v))) for l, v in PROXIMA)
    jugada = ''.join(fila_fixture(l, v, goles=(gl, gv)) for l, gl, v, gv in RESULTADOS[-1])
    return f'''<section class="fecha-fx" aria-labelledby="fx-{FECHA}"><h3 id="fx-{FECHA}">Fecha {FECHA} · la próxima</h3>
<h4 class="dia-fx">Sábado</h4><ul class="partidos-fx" role="list">{proxima}</ul></section>
<section class="fecha-fx" aria-labelledby="fx-{FECHA - 1}"><h3 id="fx-{FECHA - 1}">Fecha {FECHA - 1} · resultados</h3>
<h4 class="dia-fx">Sábado pasado</h4><ul class="partidos-fx" role="list">{jugada}</ul></section>'''


def pantalla_tabla():
    cuerpo = f'''<h1 class="titulo-pantalla">Tabla de posiciones</h1>
<section class="seccion"><header><span class="volanta">{LIGA}</span><h2>Después de la fecha {FECHA - 1}</h2></header>
{tabla_posiciones()}</section>
<section class="seccion" id="fixture"><header><span class="volanta">Calendario y resultados</span><h2>Fixture</h2></header>
<p class="suave">Solo los partidos entre managers tienen horario: los demás se juegan en el día.</p>
{fixture()}</section>'''
    pagina('tabla.html', 'Tabla de posiciones', cuerpo, 'tabla')


# --------------------------------------------------------------- Menú principal: propuestas B y C (hitos M2 y M3)
# La opción A se retiró (RN-740). Todas las propuestas ofrecen las mismas doce secciones (RN-741).

def nombre_corto(sigla):
    """Sin la primera palabra del nombre (Atlético, Unión...) ni un "de" suelto: Defensores de Loma Chata → Loma Chata."""
    resto = CLUB[sigla][1].split(' ', 1)[1]
    return resto[3:] if resto.startswith('de ') else resto


def secciones():
    """Las doce secciones del menú, en orden de importancia: rótulo, destino ('' = sin pantalla), estado, alerta."""
    r = dict(TABLA)[MI_CLUB]
    l, gl, v, gv = PARTIDOS_MIOS[-1]
    por_vencer = sum(1 for j in PLANTEL if j[7] == 'medio año')
    return {
        'formacion': ('Formación y táctica', 'previa.html', '4-3-3 · Jugarlo parejo', False),
        'plantel': ('Plantel', 'plantel.html', f'{len(PLANTEL)} jugadores · 1 lesionado', False),
        'entrenamiento': ('Entrenamiento', '', 'Semana liviana: se juega el sábado', False),
        'tabla': ('Tabla', 'tabla.html', f'{POSICION[MI_CLUB]}° con {3 * r["g"] + r["e"]} puntos, zona de octogonal', False),
        'calendario': ('Calendario y resultados', 'tabla.html#fixture', f'Última: {nombre_corto(l)} {gl}, {nombre_corto(v)} {gv}', False),
        'noticias': ('Noticias', 'club.html#novedades', '3 novedades esta semana', True),
        'fichajes': ('Fichajes', '', '2 negociaciones abiertas', False),
        'ojeadores': ('Ojeadores', '', '1 informe nuevo', True),
        'contratos': ('Contratos', '', f'{por_vencer} vencen en medio año', True),
        'caja': ('Caja', '', 'Margen justo para sueldos', False),
        'estadio': ('Estadio', '', 'Estadio del Bajo: el sábado, de local', False),
        'dirigencia': ('Dirigencia', 'club.html#dirigencia', 'Pide entrar al octogonal', False),
    }


def enlace_menu(rotulo, destino, estado, alerta=False, dibujo=''):
    """Destino con pantalla en la maqueta: href. Sin pantalla: aviso de maqueta con el nombre de la sección.
    Con dibujo, el rótulo y el estado van en una placa debajo del dibujo, dentro del mismo enlace."""
    atributos = f'href="{destino}"' if destino else f'href="#" data-maqueta="{e(rotulo)}"'
    marca = '<span class="alerta" aria-hidden="true">!</span>' if alerta else ''
    texto = f'<span class="rotulo">{e(rotulo)}</span><span class="sr">: </span><span class="estado">{e(estado)}</span>'
    if dibujo:
        return f'<a {atributos}><span class="dibujo">{dibujo}</span><span class="placa">{texto}{marca}</span></a>'
    return f'<a {atributos}>{texto}{marca}</a>'


def panel_partido(clase=''):
    """Próximo partido contra otro manager (RN-745): horario elegido por el local y nombre del manager rival."""
    return f'''<section class="menu-partido proximo seccion destacada {clase}" aria-labelledby="t-prox">
<header><span class="volanta">{ETAPA} · Fecha {FECHA} de {FECHAS}</span><h2 id="t-prox">Próximo partido</h2></header>
<div class="duelo"><span class="equipo">{escudo(MI_CLUB)}{e(CLUB[MI_CLUB][1])}</span><span class="vs">vs</span>
<span class="equipo">{escudo(RIVAL)}{e(CLUB[RIVAL][1])}<span class="manager">Manager: {e(MANAGER_RIVAL)}</span></span></div>
<p class="datos-partido"><b>Se juega el {HORARIO}</b>. Lo elegiste vos: jugamos de local, en el Estadio del Bajo.</p>
<a class="boton volumen jugar" href="previa.html" aria-describedby="jugar-d">Preparar el partido</a>
<p id="jugar-d" class="nota-jugar">Si a esa hora no estás, lo dirige tu asistente.</p>
</section>'''


def menu_a():
    """La opción A se retiró (RN-740): queda solo un aviso, sin enlaces que lleven a ella."""
    cuerpo = '''<h1 class="titulo-pantalla">Propuesta en rediseño</h1>
<section class="seccion"><p>La opción A del menú principal se está rediseñando y por ahora no está disponible.</p>
<p>Mientras tanto, mirá las otras propuestas del menú desde la <a href="index.html">portada</a>.</p></section>'''
    pagina('menu-a.html', 'Propuesta en rediseño', cuerpo, clase_body='portada')


# Opción B: un objeto de la oficina por sección, en orden de importancia (es el orden del foco).
# Lugar en la escena de la PC y posición en % (x, y, ancho, alto).
OBJETOS_B = [
    ('formacion', 'pizarron', 'pared', (20, 7, 13.75, 35)),
    ('plantel', 'carpeta', 'escritorio', (53.1, 63, 12.3, 32)),
    ('entrenamiento', 'silbato', 'escritorio', (66, 63, 12.3, 32)),
    ('tabla', 'planilla', 'pared', (66.25, 7, 13.75, 35)),
    ('calendario', 'agenda', 'escritorio', (40.2, 63, 12.3, 32)),
    ('noticias', 'diario', 'escritorio', (14.4, 63, 12.3, 32)),
    ('fichajes', 'telefono', 'escritorio', (1.5, 63, 12.3, 32)),
    ('ojeadores', 'prismaticos', 'escritorio', (78.9, 63, 12.3, 32)),
    ('contratos', 'fichero', 'lateral-der', (83, 31, 14.5, 30)),
    ('caja', 'sobre', 'escritorio', (27.3, 63, 12.3, 32)),
    ('estadio', 'ventana', 'lateral', (1.5, 9, 15.5, 44)),
    ('dirigencia', 'cuadro', 'lateral-der', (82.5, 3, 15.5, 27)),
]


def menu_b():
    s = secciones()
    items = ''
    for clave, dibujo, lugar, (x, y, w, h) in OBJETOS_B:
        rotulo, destino, estado, alerta = s[clave]
        items += (f'<li class="objeto objeto-{dibujo} en-{lugar}" style="--x:{x}%;--y:{y}%;--w:{w}%;--h:{h}%">'
                  f'{enlace_menu(rotulo, destino, estado, alerta, objeto(dibujo))}</li>')
    cuerpo = f'''<h1 class="sr">Menú principal, opción B: La oficina del técnico</h1>
<div class="oficina">
{ESCENA}
{panel_partido('puerta')}
<nav class="objetos-nav" aria-label="Secciones del club"><ul class="objetos" role="list">{items}</ul></nav>
</div>'''
    pagina('menu-b.html', 'Menú principal (opción B)', cuerpo, clase_body='menu-pantalla menu-b', menu='b')


# Opción C (RN-747): las secciones como fichas paradas por líneas en la cancha; el palco, afuera.
# Posición del título y de cada ficha en la cancha de la PC, en % (x, y). Arco propio a la izquierda.
LINEAS_C = [
    ('casa', 'Los de casa', (2.5, 1.5), [('formacion', 14.5, 30), ('plantel', 4, 9), ('entrenamiento', 4, 52), ('contratos', 14.5, 73)]),
    ('torneo', 'El torneo', (34, 1.5), [('tabla', 32, 9), ('calendario', 51.5, 13), ('estadio', 41, 73)]),
    ('ataque', 'Salir a buscar', (71, 1.5), [('fichajes', 69.5, 22), ('ojeadores', 80.5, 57)]),
]
PALCO_C = ('palco', 'El palco', ['dirigencia', 'caja', 'noticias'])
MARCA_O = '<span class="marca-o"></span>'


def ficha_c(clave, s, x=None, y=None):
    rotulo, destino, estado, alerta = s[clave]
    pos = f' style="--x:{x}%;--y:{y}%"' if x is not None else ''
    return f'<li class="ficha-c"{pos}>{enlace_menu(rotulo, destino, estado, alerta, MARCA_O)}</li>'


def linea_c(clave, titulo, fichas, s, pos_titulo=None):
    estilo = f' style="--x:{pos_titulo[0]}%;--y:{pos_titulo[1]}%"' if pos_titulo else ''
    items = ''.join(ficha_c(c, s, *xy) for c, *xy in fichas)
    return (f'<section class="linea-c linea-{clave}" aria-labelledby="g-{clave}">'
            f'<h2 id="g-{clave}" class="linea-titulo"{estilo}>{e(titulo)}</h2>'
            f'<ul class="fichas-c" role="list">{items}</ul></section>')


def menu_c():
    s = secciones()
    lineas = ''.join(linea_c(clave, titulo, fichas, s, pos) for clave, titulo, pos, fichas in LINEAS_C)
    clave, titulo, fichas = PALCO_C
    palco = linea_c(clave, titulo, [(c,) for c in fichas], s)
    cuerpo = f'''<h1 class="sr">Menú principal, opción C: La pizarra</h1>
<div class="pizarra-c">
{panel_partido('cartel')}
<nav class="pizarra-nav" aria-label="Secciones del club">
<div class="cancha-c">{cancha_apaisada()}{lineas}</div>
{palco}
</nav>
</div>'''
    pagina('menu-c.html', 'Menú principal (opción C)', cuerpo, clase_body='menu-pantalla menu-c', menu='c')


if __name__ == '__main__':
    portada()
    menu_a()
    menu_b()
    menu_c()
    pantalla_club()
    pantalla_plantel()
    pantalla_previa()
    pantalla_partido()
    pantalla_tabla()
    print('Mi club:', POSICION[MI_CLUB], '° · rival', POSICION[RIVAL], '°')
