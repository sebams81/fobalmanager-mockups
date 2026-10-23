# Ilustraciones SVG propias del menú principal (hito M2), dibujadas desde cero para esta maqueta.
# Cada figura usa clases de material (madera, papel, rojo...) que temas.css pinta según el tema:
# los trazos son los mismos en los tres temas, solo cambian rellenos, tinta, grosor y texturas.

# Tramas y texturas: van una vez por página, en el sprite oculto.
PATRONES = (
    '<defs>'
    '<pattern id="trama-clara" width="5" height="5" patternUnits="userSpaceOnUse">'
    '<rect class="trama-fondo" width="5" height="5"/><circle class="trama-punto" cx="2.5" cy="2.5" r=".9"/></pattern>'
    '<pattern id="trama-media" width="5" height="5" patternUnits="userSpaceOnUse">'
    '<rect class="trama-fondo" width="5" height="5"/><circle class="trama-punto" cx="2.5" cy="2.5" r="1.5"/></pattern>'
    '<pattern id="trama-oscura" width="5" height="5" patternUnits="userSpaceOnUse">'
    '<rect class="trama-fondo" width="5" height="5"/><circle class="trama-punto" cx="2.5" cy="2.5" r="2.1"/></pattern>'
    '<pattern id="damero" width="4" height="4" patternUnits="userSpaceOnUse">'
    '<rect class="trama-punto" width="2" height="2"/><rect class="trama-punto" x="2" y="2" width="2" height="2"/></pattern>'
    '<pattern id="franjas" width="28" height="10" patternUnits="userSpaceOnUse">'
    '<rect class="franja-a" width="14" height="10"/><rect class="franja-b" x="14" width="14" height="10"/></pattern>'
    '<pattern id="tablones" width="120" height="30" patternUnits="userSpaceOnUse">'
    '<rect class="tablon-a" width="120" height="30"/><path class="tablon-junta" d="M0 29.5h120M60 0v30"/></pattern>'
    '</defs>'
)


def _lineas(x1, x2, ys, clase='fino'):
    return ''.join(f'<path class="{clase}" d="M{x1} {y}H{x2}"/>' for y in ys)


# ---------------------------------------------------------------- Objetos de la oficina (opción B)
# Todos en una caja de 160 x 120. Vista frontal en el celular; en la PC, el CSS los apoya en la pared o el escritorio.

PIZARRON = (
    '<rect class="sombra" x="12" y="12" width="146" height="100"/>'
    '<rect class="madera" x="6" y="6" width="146" height="96"/>'
    '<rect class="pizarra" x="14" y="14" width="130" height="80"/>'
    '<path class="luz" d="M104 14h20L84 94H64z"/>'
    '<path class="tz" d="M79 14v80M14 36h14v36H14M144 36h-14v36h14"/><circle class="tz" cx="79" cy="54" r="11"/>'
    '<path class="tz" d="M34 28l8 8m0-8-8 8M34 70l8 8m0-8-8 8M52 47l8 8m0-8-8 8"/>'
    '<circle class="tz" cx="106" cy="32" r="4"/><circle class="tz" cx="112" cy="74" r="4"/><circle class="tz" cx="100" cy="54" r="4"/>'
    '<path class="tz" d="M62 48c10-16 22-20 32-14M86 30l9 4-5 8"/>'
    '<rect class="madera-2" x="10" y="100" width="138" height="9"/>'
    '<rect class="tiza" x="30" y="95" width="18" height="5"/>'
    '<rect class="metal" x="102" y="92" width="28" height="8"/><rect class="oscuro" x="102" y="96" width="28" height="4"/>'
)

TELEFONO = (
    '<path class="sombra" d="M36 46h100l10 68H26z"/>'
    '<path class="rojo" d="M30 40h100l10 66H20z"/>'
    '<path class="luz" d="M31 41h98l2 9H29z"/>'
    '<path class="rojo-2" d="M16 22c0-10 6-14 16-14h96c10 0 16 4 16 14v9c0 7-4 10-10 10h-17c-6 0-9-3-9-9v-4H52v4c0 6-3 9-9 9H26c-6 0-10-3-10-10z"/>'
    '<path class="luz" d="M30 12h100v4H30z"/>'
    + ''.join(f'<rect class="papel" x="{x}" y="{y}" width="13" height="8"/>' for y in (56, 68, 80, 92) for x in (55, 73, 91))
    + '<path d="M20 94c-9 1-10 7-5 9s3 8-3 8-6 7 0 8"/>'
)

DIARIO = (
    '<g transform="rotate(-6 80 60)">'
    '<rect class="sombra" x="26" y="16" width="114" height="98"/>'
    '<rect class="papel" x="20" y="10" width="114" height="96"/>'
    '<rect class="tinta" x="28" y="18" width="98" height="13"/>'
    '<path class="fino" d="M28 35h98M77 39v63"/>'
    '<rect class="rojo" x="28" y="40" width="44" height="7"/><rect class="rojo" x="28" y="51" width="34" height="7"/>'
    '<rect class="papel-2" x="82" y="40" width="44" height="30"/>'
    '<circle class="papel" cx="104" cy="55" r="9"/><path class="tinta" d="M104 50.5l4 3-1.5 4.5h-5l-1.5-4.5z"/>'
    + _lineas(28, 72, (66, 72, 78, 84, 90, 96))
    + _lineas(82, 126, (78, 84, 90, 96))
    + '</g>'
)

AGENDA = (
    '<rect class="sombra" x="20" y="20" width="136" height="94" rx="4"/>'
    '<rect class="cuero" x="12" y="12" width="136" height="94" rx="4"/>'
    '<rect class="papel" x="18" y="16" width="60" height="84"/><rect class="papel" x="82" y="16" width="60" height="84"/>'
    '<rect class="cuero" x="24" y="22" width="48" height="8"/>'
    + ''.join(f'<path class="fino" d="M24 {y}H72"/>' for y in (36, 48, 60, 72, 84, 94))
    + ''.join(f'<path class="fino" d="M{x} 36V94"/>' for x in (24, 31, 38, 45, 52, 59, 66, 72))
    + '<circle class="trazo-rojo" cx="48.5" cy="66" r="7"/>'
    + _lineas(88, 136, (28, 36, 44, 52, 60, 68, 76, 84, 92))
    + ''.join(f'<rect class="metal" x="73" y="{y}" width="14" height="5" rx="2.5"/>' for y in (22, 34, 46, 58, 70, 82, 94))
    + '<path class="rojo" d="M120 16v96l5-5 5 5V16z"/>'
)

PLANILLA = (
    '<rect class="sombra" x="12" y="12" width="146" height="104"/>'
    '<rect class="madera" x="6" y="6" width="146" height="106"/>'
    '<rect class="corcho" x="13" y="13" width="132" height="92"/>'
    + ''.join(f'<circle class="madera-2 sin" cx="{x}" cy="{y}" r="1.6"/>' for x, y in ((20, 24), (26, 90), (138, 40), (132, 96), (22, 56), (140, 70)))
    + '<rect class="papel-2" x="18" y="58" width="16" height="34" transform="rotate(-8 26 75)"/>'
    '<g transform="rotate(2 80 60)">'
    '<rect class="papel" x="36" y="18" width="92" height="84"/>'
    '<rect class="tinta" x="42" y="25" width="80" height="7"/>'
    '<rect class="club1 sin" x="42" y="61" width="80" height="7"/>'
    + _lineas(42, 122, (40, 48, 56, 61, 68, 76, 84, 92))
    + '<path class="fino" d="M52 32v64M108 32v64"/></g>'
    '<circle class="rojo" cx="52" cy="22" r="4.5"/><circle class="azul" cx="114" cy="24" r="4.5"/>'
)

SOBRE = (
    '<rect class="sombra" x="26" y="52" width="122" height="64"/>'
    '<path class="kraft-2" d="M20 46l60-30 60 30z"/>'
    '<g transform="rotate(-9 78 40)"><rect class="billete" x="32" y="18" width="88" height="40"/>'
    '<ellipse class="billete-2" cx="76" cy="38" rx="13" ry="10"/><path class="fino" d="M40 26h14M100 50h12"/></g>'
    '<g transform="rotate(6 82 40)"><rect class="billete" x="40" y="14" width="88" height="40"/>'
    '<ellipse class="billete-2" cx="84" cy="34" rx="13" ry="10"/><path class="fino" d="M48 22h14M108 46h12"/></g>'
    '<rect class="kraft" x="20" y="46" width="120" height="62"/>'
    '<path class="fino" d="M20 108l48-34h24l48 34"/>'
    '<rect class="rojo sin" x="20" y="64" width="120" height="6"/>'
)

VENTANA = (
    '<rect class="sombra" x="12" y="12" width="146" height="104"/>'
    '<rect class="madera" x="6" y="6" width="146" height="106"/>'
    '<rect class="cielo" x="16" y="16" width="126" height="86"/>'
    '<rect class="metal-2" x="118" y="34" width="5" height="50"/>'
    '<rect class="metal" x="108" y="24" width="25" height="13"/>'
    '<circle class="lampara sin" cx="114" cy="30.5" r="2.6"/><circle class="lampara sin" cx="120.5" cy="30.5" r="2.6"/><circle class="lampara sin" cx="127" cy="30.5" r="2.6"/>'
    '<path class="metal" d="M40 62l10-9h92v9z"/>'
    '<path class="tribuna" d="M16 74l34-12h92v32H16z"/>'
    '<path class="linea-tribuna" d="M16 81l34-11h92M16 88l34-10h92"/>'
    '<rect class="cesped" x="16" y="92" width="126" height="10"/><path class="linea-cancha" d="M16 97h126"/>'
    '<rect class="persiana" x="16" y="16" width="126" height="22"/>'
    '<path class="fino" d="M16 23h126M16 30h126"/><rect class="madera-2" x="16" y="36" width="126" height="4"/>'
    '<rect class="madera" x="76" y="16" width="6" height="86"/><rect class="madera" x="16" y="62" width="126" height="5"/>'
    '<path class="luz" d="M26 100l26-38h12l-26 38z"/>'
    '<rect class="madera-2" x="0" y="106" width="158" height="9"/>'
)

CARPETA = (
    '<path class="sombra" d="M24 28h46l8 8h70v80H24z"/>'
    '<path class="azul" d="M18 22h46l8 8h70v80H18z"/>'
    '<rect class="papel-2" x="30" y="16" width="96" height="70" transform="rotate(-4 78 50)"/>'
    '<rect class="papel" x="40" y="22" width="92" height="70"/>'
    '<rect class="papel-2" x="48" y="30" width="22" height="26"/>'
    '<circle class="oscuro sin" cx="59" cy="39" r="5"/><path class="oscuro sin" d="M50 56c1-8 5-10 9-10s8 2 9 10z"/>'
    + _lineas(76, 124, (34, 42, 50))
    + '<path class="azul" d="M14 58h132l-6 52H20z"/>'
    '<path class="luz" d="M16 59h128l-1 7H17z"/>'
    '<rect class="papel" x="56" y="74" width="46" height="16"/>'
    + _lineas(62, 96, (80, 85))
    + '<rect class="oscuro sin" x="122" y="58" width="5" height="52"/>'
)

OBJETOS = {
    'pizarron': PIZARRON, 'telefono': TELEFONO, 'diario': DIARIO, 'agenda': AGENDA,
    'planilla': PLANILLA, 'sobre': SOBRE, 'ventana': VENTANA, 'carpeta': CARPETA,
}


def objeto(nombre):
    # Apoyado abajo: en la escena de la PC el objeto queda pegado a su placa.
    return (f'<svg class="il" viewBox="0 0 160 120" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false">'
            f'{OBJETOS[nombre]}</svg>')


# ---------------------------------------------------------------- Pictogramas de las áreas (opción A)
# Caja de 48 x 48. Gruesos y de colores llenos, sin objetos de la oficina para que A no se parezca a B.

PICTOGRAMAS = {
    'equipo': (
        '<path class="club1" d="M16 6L5 12l4 10 6-3v23h18V19l6 3 4-10-11-6c-1 4-4 6-8 6s-7-2-8-6z"/>'
        '<rect class="club2 sin" x="21" y="13" width="6" height="28"/>'
        '<path class="club2" d="M16 6c1 4 4 6 8 6s7-2 8-6"/>'
    ),
    'competencia': (
        '<path d="M14 9H7c0 7 3 11 8 11M34 9h7c0 7-3 11-8 11"/>'
        '<path class="oro" d="M13 5h22v9c0 8-5 13-11 13s-11-5-11-13z"/>'
        '<path class="luz" d="M16 7h4v8c0 4 1 7 3 9-4-1-7-5-7-9z"/>'
        '<rect class="oro" x="21" y="27" width="6" height="7"/>'
        '<rect class="madera" x="13" y="34" width="22" height="9"/><rect class="papel sin" x="19" y="37.5" width="10" height="2.5"/>'
    ),
    'mercado': (
        '<path class="papel" d="M9 5h22l7 7v31H9z"/><path class="papel-2" d="M31 5v7h7z"/>'
        '<path class="fino" d="M14 16h14M14 21h18M14 26h12"/>'
        '<path d="M14 35c3-4 4 2 6-1s3-3 4 0 3 1 5-1"/>'
        '<path class="rojo" d="M29 41l12-18 5 3-12 18-6 2z"/>'
    ),
    'club': (
        '<path d="M24 11V2"/><path class="club1" d="M24 2h11l-3 3.5 3 3.5H24z"/>'
        '<path class="papel" d="M8 21h32v22H8z"/>'
        '<path class="rojo" d="M4 22l20-11 20 11z"/>'
        '<rect class="vidrio" x="12" y="26" width="7" height="7"/><rect class="vidrio" x="29" y="26" width="7" height="7"/>'
        '<rect class="madera" x="20" y="31" width="8" height="12"/>'
    ),
}


def pictograma(nombre):
    return (f'<svg class="il pictograma" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
            f'{PICTOGRAMAS[nombre]}</svg>')


# ---------------------------------------------------------------- Escena de la oficina (opción B, PC)
# Habitación en perspectiva de un punto: pared del fondo, dos paredes laterales y escritorio en primer plano.
# La puerta del centro es el próximo partido; la ventana va en la pared izquierda, no detrás del escritorio.

ESCENA = (
    '<svg class="il escena" viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
    # paredes y piso
    '<rect class="pared sin" x="300" y="0" width="1000" height="600"/>'
    '<path class="pared-lado" d="M0 0h300v600L0 780z"/><path class="pared-lado" d="M1600 0h-300v600l300 180z"/>'
    '<path class="piso" d="M0 780l300-180h1000l300 180v120H0z"/>'
    '<rect class="madera-2" x="300" y="572" width="1000" height="28"/>'
    '<path class="madera-2" d="M0 762l300-180v18L0 780zM1600 762l-300-180v18l300 180z"/>'
    '<path class="fino" d="M300 0v600M1300 0v600"/>'
    # puerta del centro
    '<rect class="madera-2" x="555" y="40" width="490" height="560"/>'
    '<rect class="madera" x="580" y="64" width="440" height="536"/>'
    '<rect class="vidrio" x="608" y="76" width="384" height="484"/>'
    '<circle class="metal" cx="996" cy="580" r="11"/>'
    '<rect class="lampara" x="740" y="12" width="120" height="18" rx="9"/>'
    # banderín y reloj en la pared derecha (decorado, sin función)
    '<path class="club1" d="M1340 120l200-40v170z"/><path class="club2 sin" d="M1340 120l200-40v28l-200 34z"/>'
    '<path d="M1340 108v40"/>'
    '<ellipse class="papel" cx="1440" cy="380" rx="44" ry="52"/><path d="M1440 380v-30M1440 380l20 12"/>'
    # escritorio
    '<path class="madera" d="M60 640h1480l60 160H0z"/>'
    '<path class="luz" d="M60 640h1480l8 22H52z"/>'
    '<rect class="madera-2" x="0" y="800" width="1600" height="100"/>'
    '<path class="fino" d="M0 846h1600"/>'
    # mate y termo (decorado)
    '<rect class="sombra" x="1406" y="606" width="54" height="170" rx="10"/>'
    '<rect class="metal" x="1396" y="596" width="54" height="170" rx="10"/>'
    '<rect class="metal-2" x="1390" y="580" width="66" height="34" rx="6"/>'
    '<path class="luz" d="M1404 620h10v130h-10z"/>'
    '<path class="metal" d="M1505 640l22-90 8 2-18 88z"/>'
    '<path class="calabaza" d="M1480 650c-4 40 6 96 44 96s48-56 44-96z"/>'
    '<ellipse class="yerba" cx="1524" cy="650" rx="44" ry="10"/>'
    '</svg>'
)
