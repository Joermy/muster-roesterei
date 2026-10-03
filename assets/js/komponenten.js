(() => {
  "use strict";

  const WURZEL = document.body.dataset.wurzel || "";

  const sicher = (wert) => {
    const div = document.createElement("div");
    div.textContent = wert == null ? "" : String(wert);
    return div.innerHTML;
  };

  function bild(name, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    const o = optionen || {};
    const srcset = b.breiten
      .map((w) => `${WURZEL}bilder/${name}-${w}.webp ${w}w`)
      .join(", ");
    const gross = b.breiten[b.breiten.length - 1];
    return (
      `<img src="${WURZEL}bilder/${name}-${gross}.webp"` +
      ` srcset="${srcset}"` +
      ` sizes="${o.sizes || "100vw"}"` +
      ` width="${b.breite}" height="${b.hoehe}"` +
      ` alt="${sicher(o.alt != null ? o.alt : b.alt)}"` +
      (o.eifrig
        ? ' fetchpriority="high" decoding="async"'
        : ' loading="lazy" decoding="async"') +
      ">"
    );
  }

  function rahmen(name, klasse, optionen) {
    const b = (window.BILDER || {})[name];
    if (!b) return "";
    return (
      `<div class="bild ${klasse}" style="--platzhalter:${b.farbe}">` +
      bild(name, optionen) +
      "</div>"
    );
  }

  const tonVon = (name) => ((window.BILDER || {})[name] || {}).farbe || "";

  window.BILDBAU = { bild, rahmen };

  document.querySelectorAll(".klapp__knopf").forEach((knopf) => {
    const inhalt = document.getElementById(knopf.getAttribute("aria-controls"));
    if (!inhalt) return;

    knopf.addEventListener("click", () => {
      const offen = knopf.getAttribute("aria-expanded") === "true";

      if (offen) {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        requestAnimationFrame(() => {
          inhalt.style.height = "0px";
        });
        knopf.setAttribute("aria-expanded", "false");
      } else {
        inhalt.style.height = `${inhalt.scrollHeight}px`;
        knopf.setAttribute("aria-expanded", "true");

        inhalt.addEventListener(
          "transitionend",
          () => {
            if (knopf.getAttribute("aria-expanded") === "true") {
              inhalt.style.height = "auto";
            }
          },
          { once: true }
        );
      }
    });
  });

  let etwasGebaut = false;

  const sortenraster = document.getElementById("sorten-raster");
  if (sortenraster && Array.isArray(window.SORTEN)) {
    sortenraster.innerHTML = window.SORTEN.map((s) => {
      const punkte = Array.from({ length: 5 }, (_, i) =>
        `<span class="sorte__punkt${i < s.roestgrad ? " ist-voll" : ""}"></span>`
      ).join("");
      const noten = (s.noten || [])
        .map((n) => `<span class="sorte__note">${sicher(n)}</span>`)
        .join("");
      return (
        `<article class="sorte einblenden" style="--ton:${tonVon(s.bild)}">` +
        '<div class="sorte__kopf">' +
        `<span class="sorte__herkunft">${sicher(s.herkunft)}</span>` +
        "</div>" +
        '<div class="freilegen">' +
        rahmen(s.bild, "bild--1-1 bild--duplex", {
          sizes: "(max-width: 640px) 88vw, (max-width: 1100px) 44vw, 300px",
        }) +
        "</div>" +
        `<h3 style="margin-top:var(--sp-5)">${sicher(s.name)}</h3>` +
        `<p style="color:var(--muted)">${sicher(s.text)}</p>` +
        `<div class="sorte__noten">${noten}</div>` +
        '<div class="sorte__skala">' +
        "<span>Röstgrad</span>" +
        `<span class="sorte__punkte" role="img" aria-label="Röstgrad ${sicher(
          s.roestgrad
        )} von 5">${punkte}</span>` +
        "</div>" +
        "</article>"
      );
    }).join("");
    etwasGebaut = true;
  }

  const spur = document.getElementById("strecke-spur");
  if (spur && Array.isArray(window.STATIONEN)) {
    spur.innerHTML = window.STATIONEN.map(
      (st, i) =>
        '<article class="station">' +
        `<span class="station__nummer">${String(i + 1).padStart(2, "0")}</span>` +
        '<div class="freilegen">' +
        rahmen(st.bild, "bild--4-5 bild--duplex", {
          sizes: "(max-width: 760px) 88vw, min(34vw, 380px)",
        }) +
        "</div>" +
        `<h3>${sicher(st.titel)}</h3>` +
        `<p>${sicher(st.text)}</p>` +
        "</article>"
    ).join("");
    etwasGebaut = true;
  }

  const laufband = document.querySelector(".laufband");
  if (laufband && Array.isArray(window.LAUFBAND)) {
    const stuecke = window.LAUFBAND.map(
      (t) => `<span class="laufband__stueck"><i></i>${sicher(t)}</span>`
    ).join("");
    laufband.innerHTML =
      `<div class="laufband__spur">${stuecke}</div>` +
      `<div class="laufband__spur" aria-hidden="true">${stuecke}</div>`;
  }

  if (etwasGebaut) {
    document.dispatchEvent(new CustomEvent("raster:bereit"));
  }
})();
