#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

PAGE = Path("public/learn/wu-xing/feng-shui/index.html")
VERSION = Path("public/version.txt")
CADDY = Path("Caddyfile")
REGISTRY = Path("config/cornerstone-links.json")
BUILD = "wuxing-feng-shui-2026-07-19-v3-link-registry"
MARKER = "CORNERSTONE_CALCULATOR_LINKS_V1"

ANCHOR_RE = re.compile(r"<a\b(?P<attrs>[^>]*)>(?P<body>.*?)</a>", re.I | re.S)
HREF_RE = re.compile(r"\bhref\s*=\s*([\"'])(?P<href>.*?)\1", re.I | re.S)
EVENT_RE = re.compile(r"\bdata-analytics-event\s*=\s*([\"'])(?P<event>.*?)\1", re.I | re.S)
DIV_TOKEN_RE = re.compile(r"<div\b[^>]*>|</div>", re.I)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load_registry() -> dict[str, str]:
    if not REGISTRY.exists():
        fail(f"missing link registry: {REGISTRY}")
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    required = {
        "sizhu_atelier",
        "sizhu_atelier_etsy",
        "bazi_chart",
        "zi_wei_dou_shu_chart",
        "wu_xing_foundations",
        "wu_xing_feng_shui",
    }
    missing = sorted(required - data.keys())
    if missing:
        fail(f"link registry keys missing: {missing}")
    return {key: str(value) for key, value in data.items()}


def set_href(attrs: str, target: str) -> str:
    if HREF_RE.search(attrs):
        return HREF_RE.sub(lambda match: f'href="{target}"', attrs, count=1)
    return f' href="{target}"{attrs}'


def rewrite_anchors(html: str, links: dict[str, str]) -> str:
    etsy_tracking = (
        links["sizhu_atelier_etsy"]
        + "&utm_source=sizhuatelier&utm_medium=learn"
        + "&utm_campaign=wuxing_feng_shui&utm_content=footer_cta"
    )
    event_targets = {
        "brand_home_click": links["sizhu_atelier"],
        "learn_home_click": links["wu_xing_foundations"],
        "wuxing_hub_header_click": links["wu_xing_foundations"],
        "hero_wuxing_hub_click": links["wu_xing_foundations"],
        "cta_wuxing_hub_click": links["wu_xing_foundations"],
        "cta_shop_click": links["sizhu_atelier"],
        "cta_etsy_click": etsy_tracking,
        "cta_bazi_chart_click": links["bazi_chart"],
        "cta_zwds_chart_click": links["zi_wei_dou_shu_chart"],
    }
    legacy_targets = {
        "https://sizhuatelier.shop/": links["sizhu_atelier"],
        "https://sizhuatelier.shop/learn/": links["wu_xing_foundations"],
        "https://sizhuatelier.shop/learn/wu-xing/": links["wu_xing_foundations"],
        "https://bazodiac.space/": links["bazi_chart"],
        "https://www.bazodiac.space/": links["bazi_chart"],
    }

    def replace(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        body = match.group("body")
        event_match = EVENT_RE.search(attrs)
        href_match = HREF_RE.search(attrs)
        target = None
        if event_match:
            target = event_targets.get(event_match.group("event"))
        if target is None and href_match:
            target = legacy_targets.get(href_match.group("href"))
        if target is None:
            return match.group(0)
        return f"<a{set_href(attrs, target)}>{body}</a>"

    return ANCHOR_RE.sub(replace, html)


def insert_before_matching_div(html: str, start_marker: str, addition: str) -> str:
    start = html.find(start_marker)
    if start < 0:
        fail(f"CTA grid not found: {start_marker}")
    depth = 0
    for token in DIV_TOKEN_RE.finditer(html, start):
        if token.group(0).lower().startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return html[: token.start()] + addition + html[token.start() :]
    fail("CTA grid closing div not found")


def ensure_calculator_cards(html: str, links: dict[str, str]) -> str:
    if MARKER in html:
        return html
    cards = f'''<!-- {MARKER} -->
<div class="cta-card"><h3>Calculate a BaZi chart</h3><p>Open the Bazodiac BaZi chart experience and generate a chart from your birth data.</p><a class="button" href="{links['bazi_chart']}" data-analytics-event="cta_bazi_chart_click">Calculate a BaZi chart</a></div>
<div class="cta-card"><h3>Calculate a Zi Wei Dou Shu chart</h3><p>Open the Zi Wei Dou Shu chart application for a separate traditional chart system.</p><a class="button" href="{links['zi_wei_dou_shu_chart']}" data-analytics-event="cta_zwds_chart_click">Calculate a Zi Wei Dou Shu chart</a></div>'''
    return insert_before_matching_div(html, '<div class="cta-grid">', cards)


def update_build_markers(html: str) -> str:
    html = re.sub(r"PUBLIC_BUILD:\s*[A-Za-z0-9._-]+", f"PUBLIC_BUILD: {BUILD}", html)
    html = re.sub(
        r'(<meta\s+name=["\']x-public-build["\']\s+content=["\'])[^"\']+(["\'])',
        rf"\g<1>{BUILD}\g<2>",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'("dateModified"\s*:\s*")[^"]+("\s*)',
        r'\g<1>2026-07-19T00:30:00+02:00\2',
        html,
        count=1,
    )
    html = re.sub(r"Build:\s*<code>[^<]+</code>", f"Build: <code>{BUILD}</code>", html)
    return html


def update_runtime_metadata(links: dict[str, str]) -> None:
    VERSION.write_text(
        "\n".join(
            [
                f"WU_XING_FENG_SHUI_PUBLIC_BUILD={BUILD}",
                "EXPECTED_ROUTE=/learn/wu-xing/feng-shui/",
                f"CANONICAL={links['wu_xing_feng_shui']}",
                f"WU_XING_FOUNDATIONS={links['wu_xing_foundations']}",
                f"SIZHU_ATELIER={links['sizhu_atelier']}",
                f"SIZHU_ATELIER_ETSY={links['sizhu_atelier_etsy']}",
                f"BAZI_CHART={links['bazi_chart']}",
                f"ZI_WEI_DOU_SHU_CHART={links['zi_wei_dou_shu_chart']}",
                "SOURCE_REVIEW=classical-correspondences-academic-history-claims-boundary",
                "GLYPH_POLICY=DOCUMENTED_MIXED",
                "ANALYTICS=vendor-neutral-dataLayer-custom-event",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if CADDY.exists():
        caddy = CADDY.read_text(encoding="utf-8")
        caddy = re.sub(r'X-Sizhu-Build\s+"[^"]+"', f'X-Sizhu-Build "{BUILD}"', caddy)
        CADDY.write_text(caddy, encoding="utf-8")


def main() -> int:
    links = load_registry()
    if not PAGE.exists():
        fail(f"missing page: {PAGE}")
    html = PAGE.read_text(encoding="utf-8")
    html = rewrite_anchors(html, links)
    html = ensure_calculator_cards(html, links)
    html = rewrite_anchors(html, links)
    html = update_build_markers(html)
    PAGE.write_text(html, encoding="utf-8")
    update_runtime_metadata(links)
    print(f"PASS: applied authoritative cornerstone links ({BUILD})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
