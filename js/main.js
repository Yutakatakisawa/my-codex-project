/**
 * TAKISAWA ROOF - JS (Mobile-Fixed)
 */

document.addEventListener('DOMContentLoaded', () => {
  initLoader();
  initScrollProgress();
  initHeader();
  initMobileNav();
  initSmoothScroll();
  initActiveNav();
  initRevealAnimations();
  initTyping();
  initParticles();
  initServiceTabs();
  initTimeline();
  initCarousel();
  initFAQ();
  initBackToTop();
  initContactForm();
  initCountUp();
  initTilt();
});

/* ===== LOADER ===== */
function initLoader() {
  const loader = document.getElementById('loader');
  if (!loader) return;
  function hide() { loader.classList.add('hide'); }
  window.addEventListener('load', () => setTimeout(hide, 600));
  setTimeout(hide, 2500);
}

/* ===== SCROLL PROGRESS ===== */
function initScrollProgress() {
  const bar = document.getElementById('scrollProgress');
  if (!bar) return;
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ===== HEADER ===== */
function initHeader() {
  const header = document.getElementById('header');
  if (!header) return;
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        header.classList.toggle('header--scrolled', window.scrollY > 30);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
}

/* ===== MOBILE NAV ===== */
function initMobileNav() {
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');
  if (!hamburger || !nav) return;

  const overlay = document.createElement('div');
  overlay.classList.add('nav-overlay');
  document.body.appendChild(overlay);

  function toggle(open) {
    nav.classList.toggle('open', open);
    hamburger.classList.toggle('active', open);
    overlay.classList.toggle('show', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  hamburger.addEventListener('click', () => toggle(!nav.classList.contains('open')));
  overlay.addEventListener('click', () => toggle(false));
  nav.querySelectorAll('.header__nav-link').forEach(l =>
    l.addEventListener('click', () => toggle(false))
  );
  window.addEventListener('resize', () => {
    if (window.innerWidth > 1024) toggle(false);
  });
}

/* ===== SMOOTH SCROLL ===== */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#') return;
      e.preventDefault();
      const target = document.querySelector(href);
      if (!target) return;
      const offset = document.getElementById('header')?.offsetHeight || 64;
      window.scrollTo({
        top: target.getBoundingClientRect().top + window.scrollY - offset,
        behavior: 'smooth'
      });
    });
  });
}

/* ===== ACTIVE NAV ===== */
function initActiveNav() {
  const links = document.querySelectorAll('[data-nav]');
  const sections = [];
  links.forEach(l => {
    const s = document.querySelector(l.getAttribute('href'));
    if (s) sections.push({ el: s, link: l });
  });
  if (!sections.length) return;

  let ticking = false;
  function update() {
    const scrollY = window.scrollY + 100;
    let current = sections[0];
    for (const s of sections) {
      if (s.el.offsetTop <= scrollY) current = s;
    }
    links.forEach(l => l.classList.remove('active'));
    current.link.classList.add('active');
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => { update(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });
  update();
}

/* ===== REVEAL ANIMATIONS ===== */
function initRevealAnimations() {
  const els = document.querySelectorAll('[data-reveal]');
  if (!els.length) return;

  if (!('IntersectionObserver' in window)) {
    els.forEach(el => el.classList.add('revealed'));
    return;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = parseInt(entry.target.dataset.delay || 0);
        setTimeout(() => entry.target.classList.add('revealed'), delay);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

  els.forEach(el => observer.observe(el));
}

/* ===== TYPING ===== */
function initTyping() {
  const el = document.getElementById('heroTyping');
  if (!el) return;

  const words = ['屋根工事専門店', '雨漏り修理', '屋根リフォーム', '雪止め工事'];
  let wordIdx = 0, charIdx = 0, isDeleting = false;

  function type() {
    const current = words[wordIdx];
    if (isDeleting) {
      charIdx--;
    } else {
      charIdx++;
    }
    el.textContent = current.substring(0, charIdx);

    let speed = isDeleting ? 50 : 100;
    if (!isDeleting && charIdx === current.length) {
      speed = 2200;
      isDeleting = true;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      wordIdx = (wordIdx + 1) % words.length;
      speed = 350;
    }
    setTimeout(type, speed);
  }

  setTimeout(type, 1000);
}

/* ===== PARTICLES ===== */
function initParticles() {
  const container = document.getElementById('heroParticles');
  if (!container) return;

  const canvas = document.createElement('canvas');
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let w, h, particles = [];
  const isMobile = window.innerWidth < 640;
  const count = isMobile ? 20 : 50;
  const connectDist = isMobile ? 80 : 110;
  let animId;

  function resize() {
    const rect = container.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = rect.width;
    h = rect.height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function createParticles() {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.5 + 0.5,
        dx: (Math.random() - 0.5) * 0.4,
        dy: (Math.random() - 0.5) * 0.4,
        alpha: Math.random() * 0.35 + 0.1
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    for (const p of particles) {
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,' + p.alpha + ')';
      ctx.fill();
    }

    if (!isMobile) {
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const a = particles[i], b = particles[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < connectDist) {
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.strokeStyle = 'rgba(255,255,255,' + (0.05 * (1 - dist / connectDist)) + ')';
            ctx.stroke();
          }
        }
      }
    }

    animId = requestAnimationFrame(draw);
  }

  resize();
  createParticles();
  draw();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      resize();
      createParticles();
    }, 200);
  });
}

/* ===== SERVICE TABS ===== */
function initServiceTabs() {
  const tabs = document.querySelectorAll('.services__tab');
  const cards = document.querySelectorAll('.svc');
  if (!tabs.length || !cards.length) return;

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const filter = tab.dataset.tab;

      cards.forEach((card, i) => {
        const show = filter === 'all' || card.dataset.category === filter;
        if (!show) {
          card.classList.add('hidden');
        } else {
          card.classList.remove('hidden');
          card.style.opacity = '0';
          card.style.transform = 'translateY(16px)';
          setTimeout(() => {
            card.style.transition = 'opacity .35s ease, transform .35s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, i * 50);
        }
      });
    });
  });
}

/* ===== TIMELINE ===== */
function initTimeline() {
  const timeline = document.getElementById('timeline');
  const fill = document.getElementById('timelineFill');
  if (!timeline || !fill) return;

  const steps = timeline.querySelectorAll('.process__step');
  let ticking = false;

  function update() {
    const rect = timeline.getBoundingClientRect();
    const trigger = window.innerHeight * 0.6;
    const progress = Math.min(Math.max((trigger - rect.top) / rect.height, 0), 1);
    fill.style.height = (progress * 100) + '%';

    steps.forEach(step => {
      const r = step.getBoundingClientRect();
      step.classList.toggle('active', (r.top + r.height / 2) < trigger);
    });
  }

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => { update(); ticking = false; });
      ticking = true;
    }
  }, { passive: true });
  update();
}

/* ===== CAROUSEL ===== */
function initCarousel() {
  const track = document.getElementById('worksTrack');
  const prevBtn = document.getElementById('worksPrev');
  const nextBtn = document.getElementById('worksNext');
  const dotsEl = document.getElementById('worksDots');
  if (!track || !prevBtn || !nextBtn || !dotsEl) return;

  const slides = Array.from(track.querySelectorAll('.works__slide'));
  let idx = 0;
  const gap = 20;

  function perView() {
    const vw = window.innerWidth;
    if (vw < 640) return 1;
    if (vw < 1024) return 2;
    return 3;
  }

  function slideWidth() {
    const containerW = track.parentElement.clientWidth;
    const pv = perView();
    return (containerW - gap * (pv - 1)) / pv;
  }

  function maxIdx() {
    return Math.max(0, slides.length - perView());
  }

  function setSlideWidths() {
    const sw = slideWidth();
    slides.forEach(s => { s.style.width = sw + 'px'; s.style.flexShrink = '0'; });
    track.style.gap = gap + 'px';
  }

  function goTo(i) {
    idx = Math.min(Math.max(i, 0), maxIdx());
    const sw = slideWidth();
    track.style.transform = 'translateX(' + (-(sw + gap) * idx) + 'px)';
    updateDots();
  }

  function buildDots() {
    dotsEl.innerHTML = '';
    const count = maxIdx() + 1;
    for (let i = 0; i < count; i++) {
      const d = document.createElement('div');
      d.classList.add('works__dot');
      if (i === idx) d.classList.add('active');
      d.addEventListener('click', () => goTo(i));
      dotsEl.appendChild(d);
    }
  }

  function updateDots() {
    dotsEl.querySelectorAll('.works__dot').forEach((d, i) => {
      d.classList.toggle('active', i === idx);
    });
  }

  prevBtn.addEventListener('click', () => goTo(idx - 1));
  nextBtn.addEventListener('click', () => goTo(idx + 1));

  // Touch/drag
  let dragging = false, startX = 0, startTranslate = 0;

  function onStart(x) {
    dragging = true;
    startX = x;
    const sw = slideWidth();
    startTranslate = -(sw + gap) * idx;
    track.classList.add('dragging');
  }

  function onMove(x) {
    if (!dragging) return;
    const diff = x - startX;
    track.style.transform = 'translateX(' + (startTranslate + diff) + 'px)';
  }

  function onEnd(x) {
    if (!dragging) return;
    dragging = false;
    track.classList.remove('dragging');
    const diff = x - startX;
    if (diff < -40) goTo(idx + 1);
    else if (diff > 40) goTo(idx - 1);
    else goTo(idx);
  }

  track.addEventListener('touchstart', e => onStart(e.touches[0].clientX), { passive: true });
  track.addEventListener('touchmove', e => onMove(e.touches[0].clientX), { passive: true });
  track.addEventListener('touchend', e => onEnd(e.changedTouches[0].clientX));

  track.addEventListener('mousedown', e => { e.preventDefault(); onStart(e.clientX); });
  document.addEventListener('mousemove', e => onMove(e.clientX));
  document.addEventListener('mouseup', e => onEnd(e.clientX));

  // Resize
  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
      idx = Math.min(idx, maxIdx());
      setSlideWidths();
      buildDots();
      goTo(idx);
    }, 150);
  });

  setSlideWidths();
  buildDots();

  // Auto-play
  let auto = setInterval(() => goTo((idx + 1) % (maxIdx() + 1)), 5000);
  track.addEventListener('touchstart', () => clearInterval(auto), { passive: true });
  track.addEventListener('mouseenter', () => clearInterval(auto));
  track.addEventListener('touchend', () => {
    auto = setInterval(() => goTo((idx + 1) % (maxIdx() + 1)), 5000);
  });
  track.addEventListener('mouseleave', () => {
    auto = setInterval(() => goTo((idx + 1) % (maxIdx() + 1)), 5000);
  });
}

/* ===== FAQ ===== */
function initFAQ() {
  document.querySelectorAll('.faq__item').forEach(item => {
    const q = item.querySelector('.faq__q');
    if (!q) return;
    q.addEventListener('click', () => {
      const open = item.classList.contains('open');
      document.querySelectorAll('.faq__item').forEach(i => {
        i.classList.remove('open');
        i.querySelector('.faq__q')?.setAttribute('aria-expanded', 'false');
      });
      if (!open) {
        item.classList.add('open');
        q.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* ===== BACK TO TOP ===== */
function initBackToTop() {
  const btn = document.getElementById('btt');
  if (!btn) return;
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        btn.classList.toggle('show', window.scrollY > 400);
        ticking = false;
      });
      ticking = true;
    }
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ===== CONTACT FORM ===== */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', e => {
    e.preventDefault();
    let valid = true;

    form.querySelectorAll('[required]').forEach(input => {
      const fg = input.closest('.fg');
      if (!input.value.trim()) { fg?.classList.add('error'); valid = false; }
      else { fg?.classList.remove('error'); }
    });

    const email = form.querySelector('#email');
    if (email?.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      email.closest('.fg')?.classList.add('error');
      valid = false;
    }

    if (!valid) return;

    const btn = document.getElementById('submitBtn');
    const orig = btn.innerHTML;
    btn.innerHTML = '<span>送信中...</span>';
    btn.disabled = true;
    btn.style.opacity = '.7';

    setTimeout(() => {
      btn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg><span>送信しました</span>';
      btn.style.background = '#38a169';
      btn.style.borderColor = '#38a169';
      btn.style.opacity = '1';
      form.reset();
      form.querySelectorAll('.fg').forEach(fg => fg.classList.remove('error'));
      setTimeout(() => {
        btn.innerHTML = orig;
        btn.disabled = false;
        btn.style.background = '';
        btn.style.borderColor = '';
      }, 3000);
    }, 1500);
  });

  form.querySelectorAll('[required]').forEach(input => {
    input.addEventListener('input', () => {
      if (input.value.trim()) input.closest('.fg')?.classList.remove('error');
    });
  });
}

/* ===== COUNT UP ===== */
function initCountUp() {
  const nums = document.querySelectorAll('[data-count]');
  if (!nums.length) return;
  if (!('IntersectionObserver' in window)) {
    nums.forEach(el => { el.textContent = el.dataset.count; });
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseInt(el.dataset.count);
        const dur = 1800;
        const start = performance.now();
        function tick(now) {
          const p = Math.min((now - start) / dur, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.5 });
  nums.forEach(el => observer.observe(el));
}

/* ===== TILT (desktop only) ===== */
function initTilt() {
  if ('ontouchstart' in window || window.innerWidth < 1024) return;
  document.querySelectorAll('[data-tilt]').forEach(el => {
    el.addEventListener('mousemove', e => {
      const r = el.getBoundingClientRect();
      const cx = r.width / 2, cy = r.height / 2;
      const rx = ((e.clientY - r.top) - cy) / cy * -3;
      const ry = ((e.clientX - r.left) - cx) / cx * 3;
      el.style.transform = 'perspective(600px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateY(-3px)';
      el.style.transition = 'transform .15s ease';
    });
    el.addEventListener('mouseleave', () => {
      el.style.transform = '';
      el.style.transition = 'transform .3s ease';
    });
  });
}
