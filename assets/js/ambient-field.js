(() => {
  "use strict";

  const canvas = document.getElementById("ambient-field");
  const button = document.getElementById("motion-toggle");
  const label = document.getElementById("motion-label");
  if (!canvas || !button || !label) return;

  let context;
  try {
    context = canvas.getContext("2d", { alpha: true });
  } catch (_) {
    return;
  }
  if (!context || !window.requestAnimationFrame || !window.matchMedia) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
  const frameInterval = 1000 / 30;
  const pointer = { x: 0, y: 0, active: false };
  let width = 0;
  let height = 0;
  let points = [];
  let edges = [];
  let elapsed = 0;
  let frame = 0;
  let lastFrameTime = null;
  let userPaused = false;

  // Fixed neighbor links keep the field sparse and its drawing cost linear.
  function sizeField() {
    width = Math.max(1, window.innerWidth);
    height = Math.max(1, window.innerHeight);
    const ratio = Math.min(window.devicePixelRatio || 1, 1.5);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);

    const mobile = width <= 760;
    const rows = mobile ? 11 : 12;
    const lanes = mobile ? 1 : 2;
    const margin = mobile ? 20 : width <= 1100 ? 36 : Math.max(56, (width - 1220) / 2);
    points = [];
    edges = [];

    for (let side = 0; side < 2; side += 1) {
      for (let row = 0; row < rows; row += 1) {
        for (let lane = 0; lane < lanes; lane += 1) {
          const index = points.length;
          points.push({
            side, lane, margin,
            v: (row + 0.5) / rows,
            phase: row * 0.46 + side * 1.7,
            x: 0, y: 0, offsetX: 0, offsetY: 0,
            radius: row % 4 === 0 ? 1.55 : 1.1,
          });
          if (row > 0) edges.push([index - lanes, index]);
          if (lane > 0 && row % 2 === 0) edges.push([index - 1, index]);
        }
      }
    }
    draw(0);
  }

  function draw(delta) {
    context.clearRect(0, 0, width, height);
    const easing = delta ? 1 - Math.exp(-delta * 5) : 1;
    const interactive = pointer.active && finePointer.matches && !userPaused && !reducedMotion.matches;

    points.forEach((point) => {
      const wave = Math.sin(point.v * Math.PI * 2.2 + elapsed * 0.12 + point.side);
      const depth = Math.cos(point.v * Math.PI * 1.4 - elapsed * 0.09);
      const laneOffset = point.lane ? 0.18 : -0.18;
      const distanceFromEdge = point.margin * (0.5 + laneOffset + wave * 0.2);
      const baseX = point.side ? width - distanceFromEdge : distanceFromEdge;
      const baseY = point.v * height + Math.sin(point.phase + elapsed * 0.15) * 9 + depth * 5;
      let targetX = 0;
      let targetY = 0;

      if (interactive) {
        const dx = baseX - pointer.x;
        const dy = baseY - pointer.y;
        const distance = Math.hypot(dx, dy);
        if (distance < 155 && distance > 0.01) {
          const force = Math.pow(1 - distance / 155, 2) * 20;
          targetX = dx / distance * force;
          targetY = dy / distance * force;
        }
      }

      point.offsetX += (targetX - point.offsetX) * easing;
      point.offsetY += (targetY - point.offsetY) * easing;
      // Pointer response stays inside the same gutters as the CSS container.
      const fromEdge = point.side ? width - baseX - point.offsetX : baseX + point.offsetX;
      const clamped = Math.max(3, Math.min(point.margin - 4, fromEdge));
      point.x = point.side ? width - clamped : clamped;
      point.y = baseY + point.offsetY;
    });

    context.lineWidth = 0.65;
    context.strokeStyle = "rgba(35, 75, 62, 0.075)";
    context.beginPath();
    edges.forEach(([from, to]) => {
      const a = points[from];
      const b = points[to];
      // Tall displays do not gain long decorative lines beside the text.
      if (Math.hypot(a.x - b.x, a.y - b.y) > 125) return;
      context.moveTo(a.x, a.y);
      context.lineTo(b.x, b.y);
    });
    context.stroke();

    points.forEach((point, index) => {
      context.fillStyle = index % 4 === 0 ? "rgba(35, 75, 62, 0.27)" : "rgba(112, 135, 111, 0.24)";
      context.beginPath();
      context.arc(point.x, point.y, point.radius, 0, Math.PI * 2);
      context.fill();
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
    // A plain action button: its visible label is also its accessible name.
    label.textContent = userPaused ? "Resume background motion" : "Pause background motion";
    button.hidden = reducedMotion.matches;

    if (isRunning()) {
      frame = window.requestAnimationFrame(animate);
    } else if (!document.hidden) {
      draw(0);
    }
  }

  button.addEventListener("click", () => {
    userPaused = !userPaused;
    updateMotion();
  });
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
