# Fobalmanager: maquetas visuales

Maquetas públicas de Fobalmanager, un manager de fútbol en el navegador, para pedir opiniones.
Son ilustrativas y no tienen funciones. Todo el contenido es ficticio: clubes, jugadores, managers,
dirigentes, medios, estadios, escudos y resultados.

Hay propuestas de menú principal y cinco pantallas (inicio del club, plantel, previa y táctica, partido en
vivo y tabla de posiciones con fixture), con una única estructura y cuatro temas visuales: Retro, Diario,
Moderno y Pizarra. Un tema cambia solo colores, tipografía, texturas, íconos y bordes, mediante las variables
de `css/temas.css`. La disposición vive en `css/base.css` y es la misma en los cuatro. El tema elegido se
recuerda en el navegador. En la primera visita se elige uno al azar, para no sesgar las opiniones.

## Menú principal: propuestas en evaluación

Ninguna está elegida. Las dos ofrecen las mismas doce secciones: cambia solo la forma de llegar a ellas.

- `menu-b.html`, "La oficina del técnico": una oficina armada con superficies (pared, escritorio, ventana y
  puerta), con cada sección como una placa con su ícono, en la pared o en el escritorio. Detrás de la
  puerta, el próximo partido.
- `menu-c.html`, "La cancha": arriba, un cartel con el próximo partido; en el centro, la cancha con la
  formación propia (lleva a la táctica); alrededor, las demás secciones con su ícono, agrupadas por uso.
- `menu-a.html` y `menu-d.html`: las opciones A y D se retiraron de la evaluación. Queda un aviso de
  propuesta en rediseño, sin enlaces que lleven a ellas.

En el celular, el partido va arriba y las secciones en grilla o en franjas; desde 64rem (1024 px), la
composición completa. Los íconos son de Phosphor Icons (licencia MIT; ver `LICENCIAS.md`), en
`fuente/iconos.py`: cada ícono trae tres pesos y cada tema muestra uno (variables `--ic-*` de
`css/temas.css`). Las canchas son SVG con las medidas reglamentarias (`fuente/ilustraciones.py`). Las
secciones sin pantalla en la maqueta muestran un aviso.

## Link del formulario de opinión

Está en un solo lugar: la primera constante de `js/maqueta.js`.

```js
const LINK_OPINION = 'PEGAR-ACA-EL-LINK-DEL-FORMULARIO';
```

Reemplazá el texto entre comillas por el link completo (`https://...`). Todos los botones
"Dar mi opinión" lo toman de ahí. Mientras no empiece con `https://`, la portada muestra el aviso
"[Link del formulario pendiente…]" y el botón no lleva a ningún lado.

## Ver una pantalla en un tema

Agregá `?tema=retro`, `?tema=diario`, `?tema=moderno` o `?tema=pizarra` a cualquier URL, por ejemplo
`partido.html?tema=diario`.

## Editar el contenido

Las páginas HTML se generan con `fuente/generar.py` y `fuente/ilustraciones.py` (Python 3, solo biblioteca
estándar):

```sh
python fuente/generar.py
```

Los datos ficticios están en ese archivo. El relato del partido (`fuente/relato.json`) usa frases
tal cual de la crónica del juego, con nombres ficticios. No hay dependencias ni paso de armado:
el sitio es HTML, CSS y un JS chico.

## Imágenes

Las imágenes ilustradas se generan con herramientas de IA a partir de los prompts del director de arte y se
integran con `herramientas/integrar_arte.py` (Python 3 con Pillow): recorta, quita el fondo liso, saca los
tamaños, optimiza y registra cada archivo en `LICENCIAS.md` con herramienta, modelo y fecha. Las originales
quedan fuera del repo, en `F:\Arte-fobalmanager\`.

```sh
python herramientas/integrar_arte.py F:/Arte-fobalmanager/aprobadas/preparador.png --nombre preparador-fisico --anchos 96,192 --herramienta ChatGPT --modelo gpt-image-1 --fecha 2026-10-24
```

Con `--fondo conservar` no quita el fondo (fondos de pantalla) y con `--pixel` escala sin suavizar, a
múltiplos enteros (el archivo lleva el ancho real en el nombre). `-h` lista todas las opciones.

## Fuentes

Las fuentes (Russo One, PT Sans, Oswald, Source Serif 4, Roboto Condensed, Space Grotesk, Inter,
Cabin Sketch y Atkinson Hyperlegible) se bajaron de Google Fonts y están alojadas en `fuentes/`, sin pedidos
a terceros y sin modificar los archivos. Todas tienen licencia SIL Open Font License 1.1; los textos de
licencia están en `fuentes/LICENCIAS.md`. Cada tema carga solo su CSS de fuentes (`css/fuentes-<tema>.css`).
En el tema Pizarra, la letra de tiza (Cabin Sketch) va solo en títulos y rótulos; el cuerpo, las tablas, los
números y los botones van en Atkinson Hyperlegible.

## Publicación

GitHub Pages, desde la rama `main` y la carpeta raíz.
