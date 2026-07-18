#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from html.parser import HTMLParser
from pathlib import Path

PAGE = Path("public/learn/wu-xing/feng-shui/index.html")
VERSION = Path("public/version.txt")
ROBOTS = Path("public/robots.txt")
SITEMAP = Path("public/sitemap.xml")
ARTWORK = Path("public/assets/learn/wu-xing-feng-shui-five-directions-south-facing.webp")
BUILD = "wuxing-feng-shui-2026-07-18-v2-visual-artwork"
CANONICAL = "https://sizhuatelier.shop/learn/wu-xing/feng-shui/"
ARTWORK_NAME = "wu-xing-feng-shui-five-directions-south-facing.webp"

REQUIRED = [
    "Wu Xing and Feng Shui",
    "Directions, seasons and colours",
    "North-up maps and traditional south-facing diagrams",
    "Feng Shui is a family of approaches, not one formula",
    "How to read rooms without turning symbolism into pseudoscience",
    "Traditional applications—and what can safely be said",
    "Limits and common misconceptions",
    "Source note",
    "Traditional south-facing layout.",
    "This is a labelled cosmographic arrangement, not a modern north-up map.",
    "DOCUMENTED_MIXED",
    "https://sizhuatelier.shop/learn/wu-xing/",
    "https://www.etsy.com/de/shop/SizhuAtelier",
    "dataLayer",
    "sizhu:analytics",
    "prefers-reduced-motion",
]
FORBIDDEN = [
    "will make you rich",
    "guarantees wealth",
    "guarantees health",
    "raises cortisol",
    "scientifically proven Feng Shui",
    "natural science of Feng Shui",
    "Bazodiac Learn",
    "BZG-",
]
TOKENS = {"五行":"wǔxíng","木":"mù","火":"huǒ","土":"tǔ","金":"jīn","水":"shuǐ","生":"shēng","克":"kè"}
EVENTS = ["hero_wuxing_hub_click","cta_wuxing_hub_click","cta_shop_click","cta_etsy_click","section_view","scroll_depth_","diagram_orientation_change"]


class Audit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.lang = ""
        self.main_ids: set[str] = set()
        self.skip = 0
        self.buttons = 0
        self.tables = 0
        self.hrefs: set[str] = set()
        self.images: list[dict[str, str]] = []
        self.json_blocks: list[str] = []
        self._json = False
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {k: v or "" for k, v in attrs}
        if tag == "html": self.lang = data.get("lang", "")
        elif tag == "h1": self.h1 += 1
        elif tag == "main" and data.get("id"): self.main_ids.add(data["id"])
        elif tag == "a":
            self.hrefs.add(data.get("href", ""))
            if data.get("class") == "skip": self.skip += 1
        elif tag == "button": self.buttons += 1
        elif tag == "table": self.tables += 1
        elif tag == "img": self.images.append(data)
        elif tag == "script" and data.get("type") == "application/ld+json":
            self._json = True
            self._chunks = []

    def handle_data(self, data: str) -> None:
        if self._json: self._chunks.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json:
            self.json_blocks.append("".join(self._chunks))
            self._json = False


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not PAGE.exists(): fail(f"missing page: {PAGE}")
    if not ARTWORK.exists() or ARTWORK.stat().st_size < 10_000: fail("supplied artwork missing or unexpectedly small")
    html = PAGE.read_text(encoding="utf-8")

    for text in REQUIRED:
        if text not in html: fail(f"required content missing: {text}")
    for text in FORBIDDEN:
        if text.lower() in html.lower(): fail(f"forbidden content present: {text}")
    for hanzi, pinyin in TOKENS.items():
        if hanzi not in html or pinyin not in html: fail(f"token or Pinyin missing: {hanzi} / {pinyin}")
    for event in EVENTS:
        if event not in html: fail(f"analytics event missing: {event}")
    if f"PUBLIC_BUILD: {BUILD}" not in html or f'content="{BUILD}"' not in html: fail("build marker missing")
    if f'<link rel="canonical" href="{CANONICAL}">' not in html: fail("canonical missing")
    if ARTWORK_NAME not in html: fail("supplied artwork is not referenced by the page")

    parser = Audit(); parser.feed(html)
    if parser.lang != "en" or parser.h1 != 1: fail("language or H1 gate failed")
    if parser.skip != 1 or "main-content" not in parser.main_ids: fail("skip link or main landmark missing")
    if parser.buttons < 2 or parser.tables != 1: fail("interactive control or table missing")
    artwork_images = [img for img in parser.images if img.get("src", "").endswith(ARTWORK_NAME)]
    if len(artwork_images) != 1 or not artwork_images[0].get("alt", "").strip(): fail("supplied artwork or descriptive alt text missing")
    if len(parser.json_blocks) != 1: fail("expected one JSON-LD block")
    try: graph = json.loads(parser.json_blocks[0]).get("@graph", [])
    except json.JSONDecodeError as exc: fail(f"invalid JSON-LD: {exc}")
    expected = {"Organization","WebSite","WebPage","Article","BreadcrumbList","DefinedTermSet"}
    types = {item.get("@type") for item in graph if isinstance(item, dict)}
    if not expected.issubset(types): fail(f"JSON-LD types missing: {expected - types}")
    if "https://sizhuatelier.shop/learn/wu-xing/" not in parser.hrefs: fail("Wu Xing hub link missing")
    if not any(h.startswith("https://www.etsy.com/de/shop/SizhuAtelier") and "utm_campaign=wuxing_feng_shui" in h for h in parser.hrefs): fail("Etsy CTA UTM missing")
    if not VERSION.exists() or f"WU_XING_FENG_SHUI_PUBLIC_BUILD={BUILD}" not in VERSION.read_text(encoding="utf-8"): fail("version marker missing")
    if not ROBOTS.exists() or "Sitemap: https://sizhuatelier.shop/sitemap.xml" not in ROBOTS.read_text(encoding="utf-8"): fail("robots gate failed")
    if not SITEMAP.exists() or CANONICAL not in SITEMAP.read_text(encoding="utf-8"): fail("sitemap gate failed")

    print("PASS: BZG-32 public content validated")
    print("- supplied south-facing artwork and alt text present")
    print("- sources, limits, schools, rooms and summary present")
    print("- Hanzi, Pinyin, SEO, JSON-LD, accessibility and analytics passed")
    print("- deterministic medical, scientific, wealth and destiny claims blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
