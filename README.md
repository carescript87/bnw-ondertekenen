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
