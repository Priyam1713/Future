import { useEffect, useRef, useState } from "react";

// Loaded after the immediately visible asset composition. React owns all controls.
export default function Orb({
  reduced,
  paused,
}: {
  reduced: boolean;
  paused: boolean;
}) {
  const host = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const settings = useRef({ reduced, paused });
  settings.current = { reduced, paused };
  useEffect(() => {
    let disposed = false,
      cleanup = () => {};
    const element = host.current!;
    void (async () => {
      const { Application, Assets, Sprite, Container, Graphics, Filter } =
        await import("pixi.js");
      // Pixi's CSP adapter replaces generated eval functions with static polyfills.
      await import("pixi.js/unsafe-eval");
      if (disposed) return;
      const app = new Application();
      await app.init({
        width: 600,
        height: 600,
        backgroundAlpha: 0,
        antialias: true,
        resolution: Math.min(devicePixelRatio, 1.5),
        autoDensity: true,
        preference: "webgl",
        powerPreference: "low-power",
      });
      if (disposed) {
        app.destroy(true);
        return;
      }
      cleanup = () => {
        app.destroy(true, { children: true, texture: false });
      };
      const [coreTexture, ringTexture] = await Promise.all([
        Assets.load("/art/fate_orb_core.png"),
        Assets.load("/art/fate_orrery.svg"),
      ]);
      if (disposed) return;
      const scene = new Container();
      scene.position.set(300, 300);
      app.stage.addChild(scene);
      const core = new Sprite(coreTexture);
      core.anchor.set(0.5);
      core.width = core.height = 462;
      const fog = Filter.from({
        gl: {
          vertex: `
        precision highp float;
        in vec2 aPosition; out vec2 vTextureCoord;
        uniform vec4 uInputSize; uniform vec4 uOutputFrame; uniform vec4 uOutputTexture;
        void main(){ vec2 p=aPosition*uOutputFrame.zw+uOutputFrame.xy;
          p.x=p.x*(2.0/uOutputTexture.x)-1.0;
          p.y=p.y*(2.0*uOutputTexture.z/uOutputTexture.y)-uOutputTexture.z;
          gl_Position=vec4(p,0.,1.); vTextureCoord=aPosition*(uOutputFrame.zw*uInputSize.zw); }`,
          fragment: `
        precision highp float;
        in vec2 vTextureCoord; out vec4 finalColor; uniform sampler2D uTexture;
        uniform vec4 uInputSize; uniform vec4 uOutputFrame;
        uniform float uTime; uniform vec2 uTouch; uniform float uPulse;
        float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
        float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);
          return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
        void main(){
          vec2 uv=vTextureCoord*uInputSize.xy/uOutputFrame.zw;
          vec2 p=uv-.5; float r=length(p); float inside=1.-smoothstep(.40,.47,r);
          vec2 wave=vec2(sin(p.y*18.+uTime*.3),cos(p.x*17.-uTime*.27))*.006*inside;
          vec2 bend=(p*.012*sin(r*18.-uTime*.4)+uTouch*.006)*inside;
          vec2 coord=clamp(vTextureCoord+(wave+bend)*uOutputFrame.zw*uInputSize.zw,vec2(0),uOutputFrame.zw*uInputSize.zw);
          vec4 base=texture(uTexture,coord);
          float n=noise(p*5.+vec2(uTime*.055,-uTime*.04));
          float n2=noise(p*10.+n*2.-uTime*.035);
          float mist=smoothstep(.3,.8,n*.6+n2*.4)*inside;
          vec3 tint=vec3(.16,.12,.33)*mist*.32+vec3(.14,.09,.025)*uPulse*inside;
          finalColor=vec4(base.rgb+tint*base.a,base.a);
        }`,
        },
        resources: {
          orbUniforms: {
            uTime: { value: 0, type: "f32" },
            uTouch: { value: new Float32Array([0, 0]), type: "vec2<f32>" },
            uPulse: { value: 0, type: "f32" },
          },
        },
      });
      core.filters = [fog];
      scene.addChild(core);
      const rings = new Sprite(ringTexture);
      rings.anchor.set(0.5);
      rings.width = rings.height = 558;
      scene.addChild(rings);
      const nearRing = new Graphics()
        .ellipse(0, 0, 248, 101)
        .stroke({ color: 0xd9bd83, width: 0.7, alpha: 0.26 });
      scene.addChild(nearRing);
      const orbit = new Container();
      scene.addChild(orbit);
      for (let i = 0; i < 40; i++) {
        const a = i * 2.39996,
          r = 245 + Math.sin(i * 9) * 28;
        const dot = new Graphics()
          .circle(0, 0, i % 9 === 0 ? 2 : 1)
          .fill({ color: 0xe5c88b, alpha: i % 9 === 0 ? 0.8 : 0.25 });
        dot.position.set(Math.cos(a) * r, Math.sin(a) * r);
        orbit.addChild(dot);
      }
      element.appendChild(app.canvas);
      app.canvas.setAttribute("aria-hidden", "true");
      let targetX = 0,
        targetY = 0,
        x = 0,
        y = 0,
        pulse = 0,
        t = 0;
      const pointer = (e: PointerEvent) => {
        const r = element.getBoundingClientRect();
        targetX = (e.clientX - r.left) / r.width - 0.5;
        targetY = (e.clientY - r.top) / r.height - 0.5;
      };
      const leave = () => {
        targetX = targetY = 0;
      };
      const press = () => {
        pulse = 1;
      };
      element.addEventListener("pointermove", pointer);
      element.addEventListener("pointerleave", leave);
      element.addEventListener("pointerdown", press);
      const render = () => {
        const moving = !settings.current.reduced && !settings.current.paused;
        if (moving) {
          t += app.ticker.deltaMS / 1000;
          x += (targetX - x) * 0.035;
          y += (targetY - y) * 0.035;
          pulse *= 0.97;
        }
        scene.position.set(
          300 + (moving ? x * 13 : 0),
          300 + (moving ? y * 10 : 0),
        );
        rings.rotation = moving ? t * 0.012 : 0;
        nearRing.rotation = -0.55 - (moving ? t * 0.008 : 0);
        orbit.rotation = moving ? t * 0.008 : 0;
        core.rotation = moving ? Math.sin(t * 0.035) * 0.04 : 0;
        fog.resources.orbUniforms.uniforms.uTime = t;
        fog.resources.orbUniforms.uniforms.uTouch = new Float32Array([
          moving ? x : 0,
          moving ? y : 0,
        ]);
        fog.resources.orbUniforms.uniforms.uPulse = moving ? pulse : 0;
      };
      app.ticker.maxFPS = 45;
      app.ticker.add(render);
      let visible = true;
      let previousActive: boolean | undefined;
      const sync = () => {
        const active =
          !document.hidden &&
          visible &&
          !settings.current.reduced &&
          !settings.current.paused;
        if (active === previousActive) return;
        previousActive = active;
        if (active) app.start();
        else {
          app.stop();
          render();
          if (!document.hidden && visible) app.render();
        }
      };
      const observer = new IntersectionObserver((entries) => {
        visible = entries[0].isIntersecting;
        sync();
      });
      observer.observe(element);
      document.addEventListener("visibilitychange", sync);
      // Handle runtime reduced-motion / pause changes without reinitializing WebGL.
      const timer = window.setInterval(sync, 250);
      cleanup = () => {
        clearInterval(timer);
        observer.disconnect();
        document.removeEventListener("visibilitychange", sync);
        element.removeEventListener("pointermove", pointer);
        element.removeEventListener("pointerleave", leave);
        element.removeEventListener("pointerdown", press);
        app.destroy(true, { children: true, texture: false });
        fog.destroy();
      };
      render();
      app.render();
      sync();
      setReady(true);
    })().catch(() => {
      /* Original layered art remains usable if WebGL is unavailable. */
    });
    return () => {
      disposed = true;
      cleanup();
    };
  }, []);
  return (
    <div
      ref={host}
      className={`orb ${ready ? "orb-ready" : ""}`}
      data-renderer={ready ? "pixi" : "artwork"}
    >
      <div className="orb-fallback" aria-hidden="true">
        <img
          src="/art/fate_orb_core.png"
          alt=""
          width="1200"
          height="1200"
          fetchPriority="high"
        />
        <img src="/art/fate_orrery.svg" alt="" width="1200" height="1200" />
      </div>
    </div>
  );
}
