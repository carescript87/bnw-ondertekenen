import type { Config, Context } from "@netlify/functions";
import { SOORTEN, type Link, links, inzendingen, json, token, geldigToken, isVerlopen } from "./_gedeeld.mts";

const MAX_PDF = 4 * 1024 * 1024;

export default async (req: Request, context: Context) => {
  const t = context.params.token;
  if (!geldigToken(t)) return json({ fout: "ongeldig" }, 404);
  const store = links();
  const l = (await store.get(t, { type: "json" })) as Link | null;
  if (!l) return json({ fout: "ongeldig" }, 404);
  if (l.ondertekend) return json({ fout: "ondertekend" }, 409);
  if (isVerlopen(l)) return json({ fout: "verlopen" }, 410);

  let form: FormData;
  try { form = await req.formData(); } catch { return json({ fout: "ongeldig" }, 400); }
  const pdf = form.get("pdf");
  if (!(pdf instanceof File) || pdf.size < 1000 || pdf.size > MAX_PDF) return json({ fout: "pdf" }, 400);
  const kop = new Uint8Array(await pdf.slice(0, 5).arrayBuffer());
  if (String.fromCharCode(...kop) !== "%PDF-") return json({ fout: "pdf" }, 400);
  if (form.get("akkoord") !== "ja") return json({ fout: "akkoord" }, 400);

  const nu = new Date();
  const ip = context.ip || req.headers.get("x-nf-client-connection-ip") || "";
  const ua = (req.headers.get("user-agent") || "").slice(0, 300);
  const sleutel = token(18);
  const g = l.gegevens;
  const meta = {
    token: t, soort: l.soort, overeenkomst: SOORTEN[l.soort], gegevens: g,
    ondertekend_op: nu.toISOString(), ip, user_agent: ua, pdf_sleutel: sleutel, pdf_bytes: pdf.size,
    link_aangemaakt: l.aangemaakt, link_verloopt: l.verloopt,
  };
  const inz = inzendingen();
  await inz.set(`${t}.pdf`, pdf, { metadata: { ondertekend_op: meta.ondertekend_op } });
  await inz.setJSON(`${t}.json`, meta);
  await store.setJSON(t, { ...l, ondertekend: meta.ondertekend_op });

  const origin = new URL(req.url).origin;
  const pdfLink = `${origin}/api/pdf/${t}?s=${sleutel}`;
  const tijd = new Intl.DateTimeFormat("nl-NL", { dateStyle: "long", timeStyle: "short", timeZone: "Europe/Amsterdam" }).format(nu);
  const velden = new URLSearchParams({
    "form-name": "ondertekening", "bot-field": "",
    praktijk: g.praktijk, overeenkomst: SOORTEN[l.soort],
    adres: `${g.straat}, ${g.postcode} ${g.plaats}`, kvk: g.kvk, agb: g.agb, naam: g.naam,
    ondertekend_op: tijd, ip_ondertekenaar: ip, browser_ondertekenaar: ua, pdf_link: pdfLink, token: t,
  });
  try {
    const r = await fetch(`${origin}/__forms.html`, { method: "POST", headers: { "content-type": "application/x-www-form-urlencoded" }, body: velden.toString() });
    if (!r.ok) console.error(`formulier-melding mislukt: ${r.status}`);
  } catch (e) { console.error("formulier-melding mislukt", e); }

  console.log(`ondertekend token=${t} soort=${l.soort} ip=${ip}`);
  return json({ ok: true, ondertekend_op: meta.ondertekend_op });
};

export const config: Config = { path: "/api/onderteken/:token", method: "POST" };
