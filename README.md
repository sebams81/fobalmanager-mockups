# Fobalmanager: maquetas visuales

Maquetas públicas de Fobalmanager, un manager de fútbol en el navegador, para pedir opiniones.
Son ilustrativas y no tienen funciones. Todo el contenido es ficticio: clubes, jugadores, dirigentes,
medios, estadios, escudos y resultados.

Hay dos propuestas de menú principal y cinco pantallas (inicio del club, plantel, previa y táctica, partido en vivo y tabla de posiciones)
con una única estructura y tres temas visuales: Retro, Diario y Moderno. Un tema cambia solo
colores, tipografía, texturas, íconos y bordes, mediante las variables de `css/temas.css`.
La disposición vive en `css/base.css` y es la misma en los tres. El tema elegido se recuerda
en el navegador. En la primera visita se elige uno al azar, para no sesgar las opiniones.

## Menú principal: dos propuestas

Hay dos propuestas de menú principal para comparar, con acceso desde la portada y cada una enlazada a la otra
desde el pie. Ninguna está elegida.

- `menu-a.html`, "Centro de mando": el próximo partido en el centro y cuatro áreas alrededor (El equipo,
  La competencia, El mercado y El club).
- `menu-b.html`, "La oficina del técnico": cada sección es un objeto de la oficina (pizarrón, carpeta,
  planilla, teléfono, diario, agenda, sobre y ventana). La puerta del centro es el próximo partido.

En el celular, el partido va arriba y las áreas u objetos en grilla; desde 64rem (1024 px), la composición
completa. Las ilustraciones son SVG propios (`fuente/ilustraciones.py`). Usan clases de material (madera,
papel, metal…) que cada tema pinta con las variables `--il-*` de `css/temas.css`: el dibujo es el mismo en
los tres temas. Las secciones sin pantalla en la maqueta muestran un aviso.

## Link del formulario de opinión

Está en un solo lugar: la primera constante de `js/maqueta.js`.

```js
const LINK_OPINION = 'PEGAR-ACA-EL-LINK-DEL-FORMULARIO';
```

Reemplazá el texto entre comillas por el link completo (`https://...`). Todos los botones
"Dar mi opinión" lo toman de ahí. Mientras no empiece con `https://`, la portada muestra el aviso
"[Link del formulario pendiente…]" y el botón no lleva a ningún lado.

## Ver una pantalla en un tema

Agregá `?tema=retro`, `?tema=diario` o `?tema=moderno` a cualquier URL, por ejemplo
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

Las fuentes (VT323, IBM Plex Mono, Oswald, Source Serif 4, Roboto Condensed, Space Grotesk e Inter)
se bajaron de Google Fonts y están alojadas en `fuentes/`, sin pedidos a terceros. Todas tienen
licencia SIL Open Font License 1.1; los textos de licencia están en `fuentes/LICENCIAS.md`.
Cada tema carga solo su CSS de fuentes (`css/fuentes-<tema>.css`).

## Publicación

GitHub Pages, desde la rama `main` y la carpeta raíz.
