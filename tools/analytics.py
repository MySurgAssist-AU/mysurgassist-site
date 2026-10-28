#!/usr/bin/env python3
"""Cloudflare Web Analytics for mysurgassist.com.au.

Puts the Cloudflare beacon at the end of <body> on every real page (the
redirect stubs are skipped) and keeps the privacy policy's analytics
paragraph in place. Safe to run again: the marked block is replaced, never
duplicated. The beacon sits in the body, so tools/seo.py never touches it.

Run from the repo root:  python3 tools/analytics.py
To change the token, edit TOKEN below and run it again.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Site token from Cloudflare dashboard > Web Analytics > mysurgassist.com.au
TOKEN = "9ec1b4095fed4151aa0266d449f87ad0"

# Meta refresh stubs for old Squarespace URLs. Counting them adds nothing.
SKIP = {
    "about/index.html",
    "contact-us/index.html",
    "home/index.html",
    "myvirtualsurgery/index.html",
    "news/index.html",
}

START = "<!-- analytics: cloudflare -->"
END = "<!-- /analytics -->"
BEACON = (
    START
    + "<script type='module' src='https://static.cloudflareinsights.com/beacon.min.js' "
    + "data-cf-beacon='{\"token\": \"" + TOKEN + "\"}'></script>"
    + END
)

PRIVACY_FILE = "privacy-policy/index.html"
PRIVACY_START = "<!-- privacy: analytics -->"
PRIVACY_END = "<!-- /privacy: analytics -->"
PRIVACY_ANCHOR = "website's functionality may be affected.</p>"
PRIVACY_P = (
    PRIVACY_START
    + '<p style="margin: 0; font-size: 15.5px; line-height: 1.75; '
    + 'color: rgba(255,255,255,0.78);">We use Cloudflare Web Analytics to count '
    + "visits to this website. It does not use cookies, does not collect personal "
    + "information and does not follow you across other websites. It records "
    + "anonymous details such as the pages viewed, the type of browser and device, "
    + "and the country a visit comes from. Cloudflare processes this information "
    + "on our behalf and it may be handled outside Australia.</p>"
    + PRIVACY_END
)

BLOCK_RE = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
PRIV_RE = re.compile(re.escape(PRIVACY_START) + ".*?" + re.escape(PRIVACY_END), re.S)


def pages():
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith((".git/", "tools/")) or rel in SKIP:
            continue
        if re.fullmatch(r"google[0-9a-f]+\.html", rel):
            continue
        yield p, rel


def main():
    if "REPLACE" in TOKEN:
        raise SystemExit("Set TOKEN first.")
    done = []
    for p, rel in pages():
        t = p.read_text(encoding="utf-8")
        t = BLOCK_RE.sub("", t)
        if t.count("</body>") != 1:
            raise SystemExit(f"{rel}: expected one </body>")
        t = t.replace("</body>", BEACON + "</body>")
        if rel == PRIVACY_FILE:
            t = PRIV_RE.sub("", t)
            if t.count(PRIVACY_ANCHOR) != 1:
                raise SystemExit("privacy policy anchor not found")
            t = t.replace(PRIVACY_ANCHOR, PRIVACY_ANCHOR + PRIVACY_P)
        p.write_text(t, encoding="utf-8")
        done.append(rel)
    print(f"Beacon on {len(done)} pages:")
    for r in done:
        print("  " + r)


if __name__ == "__main__":
    main()
