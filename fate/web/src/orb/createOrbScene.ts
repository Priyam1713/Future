import {
  Application,
  Assets,
  Container,
  Filter,
  Graphics,
  Sprite,
  Texture,
} from "pixi.js";
import "pixi.js/unsafe-eval";
import { orbVertex, orbFragment } from "./shaders";
import {
  initialQuality,
  percentile,
  QUALITY,
  resolutionFor,
  type Quality,
} from "./policy";
export interface OrbMotion {
  reduced: boolean;
  paused: boolean;
}
export interface OrbController {
  update: (motion: OrbMotion) => void;
  destroy: () => void;
  /** Used by the offline art pipeline; never captures React text or controls. */
  snapshot: () => Promise<string>;
}

function noiseCanvas() {
  const canvas = document.createElement("canvas");
  canvas.width = canvas.height = 64;
  const ctx = canvas.getContext("2d")!,
    data = ctx.createImageData(64, 64);
  let seed = 872139;
  for (let i = 0; i < data.data.length; i += 4) {
    for (let channel = 0; channel < 3; channel++) {
      seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
      data.data[i + channel] = seed >>> 24;
    }
    data.data[i + 3] = 255;
  }
  ctx.putImageData(data, 0, 0);
  return canvas;
}
export async function createOrbScene(
  host: HTMLDivElement,
  motion: OrbMotion,
  signal: AbortSignal,
  onContext: (available: boolean) => void,
): Promise<OrbController> {
  const app = new Application();
  let initialized = false,
    destroyed = false;
  let noise: Texture | undefined, filter: Filter | undefined;
  const disposers: (() => void)[] = [];
  function destroy() {
    if (destroyed) return;
    destroyed = true;
    disposers.forEach((fn) => fn());
    if (initialized) app.destroy(true, { children: true, texture: false });
    filter?.destroy();
    noise?.destroy(true);
  }
  // Listen before renderer/texture awaits: leaving during a slow texture fetch
  // must release an already initialized renderer, not wait for that fetch.
  signal.addEventListener("abort", destroy, { once: true });
  disposers.push(()=>signal.removeEventListener("abort",destroy));
  try {
    let quality: Quality = initialQuality();
    const texturesPending = Promise.all([
      Assets.load("/art/fate_orrery.svg"),
      Assets.load("/art/nebula-v1.webp"),
    ]);
    const initialization = app
      .init({
        width: 600,
        height: 600,
        resolution: resolutionFor(host.clientWidth, quality),
        autoDensity: true,
        backgroundAlpha: 0,
        antialias: false,
        preference: "webgl",
        powerPreference: "low-power",
        autoStart: false,
      })
      .then(() => {
        initialized = true;
        if (destroyed || signal.aborted) {
          app.destroy(true, { children: true, texture: false });
          initialized = false;
          throw new DOMException("Aborted", "AbortError");
        }
      });
    const [, [ringTexture, nebulaTexture]] = await Promise.all([
      initialization,
      texturesPending,
    ]);
    if (signal.aborted) {
      destroy();
      throw new DOMException("Aborted", "AbortError");
    }
    if (signal.aborted) {
      destroy();
      throw new DOMException("Aborted", "AbortError");
    }
    noise = Texture.from(noiseCanvas());
    const touch = new Float32Array(2);
    filter = Filter.from({
      gl: { vertex: orbVertex, fragment: orbFragment },
      resources: {
        uNoise: noise.source,
        uNebula: nebulaTexture.source,
        orbUniforms: {
          uTime: { value: 0, type: "f32" },
          uTouch: { value: touch, type: "vec2<f32>" },
          uPulse: { value: 0, type: "f32" },
          uDetail: { value: QUALITY[quality].detail, type: "f32" },
        },
      },
    });
    const root = new Container();
    root.position.set(300, 300);
    app.stage.addChild(root);
    const backRing = new Graphics()
      .ellipse(0, 0, 262, 103)
      .stroke({ color: 0xb7a06c, width: 1, alpha: 0.38 });
    backRing.rotation = -0.53;
    root.addChild(backRing);
    const body = new Sprite(Texture.WHITE);
    body.anchor.set(0.5);
    body.width = body.height = 600;
    body.filters = [filter];
    root.addChild(body);
    const innerDust = new Container();
    root.addChild(innerDust);
    const particles = Array.from({ length: 36 }, (_, i) => {
      const dot = new Graphics()
        .circle(0, 0, i % 9 === 0 ? 1.5 : 0.65)
        .fill({ color: i % 3 === 0 ? 0xd8c391 : 0x96c9cd, alpha: 0.7 });
      innerDust.addChild(dot);
      return dot;
    });
    const rings = new Sprite(ringTexture);
    rings.anchor.set(0.5);
    rings.width = rings.height = 558;
    rings.alpha = 0.64;
    root.addChild(rings);
    const nearRing = new Graphics()
      .ellipse(0, 0, 263, 96)
      .stroke({ color: 0xd9c18c, width: 0.8, alpha: 0.3 });
    nearRing.rotation = 0.65;
    root.addChild(nearRing);
    const uniforms = filter.resources.orbUniforms.uniforms;
    host.appendChild(app.canvas);
    app.canvas.setAttribute("aria-hidden", "true");
    let visible = true,
      lost = false,
      active = false,
      t = 0,
      pulse = 0,
      targetX = 0,
      targetY = 0,
      x = 0,
      y = 0;
    let frames = 0,
      lastFrame = 0,
      windowStart = performance.now(),
      samples: number[] = [],
      adaptiveWindows = 0;
    function resize() {
      if (destroyed) return;
      app.renderer.resolution = resolutionFor(host.clientWidth, quality);
      app.renderer.resize(600, 600);
      host.dataset.resolution = app.renderer.resolution.toFixed(3);
      if (!active && !lost) app.render();
    }
    function applyQuality() {
      app.ticker.maxFPS = QUALITY[quality].fps;
      uniforms.uDetail = QUALITY[quality].detail;
      particles.forEach(
        (dot, i) => (dot.visible = i < QUALITY[quality].particles),
      );
      host.dataset.quality = quality;
      host.dataset.targetFps = String(QUALITY[quality].fps);
      resize();
    }
    function frame() {
      const dt = Math.min(app.ticker.deltaMS / 1000, 0.05);
      if (active) {
        t += dt;
        const damping = 1 - Math.exp(-dt * 5);
        x += (targetX - x) * damping;
        y += (targetY - y) * damping;
        pulse *= Math.exp(-dt * 1.8);
      }
      root.position.set(300 + x * 9, 300 + y * 7);
      touch[0] = x;
      touch[1] = y;
      uniforms.uTime = t;
      uniforms.uPulse = pulse;
      rings.rotation = t * 0.006;
      rings.scale.y = (558 / ringTexture.height) * (1 + y * 0.025);
      backRing.rotation = -0.53 + Math.sin(t * 0.027) * 0.065;
      nearRing.rotation = 0.65 - Math.sin(t * 0.024) * 0.09;
      nearRing.scale.y = 1 + Math.sin(t * 0.031) * 0.055;
      particles.forEach((dot, i) => {
        if (!dot.visible) return;
        const a = i * 2.39996 + t * (i % 2 ? -0.009 : 0.012),
          r = 70 + ((i * 37) % 120);
        dot.position.set(
          Math.cos(a) * r + x * ((i % 4) + 1) * 1.7,
          Math.sin(a) * r * 0.88 + y * ((i % 3) + 1) * 2,
        );
        dot.alpha = 0.12 + (Math.sin(i * 3 + t * 0.34) + 1) * 0.12;
      });
      if (!active) return;
      frames++;
      const now = performance.now();
      if (lastFrame) samples.push(now - lastFrame);
      lastFrame = now;
      if (now - windowStart >= 1000 && samples.length) {
        const mean = samples.reduce((a, b) => a + b, 0) / samples.length;
        host.dataset.metrics = JSON.stringify({
          frames,
          fps: Number((1000 / mean).toFixed(1)),
          p50FrameMs: Number(percentile(samples, 0.5).toFixed(2)),
          p95FrameMs: Number(percentile(samples, 0.95).toFixed(2)),
          quality,
          resolution: app.renderer.resolution,
          targetFps: QUALITY[quality].fps,
          logicalSize: 600,
          bufferWidth: app.canvas.width,
        });
        adaptiveWindows++;
        if (adaptiveWindows >= 3 && mean > 19 && quality !== "low") {
          quality =
            quality === "cinematic"
              ? "balanced"
              : quality === "balanced"
                ? "economy"
                : "low";
          adaptiveWindows = 0;
          applyQuality();
        }
        samples = [];
        windowStart = now;
      }
    }
    function sync() {
      if (destroyed) return;
      const next =
        visible &&
        !document.hidden &&
        !lost &&
        !motion.reduced &&
        !motion.paused;
      host.dataset.renderState = next
        ? "running"
        : lost
          ? "context-lost"
          : "still";
      if (next === active) return;
      active = next;
      if (active) {
        lastFrame = 0;
        samples = [];
        windowStart = performance.now();
        app.start();
      } else {
        app.stop();
        if (visible && !document.hidden && !lost) {
          frame();
          app.render();
        }
      }
    }
    function contextLost(event: Event) {
      event.preventDefault();
      lost = true;
      onContext(false);
      sync();
    }
    function contextRestored() {
      lost = false;
      onContext(true);
      sync();
    }
    app.canvas.addEventListener("webglcontextlost", contextLost);
    app.canvas.addEventListener("webglcontextrestored", contextRestored);
    const pointer = (event: PointerEvent) => {
      if (motion.reduced || motion.paused) return;
      const r = host.getBoundingClientRect();
      targetX = Math.max(
        -1,
        Math.min(1, ((event.clientX - r.left) / r.width - 0.5) * 2),
      );
      targetY = Math.max(
        -1,
        Math.min(1, ((event.clientY - r.top) / r.height - 0.5) * 2),
      );
    };
    const leave = () => {
        targetX = targetY = 0;
      },
      press = (event: PointerEvent) => {
        pointer(event);
        if (!motion.reduced && !motion.paused) pulse = 0.8;
      };
    host.addEventListener("pointermove", pointer);
    host.addEventListener("pointerleave", leave);
    host.addEventListener("pointerdown", press);
    host.addEventListener("pointerup", leave);
    const observer = new IntersectionObserver(
      (entries) => {
        visible = entries[0].isIntersecting;
        sync();
      },
      { threshold: 0.03 },
    );
    observer.observe(host);
    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(host);
    document.addEventListener("visibilitychange", sync);
    disposers.push(() => {
      observer.disconnect();
      resizeObserver.disconnect();
      document.removeEventListener("visibilitychange", sync);
      host.removeEventListener("pointermove", pointer);
      host.removeEventListener("pointerleave", leave);
      host.removeEventListener("pointerdown", press);
      host.removeEventListener("pointerup", leave);
      app.canvas.removeEventListener("webglcontextlost", contextLost);
      app.canvas.removeEventListener("webglcontextrestored", contextRestored);
    });
    applyQuality();
    frame();
    app.render();
    app.ticker.add(frame);
    sync();
    onContext(true);
    return {
      update(next) {
        motion = next;
        sync();
      },
      destroy,
      snapshot: () =>
        app.renderer.extract.base64({ target: app.stage, format: "png" }),
    };
  } catch (error) {
    destroy();
    throw error;
  }
}
