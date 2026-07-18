# BZG-32 review checklist

## Ticket identity

- Parent epic: BZG-7 — Sizhu Atelier Learn & Knowledge Hubs
- Story: BZG-32 — English Sizhu Atelier guide “Wu Xing and Feng Shui”
- Dependency content path: BZG-31 Wu Xing hub

## Acceptance criteria

| Criterion | Evidence | Status |
|---|---|---|
| Canonical route exists | `public/learn/wu-xing/feng-shui/index.html`; canonical meta | PASS IN REPOSITORY |
| Terms, correspondences and variants reviewed | `docs/research-source-ledger.md`; validator | PASS |
| Sources, limits and summary present | Article sections `summary`, `limits`, `sources` | PASS |
| SEO metadata | title, description, canonical, robots, Open Graph, sitemap | PASS |
| Structured data | Article, WebPage, WebSite, Organization, BreadcrumbList, DefinedTermSet | PASS |
| Accessibility | skip link, landmarks, one H1, keyboard toggle, focus styles, labelled table, reduced motion | PASS BY STATIC GATE; manual assistive-tech test recommended |
| Mobile layout | responsive breakpoints at 900px and 700px | PASS BY CODE REVIEW |
| Internal links | Wu Xing hub, Learn and shop routes | PASS BY STATIC GATE |
| Product CTAs | shop and Etsy CTAs with UTM | PASS BY STATIC GATE |
| Analytics events | CTA, source, orientation, section-view and scroll-depth payloads | PASS BY CODE REVIEW |
| Repository, branch, PR and review | feature branch plus PR and this evidence package | PASS AFTER PR CREATION |
| Live publication | Railway/domain deployment and HTTP verification | PENDING DEPLOYMENT |

## Manual release checks after deployment

1. `/health` returns `ok`.
2. `/version.txt` contains the expected build marker.
3. The canonical route returns HTTP 200 and is indexable.
4. Validate JSON-LD with Rich Results Test.
5. Test keyboard navigation, focus visibility, 200% zoom and a screen reader.
6. Test 320px, 375px, 768px and desktop widths.
7. Confirm analytics payloads in the deployed analytics adapter.
8. Confirm the custom domain routes to the merged deployment.
