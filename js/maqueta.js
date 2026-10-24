// Maqueta de Fobalmanager: solo comportamiento de presentación. Nada de esto es el juego.

// ▼▼▼ LINK DEL FORMULARIO DE OPINIÓN: reemplazá el texto entre comillas por el link (https://...). ▼▼▼
const LINK_OPINION = 'PEGAR-ACA-EL-LINK-DEL-FORMULARIO';
// ▲▲▲ Es el único lugar donde está: todos los botones "Dar mi opinión" lo toman de acá. ▲▲▲

const TEMAS = { retro: 'Retro', diario: 'Diario', moderno: 'Moderno', pizarra: 'Pizarra' };
const estado = document.getElementById('estado-maqueta');

function anunciar(texto) {
  if (estado === null) return;
  estado.textContent = texto;
  estado.classList.add('visible');
  clearTimeout(anunciar.temporizador);
  anunciar.temporizador = setTimeout(() => estado.classList.remove('visible'), 2200);
}

// Tema: el script del <head> ya lo aplicó antes de pintar; acá se sincroniza el selector.
for (const radio of document.querySelectorAll('input[name="tema"]')) {
  radio.checked = radio.value === document.documentElement.dataset.tema;
  radio.addEventListener('change', () => {
    const tema = radio.value;
    document.documentElement.dataset.tema = tema;
    try {
      localStorage.setItem('fm-tema', tema);
    } catch {
      // Sin almacenamiento (navegación privada): el tema vale para esta página.
    }
    window.fmFuentes?.(tema);
    anunciar(`Estilo ${TEMAS[tema]} aplicado`);
  });
}

// Invertir colores del club (RN-753): el script del <head> ya aplicó la elección guardada.
for (const caja of document.querySelectorAll('input[name="invertir-club"]')) {
  caja.checked = 'invertirClub' in document.documentElement.dataset;
  caja.addEventListener('change', () => {
    if (caja.checked) document.documentElement.dataset.invertirClub = '';
    else delete document.documentElement.dataset.invertirClub;
    try {
      localStorage.setItem('fm-invertir-club', caja.checked ? '1' : '0');
    } catch {
      // Sin almacenamiento (navegación privada): la elección vale para esta página.
    }
    anunciar(caja.checked ? 'Colores del club invertidos' : 'Colores del club en su orden');
  });
}

// Botón "Dar mi opinión".
const linkListo = /^https?:\/\//.test(LINK_OPINION);
for (const enlace of document.querySelectorAll('[data-opinion]')) {
  if (linkListo) {
    enlace.href = LINK_OPINION;
    enlace.target = '_blank';
    enlace.rel = 'noopener';
  } else {
    enlace.addEventListener('click', (e) => {
      e.preventDefault();
      anunciar('Todavía falta el link del formulario.');
    });
  }
}
for (const marca of document.querySelectorAll('[data-opinion-pendiente]')) {
  marca.hidden = linkListo;
}

// Controles que en la maqueta no hacen nada. Si data-maqueta nombra una pantalla, el aviso la nombra.
for (const boton of document.querySelectorAll('[data-maqueta]')) {
  boton.addEventListener('click', (e) => {
    e.preventDefault();
    const pantalla = boton.dataset.maqueta;
    anunciar(pantalla ? `${pantalla}: esta pantalla todavía no está en la maqueta.` : 'Es una maqueta: este botón todavía no hace nada.');
  });
}

// Plantel: fichas desplegables.
for (const boton of document.querySelectorAll('[data-ficha]')) {
  boton.addEventListener('click', () => {
    const fila = document.getElementById(boton.getAttribute('aria-controls'));
    const abierta = boton.getAttribute('aria-expanded') === 'true';
    boton.setAttribute('aria-expanded', String(!abierta));
    fila.hidden = abierta;
  });
}

// Pestañas simples (plantel): una sola visible, con flechas para moverse entre ellas.
for (const lista of document.querySelectorAll('[data-pestanas]')) {
  const botones = [...lista.querySelectorAll('[role="tab"]')];
  const elegir = (i) => {
    botones.forEach((b, j) => {
      b.setAttribute('aria-selected', String(i === j));
      b.tabIndex = i === j ? 0 : -1;
      document.getElementById(b.getAttribute('aria-controls')).hidden = i !== j;
    });
  };
  botones.forEach((b, i) => {
    b.addEventListener('click', () => elegir(i));
    b.addEventListener('keydown', (e) => {
      const paso = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (paso === 0) return;
      const siguiente = (i + paso + botones.length) % botones.length;
      elegir(siguiente);
      botones[siguiente].focus();
    });
  });
}

// Partido: pestañas en mobile; en PC se ven los tres paneles y se quitan los roles de pestaña.
const pestanas = document.querySelector('.pestanas');
if (pestanas !== null) {
  const botones = [...pestanas.querySelectorAll('button')];
  const paneles = botones.map((b) => document.getElementById(b.getAttribute('aria-controls')));
  const elegir = (i) => {
    botones.forEach((b, j) => {
      b.setAttribute('aria-selected', String(i === j));
      b.tabIndex = i === j ? 0 : -1;
      paneles[j].hidden = i !== j;
    });
    window.scrollTo({ top: 0 });
  };
  botones.forEach((b, i) => {
    b.addEventListener('click', () => elegir(i));
    b.addEventListener('keydown', (e) => {
      const paso = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (paso === 0) return;
      const siguiente = (i + paso + botones.length) % botones.length;
      elegir(siguiente);
      botones[siguiente].focus();
    });
  });
  const pc = window.matchMedia('(min-width: 64rem)');
  const ajustar = () => {
    paneles.forEach((p) => {
      if (pc.matches) p.removeAttribute('role');
      else p.setAttribute('role', 'tabpanel');
    });
    if (pc.matches) pestanas.setAttribute('aria-hidden', 'true');
    else pestanas.removeAttribute('aria-hidden');
  };
  pc.addEventListener('change', ajustar);
  ajustar();
}
