"""Write og/og-video.html: a 1200x630 composition driven by a deterministic render(t)."""
import os
from logo import BARS, RED, bars_path
from build import LINE_A, LINE_B, ST_A, ST_B, poly_d, length, dist_to

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
S = 2

def svg():
    la, lb = length(LINE_A), length(LINE_B)
    o = ['<svg id="mapsvg" viewBox="-30 -30 500 446">', f'<path class="ghost" id="ghost" d="{bars_path(BARS,0,0,S)}"/>']
    x, y, w, h = [v * S for v in RED]
    o.append(f'<g id="start"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="#E5231B"/><text x="{x+w/2}" y="{y-10}" text-anchor="middle">YOU</text></g>')
    for cls, pts, L, pid in (("a", LINE_A, la, "ra"), ("b", LINE_B, lb, "rb")):
        o.append(f'<path class="sh" id="{pid}s" d="{poly_d(pts)}" data-len="{L}"/>')
        o.append(f'<path class="rt {cls}" id="{pid}" d="{poly_d(pts)}" data-len="{L}"/>')
    for cls, pts, L, sts, pid in (("a", LINE_A, la, ST_A, "ra"), ("b", LINE_B, lb, ST_B, "rb")):
        for lab, sx, sy in sts:
            f = dist_to(pts, sx, sy) / L
            o.append(f'<g class="stn {cls}" data-line="{pid}" data-f="{f:.4f}" style="transform-origin:{sx}px {sy}px"><circle cx="{sx}" cy="{sy}" r="16"/><text x="{sx}" y="{sy+.5}">{lab}</text></g>')
    for pid in ("ra", "rb"):
        o.append(f'<g class="train" data-path="{pid}"><rect x="-15" y="-7.5" width="30" height="15" rx="7.5"/><circle cx="-5" r="2.4" fill="#fff"/><circle cx="5" r="2.4" fill="#fff"/></g>')
    o.append("</svg>")
    return "\n".join(o)

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,600;1,8..60,600&family=JetBrains+Mono:wght@500&family=Poppins:wght@400;500;600&display=swap">
<style>
html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#F5F3EE}
#stage{position:relative;width:1200px;height:630px;overflow:hidden;font-family:Poppins,sans-serif;color:#14163A}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(46,49,146,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(46,49,146,.07) 1px,transparent 1px);background-size:32px 32px}
.brand{position:absolute;left:64px;top:52px;display:flex;align-items:center;gap:14px;will-change:transform,opacity}
.brand svg{width:52px}
.brand b{display:block;font:600 21px/1.1 Poppins}
.brand span{display:block;font:500 15px/1.3 "Noto Sans CJK SC","Noto Sans SC",sans-serif;letter-spacing:.2em;color:#585E6A}
.eyebrow{position:absolute;left:64px;top:150px;font:500 15px/1 "JetBrains Mono";letter-spacing:.12em;color:#2E3192;display:flex;gap:12px;align-items:center}
.eyebrow i{width:26px;height:9px;border-radius:9px;background:#2E3192}
h1{position:absolute;left:64px;top:180px;margin:0;font:600 66px/1.02 "Source Serif 4",serif;letter-spacing:-.022em}
h1 .ln{display:block;overflow:hidden;padding:0 8px 10px;margin:0 -8px -10px}
h1 .ln > span{display:block;will-change:transform}
h1 em{font-style:italic;color:#2E3192}
h1 .dot{color:#E5231B}
.sub{position:absolute;left:64px;top:410px;width:470px;font:400 19px/1.5 Poppins;color:#34385A;will-change:transform,opacity}
.card{position:absolute;right:56px;top:40px;width:500px;height:498px;background:#fff;border:1px solid #D9D5CB;border-radius:30px;box-shadow:0 30px 60px -36px rgba(20,22,58,.5);will-change:transform,opacity}
.card .top{position:absolute;left:28px;right:28px;top:22px;display:flex;justify-content:space-between;font:500 13px/1 "JetBrains Mono";letter-spacing:.12em;color:#585E6A;padding-bottom:14px;border-bottom:1px dashed #D9D5CB}
.card .top .r{color:#B3190F}
#mapsvg{position:absolute;left:36px;top:62px;width:428px;overflow:visible}
.ghost{fill:#2E3192}
.rt{fill:none;stroke-width:13;stroke-linecap:round;stroke-linejoin:round}.rt.a{stroke:#2E3192}.rt.b{stroke:#EF8A1D}
.sh{fill:none;stroke:#fff;stroke-width:21;stroke-linecap:round;stroke-linejoin:round}
.stn circle{fill:#fff;stroke-width:5}.stn.a circle{stroke:#2E3192}.stn.b circle{stroke:#EF8A1D}
.stn text{font:500 15px "JetBrains Mono";text-anchor:middle;dominant-baseline:central;fill:#14163A}
#start text{font:500 12px "JetBrains Mono";letter-spacing:.12em;fill:#B3190F}
.train rect{fill:#14163A}
.ticker{position:absolute;left:0;right:0;bottom:0;height:46px;background:#14163A;color:#F5F3EE;overflow:hidden;will-change:transform}
.ticker .run{position:absolute;top:0;left:0;white-space:nowrap;font:500 15px/46px "JetBrains Mono";letter-spacing:.08em;will-change:transform}
.ticker .run b{color:#FFB45E;font-weight:500;margin:0 22px}
.tabbar{position:absolute;left:64px;top:508px;display:flex;align-items:center;gap:6px;padding:6px;border-radius:999px;background:#14163A;box-shadow:0 18px 40px -14px rgba(20,22,58,.7);will-change:transform,opacity}
.tabbar .it{display:grid;justify-items:center;gap:2px;width:72px;color:rgba(255,255,255,.8);font:500 12px/1.1 Poppins}
.tabbar .it svg{width:20px;height:20px}
.tabbar .home{width:48px;display:grid;place-items:center}.tabbar .home svg{width:26px}
.tabbar .pill{display:flex;align-items:center;gap:6px;padding:0 18px;height:46px;border-radius:999px;background:#EF8A1D;color:#2A1500;font:600 14px/1 Poppins}
</style></head><body>
<svg width="0" height="0" style="position:absolute"><symbol id="m" viewBox="0 0 219 200"><path fill="currentColor" d="{MARK}"/><path fill="#E5231B" d="{RED}"/></symbol></svg>
<div id="stage"><div class="grid" id="grid"></div>
<div class="brand" id="brand"><svg viewBox="0 0 219 200" style="color:#2E3192"><use href="#m"/></svg><div><b>Ivy Tax &amp; Business</b><span>安腾会计</span></div></div>
<div class="eyebrow" id="eyebrow"><i></i>LONG ISLAND CPA · SYOSSET, NY</div>
<h1><span class="ln"><span id="l1">Precision tax</span></span><span class="ln"><span id="l2">planning,</span></span><span class="ln"><span id="l3"><em>profound savings</em><span class="dot">.</span></span></span></h1>
<p class="sub" id="sub">S-Corp strategy, clean books and IRS notice help, in English and 中文.</p>
<div class="card" id="card"><div class="top"><span>A YEAR WITH IVY · ROUTE MAP</span><span class="r">■ YOU START HERE</span></div>{SVG}</div>
<div class="tabbar" id="tabbar"><div class="home"><svg viewBox="0 0 219 200" style="color:#fff"><use href="#m"/></svg></div>
<div class="it"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" d="M5 4h10a4 4 0 0 1 0 8H9a4 4 0 0 0 0 8h10"/></svg>Services</div>
<div class="it"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 12V4h8l10 10-8 8L3 12z"/></svg>Pricing</div>
<div class="it"><svg viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>Call</div>
<div class="pill">Book a call</div></div>
<div class="ticker" id="ticker"><div class="run" id="run"></div></div>
</div>
<script>
const T_ITEMS=['516-344-8065','中文 718-801-8060','6800 JERICHO TPKE · SYOSSET, NY','S-CORP STRATEGY','BOOKKEEPING FROM $280/MO','IRS NOTICE HELP','ADVISORY FROM $350/MO','CLIENTS IN ALL 50 STATES'];
const run=document.getElementById('run'); const one=T_ITEMS.map(s=>s+'<b>●</b>').join(''); run.innerHTML=one+one+one+one;
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const ease=x=>1-Math.pow(1-clamp(x),3);
const io=x=>{x=clamp(x);return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
const spring=x=>{x=clamp(x);return 1-Math.exp(-6.5*x)*Math.cos(9*x)};
const fade=(t,a,d=.25)=>clamp((t-a)/d);
const $=id=>document.getElementById(id);
const paths={ra:$('ra'),rb:$('rb')}; const lens={ra:paths.ra.getTotalLength(),rb:paths.rb.getTotalLength()};
const DRAW={ra:[1.1,2.9],rb:[1.45,3.25]};
let W1=null;
function rise(el,t,a,dist=1){const p=ease((t-a)/.7);el.style.transform=`translate3d(0,${(1-p)*105*dist}%,0)`;}
function render(t){
  if(W1===null) W1=run.scrollWidth/4;
  $('grid').style.opacity=fade(t,0,.5);
  const c=spring((t-.15)/1.1); $('card').style.opacity=fade(t,.15,.3); $('card').style.transform=`translate3d(0,${(1-c)*40}px,0) scale(${.94+.06*c})`;
  const b=ease((t-.5)/.6); $('brand').style.opacity=fade(t,.5); $('brand').style.transform=`translate3d(0,${(1-b)*-16}px,0)`;
  $('eyebrow').style.opacity=fade(t,.75);
  rise($('l1'),t,.7); rise($('l2'),t,.85); rise($('l3'),t,1.0);
  const s=ease((t-1.5)/.6); $('sub').style.opacity=fade(t,1.5,.4); $('sub').style.transform=`translate3d(0,${(1-s)*16}px,0)`;
  $('ghost').style.opacity=.07*fade(t,.6,.8); $('start').style.opacity=fade(t,.9,.3);
  for(const k of ['ra','rb']){ const [a,e]=DRAW[k]; const p=io((t-a)/(e-a)); const L=lens[k]+2;
    for(const el of [paths[k],$(k+'s')]){ el.style.strokeDasharray=L; el.style.strokeDashoffset=L*(1-p);} }
  document.querySelectorAll('.stn').forEach(g=>{ const [a,e]=DRAW[g.dataset.line]; const at=a+(e-a)*(+g.dataset.f)+.02; const p=spring((t-at)/.6);
    g.style.opacity=fade(t,at,.15); g.style.transform=`scale(${.3+.7*p})`; });
  document.querySelectorAll('.train').forEach((g,i)=>{ const k=g.dataset.path; const st=3.4+i*.5; const L=lens[k];
    const d=clamp((t-st)/3.4)*L; const pt=paths[k].getPointAtLength(d); const pa=paths[k].getPointAtLength(Math.min(L,d+1)), pb=paths[k].getPointAtLength(Math.max(0,d-1));
    const ang=Math.round(Math.atan2(pa.y-pb.y,pa.x-pb.x)*2/Math.PI)*90;
    g.setAttribute('transform',`translate(${pt.x.toFixed(2)} ${pt.y.toFixed(2)}) rotate(${ang})`); g.style.opacity=fade(t,st,.25)*(1-fade(t,st+3.5,.3)); });
  const tk=ease((t-1.8)/.6); $('ticker').style.transform=`translate3d(0,${(1-tk)*46}px,0)`;
  const px=Math.round(Math.max(0,t-1.8)*60); run.style.transform=`translate3d(${-(px%Math.round(W1))}px,0,0)`;
  const tb=spring((t-6.3)/1.0); $('tabbar').style.opacity=fade(t,6.3,.3); $('tabbar').style.transform=`translate3d(0,${(1-tb)*90}px,0)`;
}
window.render=render; render(8);
</script></body></html>"""

if __name__ == "__main__":
    page = PAGE.replace("{MARK}", bars_path(BARS)).replace("{RED}", bars_path([RED])).replace("{SVG}", svg())
    os.makedirs(os.path.join(ROOT, "og"), exist_ok=True)
    open(os.path.join(ROOT, "og", "og-video.html"), "w", encoding="utf-8").write(page)
    print("ok")
