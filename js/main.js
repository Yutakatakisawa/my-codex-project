document.addEventListener("DOMContentLoaded", () => {
  initHeaderState();
  initMobileMenu();
  initSmoothScroll();
  initActiveNavigation();
  initRevealAnimations();
  initFaqAccordion();
  initEstimateForm();
  initBackToTop();
  setCurrentYear();
});

function initHeaderState() {
  const header = document.getElementById("siteHeader");
  if (!header) return;

  const update = () => {
    header.classList.toggle("scrolled", window.scrollY > 8);
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
}

function initMobileMenu() {
  const toggle = document.getElementById("menuToggle");
  const nav = document.getElementById("siteNav");
  const overlay = document.getElementById("navOverlay");
  if (!toggle || !nav || !overlay) return;

  const setOpen = (isOpen) => {
    nav.classList.toggle("open", isOpen);
    toggle.classList.toggle("open", isOpen);
    overlay.classList.toggle("show", isOpen);
    document.body.classList.toggle("menu-open", isOpen);
    toggle.setAttribute("aria-expanded", String(isOpen));
  };

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.contains("open");
    setOpen(!isOpen);
  });

  overlay.addEventListener("click", () => setOpen(false));

  nav.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setOpen(false));
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 960) setOpen(false);
  });
}

function initSmoothScroll() {
  const anchors = document.querySelectorAll('a[href^="#"]');
  if (!anchors.length) return;

  anchors.forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const href = anchor.getAttribute("href");
      if (!href || href === "#") return;

      const target = document.querySelector(href);
      if (!target) return;

      event.preventDefault();
      const headerHeight = document.getElementById("siteHeader")?.offsetHeight ?? 0;
      const position = target.getBoundingClientRect().top + window.scrollY - headerHeight + 2;
      window.scrollTo({ top: position, behavior: "smooth" });
    });
  });
}

function initActiveNavigation() {
  const navLinks = Array.from(document.querySelectorAll("[data-nav]"));
  if (!navLinks.length) return;

  const sectionMap = navLinks
    .map((link) => {
      const id = link.getAttribute("href");
      return id ? { link, section: document.querySelector(id) } : null;
    })
    .filter((item) => item && item.section);

  if (!sectionMap.length) return;

  const updateActive = () => {
    const headerHeight = document.getElementById("siteHeader")?.offsetHeight ?? 0;
    const point = window.scrollY + headerHeight + 110;
    let currentLink = sectionMap[0].link;

    for (const item of sectionMap) {
      if (item.section.offsetTop <= point) currentLink = item.link;
    }

    navLinks.forEach((link) => link.classList.remove("active"));
    currentLink.classList.add("active");
  };

  updateActive();
  window.addEventListener("scroll", updateActive, { passive: true });
}

function initRevealAnimations() {
  const targets = document.querySelectorAll("[data-reveal]");
  if (!targets.length) return;

  if (!("IntersectionObserver" in window)) {
    targets.forEach((item) => item.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const delay = Number(entry.target.dataset.delay ?? 0);
        setTimeout(() => {
          entry.target.classList.add("visible");
        }, delay);
        observer.unobserve(entry.target);
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -60px 0px",
    }
  );

  targets.forEach((item) => observer.observe(item));
}

function initFaqAccordion() {
  const items = document.querySelectorAll(".faq-item");
  if (!items.length) return;

  items.forEach((item) => {
    const button = item.querySelector(".faq-question");
    if (!button) return;

    button.addEventListener("click", () => {
      const isOpen = item.classList.contains("open");

      items.forEach((other) => {
        other.classList.remove("open");
        const otherButton = other.querySelector(".faq-question");
        if (otherButton) otherButton.setAttribute("aria-expanded", "false");
      });

      if (!isOpen) {
        item.classList.add("open");
        button.setAttribute("aria-expanded", "true");
      }

      syncFaqHeights();
    });
  });

  syncFaqHeights();
  window.addEventListener("resize", syncFaqHeights);
}

function syncFaqHeights() {
  document.querySelectorAll(".faq-item").forEach((item) => {
    const answer = item.querySelector(".faq-answer");
    if (!answer) return;
    if (item.classList.contains("open")) {
      answer.style.maxHeight = `${answer.scrollHeight}px`;
    } else {
      answer.style.maxHeight = "0px";
    }
  });
}

function initEstimateForm() {
  const form = document.getElementById("estimateForm");
  const submitButton = document.getElementById("submitButton");
  const status = document.getElementById("formStatus");
  if (!form || !submitButton || !status) return;

  const nameInput = form.querySelector("#name");
  const telInput = form.querySelector("#tel");
  const emailInput = form.querySelector("#email");
  const messageInput = form.querySelector("#message");
  const agreeInput = form.querySelector("#agree");

  const requiredInputs = [nameInput, telInput, messageInput].filter(Boolean);

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  const setFieldError = (input, hasError) => {
    const wrapper = input?.closest(".form-field");
    if (!wrapper) return;
    wrapper.classList.toggle("error", hasError);
  };

  const clearStatus = () => {
    status.textContent = "";
    status.classList.remove("success", "error");
  };

  requiredInputs.forEach((input) => {
    input.addEventListener("input", () => {
      if (input.value.trim()) setFieldError(input, false);
      clearStatus();
    });
  });

  if (emailInput) {
    emailInput.addEventListener("input", () => {
      const hasValue = emailInput.value.trim().length > 0;
      const invalid = hasValue && !emailPattern.test(emailInput.value.trim());
      setFieldError(emailInput, invalid);
      clearStatus();
    });
  }

  if (agreeInput) {
    agreeInput.addEventListener("change", () => {
      form.classList.remove("error-check");
      clearStatus();
    });
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    clearStatus();

    let hasError = false;

    requiredInputs.forEach((input) => {
      const invalid = !input.value.trim();
      setFieldError(input, invalid);
      if (invalid) hasError = true;
    });

    if (emailInput && emailInput.value.trim()) {
      const invalidEmail = !emailPattern.test(emailInput.value.trim());
      setFieldError(emailInput, invalidEmail);
      if (invalidEmail) hasError = true;
    } else if (emailInput) {
      setFieldError(emailInput, false);
    }

    const invalidCheck = !!agreeInput && !agreeInput.checked;
    form.classList.toggle("error-check", invalidCheck);
    if (invalidCheck) hasError = true;

    if (hasError) {
      status.textContent = "入力内容を確認してください。";
      status.classList.add("error");
      return;
    }

    const originalText = submitButton.textContent;
    submitButton.disabled = true;
    submitButton.textContent = "送信中...";

    setTimeout(() => {
      status.textContent = "送信が完了しました。担当者より折り返しご連絡します。";
      status.classList.add("success");
      form.reset();
      form.classList.remove("error-check");
      form.querySelectorAll(".form-field").forEach((field) => {
        field.classList.remove("error");
      });

      submitButton.disabled = false;
      submitButton.textContent = originalText;
    }, 900);
  });
}

function initBackToTop() {
  const button = document.getElementById("backToTop");
  if (!button) return;

  const update = () => {
    button.classList.toggle("show", window.scrollY > 320);
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
  button.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

function setCurrentYear() {
  const year = String(new Date().getFullYear());
  document.querySelectorAll("#currentYear").forEach((el) => {
    el.textContent = year;
  });
}
