(() => {
  'use strict';

  const ui = document.querySelector('#map-ui');
  const svg = document.querySelector('#map-field');
  const world = document.querySelector('#map-world');
  const details = document.querySelector('#map-detail');
  const initialDetail = details.firstElementChild.cloneNode(true);
  const status = document.querySelector('#map-announcement');
  const nodeSelect = document.querySelector('#select-node');
  const edgeSelect = document.querySelector('#select-edge');
  const relations = document.querySelector('#nessi');
  const listButton = document.querySelector('#toggle-relations');
  const pauseButton = ui.querySelector('[data-action="pause"]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const compact = matchMedia('(max-width: 720px)');

  // Coordinate di partenza per la lettura delle componenti disconnesse.
  // Le quattro coordinate indicano x/y relativi su schermo ampio e stretto.
  const layout = [
    [.47, .35, .30, .205],  // Interlocutore assente
    [.38, .19, .24, .085],  // Cheng
    [.28, .46, .30, .33],   // Rappresentazione
    [.14, .23, .20, .445],  // Shannon
    [.10, .49, .47, .44],   // Morin
    [.16, .70, .68, .349],  // Kahneman
    [.75, .52, .29, .62],   // Glickman · Sharot
    [.84, .34, .69, .59],   // Abitudine
    [.87, .70, .69, .72],   // Mediazione che educa
    [.24, .84, .24, .83],   // Lyell · Coiera
    [.39, .79, .66, .84],   // Complessità
    [.73, .16, .25, .935],  // Foucault
    [.88, .20, .69, .94],   // Interpretazione di sé
    [.53, .14, .73, .09],   // Saggio 00
    [.61, .29, .73, .195],  // Sapersi correggere
    [.59, .61, .77, .46],   // Saggio 08
  ];
  const marks = {
    evidenza: ['', 'M -3 0 a 3 3 0 1 0 6 0 a 3 3 0 1 0 -6 0'],
    intuizione: ['2 4', 'M -3 0 H 3 M 0 -3 V 3'],
    interpretazione: ['7 5', 'M -2.8 -2.8 H 2.8 V 2.8 H -2.8 Z'],
    controcaso: ['12 4 2 4', 'M 0 -4 L 4 0 L 0 4 L -4 0 Z'],
    ipotesi: ['1 6', 'M -4 0 H 4'],
    rovesciamento: ['10 3 3 3', 'M 0 -4 L 4 3 H -4 Z'],
  };
  const tension = new Set([0, 2, 8, 14]);
  const strings = document.documentElement.lang === 'en' ? {
    pause: 'Pause',
    resume: 'Resume',
    pauseLabel: 'Pause movement',
    resumeLabel: 'Resume movement',
    showList: 'Read all connections',
    hideList: 'Close the list of connections',
    selectedNode: name => `Node selected. ${name}`,
    selectedEdge: label => `Connection selected. ${label}`,
    cleared: 'Selection cleared.',
  } : {
    pause: 'Pausa',
    resume: 'Riprendi',
    pauseLabel: 'Metti in pausa il movimento',
    resumeLabel: 'Riprendi il movimento',
    showList: 'Leggi tutti i nessi',
    hideList: 'Chiudi l’elenco dei nessi',
    selectedNode: name => `Nodo selezionato. ${name}`,
    selectedEdge: label => `Nesso selezionato. ${label}`,
    cleared: 'Selezione annullata.',
  };
  const points = new Map();
  const seenTypes = new Set();
  const edgesGroup = svg.querySelector('.map-edges');
  const pointsGroup = svg.querySelector('.map-points');
  const orbitGroup = svg.querySelector('.map-orbits');
  let width = 0;
  let height = 0;
  let scale = 1;
  let offsetX = 0;
  let offsetY = 0;
  let selectedNode = null;
  let selectedEdge = null;
  let gesture = null;
  let paused = motion.matches;
  let visible = false;
  let frame = 0;
  let remaining = 0;
  let lastStep = 0;

  function svgElement(tag, attributes, parent) {
    const element = document.createElementNS('http://www.w3.org/2000/svg', tag);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    parent.append(element);
    return element;
  }

  function point(name) {
    if (points.has(name)) return points.get(name);
    const index = points.size;
    const group = svgElement('g', {class: 'map-point', 'data-point': index}, pointsGroup);
    group.classList.toggle('is-tension', tension.has(index));
    svgElement('circle', {r: 17, fill: 'transparent'}, group);
    svgElement('circle', {r: 10, class: 'point-ring'}, group);
    svgElement('circle', {r: 4, class: 'point-core'}, group);
    const label = svgElement('text', {'text-anchor': 'middle', y: 22}, group);
    label.textContent = name;
    nodeSelect.add(new Option(name, index));
    const node = {index, name, group, label, x: 0, y: 0, vx: 0, vy: 0, homeX: 0, homeY: 0, labelWidth: 0};
    points.set(name, node);
    return node;
  }

  const edges = [...relations.querySelectorAll('li[data-tipo]')].map((item, index) => {
    const {da, a, tipo} = item.dataset;
    const label = item.querySelector('h3').textContent;
    const [dash, shape] = marks[tipo];
    const group = svgElement('g', {class: 'map-edge ' + tipo, 'data-edge': index}, edgesGroup);
    const hit = svgElement('line', {stroke: 'transparent', 'stroke-width': 18}, group);
    const line = svgElement('line', {class: 'edge-line', 'stroke-dasharray': dash}, group);
    const mark = svgElement('path', {class: 'edge-mark', d: shape}, group);
    if (!seenTypes.has(tipo)) {
      const entry = document.createElement('li');
      const sample = svgElement('svg', {viewBox: '0 0 34 12', width: 34, height: 12, 'aria-hidden': 'true'}, entry);
      const swatch = svgElement('g', {class: 'map-edge ' + tipo}, sample);
      svgElement('line', {x1: 0, x2: 34, y1: 6, y2: 6, class: 'edge-line', 'stroke-dasharray': dash}, swatch);
      svgElement('path', {class: 'edge-mark', d: shape, transform: 'translate(17 6)'}, swatch);
      entry.append(item.querySelector('.relation-type').textContent.trim());
      ui.querySelector('.map-legend').append(entry);
      seenTypes.add(tipo);
    }
    edgeSelect.add(new Option(label, index));
    return {index, label, item, a: point(da), b: point(a), group, hit, line, mark, rest: 0};
  });
  const nodes = [...points.values()];
  const orbits = [-28, 16, 52].map(() => svgElement('ellipse', {}, orbitGroup));

  function syncViewport() {
    const limitX = width * (.18 + (scale - 1) / 2);
    const limitY = height * (.18 + (scale - 1) / 2);
    offsetX = Math.max(-limitX, Math.min(limitX, offsetX));
    offsetY = Math.max(-limitY, Math.min(limitY, offsetY));
    world.setAttribute('transform', `translate(${width / 2 + offsetX},${height / 2 + offsetY}) scale(${scale}) translate(${-width / 2},${-height / 2})`);
  }

  function draw() {
    for (const {a, b, line, hit, mark} of edges) {
      for (const segment of [line, hit]) {
        segment.setAttribute('x1', a.x);
        segment.setAttribute('y1', a.y);
        segment.setAttribute('x2', b.x);
        segment.setAttribute('y2', b.y);
      }
      mark.setAttribute('transform', `translate(${(a.x + b.x) / 2},${(a.y + b.y) / 2})`);
    }
    for (const n of nodes) n.group.setAttribute('transform', `translate(${n.x},${n.y})`);
  }

  function constrain(n) {
    const margin = Math.min(width / 2, n.labelWidth / 2 + 8);
    n.x = Math.max(margin, Math.min(width - margin, n.x));
    n.y = Math.max(19, Math.min(height - 30, n.y));
  }

  function arrange() {
    const bounds = svg.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    width = bounds.width;
    height = bounds.height;
    svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
    const variant = compact.matches ? 2 : 0;
    for (const node of nodes) {
      const position = layout[node.index];
      node.labelWidth = node.label.getComputedTextLength();
      node.x = width * position[variant];
      node.y = height * position[variant + 1];
      node.vx = node.vy = 0;
      constrain(node);
      node.homeX = node.x;
      node.homeY = node.y;
    }
    for (const edge of edges) {
      edge.rest = Math.max(46, Math.hypot(edge.a.x - edge.b.x, edge.a.y - edge.b.y) * .91);
    }
    orbits.forEach((orbit, index) => {
      orbit.setAttribute('cx', width * .46);
      orbit.setAttribute('cy', height * .49);
      orbit.setAttribute('rx', Math.min(width * .43, 360) * (1 - .12 * index));
      orbit.setAttribute('ry', Math.min(height * .30, 143) * (.62 + .18 * index));
      orbit.setAttribute('transform', `rotate(${[-28, 16, 52][index]} ${width * .46} ${height * .49})`);
    });
    syncViewport();
    draw();
    wake(160);
  }

  function simulate() {
    const held = gesture?.node;
    for (let i = 0; i < nodes.length; i += 1) {
      const a = nodes[i];
      for (let j = i + 1; j < nodes.length; j += 1) {
        const b = nodes[j];
        const dx = a.x - b.x || .01;
        const dy = a.y - b.y || .01;
        const distance = Math.hypot(dx, dy);
        const repulsion = Math.min(6, 1750 / Math.max(120, distance ** 2));
        let fx = dx * repulsion / distance;
        let fy = dy * repulsion / distance;

        // Collisione tra le aree che comprendono sia il punto sia l’etichetta.
        const overlapX = (a.labelWidth + b.labelWidth) / 2 + 10 - Math.abs(dx);
        const overlapY = 42 - Math.abs(dy);
        if (overlapX > 0 && overlapY > 0) {
          if (overlapX < overlapY) fx += Math.sign(dx) * overlapX * .12;
          else fy += Math.sign(dy) * overlapY * .12;
        }
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }
    }
    for (const {a, b, rest} of edges) {
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const distance = Math.hypot(dx, dy) || 1;
      const spring = (distance - rest) * .028 / distance;
      a.vx += dx * spring;
      a.vy += dy * spring;
      b.vx -= dx * spring;
      b.vy -= dy * spring;
    }
    let speed = 0;
    for (const n of nodes) {
      if (n === held) {
        n.vx = n.vy = 0;
        continue;
      }
      n.vx = (n.vx + (n.homeX - n.x) * .019 + (width * .5 - n.x) * .0006) * .78;
      n.vy = (n.vy + (n.homeY - n.y) * .019 + (height * .5 - n.y) * .0006) * .78;
      n.x += n.vx;
      n.y += n.vy;
      constrain(n);
      speed = Math.max(speed, Math.hypot(n.vx, n.vy));
    }
    return speed;
  }

  function canRun() {
    return visible && !paused && !document.hidden;
  }

  function schedule() {
    if (!frame && remaining > 0 && canRun()) frame = requestAnimationFrame(tick);
  }

  function tick(time) {
    frame = 0;
    if (!canRun()) return;
    if (time - lastStep >= 15) {
      lastStep = time;
      const speed = simulate();
      draw();
      remaining = speed < .045 ? 0 : remaining - 1;
    }
    schedule();
  }

  function wake(steps) {
    remaining = Math.max(remaining, steps);
    schedule();
  }

  function stop() {
    cancelAnimationFrame(frame);
    frame = 0;
  }

  function setPaused(value) {
    paused = value;
    pauseButton.textContent = paused ? strings.resume : strings.pause;
    pauseButton.setAttribute('aria-label', paused ? strings.resumeLabel : strings.pauseLabel);
    if (paused) stop();
    else wake(90);
  }

  function select(node, edge) {
    selectedNode = node;
    selectedEdge = edge;
    nodeSelect.value = node ? node.index : '';
    edgeSelect.value = edge ? edge.index : '';
    for (const item of nodes) item.group.classList.toggle('active', item === node || item === edge?.a || item === edge?.b);
    for (const item of edges) item.group.classList.toggle('active', edge ? item === edge : item.a === node || item.b === node);

    if (edge) {
      details.replaceChildren(...[...edge.item.children].map(child => child.cloneNode(true)));
    } else if (node) {
      const heading = document.createElement('h3');
      heading.textContent = node.name;
      const list = document.createElement('ul');
      for (const item of edges.filter(item => item.a === node || item.b === node)) {
        const row = document.createElement('li');
        const button = document.createElement('button');
        button.type = 'button';
        button.dataset.chooseEdge = item.index;
        button.textContent = item.label;
        row.append(button);
        list.append(row);
      }
      details.replaceChildren(heading, list);
    } else {
      details.replaceChildren(initialDetail.cloneNode(true));
    }
    status.textContent = edge ? strings.selectedEdge(edge.label) : node ? strings.selectedNode(node.name) : strings.cleared;
  }

  nodeSelect.addEventListener('change', () => select(nodes[nodeSelect.value === '' ? -1 : nodeSelect.value] ?? null, null));
  edgeSelect.addEventListener('change', () => select(selectedNode, edges[edgeSelect.value === '' ? -1 : edgeSelect.value] ?? null));
  details.addEventListener('click', event => {
    const button = event.target.closest('[data-choose-edge]');
    if (!button) return;
    select(selectedNode, edges[button.dataset.chooseEdge]);
    const heading = details.querySelector('h3');
    heading.tabIndex = -1;
    heading.focus({preventScroll: true});
  });
  listButton.addEventListener('click', () => {
    relations.hidden = !relations.hidden;
    listButton.setAttribute('aria-expanded', String(!relations.hidden));
    listButton.textContent = relations.hidden ? strings.showList : strings.hideList;
  });

  const pans = {left: [48, 0], right: [-48, 0], up: [0, 48], down: [0, -48]};
  ui.querySelector('.map-tools').addEventListener('click', event => {
    const action = event.target.closest('button')?.dataset.action;
    if (action === 'pause') setPaused(!paused);
    if (action === 'reset') {
      scale = 1;
      offsetX = offsetY = 0;
      select(null, null);
      arrange();
    }
    if (action === 'plus' || action === 'minus') {
      const prior = scale;
      scale = Math.max(.8, Math.min(2.5, scale * (action === 'plus' ? 1.25 : .8)));
      offsetX *= scale / prior;
      offsetY *= scale / prior;
    }
    if (action in pans) {
      offsetX += pans[action][0];
      offsetY += pans[action][1];
    }
    syncViewport();
  });

  svg.addEventListener('pointerdown', event => {
    if (gesture || !event.isPrimary || event.button !== 0) return;
    const nodeTarget = event.target.closest('[data-point]');
    const edgeTarget = event.target.closest('[data-edge]');
    if (edgeTarget) {
      select(null, edges[edgeTarget.dataset.edge]);
      return;
    }
    if (!nodeTarget && event.pointerType !== 'mouse') return;
    const node = nodeTarget ? nodes[nodeTarget.dataset.point] : null;
    if (node) select(node, null);
    gesture = {id: event.pointerId, node, x: event.clientX, y: event.clientY};
    svg.setPointerCapture(event.pointerId);
    svg.classList.add('is-dragging');
  });

  svg.addEventListener('pointermove', event => {
    if (event.pointerId !== gesture?.id) return;
    const dx = event.clientX - gesture.x;
    const dy = event.clientY - gesture.y;
    gesture.x = event.clientX;
    gesture.y = event.clientY;
    if (gesture.node) {
      gesture.node.x += dx / scale;
      gesture.node.y += dy / scale;
      constrain(gesture.node);
      draw();
      wake(105);
    } else {
      offsetX += dx;
      offsetY += dy;
      syncViewport();
    }
  });

  function finish(event) {
    if (event.pointerId !== gesture?.id) return;
    gesture = null;
    svg.classList.remove('is-dragging');
    wake(105);
  }

  for (const event of ['pointerup', 'pointercancel', 'lostpointercapture']) svg.addEventListener(event, finish);
  motion.addEventListener('change', event => setPaused(event.matches));
  document.addEventListener('visibilitychange', () => canRun() ? schedule() : stop());
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    if (canRun()) schedule();
    else stop();
  }).observe(svg);

  relations.hidden = true;
  ui.hidden = false;
  setPaused(paused);
  new ResizeObserver(arrange).observe(svg);
})();
