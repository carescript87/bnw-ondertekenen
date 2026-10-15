import type { Config, Context } from "@netlify/functions";
import { inzendingen, geldigToken, gelijk } from "./_gedeeld.mts";

export default async (req: Request, context: Context) => {
  const t = context.params.token;
  const s = new URL(req.url).searchParams.get("s") ?? "";
  if (!geldigToken(t) || !geldigToken(s)) return new Response("Niet gevonden", { status: 404 });
  const inz = inzendingen();
  const meta = (await inz.get(`${t}.json`, { type: "json" })) as any;
  if (!meta || !gelijk(String(meta.pdf_sleutel), s)) return new Response("Niet gevonden", { status: 404 });
  const pdf = await inz.get(`${t}.pdf`, { type: "arrayBuffer" });
  if (!pdf) return new Response("Niet gevonden", { status: 404 });
  const naam = `${meta.soort === "led" ? "ledenovereenkomst" : "kennismakersovereenkomst"}-bnw-${String(meta.gegevens.praktijk).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 50) || "praktijk"}.pdf`;
  return new Response(pdf, { headers: { "content-type": "application/pdf", "content-disposition": `inline; filename="${naam}"`, "cache-control": "private, no-store", "x-robots-tag": "noindex" } });
};

export const config: Config = { path: "/api/pdf/:token", method: "GET" };
