#!/usr/bin/env python3
"""SEO pass for mysurgassist.com.au.

Rewrites title, meta description and og tags per page, adds JSON-LD
(Organization, LocalBusiness, WebSite, Service, FAQPage) and fixes the
duplicate H1 on the homepage. Copy in the body is never touched.

Run from the repo root:  python3 tools/seo.py
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.mysurgassist.com.au"
TODAY = date.today().isoformat()

ORG_ID = SITE + "/#organization"
BIZ_ID = SITE + "/#localbusiness"

# Title and description per page. Written for the search query, not as taglines.
PAGES = {
    "index.html": {
        "title": "MySurgAssist | Surgical Assistant Recruitment and Billing, Australia",
        "desc": "Surgical assistant recruitment and surgical billing across Australia, run by surgical assistants. Surgeons post lists, assistants apply, and every case is billed and paid fortnightly through the app.",
    },
    "billing/index.html": {
        "title": "Surgical Billing Service for Surgical Assistants and Surgeons | MySurgAssist",
        "desc": "Surgical billing service in Australia. MySurgAssist bills every case for surgical assistants at 5% plus GST, whether or not the list came through us, and runs comprehensive practice billing for surgeons at 2% plus GST. Paid fortnightly.",
    },
    "assistants/index.html": {
        "title": "Surgical Assistant Jobs and Billing in Australia | MySurgAssist",
        "desc": "Find surgical assisting lists across Australia and get paid fortnightly. Already assisting? MySurgAssist bills your existing work too, at 5% plus GST, whether or not the list came through us.",
    },
    "surgeons/index.html": {
        "title": "Find a Surgical Assistant for Your List | MySurgAssist",
        "desc": "Post a list and MySurgAssist finds you a credentialled surgical assistant, free for surgeons and practices. Over 400 assistants across Australia, plus a surgical billing service for your practice at 2% plus GST.",
    },
    "patients/index.html": {
        "title": "Surgical Assistant Invoices for Patients | MySurgAssist",
        "desc": "A surgical assistant was part of your operation and MySurgAssist bills on their behalf. What the invoice is, how to pay it by bank transfer, and who to contact about a claim.",
    },
    "team/index.html": {
        "title": "Our Team | MySurgAssist",
        "desc": "The surgical assistants, billers and builders behind MySurgAssist, Australia's surgical assistant recruitment and billing network, based in Camperdown NSW.",
    },
    "network/index.html": {
        "title": "Our Network | MySurgAssist",
        "desc": "The surgical colleges, societies and associations MySurgAssist sponsors, and the medical technology partners it works with, across Australia.",
    },
    "resources/index.html": {
        "title": "Surgical Assistant Resources and Guides | MySurgAssist",
        "desc": "Guides for surgical assistants: how to submit billing, how and when you get paid, and the MySurgAssist loyalty programme.",
    },
    "resources/submitting-billing/index.html": {
        "title": "How to Submit Surgical Assistant Billing | MySurgAssist",
        "desc": "What MySurgAssist needs to bill a surgical assistant case, where to find it in the theatre paperwork, and how to send it in through the app.",
    },
    "resources/how-you-get-paid/index.html": {
        "title": "How Surgical Assistants Get Paid | MySurgAssist",
        "desc": "The MySurgAssist payment cycle for surgical assistants: cut off dates, processing, fortnightly disbursement and when the money lands.",
    },
    "privacy-policy/index.html": {
        "title": "Privacy Policy | MySurgAssist",
        "desc": "How MySurgAssist collects, holds, uses and discloses personal information.",
    },
}

ORGANIZATION = {
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "MySurgAssist",
    "legalName": "MySurgAssist Pty Ltd",
    "url": SITE + "/",
    "logo": SITE + "/assets/lockup.png",
    "image": SITE + "/assets/og.png",
    "foundingDate": "2023",
    "description": "Surgical assistant recruitment and surgical billing across Australia, run by surgical assistants.",
    "email": "admin@mysurgassist.com.au",
    "telephone": "+61 461 551 303",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "8/1 Barr Street",
        "addressLocality": "Camperdown",
        "addressRegion": "NSW",
        "postalCode": "2050",
        "addressCountry": "AU",
    },
    "areaServed": {"@type": "Country", "name": "Australia"},
    "sameAs": [
        "https://instagram.com/mysurgassist",
        "https://linkedin.com/company/mysurgassist",
        "https://apps.apple.com/au/app/mysurgassist/id6483004432",
        "https://play.google.com/store/apps/details?id=com.mysurgassist.app",
    ],
}

LOCAL_BUSINESS = {
    "@type": "LocalBusiness",
    "@id": BIZ_ID,
    "name": "MySurgAssist",
    "parentOrganization": {"@id": ORG_ID},
    "url": SITE + "/",
    "image": SITE + "/assets/og.png",
    "email": "admin@mysurgassist.com.au",
    "telephone": "+61 461 551 303",
    "priceRange": "5% plus GST of the assistant's fee; 2% plus GST of billings for surgeons",
    "address": ORGANIZATION["address"],
    "areaServed": {"@type": "Country", "name": "Australia"},
}

WEBSITE = {
    "@type": "WebSite",
    "@id": SITE + "/#website",
    "url": SITE + "/",
    "name": "MySurgAssist",
    "publisher": {"@id": ORG_ID},
    "inLanguage": "en-AU",
}

SERVICES = {
    "billing/index.html": [
        {
            "@type": "Service",
            "@id": SITE + "/billing/#assistant-billing",
            "name": "Surgical Billing Service for Surgical Assistants",
            "serviceType": "Surgical billing",
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "Country", "name": "Australia"},
            "audience": {"@type": "Audience", "audienceType": "Surgical assistants"},
            "description": "MySurgAssist bills every case a surgical assistant works, whether or not the list came through MySurgAssist: MBS and AMA item numbers, health funds, Medicare, WorkCover, CTP, hourly rates, precollected fees and known gap invoices. Paid fortnightly with quarterly and EOFY statements.",
            "offers": {
                "@type": "Offer",
                "description": "5% plus GST of the assistant's fee",
                "priceCurrency": "AUD",
            },
            "url": SITE + "/billing/",
        },
        {
            "@type": "Service",
            "@id": SITE + "/billing/#surgeon-billing",
            "name": "Surgical Billing Service for Surgeons",
            "serviceType": "Medical practice billing",
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "Country", "name": "Australia"},
            "audience": {"@type": "Audience", "audienceType": "Surgeons and surgical practices"},
            "description": "A comprehensive billing service for surgical practices: item numbers, health funds, Medicare and ECLIPSE, WorkCover and CTP, gap and known gap invoicing, chasing and reconciliation.",
            "offers": {
                "@type": "Offer",
                "description": "2% plus GST of billings",
                "priceCurrency": "AUD",
            },
            "url": SITE + "/billing/",
        },
    ],
    "surgeons/index.html": [
        {
            "@type": "Service",
            "@id": SITE + "/surgeons/#recruitment",
            "name": "Surgical Assistant Recruitment",
            "serviceType": "Surgical assistant recruitment",
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "Country", "name": "Australia"},
            "audience": {"@type": "Audience", "audienceType": "Surgeons and surgical practices"},
            "description": "Surgeons post a list in the MySurgAssist app, surgical assistants apply, and MySurgAssist selects the most suitable applicant and confirms hospital credentialling before the day.",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "AUD", "description": "Free for surgeons and practices"},
            "url": SITE + "/surgeons/",
        }
    ],
}

FAQ_PAT = re.compile(
    r'<div style="font-size: 15px; font-weight: 500; color: #ffffff;">(.*?)</div>'
    r'<p style="[^"]*">(.*?)</p>',
    re.S,
)


def text(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def faq_schema(page_html: str, url: str):
    pairs = FAQ_PAT.findall(page_html)
    if not pairs:
        return None
    return {
        "@type": "FAQPage",
        "@id": url + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": text(q),
                "acceptedAnswer": {"@type": "Answer", "text": text(a)},
            }
            for q, a in pairs
        ],
    }


def set_tag(h: str, pattern: str, replacement: str) -> str:
    new, n = re.subn(pattern, replacement, h, count=1)
    if n != 1:
        raise SystemExit(f"tag not found: {pattern}")
    return new


def attr(s: str) -> str:
    return html.escape(s, quote=True)


def process(rel: str, meta: dict) -> None:
    path = ROOT / rel
    h = path.read_text(encoding="utf-8")
    url = SITE + "/" + ("" if rel == "index.html" else rel.replace("index.html", ""))

    # head tags
    h = set_tag(h, r"<title>.*?</title>", f"<title>{html.escape(meta['title'])}</title>")
    h = set_tag(h, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{attr(meta["desc"])}">')
    h = set_tag(h, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{attr(meta["title"])}">')
    h = set_tag(h, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{attr(meta["desc"])}">')
    if 'property="og:locale"' not in h:
        h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="website">\n<meta property="og:locale" content="en_AU">', 1)
    if 'name="twitter:title"' not in h:
        h = h.replace(
            '<meta name="twitter:card" content="summary_large_image">',
            '<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{attr(meta["title"])}">\n'
            f'<meta name="twitter:description" content="{attr(meta["desc"])}">\n'
            f'<meta name="twitter:image" content="{SITE}/assets/og.png">',
            1,
        )
    else:
        h = set_tag(h, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{attr(meta["title"])}">')
        h = set_tag(h, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{attr(meta["desc"])}">')

    # structured data
    graph = [ORGANIZATION, LOCAL_BUSINESS]
    if rel == "index.html":
        graph.append(WEBSITE)
    graph.append({
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": meta["title"],
        "description": meta["desc"],
        "isPartOf": {"@id": SITE + "/#website"},
        "about": {"@id": ORG_ID},
        "inLanguage": "en-AU",
    })
    graph.extend(SERVICES.get(rel, []))
    faq = faq_schema(h, url)
    if faq:
        graph.append(faq)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=0)
    ld = ld.replace("</", "<\\/")
    block = f'<script type="application/ld+json">\n{ld}\n</script>'
    h = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", h, flags=re.S)
    h = h.replace("</head>", block + "\n</head>", 1)

    # homepage: one H1. The mobile hero repeats the wordmark; make it a div with the same styling.
    if rel == "index.html":
        h1s = list(re.finditer(r"<h1([^>]*)>(.*?)</h1>", h, re.S))
        if len(h1s) > 1:
            for m in reversed(h1s[1:]):
                h = h[: m.start()] + f"<div{m.group(1)}>{m.group(2)}</div>" + h[m.end():]

    path.write_text(h, encoding="utf-8")
    print(f"{rel:48s} {meta['title']}")


def sitemap() -> None:
    urls = ["/", "/assistants/", "/surgeons/", "/billing/", "/patients/", "/team/", "/network/",
            "/resources/", "/resources/submitting-billing/", "/resources/how-you-get-paid/", "/privacy-policy/"]
    prio = {"/": "1.0", "/billing/": "0.9", "/assistants/": "0.9", "/surgeons/": "0.9"}
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        out.append(f"<url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(u, '0.6')}</priority></url>")
    out.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(out), encoding="utf-8")
    print("sitemap.xml                                      rewritten")


if __name__ == "__main__":
    for rel, meta in PAGES.items():
        process(rel, meta)
    sitemap()
