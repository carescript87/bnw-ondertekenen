# BNW ondertekenen

Digitaal ondertekenen van de leden- en kennismakersovereenkomst van BNW.
Live op https://bnw-ondertekenen.netlify.app. Technische documentatie en handleiding: zie het document
"Technische opzet digitaal ondertekenen BNW".

- `bron/` — overeenkomstteksten, templates, logo en bouwscript voor de pagina's
- `scripts/build.py` — bouwt `site/` (uitvoeren na elke wijziging in `bron/`, daarna committen)
- `site/` — de uitgerolde pagina's (publish directory)
- `netlify/functions/` — serverfuncties: links maken/lezen, ondertekenen, pdf leveren, opschonen
- `test/keten.cjs` — end-to-end-test tegen `netlify dev --offline` (port 8899)

Omgevingsvariabelen (scope Functions): `INTERN_SLEUTEL`, `BEWAARTERMIJN_DAGEN`, optioneel `LINK_BEWAREN_DAGEN`, `NETLIFY_API_TOKEN`.

## Documentatie

- `docs/technische-opzet.md` en `docs/Technische-opzet-digitaal-ondertekenen-BNW.pdf` — architectuur, link-opbouw, beveiliging en privacy, beheer, verbeterpunten
- `docs/handleiding.md` en `docs/Handleiding-digitaal-ondertekenen-BNW.pdf` — handleiding voor administratie en praktijken
- `docs/huisstijl/maak_pdf.py` — maakt de pdf's in BNW-huisstijl uit de markdown (`python3 docs/huisstijl/maak_pdf.py`, vereist Playwright met Chromium)

## Architectuur in het kort

1. **BNW-medewerker** maakt op de interne pagina met de BNW-sleutel een persoonlijke link (`POST /api/links`, functie `links-maken`); de gegevens gaan naar Netlify Blobs (store `links`).
2. **Praktijk** opent de link; de pagina haalt de gegevens op (`GET /api/links/:token`), de praktijk leest, tekent en de browser maakt de pdf met jsPDF.
3. **Functie `ondertekenen`** (`POST /api/onderteken/:token`) slaat de pdf en metadata (IP-adres, browser, servertijd) op in store `inzendingen`, zet de link op gebruikt en meldt de ondertekening aan Netlify Forms.
4. **Administratie** ontvangt de pdf (per e-mail van de praktijk of via de pdf-link uit Forms, functie `pdf-lezen`).
5. **Functie `opschonen`** verwijdert elke nacht verlopen links en inzendingen ouder dan de bewaartermijn.
