const DEMOS = {
  button: {
    code: `<Button color="primary" radius="full">\n  Launch Product\n</Button>`,
    render: () => `
      <div class="demo-card">
        <p class="demo-label">Button Showcase</p>
        <div style="display:flex; gap: .6rem; flex-wrap:wrap;">
          <button class="btn btn--primary btn--sm" type="button">Primary</button>
          <button class="btn btn--ghost btn--sm" type="button">Ghost</button>
          <button class="btn btn--ghost btn--sm" type="button" disabled style="opacity:.6;">Disabled</button>
        </div>
      </div>
    `,
  },
  card: {
    code: `<Card>\n  <CardHeader title="Team Analytics" />\n  <CardBody>...</CardBody>\n</Card>`,
    render: () => `
      <div class="demo-card" style="border:1px solid var(--line); border-radius:14px; padding:.75rem;">
        <p class="demo-label">Dashboard Card</p>
        <h4 style="margin:.3rem 0 .2rem;">Team Analytics</h4>
        <p style="margin:0; color:var(--text-soft); font-size:.82rem;">Monthly active users increased by 21.4%.</p>
        <div style="margin-top:.6rem; display:flex; gap:.35rem; flex-wrap:wrap;">
          <span class="tag">+21.4%</span>
          <span class="tag">Realtime</span>
        </div>
      </div>
    `,
  },
  modal: {
    code: `const {isOpen, onOpenChange} = useDisclosure();\n<Modal isOpen={isOpen} onOpenChange={onOpenChange} />`,
    render: () => `
      <div class="demo-card">
        <p class="demo-label">Modal Pattern</p>
        <div style="border:1px solid var(--line); border-radius:14px; padding:.75rem; background:rgba(255,255,255,.02);">
          <h4 style="margin:0 0 .28rem;">Confirm deploy?</h4>
          <p style="margin:0; color:var(--text-soft); font-size:.82rem;">This action will push your current UI theme to production.</p>
          <div style="margin-top:.7rem; display:flex; gap:.5rem;">
            <button class="btn btn--ghost btn--sm" type="button">Cancel</button>
            <button class="btn btn--primary btn--sm" type="button">Deploy</button>
          </div>
        </div>
      </div>
    `,
  },
};

const COMPONENT_CATALOG = [
  { name: "Button", category: "actions", desc: "主要操作を示すCTAボタン。" },
  { name: "Input", category: "forms", desc: "検証可能なテキスト入力。" },
  { name: "Select", category: "forms", desc: "検索対応のセレクトメニュー。" },
  { name: "Modal", category: "overlays", desc: "集中タスク向けダイアログ。" },
  { name: "Toast", category: "feedback", desc: "一時的な通知表示コンポーネント。" },
  { name: "Dropdown", category: "navigation", desc: "文脈メニューや選択肢表示。" },
  { name: "Tabs", category: "navigation", desc: "関連コンテンツの切り替え。" },
  { name: "Table", category: "data", desc: "列ベースで構造化データを表示。" },
  { name: "Pagination", category: "data", desc: "ページ移動を管理するUI。" },
  { name: "Card", category: "layout", desc: "情報のまとまりを見せる器。" },
  { name: "Avatar", category: "data", desc: "ユーザー識別のビジュアル要素。" },
  { name: "Badge", category: "feedback", desc: "状態や件数をコンパクト表示。" },
];

const CATEGORY_LABELS = {
  all: "All",
  actions: "Actions",
  forms: "Forms",
  navigation: "Navigation",
  overlays: "Overlays",
  feedback: "Feedback",
  data: "Data",
  layout: "Layout",
};

const state = {
  currentDemo: "button",
  currentCategory: "all",
  mode: "dark",
};

const el = {};

document.addEventListener("DOMContentLoaded", () => {
  cache();
  initScrollProgress();
  initHeader();
  initMobileNav();
  initReveal();
  initCopyInstall();
  initDemoTabs();
  initCatalog();
  initThemePlayground();
});

function cache() {
  el.scrollProgress = document.getElementById("scrollProgress");
  el.header = document.getElementById("header");
  el.nav = document.getElementById("nav");
  el.hamburger = document.getElementById("hamburger");
  el.copyInstallBtn = document.getElementById("copyInstallBtn");
  el.installCommand = document.getElementById("installCommand");
  el.previewTabs = document.getElementById("previewTabs");
  el.previewStage = document.getElementById("previewStage");
  el.previewCode = document.getElementById("previewCode");
  el.componentFilters = document.getElementById("componentFilters");
  el.componentsGrid = document.getElementById("componentsGrid");
  el.hueRange = document.getElementById("hueRange");
  el.radiusRange = document.getElementById("radiusRange");
  el.modeSwitch = document.getElementById("modeSwitch");
  el.themePreview = document.getElementById("themePreview");
  el.tokenBrand = document.getElementById("tokenBrand");
  el.tokenRadius = document.getElementById("tokenRadius");
  el.tokenSurface = document.getElementById("tokenSurface");
}

function initScrollProgress() {
  const bar = el.scrollProgress;
  if (!bar) return;
  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const total = document.documentElement.scrollHeight - window.innerHeight;
        const ratio = total > 0 ? window.scrollY / total : 0;
        bar.style.width = `${Math.min(Math.max(ratio, 0), 1) * 100}%`;
        ticking = false;
      });
    },
    { passive: true }
  );
}

function initHeader() {
  if (!el.header) return;
  let ticking = false;
  window.addEventListener(
    "scroll",
    () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        el.header.classList.toggle("is-scrolled", window.scrollY > 12);
        ticking = false;
      });
    },
    { passive: true }
  );
}

function initMobileNav() {
  if (!el.hamburger || !el.nav) return;
  const overlay = document.createElement("div");
  overlay.className = "mobile-overlay";
  document.body.appendChild(overlay);

  const close = () => {
    el.nav.classList.remove("is-open");
    el.hamburger.classList.remove("is-open");
    overlay.classList.remove("is-open");
    el.hamburger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  };

  const open = () => {
    el.nav.classList.add("is-open");
    el.hamburger.classList.add("is-open");
    overlay.classList.add("is-open");
    el.hamburger.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
  };

  el.hamburger.addEventListener("click", () => {
    const isOpen = el.nav.classList.contains("is-open");
    if (isOpen) close();
    else open();
  });

  overlay.addEventListener("click", close);
  el.nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", close));

  window.addEventListener("resize", () => {
    if (window.innerWidth > 860) close();
  });
}

function initReveal() {
  const revealEls = document.querySelectorAll("[data-reveal]");
  if (!revealEls.length) return;
  document.body.classList.add("reveal-ready");
  if (!("IntersectionObserver" in window)) {
    revealEls.forEach((item) => item.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const delay = Number(entry.target.dataset.delay || 0);
        setTimeout(() => entry.target.classList.add("is-visible"), delay);
        io.unobserve(entry.target);
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  revealEls.forEach((item) => io.observe(item));
}

function initCopyInstall() {
  if (!el.copyInstallBtn || !el.installCommand) return;
  el.copyInstallBtn.addEventListener("click", async () => {
    const text = el.installCommand.textContent?.trim() || "";
    if (!text) return;
    const original = el.copyInstallBtn.textContent;
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      fallbackCopyText(text);
    }
    el.copyInstallBtn.textContent = "Copied";
    setTimeout(() => {
      el.copyInstallBtn.textContent = original;
    }, 1200);
  });
}

function initDemoTabs() {
  if (!el.previewTabs || !el.previewStage || !el.previewCode) return;
  const renderDemo = () => {
    const demo = DEMOS[state.currentDemo];
    if (!demo) return;
    el.previewStage.innerHTML = demo.render();
    el.previewCode.textContent = demo.code;
    el.previewTabs.querySelectorAll(".preview-tab").forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.demo === state.currentDemo);
    });
  };

  el.previewTabs.addEventListener("click", (event) => {
    const btn = event.target.closest("button[data-demo]");
    if (!btn) return;
    state.currentDemo = btn.dataset.demo;
    renderDemo();
  });

  renderDemo();
}

function initCatalog() {
  if (!el.componentFilters || !el.componentsGrid) return;
  const categories = Object.keys(CATEGORY_LABELS);

  el.componentFilters.innerHTML = categories
    .map(
      (key) =>
        `<button class="chip ${key === state.currentCategory ? "is-active" : ""}" type="button" data-category="${key}">${CATEGORY_LABELS[key]}</button>`
    )
    .join("");

  const renderGrid = () => {
    const list =
      state.currentCategory === "all"
        ? COMPONENT_CATALOG
        : COMPONENT_CATALOG.filter((item) => item.category === state.currentCategory);

    el.componentsGrid.innerHTML = list
      .map(
        (item) => `
      <article class="component-card">
        <div class="component-card__preview">
          <span class="preview-bar w"></span>
          <span class="preview-bar m"></span>
          <span class="preview-bar s"></span>
        </div>
        <div class="component-card__body">
          <h3>${escapeHtml(item.name)}</h3>
          <p>${escapeHtml(item.desc)}</p>
          <div class="component-card__meta">
            <span class="tag">${escapeHtml(CATEGORY_LABELS[item.category] || item.category)}</span>
            <span class="tag">a11y ready</span>
          </div>
        </div>
      </article>
    `
      )
      .join("");
  };

  el.componentFilters.addEventListener("click", (event) => {
    const btn = event.target.closest("button[data-category]");
    if (!btn) return;
    state.currentCategory = btn.dataset.category;
    el.componentFilters.querySelectorAll(".chip").forEach((chip) => {
      chip.classList.toggle("is-active", chip.dataset.category === state.currentCategory);
    });
    renderGrid();
  });

  renderGrid();
}

function initThemePlayground() {
  if (!el.hueRange || !el.radiusRange || !el.themePreview || !el.modeSwitch) return;

  const applyTheme = () => {
    const hue = Number(el.hueRange.value);
    const radius = Number(el.radiusRange.value);

    document.documentElement.style.setProperty("--brand-h", String(hue));
    document.documentElement.style.setProperty("--radius", `${radius}px`);

    if (el.tokenBrand) el.tokenBrand.textContent = `hsl(${hue} 96% 65%)`;
    if (el.tokenRadius) el.tokenRadius.textContent = `${radius}px`;
  };

  el.hueRange.addEventListener("input", applyTheme);
  el.radiusRange.addEventListener("input", applyTheme);

  el.modeSwitch.addEventListener("click", (event) => {
    const btn = event.target.closest("button[data-mode]");
    if (!btn) return;
    state.mode = btn.dataset.mode;
    el.themePreview.dataset.mode = state.mode;
    el.modeSwitch.querySelectorAll(".mode-btn").forEach((modeBtn) => {
      modeBtn.classList.toggle("is-active", modeBtn.dataset.mode === state.mode);
    });
    if (el.tokenSurface) {
      el.tokenSurface.textContent = state.mode === "light" ? "light" : "dark";
    }
  });

  applyTheme();
}

function fallbackCopyText(text) {
  const area = document.createElement("textarea");
  area.value = text;
  area.style.position = "fixed";
  area.style.opacity = "0";
  area.style.pointerEvents = "none";
  document.body.appendChild(area);
  area.focus();
  area.select();
  document.execCommand("copy");
  document.body.removeChild(area);
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}
