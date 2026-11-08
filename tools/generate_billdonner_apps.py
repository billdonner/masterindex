#!/usr/bin/env python3
"""Generate the billdonner.com app catalog from the canonical inventory."""

from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "current" / "index.json"
OUTPUT = ROOT / "publish" / "billdonner.com" / "apps"
RETIRED_STATUSES = {"archived", "retired"}
PUBLIC_DESCRIPTIONS = {
    "burfords-app": "All 100 of Gary B. Martin's weekly Burford cartoons, with the original reader comments.",
    "words123-app": "Read, spell, count, and race the clock in a learning playground for ages 2-7.",
    "amenbeats-app": "A pocket 16-step sequencer for studying and remixing classic drum breaks.",
    "kinflash-app": "A private family tree that quizzes you on your own relatives and exports GEDCOM.",
    "pickledballs-app": "Run a whole pickleball session from your phone with balanced courts and pairing rules.",
    "qross-app": "Trivia where the grid is the puzzle and every wrong answer closes a path.",
    "workinon-app": "One focused view of what you are working on right now, with widgets and smart updates.",
    "cardz-studio-ios-app": "Edit, review, and manage card decks from iPhone and iPad.",
    "famster-app": "A focused place for families to coordinate the things that matter.",
    "obo-ios-app": "Thirteen games built from your own family's flashcard decks.",
    "mallinbook-app": "Turn one living resident roster into a polished, print-ready community directory.",
    "nagz-app": "Family reminders shaped with AI and delivered at the right moment.",
    "oenora-app": "A personal wine knowledge system for your cellar, notes, and discoveries.",
    "pfolio-app": "See every brokerage account and your real asset allocation in one place.",
    "picklefamilia-asc-app": "Build the week's games, share one link, and let players claim their slots.",
    "screenker-asc-app": "A Mac studio for producing polished App Store screenshots efficiently.",
    "sentipods-app": "Search and read clean, speaker-labeled podcast transcripts on Mac, iPhone, and iPad.",
    "sharedspace-lab": "An experiment in nearby, peer-to-peer shared spaces across Apple devices.",
    "zerver-monitor-asc-app": "A pocket status board for the services behind these apps.",
}

# Verified against Apple's public iTunes lookup for artist 428849243 on
# November 8, 2026. Keep this small, explicit catalog until the canonical
# inventory has caught up with the App Store releases.
APP_STORE_CATALOG = [
    {
        "id": "amenbeats-app", "name": "AmenBeats", "slug": "amenbeats",
        "appStore": "https://apps.apple.com/us/app/amenbeats/id6778510642",
        "releaseDate": "September 30, 2026",
        "workEvidence": "June 9, 2026 — earliest local Git commit in the AmenBeats repository",
        "description": "A pocket 16-step sequencer for studying and remixing classic drum breaks.",
    },
    {
        "id": "burfords-app", "name": "100 Burfords", "slug": "100-burfords",
        "appStore": "https://apps.apple.com/us/app/100-burfords/id6766107636",
        "releaseDate": "May 6, 2026",
        "workEvidence": "May 3, 2026 — earliest local Git commit in the 100 Burfords repository",
        "description": "All 100 of Gary B. Martin's weekly Burford cartoons, with the original reader comments.",
    },
    {
        "id": "words123-app", "name": "123 Words", "slug": "123-words",
        "appStore": "https://apps.apple.com/us/app/123-words/id6766975041",
        "releaseDate": "May 14, 2026",
        "workEvidence": "July 27, 2026 — earliest surviving local Git commit after the repository history rewrite; an older archive is referenced but not present here",
        "description": "Read, spell, count, and race the clock in a learning playground for ages 2–7.",
    },
    {
        "id": "qross-app", "name": "DoubleQross", "slug": "doubleqross",
        "appStore": "https://apps.apple.com/us/app/doubleqross/id6759799988",
        "releaseDate": "September 22, 2026",
        "workEvidence": "February 27, 2026 — earliest local Git commit in the DoubleQross repository",
        "description": "Grid trivia where the board is the puzzle and every wrong answer closes a path.",
    },
    {
        "id": "hoabooklet-app", "name": "HOABooklet", "slug": "hoabooklet",
        "appStore": "https://apps.apple.com/us/app/hoabooklet/id6806080022",
        "releaseDate": "October 3, 2026",
        "workEvidence": "June 28, 2026 — earliest local Git evidence in the Mallinbook/HOABooklet repository line",
        "description": "Your directory, in your pocket — the iPhone and iPad companion to HOABooklet for Mac.",
    },
    {
        "id": "murdl-app", "name": "MURDL 16", "slug": "murdl-16",
        "appStore": "https://apps.apple.com/us/app/murdl-16/id6809919090",
        "releaseDate": "September 16, 2026",
        "workEvidence": "No local project history was found on this machine; this date remains unverified here",
        "description": "Guess five-letter words on 1, 2, 4, 8, or 16 boards at once.",
    },
    {
        "id": "pickledballs-app", "name": "PickleFamilia Companion", "slug": "picklefamilia-companion",
        "appStore": "https://apps.apple.com/us/app/picklefamilia-companion/id6762310890",
        "releaseDate": "November 6, 2026",
        "workEvidence": "April 21, 2026 — earliest local Git evidence in the PickledBalls repository for the current Companion product line",
        "description": "Fair courts for pickup games, and a free club that is just your roster.",
    },
]
APP_STORE_IDS = {item["id"] for item in APP_STORE_CATALOG}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def link(label: str, url: str) -> str:
    suffix = " &nearr;" if urlparse(url).netloc and urlparse(url).netloc != "billdonner.com" else " &rarr;"
    return f'<a href="{esc(url)}">{esc(label)}{suffix}</a>'


def trim_description(value: str) -> str:
    first = value.split(". ", 1)[0].strip()
    return first + ("." if first and not first.endswith(".") else "")


def section(title: str, intro: str, apps: list[dict], label: str, class_name: str) -> str:
    entries = []
    for app in apps:
        links = app.get("links") or {}
        external = []
        if links.get("appStore"):
            external.append(link("App Store", links["appStore"]))
        if app.get("noteSlug"):
            external.insert(0, link("Build note", f"/apps/notes/{app['noteSlug']}/"))
        if links.get("testFlight"):
            external.append(link("TestFlight invite", links["testFlight"]))
        product_url = links.get("productSite") or links.get("website")
        if product_url and not product_url.startswith("https://billdonner.com/apps/"):
            external.append(link("Product site", product_url))
        if app["id"] == "pfolio-app":
            external.insert(0, link("What it does", "/apps/pfoliolio/"))
        description = PUBLIC_DESCRIPTIONS.get(app["id"], trim_description(app.get("description", "")))
        entries.append(
            f'''      <article class="entry" id="app-{esc(app['id'].removesuffix('-app'))}">
        <h3>{esc(app['name'])}<span class="tag status {class_name}">{esc(label)}</span></h3>
        <p>{esc(description)}</p>
        <p class="applinks">{' '.join(external) if external else 'Details coming soon.'}</p>
      </article>'''
        )
    return f'''    <section>
      <h2>{esc(title)} &middot; {len(apps)}</h2>
      <p style="color:var(--ink-soft)">{esc(intro)}</p>
{chr(10).join(entries)}
    </section>'''


def shell(title: str, description: str, body: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{esc(title)}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(description)}">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="stylesheet" href="/assets/css/site.css">
  <script src="/assets/js/theme.js"></script>
</head>
<body>
  <nav class="nav"><div class="nav-inner">
    <a class="brand" href="/">Bill Donner's Place</a><span class="spacer"></span>
    <a class="link" href="/apps/">Apps</a><a class="link hide-sm" href="/music/planb.html">planB</a>
    <a class="link hide-sm" href="/music/abhd.html">ABHD</a><a class="link" href="/older.html">About</a>
    <button class="theme-toggle" id="theme-toggle" title="Toggle dark mode" aria-label="Toggle dark mode">&#9790;</button>
  </div></nav>
{body}
  <footer class="wrap footer-bar"><p>&copy; 2026 Bill Donner &middot; <a href="mailto:billdonner@gmail.com">billdonner@gmail.com</a></p></footer>
</body>
</html>
'''


def index_date(data: dict) -> str:
    """Render the index's generatedAt as a human date, so the catalog never claims a stale one."""
    stamp = datetime.fromisoformat(data["generatedAt"])
    return f"{stamp.strftime('%B')} {stamp.day}, {stamp.year}"


def generate_catalog(data: dict) -> str:
    mapped_bundles = {item["bundleId"] for item in data["ascApps"]["mapped"]}
    inventory_apps = [
        entity for entity in data["entities"]
        if entity.get("kind") == "app"
        and entity.get("bundleId") in mapped_bundles
        and entity.get("status") not in RETIRED_STATUSES
    ]
    by_id = {app["id"]: app for app in inventory_apps}
    store = []
    for item in APP_STORE_CATALOG:
        app = dict(by_id.get(item["id"], {}))
        app.update({"id": item["id"], "name": item["name"], "description": item["description"], "links": {"appStore": item["appStore"]}, "noteSlug": item["slug"]})
        if item["id"] == "pickledballs-app":
            app["links"]["productSite"] = "https://picklefamilia.com/companion/"
        store.append(app)
    remaining = [app for app in inventory_apps if app["id"] not in APP_STORE_IDS]
    remaining.sort(key=lambda item: (item.get("name") or "").casefold())
    beta = [app for app in remaining if (app.get("links") or {}).get("testFlight")]
    development = [app for app in remaining if app not in beta]
    generated = datetime.now().strftime("%B %-d, %Y")
    body = f'''  <header class="hero wrap">
    <p class="kicker">Everything I'm building</p><h1>Apps</h1>
    <p class="lead">{len(store)} apps currently on the App Store, with TestFlight and in-development work also listed, checked against Apple and the source repositories on {esc(generated)}.</p>
  </header>
  <main class="wrap">
{section('On the App Store', 'Published and downloadable right now.', store, 'App Store', 'live')}
{section('Open TestFlight betas', 'Public betas available through Apple TestFlight.', beta, 'TestFlight', 'beta')}
{section('In development', 'Mapped in App Store Connect and still in active development.', development, 'In development', '')}
    <section><h2>Colophon</h2><p style="color:var(--ink-soft)">Generated from the MasterIndex canonical inventory on {esc(generated)}. Archived products are omitted.</p></section>
  </main>'''
    return shell("Apps - Bill Donner", "Bill Donner's current App Store apps, TestFlight projects, and build notes.", body)


def generate_notes_index() -> str:
    entries = "\n".join(
        f'''      <article class="entry"><h3><a href="/apps/notes/{esc(item["slug"])}/">{esc(item["name"])}</a></h3><p>{esc(item["description"])}</p><p class="applinks">App Store release: {esc(item["releaseDate"])}</p></article>'''
        for item in APP_STORE_CATALOG
    )
    body = f'''  <header class="hero wrap"><p class="kicker">Build notes</p><h1>App notes</h1><p class="lead">A place for one or two paragraphs about how each app came to be. The dates below are factual anchors; the personal notes can grow over time.</p></header>
  <main class="wrap"><section><h2>Apps on the App Store</h2>{entries}</section></main>'''
    return shell("App notes - Bill Donner", "Short build notes for Bill Donner's App Store apps.", body)


def generate_note(item: dict) -> str:
    body = f'''  <header class="hero wrap"><p class="kicker">App note</p><h1>{esc(item["name"])}</h1><p class="lead">{esc(item["description"])}</p></header>
  <main class="wrap"><section><h2>Timeline</h2><p><strong>Entered the App Store</strong><br>{esc(item["releaseDate"])} — <a href="{esc(item["appStore"])}">Apple App Store listing</a></p><p><strong>Earliest work evidence</strong><br>{esc(item["workEvidence"])}.</p></section><section><h2>Your note</h2><p><em>Write one or two paragraphs here about why this app exists, what changed while you built it, and what you hope people notice.</em></p></section><p class="applinks"><a href="{esc(item["appStore"])}">Download from the App Store</a> <a href="/apps/notes/">All app notes</a></p></main>'''
    return shell(f"{item['name']} - Bill Donner", f"Build note for {item['name']}.", body)


def generate_pfoliolio(data: dict) -> str:
    app = next(entity for entity in data["entities"] if entity["id"] == "pfolio-app")
    links = app["links"]
    body = f'''  <header class="hero wrap">
    <p class="kicker">Portfolio clarity</p><h1>Pfoliolio</h1>
    <p class="lead">See brokerage accounts, manual holdings, and your real asset allocation in one native app for iPhone, iPad, and Mac.</p>
  </header>
  <main class="wrap">
    <section><h2>What it does</h2><p>Pfoliolio brings brokerage accounts and manual holdings together, then shows how your portfolio is actually allocated. Use it to review positions, compare allocation targets, and keep investment questions and reminders close to the numbers.</p>
      <p class="applinks">{link('Privacy policy', links['privacyPolicy'])} {link('Source', links['github'])}</p></section>
    <section id="support"><h2>Support</h2><p>For help with Pfoliolio, email <a href="mailto:billdonner@gmail.com?subject=Pfoliolio%20support">billdonner@gmail.com</a>.</p></section>
  </main>'''
    return shell("Pfoliolio - Bill Donner", "Pfoliolio is a native multi-account portfolio and allocation app.", body)


def main() -> None:
    data = json.loads(INDEX.read_text())
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "index.html").write_text(generate_catalog(data))
    notes = OUTPUT / "notes"
    notes.mkdir(exist_ok=True)
    (notes / "index.html").write_text(generate_notes_index())
    for item in APP_STORE_CATALOG:
        target = notes / item["slug"]
        target.mkdir(exist_ok=True)
        (target / "index.html").write_text(generate_note(item))
    pfoliolio = OUTPUT / "pfoliolio"
    pfoliolio.mkdir(exist_ok=True)
    (pfoliolio / "index.html").write_text(generate_pfoliolio(data))
    legacy = OUTPUT / "oliopfolio"
    legacy.mkdir(exist_ok=True)
    (legacy / "index.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Pfoliolio</title><link rel="canonical" href="https://billdonner.com/apps/pfoliolio/"><meta http-equiv="refresh" content="0; url=/apps/pfoliolio/"></head><body><p>Oliopfolio is now <a href="/apps/pfoliolio/">Pfoliolio</a>.</p></body></html>\n''')
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
