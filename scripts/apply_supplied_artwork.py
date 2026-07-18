#!/usr/bin/env python3
from __future__ import annotations

import base64
import binascii
import re
from pathlib import Path

PAGE = Path("public/learn/wu-xing/feng-shui/index.html")
ASSET = "/assets/learn/wu-xing-feng-shui-five-directions-south-facing.webp"
ASSET_FILE = Path("public/assets/learn/wu-xing-feng-shui-five-directions-south-facing.webp")
BUILD_OLD = "wuxing-feng-shui-2026-07-18-v1-reviewed"
BUILD_NEW = "wuxing-feng-shui-2026-07-18-v2-visual-artwork"
MARKER = "SUPPLIED_FIVE_DIRECTIONS_ARTWORK_V1"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def is_webp(data: bytes) -> bool:
    return len(data) >= 12 and data.startswith(b"RIFF") and data[8:12] == b"WEBP"


def ensure_binary_webp() -> None:
    if not ASSET_FILE.exists():
        fail(f"missing supplied artwork: {ASSET_FILE}")

    raw = ASSET_FILE.read_bytes()
    if is_webp(raw):
        print(f"PASS: supplied artwork is binary WebP ({len(raw)} bytes)")
        return

    try:
        encoded = "".join(raw.decode("ascii").split())
        decoded = base64.b64decode(encoded, validate=True)
    except (UnicodeDecodeError, binascii.Error, ValueError) as exc:
        fail(f"supplied artwork is neither binary WebP nor valid Base64: {exc}")

    if not is_webp(decoded):
        fail("decoded supplied artwork is not a WebP file")

    declared_size = int.from_bytes(decoded[4:8], "little") + 8
    if declared_size != len(decoded):
        fail(
            "decoded supplied artwork is truncated: "
            f"RIFF declares {declared_size} bytes, decoded {len(decoded)} bytes"
        )

    ASSET_FILE.write_bytes(decoded)
    print(f"PASS: decoded supplied artwork to binary WebP ({len(decoded)} bytes)")


def main() -> int:
    ensure_binary_webp()

    if not PAGE.exists():
        fail(f"missing page: {PAGE}")

    html = PAGE.read_text(encoding="utf-8")
    if MARKER in html:
        print("PASS: supplied artwork already integrated")
        return 0

    artwork = f'''<div class="compass-card supplied-artwork-card" aria-label="Traditional south-facing Wu Xing five-directions artwork">
      <!-- {MARKER} -->
      <figure class="hero-artwork">
        <img src="{ASSET}" width="800" height="600" loading="eager" decoding="async" fetchpriority="high" alt="Traditional south-facing Wu Xing diagram with Fire and South at the top, Wood and East on the left, Earth in the centre, Metal and West on the right, and Water and North at the bottom.">
        <figcaption><strong>Traditional south-facing layout.</strong> Fire/South is shown above, Water/North below, Wood/East to the left, Metal/West to the right, and Earth at the centre. This is a labelled cosmographic arrangement, not a modern north-up map. The supplied artwork uses the Traditional glyph form for East; the Five Phase characters are shared forms.</figcaption>
      </figure>'''
    html, substitutions = re.subn(
        r'<div class="compass-card" aria-label="[^"]+">',
        artwork,
        html,
        count=1,
    )
    if substitutions != 1:
        fail("compass-card insertion point not found")

    css = '''
    /* SUPPLIED_FIVE_DIRECTIONS_ARTWORK_V1 */
    .supplied-artwork-card { min-height: 0; padding: .7rem; }
    .supplied-artwork-card::before,
    .supplied-artwork-card::after,
    .supplied-artwork-card .compass-map,
    .supplied-artwork-card .orientation-control,
    .supplied-artwork-card .map-note { display: none; }
    .hero-artwork { margin: 0; overflow: hidden; border-radius: 21px; background: #eee4d5; }
    .hero-artwork img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; }
    .hero-artwork figcaption { padding: .85rem .95rem 1rem; color: var(--muted); background: rgba(255,253,247,.96); font-size: .78rem; line-height: 1.5; }
    .hero-artwork figcaption strong { color: var(--ink); }
'''
    if "</style>" not in html:
        fail("style closing tag not found")
    html = html.replace("</style>", css + "  </style>", 1)

    html = html.replace(
        '<meta property="og:url" content="https://sizhuatelier.shop/learn/wu-xing/feng-shui/">',
        '<meta property="og:url" content="https://sizhuatelier.shop/learn/wu-xing/feng-shui/">\n'
        f'  <meta property="og:image" content="https://sizhuatelier.shop{ASSET}">\n'
        '  <meta property="og:image:width" content="800">\n'
        '  <meta property="og:image:height" content="600">\n'
        '  <meta property="og:image:alt" content="Traditional south-facing Wu Xing five-directions diagram.">',
        1,
    )
    html = html.replace(
        '<meta name="twitter:card" content="summary">',
        '<meta name="twitter:card" content="summary_large_image">',
        1,
    )
    html = html.replace(BUILD_OLD, BUILD_NEW)
    html = html.replace(
        'Chinese text policy <code>CN_SIMPLIFIED</code> with shared core characters only;',
        'Chinese text policy <code>DOCUMENTED_MIXED</code> for the supplied illustration; the phase characters are shared forms and its East label uses a Traditional glyph form;',
        1,
    )

    PAGE.write_text(html, encoding="utf-8")
    print("PASS: supplied five-directions artwork integrated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
