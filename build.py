#!/usr/bin/env python3
"""Builds the static pages for almoraconstruction.com.

Edit page bodies in src/pages/*.html, shared bits below, then run:
    python3 build.py
Each src page starts with a JSON block between <!--meta and -->.
Output goes to the repo root (index.html, adus/index.html, ...), which GitHub Pages serves.
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://almoraconstruction.com"

BIZ = {
    "name": "Almora Construction",
    "phone": "(747) 368-1225",
    "tel": "+17473681225",
    "email": "almoraconstruction@gmail.com",
    "street": "10727 White Oak Ave, Unit 205",
    "city": "Granada Hills", "state": "CA", "zip": "91344",
    "license": "1159801",
    "hours": "Mon to Sat, 7am to 5pm",  # TODO confirm with owner
}

NAV = [  # (path, label, menu note)
    ("/adus/", "ADUs", "Backyard units"),
    ("/services/", "Services", "Everything we build"),
    ("/projects/", "Projects", "Past jobs"),
    ("/about/", "About", "Who we are"),
    ("/contact/", "Contact", "Free estimate"),
]

SERVICES = [  # (path, title, one line)
    ("/adus/", "ADUs", "Backyard units and garage conversions, from plans to final inspection."),
    ("/new-construction/", "New construction", "Custom homes, built from the ground up."),
    ("/remodeling/", "Remodeling", "Kitchens, bathrooms, additions and whole homes."),
    ("/commercial/", "Commercial", "Build-outs and repairs for your business."),
]

AREAS = ["Granada Hills", "Porter Ranch", "Northridge", "Mission Hills", "Sylmar",
         "Chatsworth", "North Hills", "Reseda", "Van Nuys", "Encino", "Sherman Oaks", "Woodland Hills"]

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
ICON_TEXT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 5h16v11H8l-4 4z"/></svg>'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@125,900&family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">')


def service_list(skip=None):
    rows = []
    for i, (href, title, line) in enumerate([s for s in SERVICES if s[0] != skip], 1):
        rows.append(f'<li><a href="{href}"><span class="n">0{i}</span><h3>{title}</h3>'
                    f'<span class="arr" aria-hidden="true">&rarr;</span><p>{line}</p></a></li>')
    return '<ul class="svc">' + "".join(rows) + "</ul>"


def area_list():
    return '<ul class="area-list">' + "".join(f"<li>{a}</li>" for a in AREAS) + "</ul>"


def contact_band(no="A9", heading="Get a free estimate", line="Call or text. We usually get back to you the same day."):
    b = BIZ
    return f'''<section class="sheet contact" id="contact">
  <div class="wrap contact-grid">
    <div>
      <div class="tb mono"><span class="no">{no}</span><span>Contact</span></div>
      <h2>{heading}</h2>
      <p class="lede">{line}</p>
      <a class="big-phone" href="tel:{b["tel"]}">{b["phone"]}</a>
      <div class="cta">
        <a class="btn solid" href="tel:{b["tel"]}">{ICON_PHONE}Call</a>
        <a class="btn" href="sms:{b["tel"]}">{ICON_TEXT}Text</a>
        <a class="btn" href="/contact/">Send details</a>
      </div>
    </div>
    <dl class="mono">
      <dt>Email</dt><dd><a href="mailto:{b["email"]}">{b["email"]}</a></dd>
      <dt>Office</dt><dd>{b["street"]}<br>{b["city"]}, {b["state"]} {b["zip"]}</dd>
      <dt>Hours</dt><dd>{b["hours"]}</dd>
      <dt>License</dt><dd>CSLB #{b["license"]}</dd>
    </dl>
  </div>
</section>'''


SNIPPETS = {
    "PHONE": BIZ["phone"], "TEL": BIZ["tel"], "EMAIL": BIZ["email"], "LICENSE": BIZ["license"],
    "STREET": BIZ["street"], "HOURS": BIZ["hours"],
    "ICON_PHONE": ICON_PHONE, "ICON_TEXT": ICON_TEXT,
    "SERVICES": service_list(), "AREAS": area_list(),
}


CUR = ' aria-current="page"'


def header(path):
    links = "".join(
        f'<a href="{h}"{CUR if path.startswith(h) else ""}>{l}</a>' for h, l, _ in NAV)
    menu = "".join(f'<a href="{h}">{l}<span>{n}</span></a>' for h, l, n in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="brand" href="/" aria-label="Almora Construction, home"><b>ALMORA</b><small>CONSTRUCTION</small></a>
    <nav class="nav-links" aria-label="Main">{links}</nav>
    <div class="top-right">
      <a class="call-sm" href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a>
      <details class="menu">
        <summary aria-label="Menu"><i></i>Menu</summary>
        <nav class="menu-panel" aria-label="Menu">{menu}
          <a class="btn solid" href="tel:{BIZ["tel"]}">{ICON_PHONE}Call {BIZ["phone"]}</a>
        </nav>
      </details>
    </div>
  </div>
</header>'''


def footer():
    b = BIZ
    svc = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t, _ in SERVICES)
    co = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l, _ in NAV if h not in ("/adus/", "/services/"))
    return f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="brand" href="/"><b>ALMORA</b><small>CONSTRUCTION</small></a>
        <p style="margin-top:14px">Licensed and insured general contractor.<br>CSLB #{b["license"]}</p>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Company</h4><ul>{co}</ul></div>
      <div><h4>Reach us</h4><ul>
        <li><a href="tel:{b["tel"]}">{b["phone"]}</a></li>
        <li><a href="mailto:{b["email"]}">{b["email"]}</a></li>
        <li>{b["street"]}<br>{b["city"]}, {b["state"]} {b["zip"]}</li>
      </ul></div>
    </div>
    <div class="legal mono"><span>&copy; <span id="yr">2026</span> Almora Construction</span><span>Lic. #{b["license"]}</span></div>
  </div>
</footer>
<nav class="callbar" aria-label="Quick contact">
  <a href="sms:{b["tel"]}">{ICON_TEXT}Text</a>
  <a href="tel:{b["tel"]}">{ICON_PHONE}Call now</a>
</nav>'''


def schema():
    b = BIZ
    return json.dumps({
        "@context": "https://schema.org", "@type": "GeneralContractor",
        "name": b["name"], "url": SITE + "/", "telephone": "+1-747-368-1225", "email": b["email"],
        "address": {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["city"],
                    "addressRegion": b["state"], "postalCode": b["zip"], "addressCountry": "US"},
        "areaServed": AREAS,
        "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "license",
                          "name": "California CSLB license #" + b["license"]},
    }, separators=(",", ":"))


def page(meta, body):
    path = meta["path"]
    title = meta["title"]
    full_title = title if path == "/" else f"{title} | Almora Construction"
    url = SITE + path
    extra_head = meta.get("head", "")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{meta["description"]}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{meta["description"]}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0c1f3f">
<link rel="icon" href="/assets/icon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="/assets/site.css">
{extra_head}
<script type="application/ld+json">{schema()}</script>
</head>
<body>
{header(path)}
<main id="main">
{body}
</main>
{footer()}
<script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</body>
</html>
'''


def render(text):
    # {{CONTACT}} or {{CONTACT A5}} -> contact band with that sheet number
    text = re.sub(r"\{\{CONTACT(?: (\w+))?\}\}", lambda m: contact_band(m.group(1) or "A9"), text)
    text = re.sub(r"\{\{SERVICES_EXCEPT (\S+)\}\}", lambda m: service_list(skip=m.group(1)), text)
    for k, v in SNIPPETS.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def main():
    urls = []
    for src in sorted((ROOT / "src" / "pages").glob("*.html")):
        raw = src.read_text()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
        meta = json.loads(m.group(1))
        html = page(meta, render(raw[m.end():]))
        out = ROOT / meta["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html)
        if meta.get("sitemap", True):
            urls.append(SITE + meta["path"])
        print("built", meta["out"])
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")


if __name__ == "__main__":
    main()
