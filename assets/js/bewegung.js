(() => {
  "use strict";

  const reduziert = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const kopfzeile = document.querySelector(".kopfzeile");
  if (kopfzeile) {
    const pruefen = () => {
      kopfzeile.classList.toggle("ist-gescrollt", window.scrollY > 8);
    };
    pruefen();
    window.addEventListener("scroll", pruefen, { passive: true });
  }

  if (reduziert) return;

  document.documentElement.classList.add("js-bewegung");

  const AUFDECKEN = ".einblenden, .freilegen, .zeile";

  function beobachten(elemente) {
    if (!("IntersectionObserver" in window)) {
      elemente.forEach((el) => el.classList.add("ist-sichtbar"));
      return;
    }

    const beobachter = new IntersectionObserver(
      (eintraege, obs) => {
        eintraege.forEach((eintrag) => {
          if (!eintrag.isIntersecting) return;
          eintrag.target.classList.add("ist-sichtbar");
          obs.unobserve(eintrag.target);
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -6% 0px" }
    );

    elemente.forEach((el, i) => {
      if (!el.classList.contains("zeile")) {
        el.style.transitionDelay = `${(i % 4) * 80}ms`;
      }
      beobachter.observe(el);
    });
  }

  beobachten(Array.from(document.querySelectorAll(AUFDECKEN)));

  document.addEventListener("raster:bereit", () => {
    beobachten(
      Array.from(
        document.querySelectorAll(
          ".einblenden:not(.ist-sichtbar), .freilegen:not(.ist-sichtbar), .zeile:not(.ist-sichtbar)"
        )
      )
    );
  });

  function nachzuegler() {
    const hoehe = window.innerHeight || document.documentElement.clientHeight || 0;
    document
      .querySelectorAll(
        ".einblenden:not(.ist-sichtbar), .freilegen:not(.ist-sichtbar), .zeile:not(.ist-sichtbar)"
      )
      .forEach((el) => {
        const kasten = el.getBoundingClientRect();
        if (kasten.top < hoehe && kasten.bottom > 0) el.classList.add("ist-sichtbar");
      });
  }

  setTimeout(nachzuegler, 1200);
  let nachzueglerGeplant = false;
  window.addEventListener("scroll", () => {
    if (nachzueglerGeplant) return;
    nachzueglerGeplant = true;
    setTimeout(() => { nachzueglerGeplant = false; nachzuegler(); }, 250);
  }, { passive: true });
  window.addEventListener("load", () => setTimeout(nachzuegler, 400));

  function endzustandFestschreiben() {
    document
      .querySelectorAll(".ist-sichtbar:not(.ist-fertig)")
      .forEach((el) => el.classList.add("ist-fertig"));
  }

  setTimeout(endzustandFestschreiben, 2800);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      setTimeout(nachzuegler, 80);
      setTimeout(endzustandFestschreiben, 160);
    }
  });
  window.addEventListener("focus", () => setTimeout(endzustandFestschreiben, 160));

  function hochzaehlen(el) {
    const ziel = Number(el.dataset.zaehlziel);
    if (!Number.isFinite(ziel)) return;

    const dauer = 1200;
    const start = performance.now();
    let fertig = false;

    function schritt(jetzt) {
      const anteil = Math.min((jetzt - start) / dauer, 1);
      const weich = 1 - Math.pow(1 - anteil, 3);
      el.textContent = String(Math.round(ziel * weich));
      if (anteil < 1) {
        requestAnimationFrame(schritt);
      } else {
        fertig = true;
      }
    }

    el.textContent = "0";
    requestAnimationFrame(schritt);

    setTimeout(() => {
      if (!fertig) el.textContent = String(ziel);
    }, dauer + 700);
  }

  const zahlen = Array.from(document.querySelectorAll("[data-zaehlziel]"));
  if (zahlen.length) {
    if ("IntersectionObserver" in window) {
      const zaehlBeobachter = new IntersectionObserver(
        (eintraege, obs) => {
          eintraege.forEach((eintrag) => {
            if (!eintrag.isIntersecting) return;
            obs.unobserve(eintrag.target);
            hochzaehlen(eintrag.target);
          });
        },
        { threshold: 0.6 }
      );
      zahlen.forEach((el) => zaehlBeobachter.observe(el));
    } else {
      zahlen.forEach(hochzaehlen);
    }
  }

  function anteilVon(element, abzug) {
    const kasten = element.getBoundingClientRect();
    const sichtHoehe =
      window.innerHeight || document.documentElement.clientHeight || 1;
    const strecke = Math.max(kasten.height - (abzug ? sichtHoehe : 0), 1);
    return Math.min(Math.max(-kasten.top / strecke, 0), 1);
  }

  const strecke = document.querySelector(".strecke");
  if (strecke) {
    const spur = strecke.querySelector(".strecke__spur");
    const strich = strecke.querySelector(".strecke__strich");

    function streckeAktualisieren() {
      if (!spur) return;
      if (getComputedStyle(spur).flexDirection === "column") {
        spur.style.setProperty("--schub", "0");
        return;
      }

      const anteil = anteilVon(strecke, true);
      const weg = Math.max(spur.scrollWidth - spur.clientWidth, 0);
      spur.style.setProperty("--schub", (anteil * weg).toFixed(1));
      if (strich) strich.style.setProperty("--anteil", anteil.toFixed(4));
    }

    window.addEventListener("scroll", streckeAktualisieren, { passive: true });
    window.addEventListener("resize", streckeAktualisieren, { passive: true });

    document.addEventListener("raster:bereit", streckeAktualisieren);
    window.addEventListener("load", streckeAktualisieren);
    streckeAktualisieren();
  }

  const profil = document.querySelector(".profil");
  if (profil) {
    function profilAktualisieren() {
      const kasten = profil.getBoundingClientRect();
      const sichtHoehe =
        window.innerHeight || document.documentElement.clientHeight || 1;
      const start = sichtHoehe * 0.85;
      const ende = sichtHoehe * 0.35;
      const gesamt = Math.max(start - ende + kasten.height, 1);
      const gelaufen = Math.min(Math.max(start - kasten.top, 0), gesamt);
      const anteil = gelaufen / gesamt;
      profil.style.setProperty("--gezeichnet", (anteil * 100).toFixed(2));
    }

    window.addEventListener("scroll", profilAktualisieren, { passive: true });
    window.addEventListener("resize", profilAktualisieren, { passive: true });
    profilAktualisieren();
  }

  const heroband = document.querySelector(".heroband");
  if (heroband) {
    function versatzSetzen() {
      const kasten = heroband.getBoundingClientRect();
      const hoehe = window.innerHeight || document.documentElement.clientHeight || 1;
      if (kasten.bottom < 0 || kasten.top > hoehe) return;

      const mitte = kasten.top + kasten.height / 2;
      const lage = (mitte - hoehe / 2) / (hoehe / 2 + kasten.height / 2);
      const weg = Math.max(-1, Math.min(1, lage)) * (kasten.height * 0.07);
      heroband.style.setProperty("--versatz", `${weg.toFixed(1)}px`);
    }

    window.addEventListener("scroll", versatzSetzen, { passive: true });
    window.addEventListener("resize", versatzSetzen, { passive: true });
    window.addEventListener("load", versatzSetzen);
    versatzSetzen();
  }
})();
