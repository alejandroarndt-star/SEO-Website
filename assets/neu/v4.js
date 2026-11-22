/* Runde 7: Markierung beim Scrollen, Videos nur im Bild, Raw-vs-Edited-Bühne, Ton, Stapelkarten, Parallax */
(function(){
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const M=document.body.dataset.media||((document.body.dataset.root||'')+'media/');

/* Markierung zieht sich auf, sobald die Überschrift im Bild ist */
const hio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');hio.unobserve(e.target)}}),{threshold:.6});
$$('.k-hl').forEach(h=>reduce?h.classList.add('in'):hio.observe(h));

/* Videos laufen nur, wenn sie zu sehen sind (spart Leistung, nichts ruckelt) */
const vio=new IntersectionObserver(es=>es.forEach(e=>{const v=e.target;if(v.closest('.k-zoom'))return;
  if(e.isIntersecting){if(v.dataset.wasPlaying!=='no')v.play().catch(()=>{})}else{v.dataset.wasPlaying=v.paused?'no':'yes';if(!v.paused)v.pause();v.dataset.wasPlaying='yes'}}),{rootMargin:'200px 0px'});
const watch=()=>$$('video').forEach(v=>{if(!v._w){v._w=1;vio.observe(v)}});
watch();setTimeout(watch,800);

/* Ton an/aus (Raw bleibt stumm, Ton kommt vom fertigen Schnitt) */
function soundBtn(btn,getVid){
  btn.addEventListener('pointerdown',e=>e.stopPropagation());
  btn.addEventListener('click',e=>{e.stopPropagation();const v=getVid();if(!v)return;v.muted=!v.muted;if(!v.muted)v.play().catch(()=>{});
    btn.classList.toggle('on',!v.muted);btn.textContent=v.muted?'Ton an':'Ton aus'});
}
$$('.k-full[data-autoplay]').forEach(f=>{const v=f.querySelector('video');v.muted=true;soundBtn(f.querySelector('.rv-sound'),()=>v)});

/* Raw-vs-Edited-Bühne: Pfeile, Punkte, Wischen, Ton */
$$('.rvx').forEach(x=>{
  const list=JSON.parse(x.dataset.list),stage=x.querySelector('.rvx-stage'),wrap=x.parentElement;
  const meta=wrap.querySelector('.rvx-meta'),dots=[...wrap.querySelectorAll('.rvx-dots i')];
  const r=()=>stage.querySelector('.raw-v'),e=()=>stage.querySelector('.ed-v'),snd=stage.querySelector('.rv-sound');
  let i=0;
  if(snd)soundBtn(snd,e);
  const go=(n,dir)=>{i=(n+list.length)%list.length;const [s,t,c]=list[i];
    stage.style.setProperty('--dx',(dir>0?-30:30)+'px');stage.classList.add('out');
    setTimeout(()=>{const R=r(),E=e(),muted=E.muted;
      R.poster=M+'rv-'+s+'-raw.jpg';E.poster=M+'rv-'+s+'-edit.jpg';R.src=M+'rv-'+s+'-raw.mp4';E.src=M+'rv-'+s+'-edit.mp4';R.muted=true;E.muted=muted;
      Promise.all([R,E].map(v=>new Promise(ok=>v.addEventListener('loadeddata',ok,{once:true})))).then(()=>{R.currentTime=0;E.currentTime=0;R.play().catch(()=>{});E.play().catch(()=>{})});
      meta.innerHTML=`<b>${t}</b><span>${c}</span>`;dots.forEach((d,j)=>d.classList.toggle('on',j===i));
      stage.style.setProperty('--dx',(dir>0?30:-30)+'px');requestAnimationFrame(()=>stage.classList.remove('out'))},300)};
  x.querySelector('.prev').onclick=()=>go(i-1,-1);
  x.querySelector('.next').onclick=()=>go(i+1,1);
  dots.forEach((d,j)=>d.onclick=()=>go(j,j>i?1:-1));
  let sx=null;stage.addEventListener('touchstart',ev=>{sx=ev.touches[0].clientX},{passive:true});
  stage.addEventListener('touchend',ev=>{if(sx===null)return;const dx=ev.changedTouches[0].clientX-sx;if(Math.abs(dx)>60&&!ev.target.closest('.rv-fr'))go(i+(dx<0?1:-1),dx<0?1:-1);sx=null});
});

/* Stapelkarten: die verdeckte Karte wird etwas kleiner und dunkler */
const cards=$$('.k-sc');
const stackFx=()=>{cards.forEach((c,j)=>{const n=cards[j+1];if(!n){c.style.transform='';c.style.filter='';return}
  const a=c.getBoundingClientRect(),b=n.getBoundingClientRect();const p=Math.max(0,Math.min(1,(a.bottom-b.top)/a.height));
  c.style.transform=`scale(${1-p*.06})`;c.style.filter=`brightness(${1-p*.35})`})};

/* Parallax für schwebende Elemente */
const par=$$('[data-par]');
const parFx=()=>{const y=scrollY;par.forEach(el=>{el.style.transform=`translate3d(0,${(-y*parseFloat(el.dataset.par)).toFixed(1)}px,0)`})};
if(!reduce){const f=()=>{stackFx();parFx()};addEventListener('scroll',()=>requestAnimationFrame(f),{passive:true});f()}
})();
