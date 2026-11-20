import { useEffect, useRef } from "react";

const vertex = `attribute vec2 position; void main(){gl_Position=vec4(position,0.,1.);}`;
const fragment = `
precision mediump float;
uniform vec2 size;
uniform vec2 touch;
uniform float time;
uniform float mirror;
float hash(vec3 p){
  p=fract(p*.3183099+.1);
  p*=17.;
  return fract(p.x*p.y*p.z*(p.x+p.y+p.z));
}
float noise(vec3 p){
  vec3 i=floor(p),f=fract(p); f=f*f*(3.-2.*f);
  return mix(mix(mix(hash(i),hash(i+vec3(1,0,0)),f.x),mix(hash(i+vec3(0,1,0)),hash(i+vec3(1,1,0)),f.x),f.y),
    mix(mix(hash(i+vec3(0,0,1)),hash(i+vec3(1,0,1)),f.x),mix(hash(i+vec3(0,1,1)),hash(i+vec3(1,1,1)),f.x),f.y),f.z);
}
void main(){
  vec2 p=(gl_FragCoord.xy/size*2.-1.)*vec2(1.02,1.02);
  float r=length(p);
  float mask=1.-smoothstep(.94,.99,r);
  if(mask<.001){gl_FragColor=vec4(0.);return;}
  float z=sqrt(max(0.,1.-r*r));
  vec3 normal=normalize(vec3(p,z));
  vec3 transmitted=refract(vec3(0.,0.,-1.),normal,.72);
  vec2 ray=mix(p-transmitted.xy*(.34+.25*z),p+vec2(p.y*p.y*.07,-p.x*.04),mirror)+.10*touch*z;
  float fog=0.;
  for(int i=0;i<8;i++){
    float t=float(i)/8.;
    vec3 point=vec3(ray*(2.6+t*.95)+vec2(time*.052,-time*.029),t*3.4+time*.071);
    float tendril=abs(noise(point)*2.-1.);
    float dens=smoothstep(.25,.74,.64*(1.-tendril)+.36*noise(point*2.6));
    fog += dens*(1.-fog)*(.115+z*.08);
  }
  vec3 base=mix(vec3(.033,.038,.095),vec3(.044,.021,.041),mirror);
  vec3 lights=mix(vec3(.56,.54,.91),vec3(.59,.31,.34),mirror);
  float edge=pow(1.-z,3.5);
  float facing=max(0.,dot(normal,normalize(vec3(-.49,.61,.62)+vec3(touch*.19,0.))));
  float gloss=pow(facing,25.)*.21+pow(facing,100.)*.51;
  float curtain=pow(.5+.5*cos(p.x*9.+p.y*2.+sin(p.y*5.+time*.28)*.7+time*.3),12.)*z;
  float band=(r-.93)*44.;
  float bevel=exp(-band*band)*(.27+.23*sin(atan(p.y,p.x)+1.2));
  vec2 bounced=reflect(vec3(0.,0.,-1.),normal).xy;
  float pane=smoothstep(.80,.99,1.-abs(bounced.x+.31+touch.x*.14))*smoothstep(-.2,.47,bounced.y);
  float silver=mirror*pow(max(0.,1.-abs(ray.x+.24+ray.y*.11)*4.8),6.)*(.63+.21*sin(time*.24));
  vec3 color=base+lights*(fog*(.61+.09*z)+edge*.36+bevel)+vec3(.77,.74,.96)*gloss
    + (1.-mirror)*vec3(.18,.20,.31)*pane + mirror*lights*(curtain*.14+silver*.16);
  gl_FragColor=vec4(color,mask);
}`;

function create(canvas: HTMLCanvasElement) {
  const gl = canvas.getContext("webgl", {
    alpha: true,
    premultipliedAlpha: false,
    antialias: false,
    preserveDrawingBuffer: false,
  });
  if (!gl) return null;
  const compile = (kind: number, source: string) => {
    const shader = gl.createShader(kind)!;
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  };
  const vs = compile(gl.VERTEX_SHADER, vertex),
    fs = compile(gl.FRAGMENT_SHADER, fragment);
  if (!vs || !fs) {
    if (vs) gl.deleteShader(vs);
    if (fs) gl.deleteShader(fs);
    return null;
  }
  const program = gl.createProgram()!;
  gl.attachShader(program, vs);
  gl.attachShader(program, fs);
  gl.linkProgram(program);
  gl.deleteShader(vs);
  gl.deleteShader(fs);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    gl.deleteProgram(program);
    return null;
  }
  const points = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, points);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]),
    gl.STATIC_DRAW,
  );
  gl.useProgram(program);
  const position = gl.getAttribLocation(program, "position");
  gl.enableVertexAttribArray(position);
  gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
  const uniforms = {
    size: gl.getUniformLocation(program, "size"),
    mirror: gl.getUniformLocation(program, "mirror"),
    time: gl.getUniformLocation(program, "time"),
    touch: gl.getUniformLocation(program, "touch"),
  };
  return {
    gl,
    uniforms,
    dispose: () => {
      gl.deleteBuffer(points);
      gl.deleteProgram(program);
    },
  };
}

export function GlassSurface({
  mirror,
  still,
}: {
  mirror: boolean;
  still: boolean;
}) {
  const frame = useRef<HTMLDivElement>(null),
    canvas = useRef<HTMLCanvasElement>(null);
  useEffect(() => {
    const panel = frame.current,
      surface = canvas.current;
    if (!panel || !surface || still) return;
    const gfx = create(surface);
    if (!gfx) {
      panel.dataset.renderer = "static";
      return;
    }
    const { gl, uniforms } = gfx;
    let visible = false,
      handle = 0,
      last = 0,
      first = 0,
      x = 0,
      y = 0,
      tx = 0,
      ty = 0;
    const debug = gl.getExtension("WEBGL_debug_renderer_info");
    const renderer = String(
      gl.getParameter(debug?.UNMASKED_RENDERER_WEBGL ?? gl.RENDERER),
    );
    const memory = (navigator as Navigator & { deviceMemory?: number })
      .deviceMemory;
    const low =
      /swiftshader|llvmpipe|software|basic render/i.test(renderer) ||
      navigator.hardwareConcurrency <= 4 ||
      (memory !== undefined && memory <= 2);
    const size = low ? 208 : window.innerWidth < 620 ? 300 : 420;
    panel.dataset.quality = low ? "economy" : "standard";
    surface.width = size;
    surface.height = size;
    gl.viewport(0, 0, size, size);
    gl.uniform2f(uniforms.size, size, size);
    gl.uniform1f(uniforms.mirror, Number(mirror));
    const draw = (now: number) => {
      handle = 0;
      if (!visible || document.hidden) return;
      if (!first) first = now;
      if (now - last >= (low ? 64 : 31)) {
        last = now;
        x += (tx - x) * 0.19;
        y += (ty - y) * 0.19;
        gl.uniform1f(uniforms.time, (now - first) / 1000);
        gl.uniform2f(uniforms.touch, x, y);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      }
      handle = requestAnimationFrame(draw);
    };
    const schedule = () => {
      if (handle) cancelAnimationFrame(handle);
      handle = visible && !document.hidden ? requestAnimationFrame(draw) : 0;
      panel.dataset.renderer = handle ? "volumetric" : "idle";
    };
    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      schedule();
    });
    observer.observe(panel);
    const touch = (event: PointerEvent) => {
      const rect = panel.getBoundingClientRect();
      tx = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      ty = 1 - ((event.clientY - rect.top) / rect.height) * 2;
    };
    const center = () => {
      tx = ty = 0;
    };
    const lost = () => {
      visible = false;
      schedule();
      panel.dataset.renderer = "static";
    };
    panel.addEventListener("pointermove", touch);
    panel.addEventListener("pointerleave", center);
    surface.addEventListener("webglcontextlost", lost);
    document.addEventListener("visibilitychange", schedule);
    return () => {
      observer.disconnect();
      cancelAnimationFrame(handle);
      gfx.dispose();
      panel.removeEventListener("pointermove", touch);
      panel.removeEventListener("pointerleave", center);
      surface.removeEventListener("webglcontextlost", lost);
      document.removeEventListener("visibilitychange", schedule);
      panel.dataset.renderer = "static";
    };
  }, [mirror, still]);
  return (
    <div
      className={
        "ritual-glass " +
        (mirror ? "ritual-mirror-frame" : "ritual-crystal-frame")
      }
      ref={frame}
      data-renderer="static"
      aria-hidden="true"
    >
      {!still && <canvas ref={canvas} className="glass-fog" />}
      <div className="glass-reflection" />
    </div>
  );
}
