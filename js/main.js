/**
 * TAKISAWA ROOF - Full Rebuild JS
 * Interactive features: loader, typing, particles, tabs, carousel, timeline, tilt, etc.
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
  window.addEventListener('load', () => {
    setTimeout(() => loader.classList.add('hide'), 800);
  });
  setTimeout(() => loader.classList.add('hide'), 3000);
}

/* ===== SCROLL PROGRESS ===== */
function initScrollProgress() {
  const bar = document.getElementById('scrollProgress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    const pct = h > 0 ? (window.scrollY / h) * 100 : 0;
    bar.style.width = pct + '%';
  }, { passive: true });
}

/* ===== HEADER ===== */
function initHeader() {
  const header = document.getElementById('header');
  if (!header) return;
  window.addEventListener('scroll', () => {
    header.classList.toggle('header--scrolled', window.scrollY > 40);
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
  nav.querySelectorAll('.header__nav-link').forEach(l => l.addEventListener('click', () => toggle(false)));
  window.addEventListener('resize', () => { if (window.innerWidth > 1024) toggle(false); });
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
      const offset = document.getElementById('header')?.offsetHeight || 68;
      window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset, behavior: 'smooth' });
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

  function update() {
    const scrollY = window.scrollY + 120;
    let current = sections[0];
    sections.forEach(s => { if (s.el.offsetTop <= scrollY) current = s; });
    links.forEach(l => l.classList.remove('active'));
    current.link.classList.add('active');
  }

  window.addEventListener('scroll', update, { passive: true });
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
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

  els.forEach(el => observer.observe(el));
}

/* ===== TYPING EFFECT ===== */
function initTyping() {
  const el = document.getElementById('heroTyping');
  if (!el) return;

  const words = ['屋根工事専門店', '雨漏り修理', '屋根リフォーム', '雪止め工事'];
  let wordIdx = 0, charIdx = 0, isDeleting = false;

  function type() {
    const current = words[wordIdx];

    if (isDeleting) {
      charIdx--;
      el.textContent = current.substring(0, charIdx);
    } else {
      charIdx++;
      el.textContent = current.substring(0, charIdx);
    }

    let speed = isDeleting ? 60 : 120;

    if (!isDeleting && charIdx === current.length) {
      speed = 2000;
      isDeleting = true;
    } else if (isDeleting && charIdx === 0) {
      isDeleting = false;
      wordIdx = (wordIdx + 1) % words.length;
      speed = 400;
    }

    setTimeout(type, speed);
  }

  setTimeout(type, 1200);
}

/* ===== PARTICLES ===== */
function initParticles() {
  const container = document.getElementById('heroParticles');
  if (!container) return;

  const canvas = document.createElement('canvas');
  container.appendChild(canvas);
  const ctx = canvas.getContext('2d');

  let w, h, particles = [];
  const count = window.innerWidth < 640 ? 30 : 60;

  function resize() {
    w = canvas.width = container.offsetWidth;
    h = canvas.height = container.offsetHeight;
  }

  function createParticles() {
    particles = [];
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 2 + 0.5,
        dx: (Math.random() - 0.5) * 0.5,
        dy: (Math.random() - 0.5) * 0.5,
        alpha: Math.random() * 0.4 + 0.1
      });
    }
  }

  function draw() {
    ctx.clearRect(0, 0, w, h);
    particles.forEach(p => {
      p.x += p.dx;
      p.y += p.dy;
      if (p.x < 0) p.x = w;
      if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h;
      if (p.y > h) p.y = 0;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${p.alpha})`;
      ctx.fill();
    });

    particles.forEach((a, i) => {
      for (let j = i + 1; j < particles.length; j++) {
        const b = particles[j];
        const dist = Math.hypot(a.x - b.x, a.y - b.y);
        if (dist < 120) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(255,255,255,${0.06 * (1 - dist / 120)})`;
          ctx.stroke();
        }
      }
    });

    requestAnimationFrame(draw);
  }

  resize();
  createParticles();
  draw();

  window.addEventListener('resize', () => {
    resize();
    createParticles();
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
      cards.forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.classList.toggle('hidden', !show);

        if (show) {
          card.style.opacity = '0';
          card.style.transform = 'translateY(20px)';
          requestAnimationFrame(() => {
            card.style.transition = 'opacity .4s ease, transform .4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          });
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

  function update() {
    const rect = timeline.getBoundingClientRect();
    const timelineTop = rect.top;
    const timelineHeight = rect.height;
    const triggerPoint = window.innerHeight * 0.6;

    const progress = Math.min(Math.max((triggerPoint - timelineTop) / timelineHeight, 0), 1);
    fill.style.height = (progress * 100) + '%';

    steps.forEach((step, i) => {
      const stepRect = step.getBoundingClientRect();
      const stepMid = stepRect.top + stepRect.height / 2;
      step.classList.toggle('active', stepMid < triggerPoint);
    });
  }

  window.addEventListener('scroll', update, { passive: true });
  update();
}

/* ===== CAROUSEL ===== */
function initCarousel() {
  const track = document.getElementById('worksTrack');
  const prevBtn = document.getElementById('worksPrev');
  const nextBtn = document.getElementById('worksNext');
  const dotsContainer = document.getElementById('worksDots');
  if (!track || !prevBtn || !nextBtn || !dotsContainer) return;

  const slides = track.querySelectorAll('.works__slide');
  let currentIndex = 0;
  let slidesPerView = getSlidesPerView();
  let maxIndex = Math.max(0, slides.length - slidesPerView);

  function getSlidesPerView() {
    if (window.innerWidth < 640) return 1;
    if (window.innerWidth < 1024) return 2;
    return 3;
  }

  function buildDots() {
    dotsContainer.innerHTML = '';
    const dotCount = maxIndex + 1;
    for (let i = 0; i < dotCount; i++) {
      const dot = document.createElement('div');
      dot.classList.add('works__dot');
      if (i === currentIndex) dot.classList.add('active');
      dot.addEventListener('click', () => goTo(i));
      dotsContainer.appendChild(dot);
    }
  }

  function goTo(index) {
    currentIndex = Math.min(Math.max(index, 0), maxIndex);
    const slideWidth = slides[0].offsetWidth + 24;
    track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
    updateDots();
  }

  function updateDots() {
    dotsContainer.querySelectorAll('.works__dot').forEach((d, i) => {
      d.classList.toggle('active', i === currentIndex);
    });
  }

  prevBtn.addEventListener('click', () => goTo(currentIndex - 1));
  nextBtn.addEventListener('click', () => goTo(currentIndex + 1));

  // Drag / swipe
  let isDragging = false, startX = 0, currentTranslate = 0;

  track.addEventListener('mousedown', e => startDrag(e.clientX));
  track.addEventListener('touchstart', e => startDrag(e.touches[0].clientX), { passive: true });

  function startDrag(x) {
    isDragging = true;
    startX = x;
    const slideWidth = slides[0].offsetWidth + 24;
    currentTranslate = -currentIndex * slideWidth;
    track.classList.add('dragging');
  }

  document.addEventListener('mousemove', e => { if (isDragging) drag(e.clientX); });
  document.addEventListener('touchmove', e => { if (isDragging) drag(e.touches[0].clientX); }, { passive: true });

  function drag(x) {
    const diff = x - startX;
    const slideWidth = slides[0].offsetWidth + 24;
    track.style.transform = `translateX(${currentTranslate + diff}px)`;
  }

  document.addEventListener('mouseup', e => { if (isDragging) endDrag(e.clientX); });
  document.addEventListener('touchend', e => { if (isDragging) endDrag(e.changedTouches[0].clientX); });

  function endDrag(x) {
    isDragging = false;
    track.classList.remove('dragging');
    const diff = x - startX;
    const threshold = 60;
    if (diff < -threshold) goTo(currentIndex + 1);
    else if (diff > threshold) goTo(currentIndex - 1);
    else goTo(currentIndex);
  }

  window.addEventListener('resize', () => {
    slidesPerView = getSlidesPerView();
    maxIndex = Math.max(0, slides.length - slidesPerView);
    currentIndex = Math.min(currentIndex, maxIndex);
    buildDots();
    goTo(currentIndex);
  });

  buildDots();

  // Auto-play
  let autoPlay = setInterval(() => goTo((currentIndex + 1) % (maxIndex + 1)), 5000);
  track.addEventListener('mouseenter', () => clearInterval(autoPlay));
  track.addEventListener('mouseleave', () => {
    autoPlay = setInterval(() => goTo((currentIndex + 1) % (maxIndex + 1)), 5000);
  });
}

/* ===== FAQ ===== */
function initFAQ() {
  const items = document.querySelectorAll('.faq__item');
  items.forEach(item => {
    const q = item.querySelector('.faq__q');
    if (!q) return;
    q.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      items.forEach(i => { i.classList.remove('open'); i.querySelector('.faq__q')?.setAttribute('aria-expanded', 'false'); });
      if (!isOpen) {
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
  window.addEventListener('scroll', () => {
    btn.classList.toggle('show', window.scrollY > 500);
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
      if (!input.value.trim()) {
        fg?.classList.add('error');
        valid = false;
      } else {
        fg?.classList.remove('error');
      }
    });

    const emailInput = form.querySelector('#email');
    if (emailInput && emailInput.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value)) {
      emailInput.closest('.fg')?.classList.add('error');
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
    nums.forEach(el => el.textContent = el.dataset.count);
    return;
  }

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  nums.forEach(el => observer.observe(el));
}

function animateCount(el) {
  const target = parseInt(el.dataset.count);
  const duration = 2000;
  const start = performance.now();
  function tick(now) {
    const p = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - p, 3);
    el.textContent = Math.round(target * eased);
    if (p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

/* ===== TILT EFFECT ===== */
function initTilt() {
  if (window.innerWidth < 768) return;

  document.querySelectorAll('[data-tilt]').forEach(el => {
    el.addEventListener('mousemove', e => {
      const rect = el.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotateX = (y - centerY) / centerY * -4;
      const rotateY = (x - centerX) / centerX * 4;
      el.style.transform = `perspective(600px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`;
    });

    el.addEventListener('mouseleave', () => {
      el.style.transform = '';
    });
  });
}
