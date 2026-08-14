#!/usr/bin/env python3
"""Generate the billdonner.com app catalog from the canonical inventory."""

from __future__ import annotations

import html
import json
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
    "pfoliolio-app": "See every brokerage account and your real asset allocation in one place.",
    "picklefamilia-app": "Build the week's games, share one link, and let players claim their slots.",
    "screenker-app": "A Mac studio for producing polished App Store screenshots efficiently.",
    "sentipods-app": "Search and read clean, speaker-labeled podcast transcripts on Mac, iPhone, and iPad.",
    "sharedspace-lab": "An experiment in nearby, peer-to-peer shared spaces across Apple devices.",
    "zerver-monitor-app": "A pocket status board for the services behind these apps.",
}


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
        if links.get("testFlight"):
            external.append(link("TestFlight invite", links["testFlight"]))
        product_url = links.get("productSite") or links.get("website")
        if product_url and not product_url.startswith("https://billdonner.com/apps/"):
            external.append(link("Product site", product_url))
        if app["id"] == "pfoliolio-app":
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


def generate_catalog(data: dict) -> str:
    mapped_bundles = {item["bundleId"] for item in data["ascApps"]["mapped"]}
    apps = [
        entity for entity in data["entities"]
        if entity.get("kind") == "app"
        and entity.get("bundleId") in mapped_bundles
        and entity.get("status") not in RETIRED_STATUSES
    ]
    apps.sort(key=lambda item: (item.get("name") or "").casefold())
    store = [app for app in apps if (app.get("links") or {}).get("appStore")]
    beta = [app for app in apps if not (app.get("links") or {}).get("appStore") and (app.get("links") or {}).get("testFlight")]
    development = [app for app in apps if app not in store and app not in beta]
    body = f'''  <header class="hero wrap">
    <p class="kicker">Everything I'm building</p><h1>Apps</h1>
    <p class="lead">{len(apps)} active apps, reconciled against App Store Connect and their source repositories on August 14, 2026.</p>
  </header>
  <main class="wrap">
{section('On the App Store', 'Published and downloadable right now.', store, 'App Store', 'live')}
{section('Open TestFlight betas', 'Public betas available through Apple TestFlight.', beta, 'TestFlight', 'beta')}
{section('In development', 'Mapped in App Store Connect and still in active development.', development, 'In development', '')}
    <section><h2>Colophon</h2><p style="color:var(--ink-soft)">Generated from the MasterIndex canonical inventory on August 14, 2026. Archived products are omitted.</p></section>
  </main>'''
    return shell("Apps - Bill Donner", "Bill Donner's active App Store, TestFlight, and in-development apps.", body)


def generate_pfoliolio(data: dict) -> str:
    app = next(entity for entity in data["entities"] if entity["id"] == "pfoliolio-app")
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
    pfoliolio = OUTPUT / "pfoliolio"
    pfoliolio.mkdir(exist_ok=True)
    (pfoliolio / "index.html").write_text(generate_pfoliolio(data))
    legacy = OUTPUT / "oliopfolio"
    legacy.mkdir(exist_ok=True)
    (legacy / "index.html").write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Pfoliolio</title><link rel="canonical" href="https://billdonner.com/apps/pfoliolio/"><meta http-equiv="refresh" content="0; url=/apps/pfoliolio/"></head><body><p>Oliopfolio is now <a href="/apps/pfoliolio/">Pfoliolio</a>.</p></body></html>\n''')
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
