"""Zet de twee markdown-documenten om naar pdf in de BNW-huisstijl (Nunito Sans, Diepblauw, rechte hoeken)."""
import base64, glob, html, re, subprocess, sys, os, asyncio
H = os.path.dirname(os.path.abspath(__file__))
LOGO = base64.b64encode(open(f'{H}/../../bron/logo-bnw.png', 'rb').read()).decode()
FONT = base64.b64encode(open(f'{H}/NunitoSans-latin.woff2', 'rb').read()).decode()  # latin, variabel gewicht

DIAGRAM = '''<figure class="diagram"><svg viewBox="0 0 760 300" role="img" aria-label="Stroom van link tot ontvangst" font-family="Nunito Sans, Arial, sans-serif" font-size="13">
<defs><marker id="pijl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0444A3"/></marker></defs>
<g fill="none" stroke="#0444A3" stroke-width="1.5">
<path d="M236 96H280" marker-end="url(#pijl)"/><path d="M480 96H524" marker-end="url(#pijl)"/><path d="M624 132V196" marker-end="url(#pijl)"/><path d="M524 232H480" marker-end="url(#pijl)"/></g>
<g><rect x="36" y="60" width="200" height="72" fill="#fff" stroke="#0444A3" stroke-width="1.5"/><text x="136" y="86" text-anchor="middle" font-weight="900" fill="#001692">1. BNW-medewerker</text><text x="136" y="104" text-anchor="middle" font-size="11.5" fill="#52525E">interne pagina /intern-…/</text><text x="136" y="120" text-anchor="middle" font-size="11.5" fill="#52525E">sleutel + gegevens → /api/links</text></g>
<g><rect x="280" y="60" width="200" height="72" fill="#E2F0FE" stroke="#0444A3" stroke-width="2.5"/><text x="380" y="86" text-anchor="middle" font-weight="900" fill="#001692">2. Praktijk</text><text x="380" y="104" text-anchor="middle" font-size="11.5" fill="#52525E">haalt gegevens op, leest, tekent</text><text x="380" y="120" text-anchor="middle" font-size="11.5" fill="#52525E">browser maakt de pdf</text></g>
<g><rect x="524" y="60" width="200" height="72" fill="#fff" stroke="#0444A3" stroke-width="1.5"/><text x="624" y="86" text-anchor="middle" font-weight="900" fill="#001692">3. Functies + Blobs</text><text x="624" y="104" text-anchor="middle" font-size="11.5" fill="#52525E">bewaart pdf, IP, tijd; link op gebruikt</text><text x="624" y="120" text-anchor="middle" font-size="11.5" fill="#52525E">meldt aan Netlify Forms</text></g>
<g><rect x="524" y="196" width="200" height="72" fill="#fff" stroke="#0444A3" stroke-width="1.5"/><text x="624" y="222" text-anchor="middle" font-weight="900" fill="#001692">4. E-mailmelding</text><text x="624" y="240" text-anchor="middle" font-size="11.5" fill="#52525E">naar administratie@bnw.nl</text><text x="624" y="256" text-anchor="middle" font-size="11.5" fill="#52525E">gegevens, IP, pdf-link met sleutel</text></g>
<g><rect x="280" y="196" width="200" height="72" fill="#E2F0FE" stroke="#98CAF5" stroke-width="1.5"/><text x="380" y="222" text-anchor="middle" font-weight="900" fill="#001692">Kopie voor de praktijk</text><text x="380" y="240" text-anchor="middle" font-size="11.5" fill="#52525E">dezelfde pdf, als download</text><text x="380" y="256" text-anchor="middle" font-size="11.5" fill="#52525E">direct na versturen</text></g>
<text x="258" y="50" text-anchor="middle" font-size="11.5" fill="#616161">persoonlijke link</text><text x="502" y="50" text-anchor="middle" font-size="11.5" fill="#616161">POST pdf → /api/onderteken</text><text x="610" y="168" text-anchor="end" font-size="11.5" fill="#616161">automatisch</text>
</svg><figcaption>Stroom van link tot ontvangst in vier stappen.</figcaption></figure>'''

CSS = f'''
@font-face {{ font-family: "Nunito Sans"; font-weight: 200 1000; font-style: normal; src: url(data:font/woff2;base64,{FONT}) format("woff2"); }}
@page {{ size: A4; margin: 22mm 18mm 20mm 18mm; }}
* {{ box-sizing: border-box; }}
html {{ font-family: "Nunito Sans", Arial, Helvetica, sans-serif; color: #52525E; font-size: 10.5pt; line-height: 1.5; }}
body {{ margin: 0; }}
.kop {{ display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #0444A3; padding-bottom: 12px; margin-bottom: 28px; }}
.kop img {{ width: 150px; }}
.kop .meta {{ text-align: right; font-size: 9pt; color: #616161; line-height: 1.4; }}
h1 {{ font-size: 24pt; font-weight: 900; text-transform: uppercase; color: #0444A3; letter-spacing: .25px; line-height: 1.2; margin: 0 0 6px; }}
.sub {{ font-size: 11pt; color: #616161; margin: 0 0 36px; max-width: 70ch; }}
h2 {{ font-size: 15pt; font-weight: 900; text-transform: uppercase; color: #0444A3; letter-spacing: .5px; margin: 30px 0 10px; padding-bottom: 6px; border-bottom: 2px solid #0444A3; break-after: avoid; }}
h3 {{ font-size: 10.5pt; font-weight: 900; text-transform: uppercase; color: #0444A3; margin: 18px 0 6px; break-after: avoid; }}
p {{ margin: 0 0 9px; max-width: 75ch; }}
strong {{ font-weight: 700; color: #001692; }}
ul, ol {{ margin: 0 0 10px; padding-left: 22px; }}
li {{ margin-bottom: 4px; max-width: 72ch; }}
li::marker {{ color: #0444A3; font-weight: 700; }}
code {{ font-family: "Nunito Sans", Arial, sans-serif; background: #E2F0FE; color: #001692; padding: 0 4px; font-size: 95%; }}
table {{ border-collapse: collapse; width: 100%; margin: 8px 0 16px; font-size: 9.5pt; break-inside: auto; }}
th {{ text-align: left; background: #0444A3; color: #fff; font-weight: 700; padding: 7px 9px; }}
td {{ padding: 6px 9px; vertical-align: top; border-bottom: 1px solid #E2F0FE; }}
tr:nth-child(even) td {{ background: #F3F8FE; }}
tr {{ break-inside: avoid; }}
blockquote {{ margin: 8px 0 14px; padding: 12px 16px; background: #E2F0FE; border-left: 4px solid #0444A3; color: #001692; max-width: 75ch; }}
blockquote p {{ margin: 0 0 6px; }}
figure.diagram {{ margin: 12px 0 18px; }}
figure.diagram svg {{ width: 100%; height: auto; display: block; }}
figcaption {{ font-size: 9pt; color: #616161; margin-top: 4px; }}
.voet {{ position: running(voet); }}
'''

def md_to_html(md):
    out, i, lines = [], 0, md.split('\n')
    def inline(t):
        t = html.escape(t, quote=False)
        t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
        t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
        t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
        t = re.sub(r'(?<![">])(https?://[^\s<]+)', r'<a href="\1">\1</a>', t)
        return t
    while i < len(lines):
        l = lines[i]
        if l.startswith('# '): out.append(f'<h1>{inline(l[2:])}</h1>'); i += 1
        elif l.startswith('## '): out.append(f'<h2>{inline(l[3:])}</h2>'); i += 1
        elif l.startswith('@@DIAGRAM@@'): out.append(DIAGRAM); i += 1
        elif re.match(r'^\*\*[^*]+\*\*$', l.strip()): out.append(f'<h3>{html.escape(l.strip()[2:-2])}</h3>'); i += 1
        elif l.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]); i += 1
            rows = [r for r in rows if not all(re.match(r'^-+$', c) for c in r)]
            out.append('<table><thead><tr>' + ''.join(f'<th>{inline(c)}</th>' for c in rows[0]) + '</tr></thead><tbody>' +
                       ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</tbody></table>')
        elif re.match(r'^(\d+\. |- )', l):
            tag = 'ol' if l[0].isdigit() else 'ul'; items = []
            while i < len(lines) and re.match(r'^(\d+\. |- )', lines[i]):
                items.append(re.sub(r'^(\d+\. |- )', '', lines[i])); i += 1
            out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
        elif l.startswith('>'):
            q = []
            while i < len(lines) and lines[i].startswith('>'):
                q.append(lines[i][1:].strip()); i += 1
            paras, cur = [], []
            for x in q:
                if x == '': paras.append(cur); cur = []
                else: cur.append(x)
            paras.append(cur)
            out.append('<blockquote>' + ''.join(f'<p>{"<br>".join(inline(y) for y in p)}</p>' for p in paras if p) + '</blockquote>')
        elif l.strip() == '': i += 1
        else:
            para = []
            while i < len(lines) and lines[i].strip() and not re.match(r'^(#|\||\d+\. |- |>|@@|\*\*[^*]+\*\*$)', lines[i]):
                para.append(lines[i]); i += 1
            out.append(f'<p>{inline(" ".join(para))}</p>')
    return '\n'.join(out)

DOCS = [('handleiding.md', 'Handleiding-digitaal-ondertekenen-BNW', 'Voor administratie van BNW en voor praktijken die een leden- of kennismakersovereenkomst digitaal ondertekenen.'),
        ('technische-opzet.md', 'Technische-opzet-digitaal-ondertekenen-BNW', 'Architectuur, beveiliging, beheer en verbeterpunten van het ondertekensysteem op bnw-ondertekenen.netlify.app.')]

async def render():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        for src, naam, sub in DOCS:
            body = md_to_html(open(f'{H}/../{src}', encoding='utf-8').read())
            body = body.replace('</h1>', f'</h1><p class="sub">{sub}</p>', 1)
            doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><title>{naam}</title><style>{CSS}</style></head><body>
<div class="kop"><img src="data:image/png;base64,{LOGO}" alt="BNW beweegt de zorg"><div class="meta">Versie 2 · 15 oktober 2026<br>Opgesteld voor BNW · administratie@bnw.nl</div></div>
{body}</body></html>'''
            open(f'{H}/{naam}.html', 'w', encoding='utf-8').write(doc)
            pg = await b.new_page()
            await pg.set_content(doc, wait_until='load')
            await pg.evaluate('document.fonts.ready')
            await pg.pdf(path=f'{H}/../{naam}.pdf', format='A4', print_background=True, display_header_footer=True,
                         margin={'top': '22mm', 'bottom': '20mm', 'left': '18mm', 'right': '18mm'},
                         header_template='<div></div>',
                         footer_template=f'<div style="width:100%;font-family:Arial,sans-serif;font-size:8px;color:#616161;padding:0 18mm;display:flex;justify-content:space-between;border-top:1px solid #E2F0FE;padding-top:4px;"><span>BNW · {naam.replace("-", " ").replace(" BNW", "")}</span><span>Pagina <span class="pageNumber"></span> van <span class="totalPages"></span></span></div>')
            await pg.close()
            print(naam)
        await b.close()
asyncio.run(render())
