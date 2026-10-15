import type { Config, Context } from "@netlify/functions";
import { type Link, links, inzendingen, nlDatum } from "./_gedeeld.mts";

/* Draait elke nacht om 03:00 Nederlandse wintertijd (02:00 UTC).
   - Links: weg zodra ze verlopen of ondertekend zijn en LINK_BEWAREN_DAGEN voorbij is.
   - Inzendingen (pdf + metadata): weg na BEWAARTERMIJN_DAGEN.
   - Formulierinzendingen bij Netlify: weg na BEWAARTERMIJN_DAGEN, alleen als NETLIFY_API_TOKEN is gezet. */

const dagen = (naam: string, standaard: number) => {
  const n = Number(Netlify.env.get(naam));
  return Number.isFinite(n) && n > 0 ? n : standaard;
};
const ouderDan = (iso: string, d: number) => Date.now() - Date.parse(iso) > d * 86400e3;

export default async (_req: Request, context: Context) => {
  const bewaar = dagen("BEWAARTERMIJN_DAGEN", 30), linkDagen = dagen("LINK_BEWAREN_DAGEN", 2);
  let l = 0, i = 0, f = 0;

  const ls = links();
  for (const { key } of (await ls.list()).blobs) {
    const link = (await ls.get(key, { type: "json" })) as Link | null;
    if (!link) continue;
    const verlopenOp = link.verloopt + "T23:59:59+02:00";
    const klaar = link.ondertekend ? ouderDan(link.ondertekend, linkDagen) : ouderDan(verlopenOp, linkDagen);
    if (klaar) { await ls.delete(key); l++; }
  }

  const inz = inzendingen();
  for (const { key } of (await inz.list()).blobs) {
    if (!key.endsWith(".json")) continue;
    const meta = (await inz.get(key, { type: "json" })) as any;
    if (meta?.ondertekend_op && ouderDan(meta.ondertekend_op, bewaar)) {
      await inz.delete(key.replace(/\.json$/, ".pdf"));
      await inz.delete(key);
      i++;
    }
  }

  const apiToken = Netlify.env.get("NETLIFY_API_TOKEN");
  if (apiToken) {
    const kop = { authorization: `Bearer ${apiToken}` };
    const forms = await (await fetch(`https://api.netlify.com/api/v1/sites/${context.site.id}/forms`, { headers: kop })).json();
    for (const form of forms as any[]) {
      if (form.name !== "ondertekening") continue;
      for (const state of ["verified", "spam"]) {
        const subs = await (await fetch(`https://api.netlify.com/api/v1/forms/${form.id}/submissions?state=${state}&per_page=100`, { headers: kop })).json();
        for (const s of subs as any[]) {
          if (ouderDan(s.created_at, bewaar)) {
            const r = await fetch(`https://api.netlify.com/api/v1/submissions/${s.id}`, { method: "DELETE", headers: kop });
            if (r.ok) f++;
          }
        }
      }
    }
  }
  console.log(`opschonen ${nlDatum()}: links=${l} inzendingen=${i} formulierinzendingen=${f} (termijn ${bewaar} dagen${apiToken ? "" : ", geen API-token: formulierinzendingen overgeslagen"})`);
};

export const config: Config = { schedule: "0 2 * * *" };
