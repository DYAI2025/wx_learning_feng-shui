# Wu Xing and Feng Shui public guide

Source-reviewed static learning page for BZG-32 under the BZG-7 Sizhu Atelier Learn epic.

## Public route

- `/learn/wu-xing/feng-shui/`
- Canonical: `https://sizhuatelier.shop/learn/wu-xing/feng-shui/`

## Verification routes

- `/health` returns `ok`
- `/version.txt` reports `wuxing-feng-shui-2026-07-18-v1-reviewed`

## Local validation

```bash
python3 scripts/validate_public_content.py
python3 scripts/audit_contrast.py
```

## Preview

Open `public/learn/wu-xing/feng-shui/index.html` directly, or run a static server from `public/`.

## Deployment

Railway should deploy the repository root using the included `Dockerfile`. The build fails when the deterministic content, metadata, accessibility, analytics or claim-safety checks fail.

## Editorial architecture

- `docs/research-source-ledger.md`: source and claim provenance
- `docs/claims-review.md`: audit of the supplied research draft
- `docs/review-checklist.md`: acceptance-criteria evidence
- `scripts/validate_public_content.py`: deterministic release gate
- `scripts/audit_contrast.py`: colour contrast gate

## Scope boundary

The page explains traditional and historical models. It does not claim medical, scientific, architectural, wealth, relationship or destiny effects from Feng Shui correspondences.
