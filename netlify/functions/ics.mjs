// Calendar file for one Swansea Family Events date. Website only (added 30 October 2026).
// Apple Calendar and Samsung Calendar open a real text/calendar URL directly, which a page cannot do on its own.
//
// Query: title, d YYYY-MM-DD, s/e HHMM (only when the organiser published one clear start and finish),
//        r HHMM published start for the "2 hours before" reminder on an all day entry, loc, desc, url,
//        eve=1 adds a reminder at 6pm the evening before.
// Times are UK local and are converted to UTC here.

const clip = (v, n) => String(v || "").slice(0, n);
const esc = (v) => String(v).replace(/\\/g, "\\\\").replace(/;/g, "\\;").replace(/,/g, "\\,").replace(/\r?\n/g, "\\n");
const pad = (n) => String(n).padStart(2, "0");

// Offset of Europe/London from UTC, in minutes, at a given UTC instant.
function londonOffset(utcMs) {
  const parts = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/London", hourCycle: "h23",
    year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" }).formatToParts(new Date(utcMs));
  const g = (k) => +parts.find((p) => p.type === k).value;
  return (Date.UTC(g("year"), g("month") - 1, g("day"), g("hour"), g("minute")) - utcMs) / 60000;
}
// UK local date and time to a UTC Date.
function london(dateStr, hh, mm) {
  const [y, m, d] = dateStr.split("-").map(Number);
  const guess = Date.UTC(y, m - 1, d, hh, mm);
  return new Date(guess - londonOffset(guess) * 60000);
}
const stamp = (dt) => dt.getUTCFullYear() + pad(dt.getUTCMonth() + 1) + pad(dt.getUTCDate()) + "T" +
  pad(dt.getUTCHours()) + pad(dt.getUTCMinutes()) + "00Z";
const ymd = (s) => s.replace(/-/g, "");
function nextDay(s) { const [y, m, d] = s.split("-").map(Number); const x = new Date(Date.UTC(y, m - 1, d + 1));
  return x.getUTCFullYear() + "-" + pad(x.getUTCMonth() + 1) + "-" + pad(x.getUTCDate()); }
function prevDay(s) { const [y, m, d] = s.split("-").map(Number); const x = new Date(Date.UTC(y, m - 1, d - 1));
  return x.getUTCFullYear() + "-" + pad(x.getUTCMonth() + 1) + "-" + pad(x.getUTCDate()); }
// Lines longer than 75 octets are folded, as the calendar format requires.
function fold(line) {
  const out = []; let cur = "", bytes = 0;
  for (const ch of line) {
    const b = Buffer.byteLength(ch);
    if (bytes + b > (out.length ? 74 : 75)) { out.push(cur); cur = ""; bytes = 0; }
    cur += ch; bytes += b;
  }
  out.push(cur);
  return out.join("\r\n ");
}
const hhmm = (v) => (/^\d{4}$/.test(v || "") && +v.slice(0, 2) < 24 && +v.slice(2) < 60 ? [+v.slice(0, 2), +v.slice(2)] : null);

export default async (req) => {
  const q = new URL(req.url).searchParams;
  const d = q.get("d") || "";
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) return new Response("Missing or invalid date", { status: 400 });
  const title = clip(q.get("title"), 200) || "Family event";
  const loc = clip(q.get("loc"), 300), desc = clip(q.get("desc"), 2000);
  const url = /^https:\/\//.test(q.get("url") || "") ? clip(q.get("url"), 500) : "";
  const s = hhmm(q.get("s")), e = hhmm(q.get("e")), r = hhmm(q.get("r"));
  const timed = s && e && (e[0] * 60 + e[1] > s[0] * 60 + s[1]);

  const L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Swansea Family Events//EN", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    "BEGIN:VEVENT",
    "UID:" + ymd(d) + "-" + Math.abs([...title].reduce((h, c) => (h * 31 + c.charCodeAt(0)) | 0, 7)) + "@swansea-family-events.netlify.app",
    "DTSTAMP:" + stamp(new Date())];
  if (timed) {
    L.push("DTSTART:" + stamp(london(d, s[0], s[1])), "DTEND:" + stamp(london(d, e[0], e[1])));
  } else {
    L.push("DTSTART;VALUE=DATE:" + ymd(d), "DTEND;VALUE=DATE:" + ymd(nextDay(d)), "TRANSP:TRANSPARENT");
  }
  L.push("SUMMARY:" + esc(title));
  if (loc) L.push("LOCATION:" + esc(loc));
  if (desc) L.push("DESCRIPTION:" + esc(desc));
  if (url) L.push("URL:" + url);
  if (q.get("eve") === "1") {
    L.push("BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc("Tomorrow: " + title),
      "TRIGGER;VALUE=DATE-TIME:" + stamp(london(prevDay(d), 18, 0)), "END:VALARM");
  }
  const start = timed ? s : r;
  if (start) {
    const at = new Date(london(d, start[0], start[1]).getTime() - 2 * 3600000);
    L.push("BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc("In 2 hours: " + title),
      "TRIGGER;VALUE=DATE-TIME:" + stamp(at), "END:VALARM");
  }
  L.push("END:VEVENT", "END:VCALENDAR");

  const body = L.map(fold).join("\r\n") + "\r\n";
  const name = (title.replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60) || "event") + ".ics";
  return new Response(body, { headers: {
    "Content-Type": "text/calendar; charset=utf-8",
    "Content-Disposition": 'inline; filename="' + name + '"',
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff" } });
};
