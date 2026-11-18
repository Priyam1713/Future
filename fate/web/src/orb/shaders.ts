// A bounded glass-sphere pass. The tiny noise texture replaces procedural hash
// loops; three clouds move independently, with spherical refraction/parallax.
export const orbVertex = `
precision highp float;
in vec2 aPosition; out vec2 vTextureCoord;
uniform vec4 uInputSize, uOutputFrame, uOutputTexture;
void main(){vec2 p=aPosition*uOutputFrame.zw+uOutputFrame.xy;
 p.x=p.x*2./uOutputTexture.x-1.;p.y=p.y*(2.*uOutputTexture.z/uOutputTexture.y)-uOutputTexture.z;
 gl_Position=vec4(p,0.,1.);vTextureCoord=aPosition*uOutputFrame.zw*uInputSize.zw;}`;

export const orbFragment = `
precision highp float;
in vec2 vTextureCoord;out vec4 finalColor;
uniform vec4 uInputSize,uOutputFrame;
uniform sampler2D uNoise,uNebula;
uniform float uTime,uPulse,uDetail;
uniform vec2 uTouch;
float cloud(vec2 p){
 float n=texture(uNoise,fract(p*.0075)).r*.59;
 n+=texture(uNoise,fract(p*.017+vec2(.31,.17))).g*.29;
 if(uDetail>.5)n+=texture(uNoise,fract(p*.035)).b*.12;else n+=.06;return n;
}
mat2 rotate(float a){float c=cos(a),s=sin(a);return mat2(c,-s,s,c);}
void main(){
 vec2 uv=vTextureCoord*uInputSize.xy/uOutputFrame.zw;
 vec2 q=(uv-.5)/.375;float r=length(q);
 float edge=1.-smoothstep(.992,1.007,r),z=sqrt(max(.0001,1.-dot(q,q))),t=uTime;
 vec2 lens=q/(1.28+z*.52)+uTouch*.035*z;
 vec2 drift=vec2(t*.075,-t*.047);
 float back=cloud(rotate(-.22+t*.006)*lens*8.+drift);
 vec2 warp=vec2(back-.5,cloud(lens*5.-drift*.7)-.5);
 float middle=cloud(rotate(.4-t*.009)*lens*13.+warp*2.-drift*.8);
 float front=cloud(lens*19.+warp*3.+vec2(-t*.11,t*.06));
 float density=smoothstep(.29,.78,back*.36+middle*.44+front*.2);
 float filaments=smoothstep(.43,.7,middle)*(1.-smoothstep(.38,.68,front))*.12,depth=pow(z,.7);
 vec2 light=vec2(-.28+sin(t*.095)*.17,.04+cos(t*.071)*.16);
 float innerLight=exp(-length(lens-light)*3.3),ember=exp(-length(lens-vec2(.25,-.29))*6.8);
 vec3 fog=(vec3(.13,.34,.34)*density+vec3(.12,.105,.27)*smoothstep(.38,.75,front))*(.42+innerLight*.85)*depth;
 fog+=vec3(.28,.37,.37)*filaments*depth;
 fog+=vec3(.31,.24,.12)*ember*density*.38+vec3(.2,.32,.32)*innerLight*density*.23;
 vec2 flow=vec2(sin(t*.031),cos(t*.026))*.04;
 vec2 rearUV=clamp(rotate(t*.009)*lens*.68+.5+flow+warp*.045,vec2(.02),vec2(.98));
 vec2 frontUV=clamp(rotate(-.24-t*.006)*lens*.47+.49-flow*.6+uTouch*.016,vec2(.02),vec2(.98));
 vec3 rearMist=texture(uNebula,rearUV).rgb;
 vec3 nearMist=texture(uNebula,frontUV).rgb;
 vec3 color=vec3(.009,.018,.035)+fog*.2+(rearMist*.83+nearMist*.34)*depth*(.8+innerLight*.55);
 float fresnel=pow(1.-z,3.1);vec3 normal=normalize(vec3(q,z));
 float reflection=pow(max(0.,dot(normal,normalize(vec3(-.65,-.72,.7)))),36.);
 float secondary=pow(max(0.,dot(normal,normalize(vec3(.82,.48,.16)))),16.);
 float rim=exp(-abs(r-.988)*235.);
 float upper=max(0.,dot(normalize(q+vec2(.001)),normalize(vec2(-.6,-.8))));
 color+=vec3(.69,.8,.81)*reflection*.52+vec3(.32,.25,.12)*secondary*.21;
 color+=vec3(.33,.53,.56)*fresnel*.29;
 color+=mix(vec3(.2,.28,.4),vec3(.74,.76,.63),upper)*rim*.65;
 float touchGlow=exp(-length(lens-uTouch*.7)*4.5)*uPulse;
 color+=vec3(.18,.28,.22)*touchGlow*depth;
 float halo=exp(-max(0.,r-1.)*34.)*.075*(1.-edge);
 finalColor=vec4(color*edge*.985+vec3(.09,.17,.2)*halo,edge*.985+halo);
}`;
