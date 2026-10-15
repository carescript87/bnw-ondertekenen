import type { Config, Context } from "@netlify/functions";
import { SOORTEN, VELDEN, type Gegevens, links, json, token, plusWerkdagen, gelijk } from "./_gedeeld.mts";

const WERKDAGEN = 5;
const regels: Record<string, RegExp> = {
  praktijk: /^.{2,120}$/, straat: /^(?=.*\d).{3,120}$/, postcode: /^\d{4} [A-Z]{2}$/,
  plaats: /^.{2,80}$/, kvk: /^\d{8}$/, agb: /^\d{8}$/, naam: /^.{2,120}$/,
};

export default async (req: Request, context: Context) => {
  const sleutel = Netlify.env.get("INTERN_SLEUTEL") ?? "";
  const gegeven = req.headers.get("x-bnw-sleutel") ?? "";
  if (!sleutel || !gelijk(sleutel, gegeven)) return json({ fout: "sleutel" }, 401);

  let body: any;
  try { body = await req.json(); } catch { return json({ fout: "ongeldig" }, 400); }
  const soort = String(body?.soort ?? "");
  if (!SOORTEN[soort]) return json({ fout: "soort" }, 400);
  const g = {} as Gegevens;
  for (const k of VELDEN) {
    const w = String(body?.gegevens?.[k] ?? "").trim().replace(/\s+/g, " ");
    const v = k === "postcode" ? w.toUpperCase().replace(/^(\d{4})\s*([A-Z]{2})$/, "$1 $2") : w;
    if (!regels[k].test(v)) return json({ fout: "veld", veld: k }, 400);
    g[k] = v;
  }
  const t = token();
  const link = { soort, gegevens: g, aangemaakt: new Date().toISOString(), verloopt: plusWerkdagen(WERKDAGEN), ondertekend: null };
  await links().setJSON(t, link, { onlyIfNew: true });
  const pad = soort === "led" ? "ledenovereenkomst" : "kennismakersovereenkomst";
  const url = `${new URL(req.url).origin}/${pad}/#${t}`;
  console.log(`link gemaakt soort=${soort} verloopt=${link.verloopt} door=${context.ip}`);
  return json({ url, verloopt: link.verloopt });
};

export const config: Config = { path: "/api/links", method: "POST" };
