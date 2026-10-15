"""Bouwt de map site/ uit bron/: de twee ondertekenpagina's, de interne linkpagina, de startpagina en de formulierdefinitie."""
import os, re, shutil, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B, OUT = f'{R}/bron', f'{R}/site'
INTERN = os.environ.get('INTERN_PAD', 'intern-1e2da84950')
subprocess.run([sys.executable, f'{B}/build.py'], check=True, cwd=B)
shutil.rmtree(OUT, ignore_errors=True)
HEAD = '<!doctype html>\n<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style></head><body>\n'
FOOT = '\n</body></html>\n'

def rep(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a)); return s.replace(a, b)
def cut(s, a, b, new):
    i = s.index(a); j = s.index(b, i); return s[:i] + new + s[j:]

LEES = '''/* ---------- gegevens via de API ---------- */
  var TOKEN = /^[A-Za-z0-9_-]{20,64}$/.test(location.hash.slice(1)) ? location.hash.slice(1) : null;
  var V = null;
  function waarden() { return V; }
  function totTekst(iso) { var p = iso.split("-"); return (+p[2]) + " " + MAANDEN[+p[1] - 1] + " " + p[0]; }
  function toonFout(id) { $("formulier").hidden = true; ["ongeldig", "verlopen", "ondertekend"].forEach(function (k) { $(k).hidden = k !== id; }); }
  '''
VERSTUUR = '''    var fd = new FormData();
    fd.append("akkoord", "ja");
    fd.append("pdf", new File([blob], naam, { type: "application/pdf" }));
    var url = URL.createObjectURL(blob);
    function download() { var a = document.createElement("a"); a.href = url; a.download = naam; document.body.appendChild(a); a.click(); a.remove(); }
    $("kopie").onclick = download;
    fetch("/api/onderteken/" + TOKEN, { method: "POST", body: fd }).then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw d; return d; });
    }).then(function () {
      bezig = true; $("verstuur").disabled = true; $("verstuur").textContent = "Verstuurd"; $("wis").disabled = true; $("akkoord").disabled = true;
      canvas.style.pointerEvents = "none";
      toon(["BNW heeft uw ondertekende overeenkomst ontvangen. U hoeft niets meer te doen.", "Een kopie is opgeslagen bij uw downloads als " + naam + "."], "Uw overeenkomst is ondertekend en verstuurd.", false);
      $("kopie").hidden = false; download();
    }).catch(function (d) {
      klaar();
      if (d && d.fout === "ondertekend") { toonFout("ondertekend"); return; }
      if (d && d.fout === "verlopen") { toonFout("verlopen"); return; }
      toon(["Controleer uw internetverbinding en kies opnieuw \\u2018Onderteken en verstuur\\u2019. Lukt het niet, download dan uw kopie en mail die naar administratie@bnw.nl."], "Versturen naar BNW is niet gelukt.", true);
      $("kopie").hidden = false;
    });
  });
'''
START = '''/* ---------- start ---------- */
  $("datum").textContent = datumTekst(vandaag);
  $("coopnaam").textContent = DOC.coop;
  $("rol").textContent = DOC.rol;
  $("akkoord").addEventListener("change", function () { $("akkoordblok").classList.remove("fout"); });
  if (!TOKEN) { toonFout("ongeldig"); return; }
  $("formulier").hidden = true; $("laden").hidden = false;
  fetch("/api/links/" + TOKEN, { cache: "no-store" }).then(function (r) {
    return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw d; return d; });
  }).then(function (d) {
    V = d.gegevens; V.tot = d.verloopt;
    $("laden").hidden = true; $("formulier").hidden = false;
    $("geldig").textContent = "U kunt tot en met " + totTekst(V.tot) + " ondertekenen.";
    bouwAkte(); ververs(); maat();
    if (window.ResizeObserver) new ResizeObserver(maat).observe(canvas);
  }).catch(function (d) {
    $("laden").hidden = true;
    toonFout(d && d.fout === "verlopen" ? "verlopen" : d && d.fout === "ondertekend" ? "ondertekend" : "ongeldig");
  });
'''
for name, path in [('ledenovereenkomst-bnw', 'ledenovereenkomst'), ('kennismakersovereenkomst-bnw', 'kennismakersovereenkomst')]:
    s = open(f'{B}/{name}.html', encoding='utf-8').read()
    s = rep(s, 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js', '/jspdf.umd.min.js')
    s = rep(s, 'U controleert ze, leest de overeenkomst en zet uw handtekening. Daarna slaat u de ondertekende overeenkomst op als pdf.', 'U controleert ze, leest de overeenkomst en zet uw handtekening. BNW ontvangt de ondertekende overeenkomst daarna automatisch en u krijgt een kopie als pdf.')
    s = rep(s, '<li><b>3</b>Onderteken en sla op</li>', '<li><b>3</b>Onderteken en verstuur</li>')
    s = rep(s, '<button type="submit" id="verstuur">Onderteken en sla op als pdf</button>', '<button type="submit" id="verstuur">Onderteken en verstuur</button>')
    s = rep(s, '<div class="status" id="status" role="status" aria-live="polite" hidden></div>', '<div class="status" id="status" role="status" aria-live="polite" hidden></div>\n        <div class="rij"><button type="button" class="stil" id="kopie" hidden>Download uw kopie</button></div>')
    s = rep(s, 'toon(["Uw pdf wordt gemaakt. Bevestig daarna het opslaan."], null, false);', 'toon(["Uw overeenkomst wordt verstuurd naar BNW. Een moment."], null, false);')
    s = rep(s, '  <form id="formulier" novalidate>', '''  <div class="status" id="ondertekend" hidden>
    <strong>Deze overeenkomst is al ondertekend.</strong>
    <span>BNW heeft de ondertekende overeenkomst ontvangen. Heeft u vragen, mail dan naar <b class="mail">administratie@bnw.nl</b>.</span>
  </div>
  <p class="hulp" id="laden" hidden>Uw gegevens worden opgehaald.</p>

  <form id="formulier" novalidate>''')
    s = rep(s, 'Een ondertekenlink is vijf werkdagen geldig.', 'Een ondertekenlink is vijf werkdagen geldig en werkt één keer.')
    s = cut(s, '/* ---------- waarden ---------- */', '  var vandaag', LEES)
    s = rep(s, '    if (verlopen()) { $("formulier").hidden = true; $("verlopen").hidden = false; $("verlopen").scrollIntoView({ block: "center" }); return; }\n', '')
    s = cut(s, '    opslaan.then(function (dl) {', '  function klaar()', VERSTUUR)
    s = rep(s, '  var opslaan = (window.claude && window.claude.use) ? window.claude.use("downloads") : Promise.resolve(null);\n', '')
    s = cut(s, '/* ---------- start ---------- */', '  window.__bnwTest', START)
    assert 'leesCode' not in s and 'verlopen()' not in s
    os.makedirs(f'{OUT}/{path}'); open(f'{OUT}/{path}/index.html', 'w', encoding='utf-8').write(HEAD + s + FOOT)

p = open(f'{B}/bnw-ondertekenlinks.html', encoding='utf-8').read()
p = cut(p, '    <details>', '    </details>\n', '''    <section aria-labelledby="k0">
      <h2 id="k0">Toegang</h2>
      <div class="veld"><label class="l" for="sleutel">Sleutel van BNW</label><input type="password" id="sleutel" autocomplete="off" placeholder="Zonder sleutel kan geen link worden gemaakt">
      <span class="hulp">De sleutel wordt op deze computer onthouden. Vraag hem aan de beheerder van de site.</span></div>
    </section>
''')
p = rep(p, 'input[type=text], textarea {', 'input[type=text], input[type=password], textarea {')
p = rep(p, '''  var $ = function (id) { return document.getElementById(id); };''', '''  var $ = function (id) { return document.getElementById(id); };
  try { $("sleutel").value = localStorage.getItem("bnw-sleutel") || ""; } catch (e) {}
  $("sleutel").addEventListener("change", function () { try { localStorage.setItem("bnw-sleutel", $("sleutel").value.trim()); } catch (e) {} });''')
p = cut(p, '  /* De gegevens gaan als code achter het # in de link', '  $("formulier").addEventListener("submit"', '''  var DAGEN = ["zondag", "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag"];
  var MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"];
  function melding(t) { $("fout").textContent = t; $("fout").hidden = !t; }
''')
p = cut(p, '    var soort = document.querySelector("input[name=soort]:checked").value;', '  $("kopieer").addEventListener', '''    var soort = document.querySelector("input[name=soort]:checked").value;
    var sleutel = $("sleutel").value.trim();
    if (!sleutel) { melding("Vul eerst de sleutel van BNW in."); $("sleutel").focus(); return; }
    melding(""); $("uit").hidden = true; $("maak").disabled = true;
    fetch("/api/links", { method: "POST", headers: { "content-type": "application/json", "x-bnw-sleutel": sleutel }, body: JSON.stringify({ soort: soort, gegevens: v }) })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (d) { if (!r.ok) throw d; return d; }); })
      .then(function (d) {
        var tot = new Date(d.verloopt + "T12:00:00");
        $("geldig").textContent = "Geldig tot en met " + DAGEN[tot.getDay()] + " " + tot.getDate() + " " + MAANDEN[tot.getMonth()] + " " + tot.getFullYear() + " (vijf werkdagen) en werkt \\u00e9\\u00e9n keer. Daarna toont de link alleen dat hij verlopen of al gebruikt is.";
        $("link").value = d.url; $("open").href = d.url;
        $("voorwie").textContent = NAAM[soort] + " voor " + v.praktijk;
        $("gekopieerd").textContent = ""; $("uit").hidden = false; $("uit").scrollIntoView({ block: "nearest" });
      }).catch(function (d) {
        if (d && d.fout === "sleutel") melding("De sleutel is onjuist. Controleer hem bij de beheerder van de site.");
        else if (d && d.fout === "veld") melding("Een van de gegevens is niet geaccepteerd. Controleer de invoer.");
        else melding("De link kon niet worden gemaakt. Controleer uw internetverbinding en probeer het opnieuw.");
      }).finally(function () { $("maak").disabled = false; });
  });
''')
p = rep(p, '<button type="submit">Maak link</button>', '<button type="submit" id="maak">Maak link</button>\n        <span class="melding" id="fout" hidden></span>')
assert 'code(v' not in p and 'basis-' not in p
os.makedirs(f'{OUT}/{INTERN}'); open(f'{OUT}/{INTERN}/index.html', 'w', encoding='utf-8').write(HEAD + p + FOOT)

logo = p[p.index('src="data:image/png') + 5:]; logo = logo[:logo.index('"')]
open(f'{OUT}/index.html', 'w', encoding='utf-8').write(HEAD + '''<title>BNW Ondertekenen</title>
<style>body{font:400 16px/1.5 Arial,Helvetica,sans-serif;color:#52525E;background:#fff;padding:32px 20px}main{max-width:640px;margin:0 auto;display:flex;flex-direction:column;gap:20px}h1{font-size:26px;font-weight:900;text-transform:uppercase;color:#0444A3;margin:0}p{margin:0}b{color:#0444A3}</style>
<main><img src="''' + logo + '''" alt="BNW beweegt de zorg" style="width:240px">
<h1>Overeenkomst ondertekenen</h1>
<p>Op deze site ondertekent u een overeenkomst met BNW via een persoonlijke link. Open de link die u van BNW per e-mail heeft ontvangen.</p>
<p>Heeft u geen link of werkt hij niet? Mail naar <b>administratie@bnw.nl</b>.</p></main>''' + FOOT)
open(f'{OUT}/__forms.html', 'w', encoding='utf-8').write('''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Formulier</title></head><body>
<form name="ondertekening" method="POST" data-netlify="true" netlify-honeypot="bot-field" hidden>
  <input type="hidden" name="subject" value="Ondertekende overeenkomst BNW (%{submissionId})">
  <input name="bot-field">
  <input type="text" name="praktijk">
  <input type="text" name="overeenkomst">
  <input type="text" name="adres">
  <input type="text" name="kvk">
  <input type="text" name="agb">
  <input type="text" name="naam">
  <input type="text" name="ondertekend_op">
  <input type="text" name="ip">
  <input type="text" name="user_agent">
  <input type="text" name="pdf_link">
  <input type="text" name="token">
  <input type="file" name="pdf" hidden>
</form></body></html>''')
shutil.copy(f'{B}/jspdf.umd.min.js', f'{OUT}/jspdf.umd.min.js')
print('gebouwd:', sorted(os.listdir(OUT)))
