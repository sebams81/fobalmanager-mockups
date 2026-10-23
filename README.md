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

- `menu-b.html`, "La oficina del técnico": cada sección es un objeto de la oficina (pizarrón, carpeta,
  silbato, planilla, agenda, diario, teléfono, prismáticos, fichero, sobre, ventana y cuadro de la
  comisión directiva). La puerta del centro es el próximo partido.
- `menu-c.html`, "La pizarra": arriba, un cartel con el próximo partido; abajo, la cancha, con las
  secciones como fichas paradas por líneas ("Los de casa", "El torneo", "Salir a buscar") y "El palco"
  afuera de la línea de cal. El círculo central queda vacío.
- `menu-a.html`: la opción A se retiró de la evaluación. Queda un aviso de propuesta en rediseño, sin
  enlaces que lleven a ella.

En el celular, el partido va arriba y las secciones en grilla o en franjas; desde 64rem (1024 px), la
composición completa. Las ilustraciones y las canchas son SVG propios (`fuente/ilustraciones.py`). Usan
clases de material (madera, papel, metal…) y de cancha que cada tema pinta con las variables `--il-*` y
`--cancha-*` de `css/temas.css`: el dibujo es el mismo en los cuatro temas. Las secciones sin pantalla en la
maqueta muestran un aviso.

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

## Fuentes

Las fuentes (VT323, IBM Plex Mono, Oswald, Source Serif 4, Roboto Condensed, Space Grotesk, Inter,
Cabin Sketch y Atkinson Hyperlegible) se bajaron de Google Fonts y están alojadas en `fuentes/`, sin pedidos
a terceros y sin modificar los archivos. Todas tienen licencia SIL Open Font License 1.1; los textos de
licencia están en `fuentes/LICENCIAS.md`. Cada tema carga solo su CSS de fuentes (`css/fuentes-<tema>.css`).
En el tema Pizarra, la letra de tiza (Cabin Sketch) va solo en títulos y rótulos; el cuerpo, las tablas, los
números y los botones van en Atkinson Hyperlegible.

## Publicación

GitHub Pages, desde la rama `main` y la carpeta raíz.
