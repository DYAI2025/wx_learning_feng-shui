## Summary

- [ ] BZG-32 content and route implemented
- [ ] Source ledger and claim review included
- [ ] Deterministic validation passes
- [ ] Canonical, structured data, accessibility and analytics reviewed

## Evidence

- Validation: `python3 scripts/validate_public_content.py`
- Contrast: `python3 scripts/audit_contrast.py`
- Route: `/learn/wu-xing/feng-shui/`

## Release boundary

Merging does not prove live publication. Verify Railway deployment, custom-domain routing, `/health`, `/version.txt`, structured data and analytics after deploy.
