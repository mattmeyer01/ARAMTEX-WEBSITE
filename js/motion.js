/* Pas ruchu strony glownej: Lenis + GSAP ScrollTrigger.
   Wszystko za bramka prefers-reduced-motion; stany poczatkowe zawsze widoczne. */
(function () {
  "use strict";

  if (!window.gsap || !window.ScrollTrigger) return;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce) return;

  gsap.registerPlugin(ScrollTrigger);
  var finePointer = window.matchMedia("(pointer: fine)").matches;

  /* ---------- Lenis smooth scroll zmostkowany z GSAP ---------- */
  var lenis = null;
  if (window.Lenis && finePointer) {
    document.documentElement.style.scrollBehavior = "auto";
    lenis = new Lenis({ autoRaf: false, duration: 1.05 });
    lenis.on("scroll", ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);

    document.querySelectorAll('a[href^="#"]').forEach(function (a) {
      a.addEventListener("click", function (e) {
        var target = document.querySelector(a.getAttribute("href"));
        if (!target) return;
        e.preventDefault();
        lenis.scrollTo(target, { offset: -68, duration: 1.2 });
      });
    });
  }

  /* ---------- pasek postepu (kobaltowa linia miary) ---------- */
  var progress = document.getElementById("scrollProgress");
  if (progress) {
    gsap.to(progress, {
      scaleX: 1,
      ease: "none",
      scrollTrigger: { start: 0, end: "max", scrub: 0.3 }
    });
  }

  /* ---------- hero: budowa naglowka per znak ---------- */
  var title = document.querySelector(".hero__title");
  if (title) {
    title.classList.add("js-split");
    var chars = [];
    title.querySelectorAll(".line > span").forEach(function (lineSpan) {
      var words = lineSpan.textContent.split(" ");
      lineSpan.textContent = "";
      words.forEach(function (word, wi) {
        var w = document.createElement("span");
        w.className = "word";
        Array.from(word).forEach(function (ch) {
          var s = document.createElement("span");
          s.className = "ch";
          s.textContent = ch;
          w.appendChild(s);
          chars.push(s);
        });
        lineSpan.appendChild(w);
        if (wi < words.length - 1) lineSpan.appendChild(document.createTextNode(" "));
      });
    });
    gsap.from(chars, {
      yPercent: 118,
      rotate: 4,
      duration: 0.9,
      stagger: 0.016,
      ease: "power4.out",
      delay: 0.05
    });
    gsap.from([".hero__brands", ".hero__sub", ".hero__ctas", ".hero__meta"], {
      y: 26,
      duration: 0.9,
      stagger: 0.1,
      delay: 0.35,
      ease: "power3.out"
    });
  }

  /* ---------- hero: schemat rurociagu rysuje sie od lewej ---------- */
  var pipeline = document.querySelector(".hero__pipeline svg");
  if (pipeline) {
    gsap.fromTo(pipeline.querySelectorAll(".pl-draw"),
      { strokeDasharray: "1 1", strokeDashoffset: 1 },
      { strokeDashoffset: 0, duration: 0.55, stagger: 0.09, delay: 0.55, ease: "power1.inOut" }
    );
    gsap.from(pipeline.querySelectorAll(".pl-label"), {
      y: 12,
      autoAlpha: 0,
      duration: 0.55,
      stagger: 0.16,
      delay: 1.7,
      ease: "power2.out"
    });
  }

  /* ---------- hero przypiete: tresc cofa sie pod nasuwajaca sie strone ---------- */
  gsap.to(".hero__content", {
    yPercent: 14,
    scale: 0.96,
    autoAlpha: 0.25,
    transformOrigin: "left top",
    ease: "none",
    scrollTrigger: { trigger: ".hero", start: "top top", end: "bottom top", scrub: true }
  });

  /* ---------- naglowki sekcji: slowa wjezdzaja ---------- */
  document.querySelectorAll(".h2").forEach(function (h) {
    var words = h.textContent.trim().split(/\s+/);
    h.textContent = "";
    words.forEach(function (w, i) {
      var s = document.createElement("span");
      s.className = "w";
      s.textContent = w;
      h.appendChild(s);
      if (i < words.length - 1) h.appendChild(document.createTextNode(" "));
    });
    gsap.from(h.querySelectorAll(".w"), {
      yPercent: 70,
      duration: 0.8,
      stagger: 0.055,
      ease: "power3.out",
      scrollTrigger: { trigger: h, start: "top 88%", once: true }
    });
  });

  /* ---------- kafle katalogu: scrub skali zdjecia ---------- */
  gsap.utils.toArray(".tile__media").forEach(function (m) {
    gsap.fromTo(m,
      { scale: 1.07, yPercent: 2 },
      {
        scale: 1,
        yPercent: 0,
        ease: "none",
        scrollTrigger: { trigger: m, start: "top bottom", end: "top 42%", scrub: true }
      }
    );
  });

  /* ---------- metryki: liczniki ---------- */
  document.querySelectorAll(".metric__num[data-count]").forEach(function (el) {
    var end = parseInt(el.getAttribute("data-count"), 10);
    var suffix = el.getAttribute("data-suffix") || "";
    var proxy = { v: 0 };
    ScrollTrigger.create({
      trigger: el,
      start: "top 88%",
      once: true,
      onEnter: function () {
        gsap.to(proxy, {
          v: end,
          duration: 1.4,
          ease: "power2.out",
          onUpdate: function () {
            el.textContent = Math.round(proxy.v).toLocaleString("pl-PL") + suffix;
          }
        });
      }
    });
  });

  /* ---------- proces: linia trasy rysuje sie scrollem ---------- */
  var draw = document.querySelector(".route-draw");
  if (draw) {
    gsap.fromTo(draw,
      { strokeDasharray: "1 1", strokeDashoffset: 1 },
      {
        strokeDashoffset: 0,
        ease: "none",
        scrollTrigger: { trigger: ".steps", start: "top 82%", end: "bottom 55%", scrub: 0.4 }
      }
    );
  }

  /* ---------- dokumenty i "dla kogo": dryf zdjec ---------- */
  var docsImg = document.querySelector(".docs__media img");
  if (docsImg) {
    gsap.fromTo(docsImg,
      { yPercent: -8, scale: 1.14 },
      {
        yPercent: 8,
        scale: 1.14,
        ease: "none",
        scrollTrigger: { trigger: ".docs", start: "top bottom", end: "bottom top", scrub: true }
      }
    );
  }
  gsap.utils.toArray(".aud__media img").forEach(function (img) {
    gsap.fromTo(img,
      { yPercent: -6, scale: 1.12 },
      {
        yPercent: 6,
        scale: 1.12,
        ease: "none",
        scrollTrigger: { trigger: img.closest(".aud__row"), start: "top bottom", end: "bottom top", scrub: true }
      }
    );
  });

  /* ---------- magnetyczne CTA (tylko precyzyjny kursor) ---------- */
  if (finePointer) {
    document.querySelectorAll(".cta-copper, .cta-outline, .nav__cta, .cta-stamp").forEach(function (el) {
      el.addEventListener("pointermove", function (e) {
        var r = el.getBoundingClientRect();
        gsap.to(el, {
          x: (e.clientX - r.left - r.width / 2) * 0.22,
          y: (e.clientY - r.top - r.height / 2) * 0.22,
          duration: 0.4,
          ease: "power3.out"
        });
      });
      el.addEventListener("pointerleave", function () {
        gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1, 0.45)" });
      });
    });
  }
})();
