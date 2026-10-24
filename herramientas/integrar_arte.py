# Integra al sitio una imagen generada con IA y aprobada por el director de arte.
# Recorta, quita el fondo liso, saca los tamaños pedidos, optimiza y registra el archivo en LICENCIAS.md.
# La original no se toca y queda fuera del repo, en F:\Arte-fobalmanager\.
# Uso: python herramientas/integrar_arte.py ORIGINAL --nombre N --anchos 96,192 --herramienta H --modelo M --fecha AAAA-MM-DD
# Requiere Pillow.

import argparse
import re
import sys
from collections import deque
from datetime import date
from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ARTE = Path('F:/Arte-fobalmanager')
MARGEN = 2  # píxeles transparentes que quedan alrededor de la figura después de recortar


def color_de_fondo(img):
    """El color más repetido en el borde de la imagen: el fondo liso que pide el prompt."""
    ancho, alto = img.size
    px = img.load()
    borde = [px[x, y][:3] for x in range(ancho) for y in (0, alto - 1)]
    borde += [px[x, y][:3] for y in range(alto) for x in (0, ancho - 1)]
    return max(set(borde), key=borde.count)


def distancia(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def quitar_fondo(img, tolerancia):
    """Vuelve transparente el fondo conectado con el borde (relleno desde afuera, así no agujerea la figura).
    Los píxeles del contorno que se parecen al fondo quedan semitransparentes, para que el borde no serruche."""
    img = img.convert('RGBA')
    ancho, alto = img.size
    px = img.load()
    fondo = color_de_fondo(img)
    visto = bytearray(ancho * alto)
    cola = deque()
    for x in range(ancho):
        cola.extend(((x, 0), (x, alto - 1)))
    for y in range(alto):
        cola.extend(((0, y), (ancho - 1, y)))
    while cola:
        x, y = cola.popleft()
        i = y * ancho + x
        if visto[i]:
            continue
        visto[i] = 1
        r, g, b, a = px[x, y]
        d = distancia((r, g, b), fondo)
        if d > tolerancia * 2:
            continue
        if d <= tolerancia:
            px[x, y] = (r, g, b, 0)
        else:
            # Zona de transición: alfa proporcional a cuánto se aleja del fondo. No se sigue expandiendo.
            px[x, y] = (r, g, b, min(a, round(255 * (d - tolerancia) / tolerancia)))
            continue
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < ancho and 0 <= ny < alto and not visto[ny * ancho + nx]:
                cola.append((nx, ny))
    return img


def recortar(img):
    caja = img.getchannel('A').getbbox()
    if not caja:
        sys.exit('La imagen quedó vacía al quitar el fondo: bajá la tolerancia o usá --fondo conservar.')
    x0, y0, x1, y1 = caja
    return img.crop((max(0, x0 - MARGEN), max(0, y0 - MARGEN), min(img.width, x1 + MARGEN), min(img.height, y1 + MARGEN)))


def escalar(img, ancho, pixel):
    if pixel:
        # Pixel art: sin suavizado y a un múltiplo (o divisor) entero del original, para que cada píxel sea parejo.
        factor = ancho / img.width
        if factor >= 1:
            factor = max(1, round(factor))
        else:
            factor = 1 / max(1, round(1 / factor))
        nuevo = (max(1, round(img.width * factor)), max(1, round(img.height * factor)))
        return img.resize(nuevo, Image.NEAREST)
    alto = max(1, round(img.height * ancho / img.width))
    return img.resize((ancho, alto), Image.LANCZOS)


def guardar(img, destino, pixel):
    """PNG optimizado y WebP. Pillow no copia los metadatos de la original: la procedencia va en LICENCIAS.md."""
    png = destino.with_suffix('.png')
    img.save(png, optimize=True)
    webp = destino.with_suffix('.webp')
    if pixel:
        img.save(webp, lossless=True, method=6)
    else:
        img.save(webp, quality=86, method=6)
    return [png, webp]


def registrar(licencias, archivos, herramienta, modelo, fecha, original):
    """Agrega una fila por archivo a la tabla de "Imágenes generadas con IA"; si el archivo ya estaba, la reemplaza."""
    texto = licencias.read_text(encoding='utf-8')
    encabezado = '| Archivo | Herramienta | Modelo | Fecha | Original |\n|---|---|---|---|---|\n'
    if encabezado not in texto:
        sys.exit(f'No encuentro la tabla de imágenes generadas en {licencias}.')
    inicio = texto.index(encabezado) + len(encabezado)
    fin = inicio
    filas = []
    for linea in texto[inicio:].splitlines(keepends=True):
        if not linea.startswith('|'):
            break
        filas.append(linea)
        fin += len(linea)
    nuevos = {f'`{a}`' for a in archivos}
    filas = [f for f in filas if f.split('|')[1].strip() not in nuevos]
    filas += [f'| `{a}` | {herramienta} | {modelo} | {fecha} | `{original}` |\n' for a in archivos]
    licencias.write_text(texto[:inicio] + ''.join(filas) + texto[fin:], encoding='utf-8', newline='\n')


def main():
    p = argparse.ArgumentParser(description='Integra al sitio una imagen generada con IA y aprobada.')
    p.add_argument('original', type=Path, help='imagen aprobada, dentro de F:\\Arte-fobalmanager\\')
    p.add_argument('--nombre', required=True, help='nombre del archivo publicado, sin extensión (ej. preparador-fisico)')
    p.add_argument('--anchos', required=True, help='anchos en píxeles, separados por coma (ej. 96,192)')
    p.add_argument('--herramienta', required=True, help='ej. ChatGPT, Gemini')
    p.add_argument('--modelo', required=True, help='ej. gpt-image-1, gemini-2.5-flash-image')
    p.add_argument('--fecha', required=True, help='fecha de generación, AAAA-MM-DD')
    p.add_argument('--fondo', choices=['quitar', 'conservar'], default='quitar',
                   help='quitar: vuelve transparente el fondo liso (personajes, íconos); conservar: fondos de pantalla')
    p.add_argument('--tolerancia', type=int, default=24, help='cuánto puede variar el color del fondo (0 a 255)')
    p.add_argument('--pixel', action='store_true', help='pixel art: escala sin suavizar, a múltiplos enteros')
    p.add_argument('--nativo', help='pixel art: resolución nativa a la que se reduce antes de escalar (ej. 32x48)')
    p.add_argument('--colores', type=int, default=16, help='con --nativo: colores máximos de la paleta')
    p.add_argument('--destino', type=Path, default=RAIZ / 'img' / 'arte', help='carpeta del sitio')
    p.add_argument('--licencias', type=Path, default=RAIZ / 'LICENCIAS.md')
    p.add_argument('--fuera-de-arte', action='store_true', help='acepta una original fuera de F:\\Arte-fobalmanager\\ (pruebas)')
    a = p.parse_args()

    original = a.original.resolve()
    if not original.is_file():
        sys.exit(f'No existe {original}.')
    if not a.fuera_de_arte and ARTE.resolve() not in original.parents:
        sys.exit(f'La original tiene que estar en {ARTE}, fuera de los repos.')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', a.nombre):
        sys.exit('El nombre va en minúsculas, sin acentos, con guiones (ej. preparador-fisico).')
    date.fromisoformat(a.fecha)
    if a.nativo and not re.fullmatch(r'\d+[xX]\d+', a.nativo):
        sys.exit('--nativo va como ANCHOxALTO (ej. 32x48).')
    if a.nativo:
        a.pixel = True
    anchos = sorted({int(x) for x in a.anchos.split(',')})

    img = Image.open(original)
    img.load()
    if a.nativo:
        # Los generadores no respetan una grilla real: se reduce a la resolución nativa tomando un color por celda
        # (vecino más cercano, sin promediar) y se limita la paleta. El retoque a mano, si hace falta, va después.
        ancho_n, alto_n = (int(v) for v in a.nativo.lower().split('x'))
        img = img.convert('RGBA').resize((ancho_n, alto_n), Image.NEAREST)
        alfa = img.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
        img = img.convert('RGB').quantize(colors=a.colores, method=Image.Quantize.MEDIANCUT).convert('RGBA')
        img.putalpha(alfa)
    if a.fondo == 'quitar':
        tiene_alfa = img.mode in ('RGBA', 'LA') and img.getchannel('A').getextrema()[0] < 255
        img = recortar(img.convert('RGBA') if tiene_alfa else quitar_fondo(img, a.tolerancia))
    else:
        img = img.convert('RGB')

    a.destino.mkdir(parents=True, exist_ok=True)
    publicados = []
    hechos = set()
    for ancho in anchos:
        if not a.pixel and ancho > img.width:
            print(f'Aviso: {ancho} px es más que el original ({img.width} px); se agranda y puede verse borroso.')
        salida = escalar(img, ancho, a.pixel)
        # El archivo lleva el ancho real: en pixel art puede no ser el pedido, por la escala entera.
        if salida.width in hechos:
            continue
        hechos.add(salida.width)
        for archivo in guardar(salida, a.destino / f'{a.nombre}-{salida.width}', a.pixel):
            publicados.append(archivo)
            print(f'{archivo.relative_to(RAIZ) if RAIZ in archivo.parents else archivo}: '
                  f'{salida.width}x{salida.height}, {archivo.stat().st_size // 1024} KB')

    relativos = [f.relative_to(RAIZ).as_posix() if RAIZ in f.parents else f.as_posix() for f in publicados]
    # La original se anota relativa a la carpeta de arte, sin la ruta local completa.
    fuente = original.relative_to(ARTE.resolve()).as_posix() if ARTE.resolve() in original.parents else original.name
    registrar(a.licencias, relativos, a.herramienta, a.modelo, a.fecha, fuente)
    print(f'Registrado en {a.licencias.name}.')


if __name__ == '__main__':
    main()
