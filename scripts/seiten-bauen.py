#!/usr/bin/env python3

import json
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parent.parent

BETRIEB = "Röstwerk Nord"

CSP = (
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; "
    "img-src 'self' data:; font-src 'self'; connect-src 'self'; "
    "object-src 'none'; base-uri 'none'; form-action 'none'; "
    "upgrade-insecure-requests"
)

NAVIGATION = [
    ("kaffees", "Kaffees"),
    ("roesterei", "Rösterei"),
    ("besuch", "Besuch"),
    ("kontakt", "Kontakt"),
]

_nachweise = WURZEL / "bilder" / "nachweise.json"
BILDER = {}
if _nachweise.exists():
    BILDER = json.loads(_nachweise.read_text(encoding="utf-8"))["bilder"]

def bild(name: str, sizes: str, *, eifrig: bool = False, alt: str = None) -> str:
    b = BILDER.get(name)
    if not b:
        return f"<!-- Bild fehlt: {name} — scripts/bilder-holen.py laufen lassen -->"
    srcset = ", ".join(f"../bilder/{name}-{w}.webp {w}w" for w in b["breiten"])
    gross = b["breiten"][-1]
    laden = (
        'fetchpriority="high" decoding="async"'
        if eifrig
        else 'loading="lazy" decoding="async"'
    )
    return (
        f'<img src="../bilder/{name}-{gross}.webp" srcset="{srcset}" '
        f'sizes="{sizes}" width="{b["breite"]}" height="{b["hoehe"]}" '
        f'alt="{alt or b["alt"]}" {laden}>'
    )

def rahmen(name: str, klasse: str, sizes: str, **kw) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--bg-2)"
    return (
        f'<div class="bild {klasse}" style="--platzhalter:{farbe}">'
        + bild(name, sizes, **kw)
        + "</div>"
    )

def bildband(name: str, alt: str = None) -> str:
    b = BILDER.get(name)
    farbe = b["farbe"] if b else "var(--bg-2)"
    return (
        f'\n    <div class="heroband" style="--platzhalter:{farbe}">\n      '
        + bild(name, "100vw", eifrig=True, alt=alt)
        + "\n    </div>\n"
    )

def zeilen(*texte) -> str:
    aus = []
    for i, text in enumerate(texte):
        verzug = f' style="--verzug:{i * 110}ms"' if i else ""
        aus.append(
            f'<span class="zeile"><span class="zeile__inner"{verzug}>{text}</span></span>'
        )
    return "\n        ".join(aus)

def kopf(slug: str, titel: str, beschreibung: str) -> str:
    nav = "\n".join(
        f'          <li><a href="../{ziel}/index.html"'
        f'{" aria-current=\"page\"" if ziel == slug else ""}>{text}</a></li>'
        for ziel, text in NAVIGATION
    )

    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <meta http-equiv="Content-Security-Policy" content="{CSP}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <title>{titel} — {BETRIEB}</title>
  <meta name="description" content="{beschreibung}">
  <link rel="icon" href="../assets/icons/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="../assets/css/basis.css">
  <link rel="stylesheet" href="../assets/css/raster.css">
  <link rel="stylesheet" href="../assets/css/komponenten.css">
  <link rel="stylesheet" href="../assets/css/bilder.css">
  <link rel="stylesheet" href="../assets/css/bewegung.css">
</head>
<body data-wurzel="../">
  <a class="sprunglink" href="#inhalt">Zum Inhalt</a>
  <div class="koernung" aria-hidden="true"></div>

  <header class="kopfzeile">
    <div class="breite kopfzeile__inhalt">
      <a class="marke" href="../index.html">{BETRIEB}<i></i></a>
      <nav class="hauptnav" aria-label="Hauptnavigation">
        <ul>
{nav}
        </ul>
      </nav>
    </div>
  </header>

  <main id="inhalt">
"""

FUSS = f"""  </main>

  <footer class="fusszeile">
    <div class="breite">
      <div class="fusszeile__raster">
        <div>
          <p class="fusszeile__marke">Röstwerk<br>Nord</p>
        </div>
        <div>
          <h2>Rösterei</h2>
          <p style="color:var(--muted)">
            Helmstedter Straße 27<br>
            38102 Braunschweig
          </p>
        </div>
        <div>
          <h2>Kontakt</h2>
          <ul>
            <li><a href="tel:+495312408815">0531 240 88 15</a></li>
            <li><a href="mailto:hallo@roestwerk-nord.de">hallo@roestwerk-nord.de</a></li>
          </ul>
        </div>
        <div>
          <h2>Seiten</h2>
          <ul>
            <li><a href="../kaffees/index.html">Kaffees</a></li>
            <li><a href="../roesterei/index.html">Rösterei</a></li>
            <li><a href="../besuch/index.html">Besuch</a></li>
            <li><a href="../kontakt/index.html">Kontakt</a></li>
          </ul>
        </div>
      </div>

      <p class="fusszeile__hinweis">
        <strong>Musterprojekt.</strong> Betrieb, Anschrift und Inhalte sind frei
        erfunden. Kein Kundenauftrag. Diese Seite dient als Arbeitsprobe.
        Die Fotos stammen von Unsplash und zeigen nicht diesen Betrieb —
        Urheber und Lizenz stehen im <a href="../impressum/index.html">Impressum</a>.
      </p>

      <div class="fusszeile__unten">
        <p>{BETRIEB} — © 2026</p>
        <ul>
          <li><a href="../impressum/index.html">Impressum</a></li>
          <li><a href="../datenschutz/index.html">Datenschutz</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="../daten/inhalte.js" defer></script>
  <script src="../daten/bilder.js" defer></script>
  <script src="../assets/js/bewegung.js" defer></script>
  <script src="../assets/js/komponenten.js" defer></script>
</body>
</html>
"""

def seitenkopf(etikett: str, *kopfzeilen, lead: str = "") -> str:
    lead_html = (
        f'\n      <p class="hero__lead einblenden">{lead}</p>' if lead else ""
    )
    return f"""
    <section class="hero breite">
      <p class="etikett einblenden">{etikett}</p>
      <h1 style="font-size:var(--fs-h2)">
        {zeilen(*kopfzeilen)}
      </h1>{lead_html}
    </section>
"""

SEITEN = {
    "kaffees": {
        "titel": "Kaffees",
        "beschreibung": "Vier Kaffees aus eigener Röstung: Hausmischung, Filter, Espresso und koffeinfrei.",
        "inhalt": seitenkopf(
            "Im Regal",
            "Vier Kaffees,",
            "<em>ein Röster.</em>",
            lead="Mehr sind es absichtlich nicht. Vier Kaffees kann man kennen; "
            "zwanzig kann man nur verwalten.",
        )
        + bildband("bohnen-schale", "Geröstete Bohnen in einer runden Schale")
        + """
    <section class="abschnitt breite">
      <div class="spalten spalten--2" id="sorten-raster"></div>
      <noscript>
        <ul>
          <li>Hafenkante — Hausmischung, Röstgrad 4</li>
          <li>Nordlicht — Filter, Röstgrad 2</li>
          <li>Werkstatt — Espresso, Röstgrad 5</li>
          <li>Stillstand — koffeinfrei, Röstgrad 3</li>
        </ul>
      </noscript>

      <div class="einblenden" style="margin-top:var(--sp-9)">
        __STRECKE_KAFFEES__
      </div>

      <p class="etikett einblenden" style="margin-top:var(--sp-8)">
        Alle Sorten gibt es als 250-Gramm-Packung und als Kilo. Ganze Bohne, oder auf Wunsch gemahlen — dann sagen Sie bitte, womit Sie aufbrühen.
      </p>
    </section>

    <section class="abschnitt breite" aria-labelledby="mahlgrad-titel">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">01</span>
          <p class="etikett kapitel__titel">Zubereitung</p>
        </div>
        <div>
          <h2 id="mahlgrad-titel">Welcher Kaffee wofür?</h2>

          <div class="einblenden" style="margin-top:var(--sp-7)">
            <div class="klapp">
              <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="z-1">
                <span>Espressomaschine</span><span class="klapp__zeichen" aria-hidden="true"></span>
              </button>
              <div class="klapp__inhalt" id="z-1">
                <div><p>Werkstatt oder Hafenkante. Beide halten Druck aus und
                brechen in Milch nicht weg. Nordlicht ist dafür zu hell geröstet —
                sie wird im Siebträger sauer.</p></div>
              </div>
            </div>

            <div class="klapp">
              <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="z-2">
                <span>Handfilter und Karaffe</span><span class="klapp__zeichen" aria-hidden="true"></span>
              </button>
              <div class="klapp__inhalt" id="z-2">
                <div><p>Nordlicht. Grob mahlen, Wasser bei etwa 94 Grad,
                drei Minuten Gesamtzeit. Als Verhältnis: 60 Gramm auf den Liter.</p></div>
              </div>
            </div>

            <div class="klapp">
              <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="z-3">
                <span>Vollautomat</span><span class="klapp__zeichen" aria-hidden="true"></span>
              </button>
              <div class="klapp__inhalt" id="z-3">
                <div><p>Hafenkante. Sie verzeiht Schwankungen im Mahlgrad,
                und genau die hat jeder Vollautomat.</p></div>
              </div>
            </div>

            <div class="klapp">
              <button class="klapp__knopf" type="button" aria-expanded="false" aria-controls="z-4">
                <span>French Press</span><span class="klapp__zeichen" aria-hidden="true"></span>
              </button>
              <div class="klapp__inhalt" id="z-4">
                <div><p>Stillstand oder Hafenkante, grob gemahlen, vier Minuten
                ziehen lassen, dann abgießen statt stehen lassen.</p></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
""",
    },
    "roesterei": {
        "titel": "Rösterei",
        "beschreibung": "Wie in Braunschweig geröstet wird: Trommel statt Heißluft, zwölf Kilo je Charge, jede Röstung protokolliert.",
        "inhalt": seitenkopf(
            "Handwerk",
            "Zwölf Kilo,",
            "achtzehn Minuten,",
            "<em>ein Protokoll.</em>",
            lead="Die Rösterei steht im selben Raum wie die Theke. "
            "Das ist keine Inszenierung, sondern eine Platzfrage.",
        )
        + bildband("roester-detail", "Nahaufnahme der Röstmaschine")
        + """
    <section class="abschnitt breite" aria-labelledby="warum-titel">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">01</span>
          <p class="etikett kapitel__titel">Trommel</p>
        </div>
        <div>
          <h2 id="warum-titel">Warum nicht schneller?</h2>
          <p class="einblenden" style="margin-top:var(--sp-6);color:var(--muted)">
            Industrieröster arbeiten mit Heißluft und sind in unter fünf Minuten
            fertig. Das Ergebnis ist außen dunkel und innen roh. Eine Trommel
            gibt die Wärme langsamer ab; die Bohne durchwärmt gleichmäßig, und
            genau daran hängt, ob ein Kaffee süß wird oder nur bitter.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Bei uns steht ein Trommelröster mit zwölf Kilo Fassung, Baujahr 1998, seitdem zweimal überholt.
          </p>

          <div class="freilegen" style="margin-top:var(--sp-8)">
            __BILD_GLUT__
          </div>
          <p class="bildzeile"><b>Minute 14</b><span>kurz vor dem ersten Knacken</span></p>
        </div>
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="verkostung-titel">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">02</span>
          <p class="etikett kapitel__titel">Verkostung</p>
        </div>
        <div>
          <h2 id="verkostung-titel">Jede Charge wird probiert.</h2>
          <p class="einblenden" style="margin-top:var(--sp-6);color:var(--muted)">
            Nach dem Ruhen wird aufgebrüht und gelöffelt — immer gleich
            aufgesetzt, damit die Tassen vergleichbar sind. Was nicht besteht,
            geht nicht in den Verkauf.
          </p>

          <div class="versetzt" style="margin-top:var(--sp-8)">
            <div class="freilegen">
              __BILD_AUFGUSS__
              <p class="bildzeile"><b>Aufguss</b><span>gleiche Menge, gleiches Wasser</span></p>
            </div>
            <div class="freilegen">
              __BILD_LOEFFEL__
              <p class="bildzeile"><b>Löffel</b><span>abschöpfen, riechen, schlürfen</span></p>
            </div>
          </div>

          <p class="einblenden" style="margin-top:var(--sp-7)">
            <a class="knopf knopf--leer" href="../besuch/index.html">Samstags mitverkosten</a>
          </p>
        </div>
      </div>
    </section>

    <section class="abschnitt--eng breite">
      <dl class="kennzahlen einblenden">
        <div class="kennzahl">
          <dt>Kilo je Charge</dt>
          <dd><span data-zaehlziel="12">12</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Minuten Röstzeit</dt>
          <dd><span data-zaehlziel="18">18</span></dd>
        </div>
        <div class="kennzahl">
          <dt>Herkünfte im Jahr</dt>
          <dd><span data-zaehlziel="9">9</span></dd>
        </div>
      </dl>
    </section>
""",
    },
    "besuch": {
        "titel": "Besuch",
        "beschreibung": "Öffnungszeiten, Verkostung am Samstag und Anfahrt zur Rösterei in Braunschweig.",
        "inhalt": seitenkopf(
            "Gastraum",
            "Kommen Sie",
            "<em>samstags.</em>",
            lead="Dann wird geröstet, und dann wird verkostet. "
            "An den anderen Tagen ist es ruhiger — auch schön.",
        )
        + bildband("cafe-raum", "Gastraum mit Holztischen und Bänken")
        + """
    <section class="abschnitt breite">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">01</span>
          <p class="etikett kapitel__titel">Öffnungszeiten</p>
        </div>
        <div>
          <dl class="zeiten einblenden">
            <div><dt>Montag</dt><dd>Ruhetag</dd></div>
            <div><dt>Dienstag bis Freitag</dt><dd>8 – 18 Uhr</dd></div>
            <div><dt>Samstag</dt><dd>9 – 16 Uhr</dd></div>
            <div><dt>Sonntag</dt><dd>10 – 16 Uhr</dd></div>
          </dl>

          <h2 style="margin-top:var(--sp-9)">Verkostung</h2>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Samstags wird geröstet und anschließend verkostet. Wer dabei sein
            will, kommt einfach vorbei — Anmeldung braucht es nicht, einen
            Platz an der Theke schon.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Los geht es samstags um 11 Uhr, die Runde dauert etwa 45 Minuten und kostet nichts.
          </p>

          <div class="freilegen" style="margin-top:var(--sp-8)">
            __BILD_STUEHLE__
          </div>
          <p class="bildzeile"><b>Vor der Öffnung</b><span>zehn Tische, eine Theke</span></p>
        </div>
      </div>
    </section>

    <section class="abschnitt breite">
      <div class="einblenden">
        __STRECKE_BESUCH__
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="anfahrt-titel">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">03</span>
          <p class="etikett kapitel__titel">Anfahrt</p>
        </div>
        <div>
          <h2 id="anfahrt-titel">So finden Sie her.</h2>
          <p class="einblenden" style="margin-top:var(--sp-6);color:var(--muted)">
            Mit der Straßenbahn 1 oder 2 bis Helmstedter Straße, von dort hundert Meter stadtauswärts auf der linken Seite. Mit dem Auto über den Bohlweg; im Hof stehen sechs Plätze für Kundschaft.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-5);font-size:var(--fs-meta);color:var(--muted)">
            Eine eingebettete Karte fehlt hier bewusst: sie würde beim Aufruf
            Daten an einen fremden Anbieter senden, bevor jemand eingewilligt
            hat. Der Link darunter wird erst auf Klick geöffnet.
          </p>
          <p class="einblenden" style="margin-top:var(--sp-6)">
            <a class="knopf knopf--leer" href="https://www.openstreetmap.org/search?query=Helmstedter%20Stra%C3%9Fe%2027%2C%2038102%20Braunschweig" rel="noopener">
              In der Karte öffnen
            </a>
          </p>
        </div>
      </div>
    </section>
""",
    },
    "kontakt": {
        "titel": "Kontakt",
        "beschreibung": "Telefon, E-Mail und Ansprechpartner der Rösterei Röstwerk Nord in Braunschweig.",
        "inhalt": seitenkopf(
            "Kontakt",
            "Rufen Sie an.",
            lead="Für Bestellungen, Gastronomie-Anfragen und alles, was sich "
            "am Telefon in fünf Minuten klären lässt.",
        )
        + bildband("bar-barista", "Barista an der Espressomaschine")
        + """
    <section class="abschnitt breite">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">01</span>
          <p class="etikett kapitel__titel">Direkt</p>
        </div>
        <div>
          <dl class="kontaktliste einblenden">
            <dt>Telefon</dt>
            <dd><a href="tel:+495312408815">0531 240 88 15</a></dd>
            <dt>E-Mail</dt>
            <dd><a href="mailto:hallo@roestwerk-nord.de">hallo@roestwerk-nord.de</a></dd>
            <dt>Rösterei</dt>
            <dd>Helmstedter Straße 27<br>38102 Braunschweig</dd>
          </dl>

          <p class="einblenden" style="margin-top:var(--sp-6);font-size:var(--fs-meta);color:var(--muted)">
            Diese Seite hat kein Kontaktformular. Ein Formular braucht eine
            Verarbeitung im Hintergrund, eine Einwilligung und einen Eintrag in
            der Datenschutzerklärung. Telefon und E-Mail leisten dasselbe, ohne
            das alles.
          </p>
        </div>
      </div>
    </section>

    <section class="abschnitt breite" aria-labelledby="gastro-titel">
      <div class="kapitel">
        <div class="kapitel__marke">
          <span class="kapitel__nummer">02</span>
          <p class="etikett kapitel__titel">Gastronomie</p>
        </div>
        <div>
          <h2 id="gastro-titel">Kaffee für Cafés und Büros.</h2>
          <p class="einblenden" style="margin-top:var(--sp-6);color:var(--muted)">
            Wir beliefern Braunschweig, Wolfenbüttel und Salzgitter mit festen Lieferterminen.
            Zur Belieferung gehört eine Einweisung an der Maschine — Kaffee, den
            niemand richtig aufbrühen kann, macht keine Freude.
          </p>
          <div class="einblenden" style="margin-bottom:var(--sp-7)">
            __STRECKE_KONTAKT__
          </div>

          <p class="einblenden" style="margin-top:var(--sp-5);color:var(--muted)">
            Ab fünf Kilo im Monat, geliefert wird dienstags und freitags. Ansprechpartnerin ist Katrin Bohlen.
          </p>
        </div>
      </div>
    </section>
""",
    },
}

def strecke(*eintraege):
    karten = []
    for name, titel, zeile in eintraege:
        karten.append(
            '<div class="freilegen">'
            + rahmen(name, "bild--3-2 bild--duplex",
                     "(max-width: 640px) 90vw, (max-width: 1100px) 45vw, 30vw")
            + f'<p class="bildzeile"><b>{titel}</b><span>{zeile}</span></p>'
            + "</div>"
        )
    return '<div class="spalten spalten--3">' + "".join(karten) + "</div>"


MARKEN = {
    "__STRECKE_KAFFEES__": lambda: strecke(
        ("bohnen-makro", "Ganze Bohne", "frisch aus der Trommel"),
        ("weg-5-muehle", "Mahlgrad", "kurz vor dem Aufguss"),
        ("verkostung-tassen", "Verkostung", "jede Charge wird probiert"),
    ),
    "__STRECKE_BESUCH__": lambda: strecke(
        ("cafe-lampen", "Langer Tisch", "für alle, die allein kommen"),
        ("bar-barista", "Theke", "zwei Mühlen, ein Siebträger"),
        ("verkostung-loeffel", "Samstags", "Löffel, Tasse, Gespräch"),
    ),
    "__STRECKE_KONTAKT__": lambda: strecke(
        ("roester-detail", "Röster", "zwölf Kilo Fassung"),
        ("weg-3-sack", "Rohkaffee", "so kommt er an"),
        ("cafe-stuehle", "Vor der Öffnung", "zehn Tische, eine Theke"),
    ),
    "__BILD_GLUT__": lambda: rahmen(
        "roester-glut", "bild--4-5 bild--duplex", "(max-width: 900px) 88vw, 46vw"
    ),
    "__BILD_AUFGUSS__": lambda: rahmen(
        "verkostung-aufguss", "bild--4-5 bild--duplex", "(max-width: 800px) 88vw, 40vw"
    ),
    "__BILD_LOEFFEL__": lambda: rahmen(
        "verkostung-loeffel", "bild--3-2 bild--duplex", "(max-width: 800px) 88vw, 40vw"
    ),
    "__BILD_STUEHLE__": lambda: rahmen(
        "cafe-stuehle", "bild--3-2 bild--duplex", "(max-width: 900px) 88vw, 60vw"
    ),
}

def bauen() -> None:
    if not BILDER:
        print("WARNUNG: bilder/nachweise.json fehlt.")
        print("         Erst scripts/bilder-holen.py laufen lassen.\n")

    for slug, seite in SEITEN.items():
        inhalt = seite["inhalt"]
        for marke, bauer in MARKEN.items():
            if marke in inhalt:
                inhalt = inhalt.replace(marke, bauer())

        ziel = WURZEL / slug / "index.html"
        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(
            kopf(slug, seite["titel"], seite["beschreibung"]) + inhalt + FUSS,
            encoding="utf-8",
        )
        print(f"geschrieben: {ziel.relative_to(WURZEL)}")

if __name__ == "__main__":
    bauen()
    print("\nImpressum und Datenschutz werden NICHT erzeugt — sie stehen von Hand,")
    print("damit kein Generator versehentlich eine Pflichtangabe umschreibt.")
