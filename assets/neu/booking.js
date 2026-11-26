/* ---------- Kontor Terminbuchung: eigenes Widget, Backend ist ein Google Apps Script ----------
   Markup: <div class="k-bk" data-api="https://script.google.com/macros/s/.../exec" data-fallback="Google-Buchungsseite"></div>
   GET  api?a=slots           -> {ok, tage:{'2026-12-01':['09:00',...]}}
   POST api {a:'book', ...}   -> {ok, wann} | {ok:false, fehler}
   POST api {a:'rueckruf',..} -> {ok}
   Die freien Zeiten werden erst geladen, wenn das Widget in Sichtweite kommt. */
(function(){
const MON=['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'];
const WT=['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'];
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const key=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
const fromKey=k=>{const [y,m,d]=k.split('-').map(Number);return new Date(y,m-1,d)};
const ICON={
  uhr:'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  cam:'<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/></svg>',
  ok:'<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
  l:'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 6l-6 6 6 6"/></svg>',
  r:'<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>'
};

document.querySelectorAll('.k-bk').forEach(box=>{
  const api=box.dataset.api||'',fallback=box.dataset.fallback||'';
  const st={tab:'termin',tage:null,err:false,view:null,day:null,time:null,step:'wahl',busy:false,msg:'',done:null};

  const fallbackHtml=()=>`<div class="k-bk-note">Der Kalender lädt gerade nicht. ${fallback?`<a href="${esc(fallback)}" target="_blank" rel="noopener">Termin hier direkt buchen</a> oder `:''}rufen Sie an: <a href="tel:+491771885605">0177 188 5605</a>.</div>`;

  function kopf(){
    return `<div class="k-bk-hd">
      <img src="assets/img/alejandro-avatar.jpg" alt="Alejandro Arndt" width="56" height="56" loading="lazy">
      <div><small>Alejandro Arndt, Kontor</small><h3>Erstgespräch</h3>
      <p class="k-bk-meta"><span>${ICON.uhr}30 Min.</span><span>${ICON.cam}Google Meet, Link per Mail</span></p></div>
    </div>
    <div class="k-bk-tabs" role="tablist">
      <button type="button" role="tab" aria-selected="${st.tab==='termin'}" data-tab="termin">Termin</button>
      <button type="button" role="tab" aria-selected="${st.tab==='rueckruf'}" data-tab="rueckruf">Rückruf</button>
    </div>`;
  }

  function kalender(){
    if(st.err)return fallbackHtml();
    if(!st.tage)return `<div class="k-bk-load"><span></span>Freie Termine werden geladen …</div>`;
    const tage=Object.keys(st.tage).sort();
    if(!tage.length)return `<div class="k-bk-note">Gerade sind keine Termine frei. Schreiben Sie mir oder bitten Sie um einen Rückruf.</div>`;
    if(!st.view){const f=fromKey(tage[0]);st.view=new Date(f.getFullYear(),f.getMonth(),1)}
    const v=st.view,first=new Date(v.getFullYear(),v.getMonth(),1),last=new Date(v.getFullYear(),v.getMonth()+1,0);
    const minM=fromKey(tage[0]),maxM=fromKey(tage[tage.length-1]);
    const canPrev=v>new Date(minM.getFullYear(),minM.getMonth(),1),canNext=v<new Date(maxM.getFullYear(),maxM.getMonth(),1);
    let cells='';
    let f1=new Date(first);while(f1.getDay()===0||f1.getDay()===6)f1.setDate(f1.getDate()+1);
    const lead=(f1.getDay()+6)%7;                          // erster Werktag: Mo = 0 ... Fr = 4
    for(let i=0;i<lead;i++)cells+='<span></span>';
    for(let d=1;d<=last.getDate();d++){
      const dt=new Date(v.getFullYear(),v.getMonth(),d),w=dt.getDay();
      if(w===0||w===6)continue;
      const k=key(dt),frei=!!st.tage[k];
      cells+=frei?`<button type="button" class="av${st.day===k?' sel':''}" data-day="${k}" aria-label="${WT[w]}, ${d}. ${MON[dt.getMonth()]}">${d}</button>`:`<span class="no">${d}</span>`;
    }
    let slots='';
    if(st.day&&st.tage[st.day]){
      const dd=fromKey(st.day);
      slots=`<div class="k-bk-slots"><h4>${WT[dd.getDay()]}, ${dd.getDate()}. ${MON[dd.getMonth()]}</h4><div class="k-bk-times">`+
        st.tage[st.day].map(t=>`<button type="button" data-time="${t}" class="${st.time===t?'sel':''}">${t}</button>`).join('')+`</div></div>`;
    }
    return `<p class="k-bk-lbl">Datum und Uhrzeit wählen</p>
      <div class="k-bk-mon"><button type="button" class="pv" ${canPrev?'':'disabled'} aria-label="Vorheriger Monat">${ICON.l}</button><b>${MON[v.getMonth()]} ${v.getFullYear()}</b><button type="button" class="nx" ${canNext?'':'disabled'} aria-label="Nächster Monat">${ICON.r}</button></div>
      <div class="k-bk-grid"><i>Mo</i><i>Di</i><i>Mi</i><i>Do</i><i>Fr</i>${cells}</div>${slots}`;
  }

  function formular(){
    const dd=fromKey(st.day);
    return `<div class="k-bk-sum"><div><small>Ihr Termin</small><b>${WT[dd.getDay()]}, ${dd.getDate()}. ${MON[dd.getMonth()]}, ${st.time} Uhr</b></div><button type="button" class="k-bk-back">Ändern</button></div>
    <form class="k-bk-form" novalidate>
      <div class="k-bk-2"><label>Vorname<input name="vorname" required autocomplete="given-name"></label><label>Nachname<input name="nachname" required autocomplete="family-name"></label></div>
      <label>E-Mail<input type="email" name="email" required autocomplete="email"></label>
      <label>Betrieb und Ort<input name="betrieb" required placeholder="z. B. Autohaus Muster, Göppingen" autocomplete="organization"></label>
      <label>Was möchten Sie aus dem Gespräch mitnehmen?<input name="ziel" required maxlength="300" placeholder="Ein Satz reicht"></label>
      <input name="hp" class="k-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label class="k-bk-ok"><input type="checkbox" required><span>Ich bin einverstanden, dass meine Angaben für den Termin verarbeitet werden. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
      ${st.msg?`<p class="k-bk-err">${st.msg}</p>`:''}
      <button class="kb kb-fill" type="submit" ${st.busy?'disabled':''}>${st.busy?'Wird gebucht …':'Termin buchen'}</button>
    </form>`;
  }

  function rueckruf(){
    return `<p class="k-bk-lbl">Lieber erst telefonieren? Ich rufe Sie zurück.</p>
    <form class="k-bk-form" data-kind="rueckruf" novalidate>
      <label>Name<input name="name" required autocomplete="name"></label>
      <label>Betrieb und Ort<input name="betrieb" required autocomplete="organization"></label>
      <label>Telefon<input type="tel" name="telefon" required autocomplete="tel"></label>
      <fieldset class="k-bk-chips"><legend>Am besten erreichbar</legend>
        ${['Vormittags','Mittags','Nachmittags','Egal'].map((z,i)=>`<label><input type="radio" name="zeit" value="${z}" ${i===3?'checked':''}><span>${z}</span></label>`).join('')}
      </fieldset>
      <input name="hp" class="k-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <label class="k-bk-ok"><input type="checkbox" required><span>Ich bin einverstanden, dass meine Angaben für den Rückruf verarbeitet werden. Mehr in der <a href="datenschutz.html">Datenschutzerklärung</a>.</span></label>
      ${st.msg?`<p class="k-bk-err">${st.msg}</p>`:''}
      <button class="kb kb-fill" type="submit" ${st.busy?'disabled':''}>${st.busy?'Wird gesendet …':'Rückruf anfordern'}</button>
    </form>`;
  }

  function fertig(){
    return st.done.kind==='rueckruf'
      ?`<div class="k-bk-done"><i>${ICON.ok}</i><h4>Danke, ich rufe Sie zurück.</h4><p>Meistens noch am selben oder am nächsten Werktag.</p></div>`
      :`<div class="k-bk-done"><i>${ICON.ok}</i><h4>Termin gebucht</h4><p><b>${esc(st.done.wann)}</b></p><p>Bestätigung und Google-Meet-Link sind per E-Mail unterwegs. Einen Tag vorher kommt eine kurze Erinnerung.</p></div>`;
  }

  function render(){
    let body;
    if(st.done)body=fertig();
    else if(st.tab==='rueckruf')body=rueckruf();
    else body=st.step==='form'?formular():kalender();
    box.innerHTML=`<div class="k-bk-in">${kopf()}<div class="k-bk-body">${body}</div></div>`;
    bind();
  }

  function bind(){
    box.querySelectorAll('[data-tab]').forEach(b=>b.onclick=()=>{st.tab=b.dataset.tab;st.msg='';st.done=null;render()});
    const pv=box.querySelector('.pv'),nx=box.querySelector('.nx');
    if(pv)pv.onclick=()=>{st.view=new Date(st.view.getFullYear(),st.view.getMonth()-1,1);render()};
    if(nx)nx.onclick=()=>{st.view=new Date(st.view.getFullYear(),st.view.getMonth()+1,1);render()};
    box.querySelectorAll('[data-day]').forEach(b=>b.onclick=()=>{st.day=b.dataset.day;st.time=null;render();const s=box.querySelector('.k-bk-slots');if(s)s.scrollIntoView({block:'nearest',behavior:'smooth'})});
    box.querySelectorAll('[data-time]').forEach(b=>b.onclick=()=>{st.time=b.dataset.time;st.step='form';st.msg='';render();const f=box.querySelector('input[name=vorname]');if(f)f.focus({preventScroll:true})});
    const back=box.querySelector('.k-bk-back');if(back)back.onclick=()=>{st.step='wahl';st.msg='';render()};
    const f=box.querySelector('.k-bk-form');if(f)f.onsubmit=senden;
  }

  async function senden(e){
    e.preventDefault();
    const f=e.target;let ok=true;
    f.querySelectorAll('[required]').forEach(i=>{const bad=i.type==='checkbox'?!i.checked:!i.value.trim()||(i.type==='email'&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value));i.classList.toggle('bad',bad);if(bad)ok=false});
    if(!ok){st.msg='Bitte füllen Sie die markierten Felder aus und bestätigen Sie die Einwilligung.';const p=f.querySelector('.k-bk-err');if(p)p.textContent=st.msg;else f.querySelector('button[type=submit]').insertAdjacentHTML('beforebegin',`<p class="k-bk-err">${st.msg}</p>`);return}
    const d=Object.fromEntries(new FormData(f).entries());
    const rr=f.dataset.kind==='rueckruf';
    d.a=rr?'rueckruf':'book';if(!rr){d.tag=st.day;d.zeit=st.time}
    const werte={...d};                                      // Eingaben behalten, falls etwas schiefgeht
    st.busy=true;st.msg='';render();refill(werte);
    try{
      const r=await fetch(api,{method:'POST',body:JSON.stringify(d)});
      const j=await r.json();
      if(!j.ok){
        if(j.fehler==='vergeben'){st.msg='Dieser Termin wurde gerade vergeben. Bitte wählen Sie einen anderen.';st.step='wahl';st.time=null;st.busy=false;await laden(true);return}
        throw new Error(j.fehler||'Fehler');
      }
      st.done={kind:rr?'rueckruf':'termin',wann:j.wann||''};
    }catch(err){
      st.msg='Das hat leider nicht geklappt. Bitte versuchen Sie es noch einmal oder schreiben Sie an <a href="mailto:alejandroarndt@kontor-seo.de">alejandroarndt@kontor-seo.de</a>.';
    }
    st.busy=false;render();if(!st.done)refill(werte);
  }

  function refill(w){const f=box.querySelector('.k-bk-form');if(!f)return;Object.entries(w).forEach(([k,v])=>{const i=f.querySelector(`[name="${k}"]`);if(i&&i.type!=='radio')i.value=v});f.querySelectorAll('input[type=checkbox]').forEach(c=>c.checked=true)}

  async function laden(neu){
    if(!api){st.err=true;render();return}
    try{
      const r=await fetch(api+'?a=slots'+(neu?'&t='+Date.now():''));
      const j=await r.json();
      if(!j.ok)throw new Error('slots');
      st.tage=j.tage||{};st.err=false;
      if(st.day&&!st.tage[st.day])st.day=null;
    }catch(e){st.err=true}
    render();
  }

  render();
  const io=new IntersectionObserver(es=>{if(es.some(x=>x.isIntersecting)){io.disconnect();laden()}},{rootMargin:'300px'});
  io.observe(box);
});
})();
