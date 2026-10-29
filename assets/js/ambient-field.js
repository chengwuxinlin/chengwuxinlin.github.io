(() => {
  "use strict";
  const canvas = document.getElementById("ambient-field");
  const button = document.getElementById("motion-toggle");
  const label = document.getElementById("motion-label");
  if (!canvas || !button || !label) return;
  let context;
  try { context = canvas.getContext("2d", { alpha: true }); } catch (_) { return; }
  if (!context || !window.requestAnimationFrame || !window.matchMedia) return;
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const pointer = { x: 0, y: 0, active: false, strength: 0 };
  const frameInterval = 1000 / 30;
  const tau = Math.PI * 2;
  let width = 0;
  let height = 0;
  let points = [];
  let edges = [];
  let elapsed = 0;
  let frame = 0;
  let lastFrameTime = null;
  let userPaused = false;

  function smoothstep(from, to, value) {
    const t = Math.max(0, Math.min(1, (value - from) / (to - from)));
    return t * t * (3 - 2 * t);
  }

  // Reproducible, irregular surface samples: no rows, rails, or mirrored lanes.
  function sampleSurface(count) {
    let seed = 38171;
    function random() {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      return seed / 4294967296;
    }
    const samples = [];
    const separation = 7 / count * 0.34;
    for (let attempt = 0; samples.length < count && attempt < count * 80; attempt += 1) {
      const u = random() * 2.8 - 1.4;
      const v = random() * 2.5 - 1.25;
      if (samples.some((p) => (u - p.u) ** 2 + (v - p.v) ** 2 < separation)) continue;
      samples.push({ u, v, phase: random() * tau, size: 0.8 + random() * 0.85, accent: samples.length % 31 === 0 });
    }
    return samples;
  }

  function buildEdges() {
    const links = new Map();
    points.forEach((a, i) => {
      const neighbors = points.map((b, j) => ({ j, distance: (a.u - b.u) ** 2 + (a.v - b.v) ** 2 }))
        .filter((n) => n.j !== i && n.distance < 0.22)
        .sort((a, b) => a.distance - b.distance).slice(0, 2);
      neighbors.forEach(({ j }) => {
        const first = Math.min(i, j);
        const last = Math.max(i, j);
        links.set(`${first}:${last}`, [first, last]);
      });
    });
    edges = Array.from(links.values());
  }

  function sizeField() {
    width = Math.max(1, window.innerWidth);
    height = Math.max(1, window.innerHeight);
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const mobile = width <= 760;
    const count = mobile ? Math.min(80, Math.max(54, Math.round(width * height / 6500)))
      : Math.min(220, Math.max(130, Math.round(width * height / 6500)));
    points = sampleSurface(count);
    buildEdges();
    draw(0);
  }

  // A shallow saddle with a long travelling wave, viewed obliquely in 3D.
  // All points and traces use this same surface, including pointer deformation.
  function project(u, v) {
    const phase = elapsed * 0.065;
    const z = 0.22 * (u * u - v * v) + 0.28 * Math.sin(2.4 * u + phase) * Math.cos(1.5 * v)
      + 0.1 * Math.sin(2 * v - phase * 0.6);
    const x = u * 0.94 + z * 0.342;
    const depth = -u * 0.342 + z * 0.94;
    const y = v * 0.825 - depth * 0.565;
    const rotatedDepth = v * 0.565 + depth * 0.825;
    const perspective = 1 / (1 + rotatedDepth * 0.16);
    let screenX = width * 0.5 + (x * 0.969 + y * 0.247) * width * 0.46 * perspective;
    let screenY = height * 0.5 + (-x * 0.247 + y * 0.969) * height * 0.58 * perspective;
    if (pointer.strength > 0.001) {
      const dx = screenX - pointer.x;
      const dy = screenY - pointer.y;
      const radius = Math.min(230, width * 0.3);
      const influence = Math.exp(-(dx * dx + dy * dy) / (radius * radius)) * pointer.strength;
      // A local bend follows the pointer; the sheet never collapses into it.
      screenX += (dx * 0.09 - dy * 0.035) * influence;
      screenY += (dy * 0.09 + dx * 0.035 - 15) * influence;
    }
    return { x: screenX, y: screenY, depth: Math.max(0, Math.min(1, (1.35 - rotatedDepth) / 2.7)) };
  }

  function draw(delta) {
    context.clearRect(0, 0, width, height);
    const interactive = pointer.active && finePointer.matches && !userPaused && !reducedMotion.matches;
    const target = interactive ? 1 : 0;
    pointer.strength += (target - pointer.strength) * (delta ? 1 - Math.exp(-delta * 3) : 1);
    // Two nonparallel curves reveal the surface without a repeated wire grid.
    context.lineWidth = 0.8;
    [-0.63, 0.47].forEach((offset, trace) => {
      context.beginPath();
      for (let step = 0; step <= 72; step += 1) {
        const u = -1.45 + step / 72 * 2.9;
        const v = offset + 0.22 * Math.sin(u * 1.8 + trace * 1.4 + elapsed * 0.025);
        const p = project(u, v);
        if (!step) context.moveTo(p.x, p.y);
        else context.lineTo(p.x, p.y);
      }
      context.strokeStyle = trace ? "rgba(135, 114, 70, 0.06)" : "rgba(35, 75, 62, 0.075)";
      context.stroke();
    });

    points.forEach((point) => {
      const u = ((point.u + 1.4 + elapsed * 0.012) % 2.8) - 1.4;
      const v = point.v + Math.sin(elapsed * 0.09 + point.phase) * 0.035;
      const projected = project(u, v);
      point.x = projected.x;
      point.y = projected.y;
      point.depth = projected.depth;
      point.fade = smoothstep(0, 0.2, 1.4 - Math.abs(u));
    });
    const maxLength = width <= 760 ? 92 : 150;
    context.lineWidth = 0.7;
    edges.forEach(([from, to]) => {
      const a = points[from];
      const b = points[to];
      const distance = Math.hypot(a.x - b.x, a.y - b.y);
      if (distance > maxLength) return;
      const alpha = (0.04 + (a.depth + b.depth) * 0.027) * (1 - smoothstep(maxLength * 0.55, maxLength, distance))
        * Math.min(a.fade, b.fade);
      context.strokeStyle = `rgba(35, 75, 62, ${alpha})`;
      context.beginPath();
      context.moveTo(a.x, a.y);
      context.lineTo(b.x, b.y);
      context.stroke();
    });
    points.forEach((point) => {
      const alpha = (0.15 + point.depth * 0.19) * point.fade;
      const radius = point.size * (0.7 + point.depth * 0.55);
      context.fillStyle = point.accent ? `rgba(160, 121, 58, ${alpha})` : `rgba(35, 75, 62, ${alpha})`;
      context.beginPath();
      context.arc(point.x, point.y, radius, 0, tau);
      context.fill();
      if (point.accent && point.depth > 0.5) {
        context.strokeStyle = `rgba(160, 121, 58, ${alpha * 0.3})`;
        context.beginPath();
        context.arc(point.x, point.y, radius + 3, 0, tau);
        context.stroke();
      }
    });
  }

  function isRunning() {
    return !userPaused && !reducedMotion.matches && !document.hidden;
  }
  function animate(timestamp) {
    frame = 0;
    if (!isRunning()) return;
    if (lastFrameTime === null) lastFrameTime = timestamp - frameInterval;
    const difference = timestamp - lastFrameTime;
    if (difference >= frameInterval - 0.1) {
      const delta = Math.min(difference, 66) / 1000;
      elapsed += delta;
      draw(delta);
      lastFrameTime = timestamp;
    }
    frame = window.requestAnimationFrame(animate);
  }
  function updateMotion() {
    if (frame) window.cancelAnimationFrame(frame);
    frame = 0;
    lastFrameTime = null;
    pointer.active = false;
    label.textContent = userPaused ? "Resume background motion" : "Pause background motion";
    button.hidden = reducedMotion.matches;
    if (isRunning()) frame = window.requestAnimationFrame(animate);
    else if (!document.hidden) draw(0);
  }
  button.addEventListener("click", () => { userPaused = !userPaused; updateMotion(); });
  window.addEventListener("pointermove", (event) => {
    if (!isRunning() || !finePointer.matches || event.pointerType !== "mouse") return;
    pointer.x = event.clientX;
    pointer.y = event.clientY;
    pointer.active = true;
  }, { passive: true });
  document.documentElement.addEventListener("pointerleave", () => { pointer.active = false; }, { passive: true });
  window.addEventListener("blur", () => { pointer.active = false; });
  window.addEventListener("resize", sizeField, { passive: true });
  document.addEventListener("visibilitychange", updateMotion);
  function listenToPreference(query, listener) {
    if (query.addEventListener) query.addEventListener("change", listener);
    else if (query.addListener) query.addListener(listener);
  }
  listenToPreference(reducedMotion, updateMotion);
  listenToPreference(finePointer, () => { pointer.active = false; });
  sizeField();
  updateMotion();
})();
