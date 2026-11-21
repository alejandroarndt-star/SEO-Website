/* Raw vs Edited: Videos synchron halten, Regler, Umschalter, Zeitleisten */
(function(){
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const DATA=Object.fromEntries((window.K_RV||[]).map(d=>[d.slug,d]));
const M=document.body.dataset.media||((document.body.dataset.root||'')+'media/');
const mmss=s=>Math.floor(s/60)+':'+String(Math.round(s%60)).padStart(2,'0');

/* Paare synchron: beide starten gemeinsam, Abweichung wird nachgezogen */
function syncPair(root){
  const r=root.querySelector('.raw-v'),e=root.querySelector('.ed-v');if(!r||!e)return;
  [r,e].forEach(v=>{v.muted=true;v.loop=true;v.playsInline=true});
  const start=()=>{r.currentTime=0;e.currentTime=0;r.play().catch(()=>{});e.play().catch(()=>{})};
  let ready=0;[r,e].forEach(v=>v.addEventListener('loadeddata',()=>{if(++ready===2)start()},{once:true}));
  setInterval(()=>{if(!r.paused&&Math.abs(r.currentTime-e.currentTime)>.12)e.currentTime=r.currentTime},400);
  root._tl=()=>r.currentTime/(r.duration||10);
}

/* Zeitleiste aus echten Schnittdaten */
function timeline(el){
  const d=DATA[el.dataset.rv];if(!d)return;
  const edW=Math.max(16,Math.min(100,d.final_len/d.raw_len*100));
  let x=0;const tot=d.segs.reduce((a,[s,e])=>a+(e-s),0);
  const cols=['var(--c1)','var(--c2)','var(--c5)','var(--c4)','var(--c3)'];
  const raw=d.segs.map(([s,e])=>`<i class="seg" style="left:${s*100}%;width:${Math.max(.6,(e-s)*100)}%"></i>`).join('');
  const ed=d.segs.map(([s,e],i)=>{const w=(e-s)/tot*100;const h=`<i class="seg" style="left:${x}%;width:calc(${w}% - 2px);background:${cols[i%5]}"></i>`;x+=w;return h}).join('');
  el.innerHTML=`<div class="row"><b>Raw</b><div class="tr raw">${raw}<span class="ph"></span></div><span class="t">${mmss(d.raw_len)}</span></div>
  <div class="row"><b>Edited</b><div class="tr ed" style="width:${edW}%">${ed}<span class="ph"></span></div><span class="t">${mmss(d.final_len)}</span></div>
  <div class="stats"><span><b>${d.cuts}</b> Schnitte</span><span><b>${Math.round(d.kept)} von ${Math.round(d.raw_len)}</b> Sekunden behalten</span></div>`;
  const pair=el.closest('.rv-cell,.rv-home')?.querySelector('.rv');
  const phs=$$('.ph',el);
  if(!reduce)(function tick(){const p=pair&&pair._tl?pair._tl():((performance.now()/10000)%1);
    /* Rohspur: Spielkopf springt durch die behaltenen Stücke; Schnittspur: läuft gleichmäßig */
    const t=p*Math.min(10,d.kept)/d.kept;let acc=0,pos=0;
    for(const [s,e] of d.segs){const len=(e-s)/(d.segs.reduce((a,[q,w])=>a+(w-q),0));if(t<=acc+len){pos=s+(t-acc)/len*(e-s);break}acc+=len;pos=e}
    phs[0].style.left=(pos*100)+'%';phs[1].style.left=(t*100)+'%';requestAnimationFrame(tick)})();
}

/* Schieberegler: wandert von selbst, bis jemand zieht */
function slider(root){
  const fr=root.querySelector('.rv-fr');let x=50,drag=false,touched=false;
  const set=v=>{x=Math.max(0,Math.min(100,v));fr.style.setProperty('--x',x+'%')};
  const at=e=>{const r=fr.getBoundingClientRect();set((e.clientX-r.left)/r.width*100)};
  fr.addEventListener('pointerdown',e=>{drag=touched=true;fr.setPointerCapture(e.pointerId);at(e)});
  fr.addEventListener('pointermove',e=>{if(drag)at(e)});
  fr.addEventListener('pointerup',()=>drag=false);
  if(!reduce)(function sweep(t){if(!touched)set(50+34*Math.sin(t/1400));requestAnimationFrame(sweep)})(0);
}

/* Wechsel: alle 2,8 s, Klick legt fest */
function flip(root){
  let auto=!reduce;const set=raw=>root.classList.toggle('raw-on',raw);
  root.querySelector('.r').onclick=()=>{auto=false;set(true)};
  root.querySelector('.e').onclick=()=>{auto=false;set(false)};
  setInterval(()=>{if(auto)set(!root.classList.contains('raw-on'))},2800);
}

$$('.rv').forEach(syncPair);
$$('.rv-slide').forEach(slider);
$$('.rv-flip').forEach(flip);
$$('.rv-tl').forEach(timeline);

/* Startseite: Videoauswahl für den großen Regler */
$$('.rv-pick').forEach(pick=>{
  const home=pick.closest('.rv-home'),pair=home.querySelector('.rv'),tl=home.querySelector('.rv-tl');
  $$('button',pick).forEach(b=>b.onclick=()=>{
    $$('button',pick).forEach(x=>x.classList.toggle('on',x===b));
    const s=b.dataset.rv,r=pair.querySelector('.raw-v'),e=pair.querySelector('.ed-v');
    r.poster=M+'rv-'+s+'-raw.jpg';e.poster=M+'rv-'+s+'-edit.jpg';r.src=M+'rv-'+s+'-raw.mp4';e.src=M+'rv-'+s+'-edit.mp4';
    Promise.all([r,e].map(v=>new Promise(ok=>v.addEventListener('loadeddata',ok,{once:true})))).then(()=>{r.currentTime=0;e.currentTime=0;r.play();e.play()});
    tl.dataset.rv=s;timeline(tl);
  });
});
})();
