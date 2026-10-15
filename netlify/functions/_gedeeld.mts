import { getStore } from "@netlify/blobs";

export const SOORTEN: Record<string, string> = {
  led: "Ledenovereenkomst",
  ken: "Kennismakersovereenkomst",
};
export const VELDEN = ["praktijk", "straat", "postcode", "plaats", "kvk", "agb", "naam"] as const;
export type Gegevens = Record<(typeof VELDEN)[number], string>;

export interface Link {
  soort: string;
  gegevens: Gegevens;
  aangemaakt: string;   // ISO-tijd
  verloopt: string;     // JJJJ-MM-DD, laatste geldige dag (Nederlandse tijd)
  ondertekend: string | null; // ISO-tijd zodra ondertekend
}

export const links = () => getStore({ name: "links", consistency: "strong" });
export const inzendingen = () => getStore({ name: "inzendingen", consistency: "strong" });

export const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });

export const token = (bytes = 24) => {
  const b = new Uint8Array(bytes);
  crypto.getRandomValues(b);
  return Buffer.from(b).toString("base64url");
};

const TOKEN_RE = /^[A-Za-z0-9_-]{20,64}$/;
export const geldigToken = (t: string | undefined): t is string => !!t && TOKEN_RE.test(t);

/** Datum in Nederland als JJJJ-MM-DD. */
export const nlDatum = (d = new Date()) =>
  new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Amsterdam" }).format(d);

/** Vandaag plus n werkdagen (zaterdag en zondag tellen niet mee). */
export const plusWerkdagen = (n: number) => {
  const d = new Date(nlDatum() + "T12:00:00Z");
  let k = 0;
  while (k < n) {
    d.setUTCDate(d.getUTCDate() + 1);
    if (d.getUTCDay() !== 0 && d.getUTCDay() !== 6) k++;
  }
  return d.toISOString().slice(0, 10);
};

export const isVerlopen = (l: Link) => nlDatum() > l.verloopt;

/** Vergelijkt twee strings in constante tijd. */
export const gelijk = (a: string, b: string) => {
  const x = Buffer.from(a), y = Buffer.from(b);
  if (x.length !== y.length) return false;
  let r = 0;
  for (let i = 0; i < x.length; i++) r |= x[i] ^ y[i];
  return r === 0;
};
