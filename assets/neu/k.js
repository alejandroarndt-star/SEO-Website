/* Kontor Vorschau: Verhalten für alle Seiten. Kein Framework. */
(function(){
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const R=document.body.dataset.root||'';
const M=document.body.dataset.media||(R+'media/');

/* ---------- Videos in Handys und Reels ---------- */
const vid=n=>`<video muted loop playsinline autoplay preload="metadata" poster="${M}${n}.jpg"><source src="${M}${n}.mp4" type="video/mp4"></video>`;
$$('.k-iph[data-reel]').forEach(el=>el.innerHTML=`<div class="k-scr">${vid(el.dataset.reel)}<span class="k-isl"></span></div>`);
$$('.k-reel[data-reel]').forEach(el=>el.innerHTML=vid(el.dataset.reel));
$$('video').forEach(v=>v.play().catch(()=>{}));

/* ---------- Kopfzeile ---------- */
const hdr=document.querySelector('.k-hdr');
const fan=document.querySelector('.k-fan');
const onScroll=()=>{
  if(hdr)hdr.classList.toggle('scrolled',scrollY>8);
  if(fan&&!reduce)fan.style.setProperty('--spread',Math.min(1,scrollY/420).toFixed(3));
};
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* ---------- Vollbild-Menü ---------- */
const menu=document.querySelector('.k-menu');
if(menu){
  const open=on=>{menu.classList.toggle('on',on);document.body.classList.toggle('k-lock',on)};
  $$('.k-menu-btn').forEach(b=>b.onclick=()=>open(true));
  menu.querySelector('.x').onclick=()=>open(false);
  addEventListener('keydown',e=>{if(e.key==='Escape')open(false)});
  const pvs=$$('.k-pv',menu);
  const show=k=>pvs.forEach(p=>p.classList.toggle('on',p.dataset.pv===k));
  $$('.k-mlinks a',menu).forEach(a=>a.addEventListener('mouseenter',()=>show(a.dataset.pv)));
  const cur=menu.querySelector('.k-mlinks a.on');show(cur?cur.dataset.pv:'start');
}

/* ---------- Kippen zur Maus ---------- */
if(!reduce&&matchMedia('(hover:hover)').matches){
  $$('[data-tilt]').forEach(el=>{
    const base=el.style.transform||'';
    el.addEventListener('mousemove',e=>{const r=el.getBoundingClientRect();const x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
      el.style.transform=`${base} perspective(900px) rotateY(${x*12}deg) rotateX(${-y*12}deg) translateZ(14px)`});
    el.addEventListener('mouseleave',()=>el.style.transform=base);
  });
}

/* ---------- Mitlaufendes Etikett ---------- */
const cur=document.createElement('div');cur.className='k-cursor';document.body.append(cur);
let cx=0,cy=0,tx=0,ty=0;
addEventListener('mousemove',e=>{tx=e.clientX;ty=e.clientY});
(function loop(){cx+=(tx-cx)*.2;cy+=(ty-cy)*.2;cur.style.left=cx+'px';cur.style.top=cy+'px';requestAnimationFrame(loop)})();
$$('[data-open],[data-label]').forEach(el=>{
  el.addEventListener('mouseenter',()=>{cur.textContent=el.dataset.label||'Ansehen';cur.classList.add('on')});
  el.addEventListener('mouseleave',()=>cur.classList.remove('on'));
});

/* ---------- Reel-Lupe: Display zoomt auf Vollbild ---------- */
const NAMES={pearl:'PearlHouse, Göppingen',masson:'Masson Beauty, Eislingen'};
const opens=$$('[data-open]');
if(opens.length){
  const z=document.createElement('div');z.className='k-zoom';
  z.innerHTML='<div class="k-zv"><video playsinline loop></video></div><div class="k-zui"><button class="x" aria-label="Schließen">✕</button><button class="prev" aria-label="Vorheriges Reel">‹</button><button class="next" aria-label="Nächstes Reel">›</button><button class="mute">Ton an</button><p class="lbl"></p></div>';
  document.body.append(z);
  const box=z.querySelector('.k-zv'),v=box.querySelector('video'),lbl=z.querySelector('.lbl'),mute=z.querySelector('.mute');
  const list=[...new Set(opens.map(o=>o.dataset.open))];let idx=0,src=null;
  const target=()=>{const h=innerHeight*.9,w=Math.min(innerWidth*.92,h*9/16);return{left:(innerWidth-w)/2,top:(innerHeight-w*16/9)/2,width:w,height:w*16/9,radius:22}};
  const place=(r,rad)=>Object.assign(box.style,{left:r.left+'px',top:r.top+'px',width:r.width+'px',height:r.height+'px',borderRadius:rad+'px'});
  const load=i=>{idx=(i+list.length)%list.length;const n=list[idx];v.src=M+n+'.mp4';v.poster=M+n+'.jpg';v.muted=true;mute.textContent='Ton an';v.play().catch(()=>{});
    lbl.innerHTML=(NAMES[n.split('-')[0]]||'')+'<span>Reel '+(idx+1)+' von '+list.length+'</span>'};
  const openFrom=el=>{src=el.querySelector('video')||el;const r=src.getBoundingClientRect();
    load(list.indexOf(el.dataset.open));box.style.transition='none';place(r,20);box.offsetWidth;box.style.transition='';
    z.classList.add('on');document.body.classList.add('k-lock');cur.classList.remove('on');
    requestAnimationFrame(()=>place(target(),22))};
  const close=()=>{const r=src?src.getBoundingClientRect():target();place(r,20);z.classList.add('closing');z.classList.remove('on');document.body.classList.remove('k-lock');setTimeout(()=>{z.classList.remove('closing');if(!z.classList.contains('on'))v.pause()},700)};
  opens.forEach(o=>o.addEventListener('click',e=>{e.preventDefault();openFrom(o)}));
  z.querySelector('.x').onclick=close;
  z.addEventListener('click',e=>{if(e.target===z)close()});
  z.querySelector('.prev').onclick=()=>load(idx-1);
  z.querySelector('.next').onclick=()=>load(idx+1);
  mute.onclick=()=>{v.muted=!v.muted;mute.textContent=v.muted?'Ton an':'Ton aus'};
  addEventListener('keydown',e=>{if(!z.classList.contains('on'))return;if(e.key==='Escape')close();if(e.key==='ArrowRight')load(idx+1);if(e.key==='ArrowLeft')load(idx-1)});
  addEventListener('resize',()=>{if(z.classList.contains('on'))place(target(),22)});
}

/* ---------- 3D-Osmo / Mic mit Drehteller ---------- */
const F='<span class="pk-f pk-vo"></span><span class="pk-f pk-hi"></span><span class="pk-f pk-li"></span><span class="pk-f pk-re"></span><span class="pk-f pk-ob"></span><span class="pk-f pk-un"></span>';
const DEV={pocket:`<div class="pk-koerper">${F}<span class="pk-schirm"><span class="pk-schirm-bild"></span></span><span class="pk-rad"></span><span class="pk-knopf"></span><span class="pk-marke">dji</span></div><div class="pk-stiel">${F}</div><div class="pk-motor">${F}</div><div class="pk-kopf">${F}<span class="pk-linse"><span class="pk-linse-glas"></span></span></div>`,
  mic:`<div class="mic-koerper">${F}<span class="mic-gitter"></span><span class="mic-led"></span><span class="mic-marke">dji</span></div><div class="mic-clip">${F}</div>`};
$$('[data-dev]').forEach(p=>{
  p.innerHTML=DEV[p.dataset.dev];const st=p.parentElement;let ry=-28,rx=-8,drag=false,x0,y0,ry0,rx0,touched=false;
  const set=()=>{p.style.setProperty('--ry',ry+'deg');p.style.setProperty('--rx',rx+'deg')};
  st.addEventListener('pointerdown',e=>{drag=touched=true;x0=e.clientX;y0=e.clientY;ry0=ry;rx0=rx;st.setPointerCapture(e.pointerId)});
  st.addEventListener('pointermove',e=>{if(!drag)return;ry=ry0+(e.clientX-x0)*.55;rx=Math.max(-46,Math.min(46,rx0-(e.clientY-y0)*.35));set()});
  st.addEventListener('pointerup',()=>drag=false);
  if(!reduce){const spin=()=>{if(!touched&&!drag){ry+=.22;set()}requestAnimationFrame(spin)};requestAnimationFrame(spin)}
  set();
});

/* ---------- Vom Skript zum Reel: Reiter, wechseln von selbst nur wenn sichtbar ---------- */
const tabs=$$('.k-tab'),steps=$$('.k-step'),stage=document.querySelector('.k-stage');
if(tabs.length){
  let i=0,el=0,last=performance.now(),hover=false,clicked=false,vis=false;const DUR=6500;
  const bar=()=>tabs.forEach((t,j)=>t.querySelector('.prog').style.transform=`scaleX(${j===i?Math.min(1,el/DUR):0})`);
  const go=n=>{i=n;el=0;tabs.forEach((t,j)=>t.classList.toggle('on',j===i));steps.forEach((s,j)=>s.classList.toggle('on',j===i));stage.style.setProperty('--sc',tabs[i].style.getPropertyValue('--tc'));bar()};
  /* Wer selbst klickt, bestimmt: dann kein automatischer Wechsel mehr */
  tabs.forEach((t,j)=>t.onclick=()=>{clicked=true;go(j)});
  new IntersectionObserver(es=>vis=es[0].isIntersecting,{threshold:.4}).observe(stage);
  stage.addEventListener('mouseenter',()=>hover=true);stage.addEventListener('mouseleave',()=>hover=false);
  go(0);
  if(!reduce)(function tick(now){const dt=now-last;last=now;if(vis&&!hover&&!clicked){el+=dt;if(el>=DUR)go((i+1)%tabs.length);else bar()}requestAnimationFrame(tick)})(performance.now());
}

/* ---------- FAQ aus Daten ---------- */
$$('[data-faq]').forEach(el=>{const F=window.K_FAQ||[];el.innerHTML=F.map(([q,a])=>`<details class="k-q"><summary>${q}</summary><p class="a">${a}</p></details>`).join('')});

/* ---------- Terminkalender (nur Gestaltung, nicht verbunden) ---------- */
$$('.k-cal').forEach(cal=>{
  const MON=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
  const today=new Date();today.setHours(0,0,0,0);let view=new Date(today.getFullYear(),today.getMonth(),1),sel=null;
  const q=s=>cal.querySelector(s);
  const slots=d=>{const w=d.getDay();if(w===0||w===6)return[];return w===5?['09:00','10:30','13:00','15:30']:['17:30','18:15','19:00']};
  const render=()=>{q('.m').textContent=MON[view.getMonth()]+' '+view.getFullYear();q('.p').disabled=view<=new Date(today.getFullYear(),today.getMonth(),1);
    const first=(view.getDay()+6)%7,n=new Date(view.getFullYear(),view.getMonth()+1,0).getDate();let h='';for(let k=0;k<first;k++)h+='<span></span>';
    for(let d=1;d<=n;d++){const dt=new Date(view.getFullYear(),view.getMonth(),d);const ok=dt>today&&slots(dt).length;h+=`<button ${ok?`class="av${sel&&+dt===+sel?' sel':''}"`:'disabled'} data-d="${+dt}">${d}</button>`}
    q('.days').innerHTML=h;cal.querySelectorAll('.days .av').forEach(b=>b.onclick=()=>{sel=new Date(+b.dataset.d);render();rs()})};
  const rs=()=>{const wd=['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'][sel.getDay()];q('.slots h4').textContent=`${wd}, ${sel.getDate()}. ${MON[sel.getMonth()]}`;
    const L=q('.slots .list');L.innerHTML=slots(sel).map(t=>`<button>${t} Uhr</button>`).join('');
    L.querySelectorAll('button').forEach(b=>b.onclick=()=>{L.querySelectorAll('button').forEach(x=>x.classList.remove('sel'));b.classList.add('sel');q('form').classList.add('show');q('.done').style.display='none'})};
  q('.p').onclick=()=>{view=new Date(view.getFullYear(),view.getMonth()-1,1);render()};
  q('.n').onclick=()=>{view=new Date(view.getFullYear(),view.getMonth()+1,1);render()};
  q('form').onsubmit=e=>{e.preventDefault();const f=[...q('form').querySelectorAll('input')].map(i=>i.value.trim());const t=(q('.slots button.sel')||{}).textContent||'';
    const wd=['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'][sel.getDay()];
    const body=`Terminwunsch Erstgespräch: ${wd}, ${sel.getDate()}. ${MON[sel.getMonth()]} ${sel.getFullYear()}, ${t}\n\nName: ${f[0]}\nBetrieb: ${f[1]}\nKontakt: ${f[2]}`;
    location.href='mailto:alejandroarndt@kontor-seo.de?subject='+encodeURIComponent('Terminwunsch Erstgespräch')+'&body='+encodeURIComponent(body);
    q('form').classList.remove('show');q('.done').style.display='block'};
  render();
});

/* ---------- Entwurfsleiste: Schrift (nur in der Vorschau) ---------- */
if(document.body.dataset.draft){
const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}},put=(k,v)=>{try{localStorage.setItem(k,v)}catch(e){}};
const dock=document.createElement('div');dock.className='k-dock';
const names=['Bricolage/Archivo','Schibsted Grotesk','Urbanist','Familjen/Hanken','Geist'];
dock.innerHTML='<span>Entwurf · Schrift</span>'+names.map((n,i)=>`<button title="${n}">${i+1}</button>`).join('')+'<span style="cursor:pointer" class="hide">Leiste aus (H)</span>';
document.body.append(dock);
const setF=v=>{document.body.dataset.font=v;put('k-font',v);dock.querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.textContent===v))};
dock.querySelectorAll('button').forEach(b=>b.onclick=()=>setF(b.textContent));
dock.querySelector('.hide').onclick=()=>document.body.classList.add('clean');
addEventListener('keydown',e=>{if((e.key==='h'||e.key==='H')&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName))document.body.classList.toggle('clean')});
setF(get('k-font')||'1');
}
})();

/* ---------- Anfrageformular: geht per FormSubmit als E-Mail raus ---------- */
(function(){
document.querySelectorAll('.k-form').forEach(f=>{
  const msg=f.querySelector('.k-msg'),btn=f.querySelector('button[type=submit]');
  const show=(cls,html)=>{msg.hidden=false;msg.className='k-msg '+cls;msg.innerHTML=html};
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    if(f.querySelector('.k-hp').value)return;                  // Spam-Falle
    let ok=true;f.querySelectorAll('[required]').forEach(i=>{const bad=i.type==='checkbox'?!i.checked:!i.value.trim()||(i.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value));i.classList.toggle('bad',bad);if(bad)ok=false});
    if(!ok){show('err','Bitte füllen Sie die markierten Felder aus und bestätigen Sie die Einwilligung.');return}
    const fd=new FormData(f),data={};
    for(const [k,v] of fd.entries()){if(k==='_honey')continue;data[k]=data[k]?data[k]+', '+v:v}
    data._subject=`Neue Anfrage: ${data.Betrieb||''} (${data.Ort||''})`;data._template='table';data._replyto=data['E-Mail'];
    btn.disabled=true;btn.textContent='Wird gesendet …';
    try{
      const r=await fetch('https://formsubmit.co/ajax/'+f.dataset.to,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
      const j=await r.json().catch(()=>({}));
      if(!r.ok||String(j.success)==='false'){console.warn('FormSubmit:',r.status,j);throw new Error(j.message||'Fehler')}
      f.querySelectorAll('input,select,textarea,fieldset').forEach(x=>x.style.display='none');f.querySelectorAll('.k-fg,.k-send,.k-chipset,label').forEach(x=>x.style.display='none');
      show('ok','Danke, Ihre Anfrage ist angekommen. Ich melde mich innerhalb von zwei Werktagen.');
    }catch(err){
      console.warn('Anfrage nicht gesendet:',err&&err.message);
      show('err','Das hat leider nicht geklappt. Schreiben Sie mir bitte direkt an <a href="mailto:'+f.dataset.to+'">'+f.dataset.to+'</a>.');
    }finally{btn.disabled=false;btn.textContent='Anfrage senden'}
  });
});
})();
