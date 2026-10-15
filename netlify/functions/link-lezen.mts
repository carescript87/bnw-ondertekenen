import type { Config, Context } from "@netlify/functions";
import { SOORTEN, type Link, links, json, geldigToken, isVerlopen } from "./_gedeeld.mts";

export default async (_req: Request, context: Context) => {
  const t = context.params.token;
  if (!geldigToken(t)) return json({ fout: "ongeldig" }, 404);
  const l = (await links().get(t, { type: "json" })) as Link | null;
  if (!l) return json({ fout: "ongeldig" }, 404);
  if (l.ondertekend) return json({ fout: "ondertekend", op: l.ondertekend }, 409);
  if (isVerlopen(l)) return json({ fout: "verlopen", verloopt: l.verloopt }, 410);
  return json({ soort: l.soort, naam: SOORTEN[l.soort], gegevens: l.gegevens, verloopt: l.verloopt });
};

export const config: Config = { path: "/api/links/:token", method: "GET" };
