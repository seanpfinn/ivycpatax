"""Assemble index.html from template.html: route map SVG, FAQ, JSON-LD, brand mark."""
import json, os, html, urllib.parse
from logo import BARS, RED, bars_path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.environ.get("SITE", "https://ivycpatax.vercel.app/")

S = 2  # map scale: the mark's 219x200 box drawn at 2x
LINE_A = [(110, 145), (18, 145), (18, 18), (420, 18), (420, 145), (220, 145), (220, 332)]
LINE_B = [(374, 82), (156, 82), (156, 382), (282, 382), (282, 190)]
ST_A = [("1", 18, 82), ("2", 200, 18), ("3", 420, 82), ("4", 320, 145), ("5", 220, 332)]
ST_B = [("A", 374, 82), ("B", 156, 230), ("C", 219, 382), ("D", 282, 190)]

def poly_d(pts):
    return "M" + " L".join(f"{x} {y}" for x, y in pts)

def length(pts):
    return sum(abs(x2 - x1) + abs(y2 - y1) for (x1, y1), (x2, y2) in zip(pts, pts[1:]))

def dist_to(pts, px, py):
    d = 0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2):
            return d + abs(px - x1) + abs(py - y1)
        d += abs(x2 - x1) + abs(y2 - y1)
    return d

def map_svg():
    la, lb = length(LINE_A), length(LINE_B)
    out = ['<svg viewBox="-30 -30 500 446" aria-hidden="true" focusable="false">']
    out.append(f'<path class="ghost" d="{bars_path(BARS, 0, 0, S)}"/>')
    # start square (the red square of the logo) + label
    x, y, w, h = [v * S for v in RED]
    out.append(f'<g class="start"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/><text x="{x + w/2}" y="{y - 10}" text-anchor="middle">YOU</text></g>')
    for cls, pts, L, d0, pid in (("a", LINE_A, la, 1.0, "ra"), ("b", LINE_B, lb, 1.35, "rb")):
        d = poly_d(pts)
        out.append(f'<path class="rt-shadow" d="{d}" style="--len:{L+2};--d:{d0}s"/>')
        out.append(f'<path class="rt {cls}" id="{pid}" d="{d}" style="--len:{L+2};--d:{d0}s"/>')
    for cls, pts, L, d0, sts in (("a", LINE_A, la, 1.0, ST_A), ("b", LINE_B, lb, 1.35, ST_B)):
        for label, sx, sy in sts:
            frac = dist_to(pts, sx, sy) / L
            dl = d0 + 1.8 * frac + 0.05
            out.append(f'<g class="stn {cls}" data-s="{label}" style="--d:{dl:.2f}s"><circle cx="{sx}" cy="{sy}" r="16"/><text x="{sx}" y="{sy + 0.5}">{label}</text></g>')
    for pid, off in (("ra", 0.0), ("rb", 4.2)):
        out.append(f'<g class="train" data-path="{pid}" data-off="{off}" style="opacity:0"><rect x="-15" y="-7.5" width="30" height="15" rx="7.5"/><circle cx="-5" cy="0" r="2.4"/><circle cx="5" cy="0" r="2.4"/></g>')
    out.append("</svg>")
    return "\n".join(out)

FAQ = [
    ("Do you specialize in S-Corporations?",
     "Yes. S-Corporation tax planning, payroll compliance and reasonable compensation strategy are core areas of our work."),
    ("Do you only work with New York clients?",
     "No. We serve clients nationwide, in all 50 states, while keeping strong New York State tax expertise."),
    ("Do you provide tax planning or just tax preparation?",
     "Planning is built into how we work. We focus on strategy, not just filing. If you only need a return filed, our filing-only individual and business returns are available too."),
    ("Do you process payroll directly?",
     "Payroll is processed by a trusted third-party provider. We provide CPA oversight, reconciliation and compliance coordination."),
    ("Are tax reduction strategies legal?",
     "Yes. Legitimate tax reduction strategies are fully legal and compliant with IRS and state tax law. Every recommendation we make is documented and built to withstand IRS scrutiny. Tax reduction is different from tax evasion, which is illegal."),
    ("How long do I have to respond to an IRS notice?",
     "Most IRS notices state a specific due date, commonly 15 to 30 days. Missing it can add penalties and interest or cost you appeal rights, so send it to us as soon as it arrives."),
    ("Can I work with you in Chinese?",
     "Yes. Call or text our Chinese-speaking line at 718-801-8060, or reach us on WeChat at Ivycpatax. Our English line is 516-344-8065."),
]

def faq_html():
    return "\n".join(
        f'<details><summary>{html.escape(q)}<i aria-hidden="true"></i></summary><p>{html.escape(a)}</p></details>'
        for q, a in FAQ)

SERVICES = [
    ("Tax planning & strategy", "https://ivycpatax.com/en/tax-reduction/", 350, "MON"),
    ("Bookkeeping", "https://ivycpatax.com/en/bookkeeping/", 280, "MON"),
    ("Individual tax return", "https://ivycpatax.com/en/individual-tax/", 500, None),
    ("Business tax return", "https://ivycpatax.com/en/business-tax/", 1600, None),
    ("Payroll management", "https://ivycpatax.com/en/payroll-taxes/", None, None),
    ("IRS notice help & Offer in Compromise", "https://ivycpatax.com/en/irs-notice/", None, None),
    ("Business formation", "https://ivycpatax.com/en/business-formation/", None, None),
    ("Fractional CFO services", "https://ivycpatax.com/en/cfo-fractional-services-2/", None, None),
]

def jsonld():
    biz = SITE + "#business"
    offers = []
    for name, url, price, unit in SERVICES:
        o = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name, "url": url}}
        if price:
            ps = {"@type": "PriceSpecification", "minPrice": price, "priceCurrency": "USD"}
            if unit:
                ps = {"@type": "UnitPriceSpecification", "minPrice": price, "priceCurrency": "USD", "unitCode": unit}
            o["priceSpecification"] = ps
        offers.append(o)
    towns = ["Syosset", "Jericho", "Plainview", "Hicksville", "Woodbury", "Melville", "Oyster Bay", "Brookville",
             "Cold Spring Harbor", "East Norwich", "Laurel Hollow", "Muttontown", "Huntington"]
    g = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "#website", "url": SITE, "name": "Ivy Tax & Business",
         "alternateName": "安腾会计", "inLanguage": "en-US", "publisher": {"@id": biz}},
        {"@type": "WebPage", "@id": SITE + "#webpage", "url": SITE,
         "name": "Ivy Tax & Business · Long Island CPA for S-Corp & Business Tax Planning · Syosset, NY",
         "isPartOf": {"@id": SITE + "#website"}, "about": {"@id": biz},
         "primaryImageOfPage": {"@id": SITE + "#ogimage"}, "video": {"@id": SITE + "#ogvideo"}, "inLanguage": "en-US"},
        {"@type": "ImageObject", "@id": SITE + "#ogimage", "url": SITE + "og/og-image.jpg", "contentUrl": SITE + "og/og-image.jpg",
         "width": 1200, "height": 630, "caption": "The Ivy T mark drawn as a route map beside the headline Precision tax planning, profound savings."},
        {"@type": "VideoObject", "@id": SITE + "#ogvideo", "name": "Ivy Tax & Business · Precision tax planning, profound savings",
         "description": "The Ivy T mark draws itself as a route map: a compliance line and a strategy line, both starting with you.",
         "thumbnailUrl": SITE + "og/og-image.jpg", "contentUrl": SITE + "og/og-video.mp4", "uploadDate": "2026-11-24",
         "duration": "PT8S", "width": 1200, "height": 630},
        {"@type": ["AccountingService", "LocalBusiness"], "@id": biz, "name": "Ivy Tax & Business Inc.",
         "alternateName": ["Ivy Tax & Business", "安腾会计", "Ivy CPA Tax"], "url": SITE,
         "logo": SITE + "logo.svg", "image": SITE + "og/og-image.jpg",
         "slogan": "Precision Tax Planning, Profound Savings",
         "description": "CPA-led tax planning, S-Corporation strategy, bookkeeping, payroll oversight and IRS representation for business owners, real estate investors and high-income individuals.",
         "telephone": "+1-516-344-8065", "email": "info@ivycpatax.com",
         "contactPoint": [
             {"@type": "ContactPoint", "telephone": "+1-516-344-8065", "contactType": "customer service", "availableLanguage": ["English"]},
             {"@type": "ContactPoint", "telephone": "+1-718-801-8060", "contactType": "customer service", "availableLanguage": ["Chinese"]}],
         "address": {"@type": "PostalAddress", "streetAddress": "6800 Jericho Tpke, Suite 120W", "addressLocality": "Syosset",
                     "addressRegion": "NY", "postalCode": "11791", "addressCountry": "US"},
         "hasMap": "https://www.google.com/maps/search/?api=1&query=6800+Jericho+Tpke+Suite+120W+Syosset+NY+11791",
         "knowsLanguage": ["en", "zh"],
         "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ["Nassau County, NY", "Suffolk County, NY", "New York City", "United States"]]
                       + [{"@type": "City", "name": t + ", NY"} for t in towns],
         "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Tax and accounting services", "itemListElement": offers},
         "sameAs": ["https://www.facebook.com/ivycpatax", "https://www.instagram.com/ivytaxbusiness/",
                    "https://www.linkedin.com/company/ivy-tax-business-inc"]},
        {"@type": "FAQPage", "@id": SITE + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    s = json.dumps(g, ensure_ascii=False, separators=(",", ":"))
    json.loads(s)
    return s.replace("</", "<\\/")

if __name__ == "__main__":
    t = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    zh = "安腾会计中文我们说网站微信收到了谢"
    rep = {
        "{{SITE}}": SITE,
        "{{MARK}}": bars_path(BARS),
        "{{RED}}": bars_path([RED]),
        "{{MAPSVG}}": map_svg(),
        "{{FAQHTML}}": faq_html(),
        "{{JSONLD}}": jsonld(),
        "{{ZHTEXT}}": urllib.parse.quote("".join(dict.fromkeys(zh))),
    }
    for k, v in rep.items():
        assert k in t, k
        t = t.replace(k, v)
    assert "{{" not in t
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(t)
    print("built", len(t))
