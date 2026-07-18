(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- nav ---------------- */
  var nav = document.getElementById("nav");
  var burger = document.getElementById("navBurger");
  var links = document.getElementById("navLinks");

  function syncNav() {
    if (!nav) return;
    var solid = window.scrollY > 24 || !nav.classList.contains("nav--dark");
    nav.classList.toggle("is-solid", solid);
  }
  window.addEventListener("scroll", syncNav, { passive: true });
  syncNav();

  if (burger && links) {
    burger.addEventListener("click", function () {
      var open = links.classList.toggle("is-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) nav.classList.add("is-solid");
      else syncNav();
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        links.classList.remove("is-open");
        burger.setAttribute("aria-expanded", "false");
      }
    });
  }

  /* ---------------- wejscia sekcji (transform-only, zawsze widoczne) ---------------- */
  var risers = document.querySelectorAll(".rise");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    risers.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) {
            en.target.classList.add("is-in");
            io.unobserve(en.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px" }
    );
    risers.forEach(function (el) { io.observe(el); });
  }

  /* ---------------- prefill tematu zapytania ---------------- */
  var msg = document.getElementById("f-msg");
  if (msg) {
    var params = new URLSearchParams(window.location.search);
    var temat = params.get("temat");
    if (temat && !msg.value) msg.value = temat;
    document.querySelectorAll("[data-topic]").forEach(function (el) {
      el.addEventListener("click", function () {
        if (!msg.value) msg.value = el.getAttribute("data-topic");
      });
    });
  }

  /* ---------------- formularz ---------------- */
  var form = document.getElementById("contactForm");
  var status = document.getElementById("formStatus");
  if (form && status) {
    var setInvalid = function (input, invalid) {
      var field = input.closest(".field");
      if (field) field.classList.toggle("is-invalid", invalid);
    };
    var validate = function () {
      var ok = true;
      form.querySelectorAll("input[required], textarea[required]").forEach(function (input) {
        var bad = !input.value.trim();
        if (!bad && input.type === "email") {
          bad = !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
        }
        if (input.type === "checkbox") bad = !input.checked;
        if (input.type !== "checkbox") setInvalid(input, bad);
        if (bad) ok = false;
      });
      return ok;
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      status.className = "form__status";
      if (!validate()) {
        status.classList.add("is-err");
        status.textContent = "Uzupełnij zaznaczone pola i spróbuj ponownie.";
        return;
      }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = v; });

      fetch("https://formsubmit.co/ajax/contact@matmeyer.com", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(data)
      })
        .then(function (r) {
          if (!r.ok) throw new Error("http " + r.status);
          return r.json();
        })
        .then(function () {
          form.reset();
          status.classList.add("is-ok");
          status.textContent = "Dziękujemy. Zapytanie dotarło, odpowiemy najpóźniej następnego dnia roboczego.";
        })
        .catch(function () {
          status.classList.add("is-err");
          status.textContent = "Nie udało się wysłać formularza. Napisz do nas: biuro@armatex.pl lub zadzwoń +48 22 300 40 50.";
        })
        .finally(function () {
          btn.disabled = false;
        });
    });
  }
})();
