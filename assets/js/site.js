/* No external dependencies, no cookies, no tracking. */
(function () {
  'use strict';

  /* ---- sticky header ---- */
  var hdr = document.querySelector('.hdr');
  var onScroll = function () {
    if (hdr) hdr.classList.toggle('scrolled', window.scrollY > 24);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---- mobile nav ---- */
  var burger = document.querySelector('.burger');
  var mnav = document.querySelector('.mnav');
  if (burger && mnav) {
    var toggle = function (force) {
      var open = typeof force === 'boolean' ? force : !mnav.classList.contains('open');
      mnav.classList.toggle('open', open);
      burger.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    burger.addEventListener('click', function () { toggle(); });
    mnav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') toggle(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') toggle(false);
    });
  }

  /* ---- scroll reveal ---- */
  var reveals = document.querySelectorAll('.rv, .serp');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---- animated counters ---- */
  var nums = document.querySelectorAll('[data-count]');
  if (nums.length && 'IntersectionObserver' in window) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        cio.unobserve(el);
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var prefix = el.getAttribute('data-prefix') || '';
        if (reduce) { el.textContent = prefix + target + suffix; return; }
        var dur = 1500, t0 = null;
        var tick = function (ts) {
          if (!t0) t0 = ts;
          var p = Math.min((ts - t0) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          var val = target % 1 ? (target * eased).toFixed(1) : Math.round(target * eased);
          el.textContent = prefix + val + suffix;
          if (p < 1) requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      });
    }, { threshold: 0.5 });
    nums.forEach(function (el) { cio.observe(el); });
  }

  /* ---- Handyvideos im Gratismonat ----
     Zwei gleichzeitig wischende Videos sehen sofort nach Attrappe aus.
     Deshalb laufen sie unterschiedlich lang und das rechte startet
     versetzt. Bei reduzierter Bewegung bleibt das Standbild stehen. */
  var reels = document.querySelectorAll('.phone-screen video');
  if (reels.length) {
    var ruhig = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    Array.prototype.forEach.call(reels, function (v) {
      if (ruhig) {
        v.removeAttribute('autoplay');
        v.addEventListener('play', function () { v.pause(); });
        v.pause();
        return;
      }
      var versatz = parseFloat(v.getAttribute('data-versatz') || '0');
      var setzen = function () {
        if (versatz && v.duration && versatz < v.duration) {
          try { v.currentTime = versatz; } catch (e) {}
        }
      };
      if (v.readyState >= 1) setzen();
      else v.addEventListener('loadedmetadata', setzen);
    });

    /* Auf dem Handy startet autoplay nicht zuverlaessig, wenn das Video beim
       Laden noch weit unterhalb des Bildschirms liegt. Safari auf iOS laesst
       es dann einfach stehen, und man muesste auf Abspielen tippen. Deshalb
       wird hier angestossen, sobald der Abschnitt in Sicht kommt, und wieder
       angehalten, wenn er weg ist. Das spart ausserdem Akku. */
    if (!ruhig) {
      /* iOS verlangt die Eigenschaft, nicht nur das Attribut. Ohne sie gilt das
         Video als nicht stumm und autoplay wird verweigert. */
      Array.prototype.forEach.call(reels, function (v) {
        v.muted = true;
        v.setAttribute('muted', '');
        v.playsInline = true;
      });

      var inSicht = [];
      var anstossen = function (v) {
        /* Der Versatz muss beim ersten echten Start sitzen. Setzt man ihn nur
           beim Laden der Metadaten, beginnt das Video beim Abspielen doch
           wieder bei null und beide Handys wischen im Gleichschritt. */
        if (!v.getAttribute('data-versetzt')) {
          var vz = parseFloat(v.getAttribute('data-versatz') || '0');
          if (vz && v.duration && vz < v.duration) {
            try { v.currentTime = vz; } catch (e) {}
          }
          v.setAttribute('data-versetzt', '1');
        }
        var p = v.play();
        if (p && p['catch']) {
          p['catch'](function () {
            /* Abgelehnt, etwa im Stromsparmodus. Dann beim ersten Tippen
               irgendwo auf der Seite noch einmal versuchen. */
            nachTipp();
          });
        }
      };
      var getippt = false;
      var nachTipp = function () {
        if (getippt) return;
        getippt = true;
        var los = function () {
          inSicht.forEach(function (v) {
            var p = v.play();
            if (p && p['catch']) { p['catch'](function () {}); }
          });
          document.removeEventListener('touchstart', los);
          document.removeEventListener('click', los);
        };
        document.addEventListener('touchstart', los, { passive: true, once: true });
        document.addEventListener('click', los, { once: true });
      };

      if ('IntersectionObserver' in window) {
        var vio = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            var v = en.target;
            var i = inSicht.indexOf(v);
            if (en.isIntersecting) {
              if (i < 0) inSicht.push(v);
              anstossen(v);
            } else {
              if (i >= 0) inSicht.splice(i, 1);
              if (!v.paused) v.pause();
            }
          });
        }, { threshold: 0.15 });
        Array.prototype.forEach.call(reels, function (v) { vio.observe(v); });
      } else {
        Array.prototype.forEach.call(reels, function (v) {
          inSicht.push(v); anstossen(v);
        });
      }
    }
  }

  /* ---- Sprungmarke auf ein Klappfeld: aufklappen und hinscrollen ----
     Die Felder auf der Startseite verweisen auf einzelne Punkte der
     Leistungsseite. Ohne das hier landet man oben auf einem zugeklappten Feld. */
  var oeffneZiel = function () {
    if (!window.location.hash) return;
    var ziel;
    try { ziel = document.querySelector(window.location.hash); } catch (e) { return; }
    if (!ziel || ziel.tagName !== 'DETAILS') return;
    ziel.open = true;
    var sanft = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    ziel.scrollIntoView({ block: 'start', behavior: sanft ? 'smooth' : 'auto' });
  };
  oeffneZiel();
  window.addEventListener('hashchange', oeffneZiel);

  /* ---- Bildergalerie auf der Referenzseite ---- */
  var gal = document.querySelector('[data-gal]');
  if (gal) {
    var spur = gal.querySelector('.gal-spur');
    var punkte = document.querySelectorAll('.gal-punkt');
    var anzahl = spur.children.length;
    var zeige = function (i) {
      i = Math.max(0, Math.min(anzahl - 1, i));
      var ziel = spur.clientWidth * i;
      var sanft = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      spur.scrollTo({ left: ziel, behavior: sanft ? 'smooth' : 'auto' });
      /* In manchen Browsern wird ein weiches Scrollen von
         scroll-snap-type: mandatory verschluckt und es passiert gar nichts.
         Deshalb kurz nachsehen und notfalls hart setzen. */
      if (sanft) {
        window.setTimeout(function () {
          if (Math.abs(spur.scrollLeft - ziel) > 4) {
            spur.scrollTo({ left: ziel, behavior: 'auto' });
          }
        }, 320);
      }
    };
    var aktuell = function () { return Math.round(spur.scrollLeft / spur.clientWidth); };
    gal.querySelector('.gal-vor').addEventListener('click', function () { zeige(aktuell() + 1); });
    gal.querySelector('.gal-zurueck').addEventListener('click', function () { zeige(aktuell() - 1); });
    Array.prototype.forEach.call(punkte, function (k, i) {
      k.addEventListener('click', function () { zeige(i); });
    });
    var merk = -1;
    spur.addEventListener('scroll', function () {
      var i = aktuell();
      if (i === merk) return;
      merk = i;
      Array.prototype.forEach.call(punkte, function (k, j) { k.classList.toggle('an', j === i); });
    }, { passive: true });
  }

  /* ---- Die Geraete drehen und durchblaettern ----
     Gedreht wird nur das Geraet. Die Neigung ist begrenzt, sonst steht es
     irgendwann auf dem Kopf. */
  var buehnen = document.querySelectorAll('.pocket-stage');
  Array.prototype.forEach.call(buehnen, function (stage) {
    var teil = stage.querySelector('.pocket');
    if (!teil) return;
    var ry = -28, rx = -8, zieht = false, x0 = 0, y0 = 0, ry0 = 0, rx0 = 0;
    var klemm = function (v, min, max) { return v < min ? min : (v > max ? max : v); };
    var setzen = function () {
      teil.style.setProperty('--ry', ry + 'deg');
      teil.style.setProperty('--rx', rx + 'deg');
    };
    stage.addEventListener('pointerdown', function (e) {
      zieht = true; x0 = e.clientX; y0 = e.clientY; ry0 = ry; rx0 = rx;
      teil.classList.add('greift');
      stage.setPointerCapture(e.pointerId);
    });
    stage.addEventListener('pointermove', function (e) {
      if (!zieht) return;
      ry = ry0 + (e.clientX - x0) * 0.55;
      rx = klemm(rx0 - (e.clientY - y0) * 0.35, -46, 46);
      setzen();
    });
    var los = function (e) {
      if (!zieht) return;
      zieht = false;
      teil.classList.remove('greift');
      if (e && e.pointerId != null && stage.hasPointerCapture(e.pointerId)) {
        stage.releasePointerCapture(e.pointerId);
      }
    };
    stage.addEventListener('pointerup', los);
    stage.addEventListener('pointercancel', los);
    teil.addEventListener('keydown', function (e) {
      var k = e.key, schritt = 12;
      if (k === 'ArrowLeft') { ry -= schritt; }
      else if (k === 'ArrowRight') { ry += schritt; }
      else if (k === 'ArrowUp') { rx = klemm(rx + schritt, -46, 46); }
      else if (k === 'ArrowDown') { rx = klemm(rx - schritt, -46, 46); }
      else { return; }
      e.preventDefault();
      setzen();
    });
    setzen();
  });

  var geraete = document.querySelector('[data-geraete]');
  if (geraete) {
    var liste = geraete.querySelectorAll('.geraet');
    var schild = document.querySelector('[data-geraet-name]');
    var nr = 0;
    var zeigeGeraet = function (i) {
      nr = (i + liste.length) % liste.length;
      Array.prototype.forEach.call(liste, function (g, j) { g.hidden = j !== nr; });
      if (schild) schild.textContent = liste[nr].getAttribute('data-name');
    };
    geraete.querySelector('.geraet-vor').addEventListener('click', function () { zeigeGeraet(nr + 1); });
    geraete.querySelector('.geraet-zurueck').addEventListener('click', function () { zeigeGeraet(nr - 1); });
    zeigeGeraet(0);
  }

  /* ---- active nav link by scroll position (homepage only) ---- */
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav a[href^="#"]');
  if (sections.length && navLinks.length && 'IntersectionObserver' in window) {
    var sio = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var id = en.target.getAttribute('id');
        navLinks.forEach(function (a) {
          a.classList.toggle('active', a.getAttribute('href') === '#' + id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { sio.observe(s); });
  }

  /* ---- pause hero video when offscreen (saves battery/data) ---- */
  var hv = document.querySelector('.hero-media video');
  if (hv && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { var p = hv.play(); if (p) p.catch(function () {}); }
        else { hv.pause(); }
      });
    }, { threshold: 0.05 }).observe(hv);
  }
})();

/* ---- Referenzen category filter ---- */
(function () {
  'use strict';
  var bar = document.querySelector('.ref-filters');
  if (!bar) return;
  var cards = [].slice.call(document.querySelectorAll('.ref-card, .post[data-cats]'));
  var empty = document.querySelector('.ref-empty');
  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('.ref-filter');
    if (!btn) return;
    var cat = btn.getAttribute('data-cat');
    bar.querySelectorAll('.ref-filter').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b === btn));
    });
    var shown = 0;
    cards.forEach(function (c) {
      var hit = cat === 'alle' || (c.getAttribute('data-cats') || '').split(' ').indexOf(cat) > -1;
      c.hidden = !hit;
      if (hit) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  });
})();

/* ---- Terminbuchung: Kalender erst nach dem Klick laden ----------------
   Vorher geht keine Anfrage an Google. Der Link daneben bleibt immer
   erreichbar, falls Google das Einbetten der Seite ablehnt. */
(function () {
  var box = document.querySelector('.book[data-booking]');
  if (!box) return;
  var url = box.getAttribute('data-booking');
  var btn = box.querySelector('.book-go');
  var hint = box.querySelector('.book-hint');
  var fallback = box.querySelector('.book-fallback');
  var ready = url && url.indexOf('http') === 0;

  if (!ready) {
    // Noch keine Buchungsseite hinterlegt: nicht so tun, als gaebe es eine.
    if (btn) btn.remove();
    if (hint) hint.textContent = 'Die Buchungsseite wird gerade eingerichtet. Schreiben Sie uns bis dahin kurz eine Mail, wir melden uns am selben Werktag.';
    if (fallback) fallback.remove();
    return;
  }

  btn.addEventListener('click', function () {
    var frame = document.createElement('iframe');
    frame.src = url;
    frame.title = 'Terminbuchung';
    frame.loading = 'lazy';
    frame.className = 'book-frame';
    frame.setAttribute('referrerpolicy', 'no-referrer-when-downgrade');
    btn.remove();
    if (hint) hint.remove();
    box.appendChild(frame);
    if (fallback) fallback.hidden = false;
  });
})();

/* ---- Kapitelverzeichnis einer Beitragsseite --------------------------
   Entsteht aus allen h2 des Beitrags, wie bei PoseyPets. Ohne h2 bleibt
   der Kasten ausgeblendet. */
(function () {
  var box = document.querySelector('.art-toc');
  var body = document.querySelector('.art-body');
  if (!box || !body) return;
  var heads = [].slice.call(body.querySelectorAll('h2'));
  if (!heads.length) return;

  var list = box.querySelector('ol');
  var links = [];
  heads.forEach(function (h, i) {
    if (!h.id) {
      h.id = 'kap-' + (i + 1) + '-' + h.textContent.toLowerCase()
        .replace(/[äöüß]/g, function (c) { return {'ä':'ae','ö':'oe','ü':'ue','ß':'ss'}[c]; })
        .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 40);
    }
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    li.appendChild(a);
    list.appendChild(li);
    links.push(a);
  });
  box.hidden = false;

  if (!('IntersectionObserver' in window)) return;
  var seen = {};
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { seen[en.target.id] = en.isIntersecting; });
    var active = null;
    heads.forEach(function (h) { if (seen[h.id] && !active) active = h.id; });
    links.forEach(function (a) {
      a.classList.toggle('on', !!active && a.getAttribute('href') === '#' + active);
    });
  }, { rootMargin: '-90px 0px -65% 0px' });
  heads.forEach(function (h) { io.observe(h); });
})();
