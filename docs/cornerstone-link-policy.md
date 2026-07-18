# Cornerstone link policy

These destinations are the authoritative public links for Sizhu Atelier and Bazodiac learning pages. New and updated cornerstone pages must read them from `config/cornerstone-links.json` rather than hard-code legacy domains.

| Purpose | Registry key |
|---|---|
| Sizhu Atelier shop | `sizhu_atelier` |
| Sizhu Atelier on Etsy | `sizhu_atelier_etsy` |
| BaZi chart calculator / Bazodiac CTA | `bazi_chart` |
| Zi Wei Dou Shu chart calculator | `zi_wei_dou_shu_chart` |
| Wu Xing foundations page | `wu_xing_foundations` |
| Wu Xing and Feng Shui guide | `wu_xing_feng_shui` |

## Rules

1. Use the registry destination whenever the corresponding brand, calculator, shop, or learning page is linked.
2. Link related cornerstone pages in both directions when both pages exist.
3. Canonical and structured-data identifiers may continue to use the intended canonical publication domain; this registry governs clickable destinations.
4. UTM parameters may be appended to the Etsy destination, but the registered shop URL remains the base.
5. Validators must fail when required cross-links or registered destinations are absent.
