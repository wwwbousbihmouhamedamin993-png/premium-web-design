# design-systems/ — index

Reverse-engineered `DESIGN.md` specs from ~130 production web apps, organized by domain. Each
app folder carries a `DESIGN.md`; screenshots are supporting evidence only — every rule is
fully expressible in text.

Load 1–2 specs per task, never more than 2–3 at once. Pick **posture-fit** apps before
building (`references/signature-moves.md`): *restrained instrument* (Linear, Stripe, Grafana,
Vercel) or *committed brand* (Figma, Retool, Slack). Steal moves, not layouts.

One category is exempt from posture-fit: **`system-docs/`** holds public design-system
documentation sites (Fluent 2, Spectrum, Uber Base, Gestalt, Lightning, Geist, Wise). Those are
standards references for tokens, component state matrices, density mechanics, and per-component
a11y docs — never visual direction. Its README also carries the **same-problem comparison**
protocol: read one component across all seven specs before building it. See its README.

## Categories

| Category | Path | Notable |
|---|---|---|
| Developer tools & CI | `devtools/` | Vercel, Linear, GitHub, Retool, Sourcegraph, Sentry |
| Observability | `observability/` | Grafana, Datadog, Honeycomb, Prometheus, Kibana |
| Data & BI | `data-bi/` | Databricks, Snowflake, Tableau, Metabase, Hex |
| Databases & backend | `backend/` | Supabase, MongoDB Atlas, PlanetScale, Neon, Cloudflare |
| CRM & sales | `crm/` | HubSpot, Pipedrive, Attio, Close |
| Support | `support/` | Zendesk, Intercom, Front, Freshdesk |
| Project & knowledge | `workspace/` | Notion, Airtable, Asana, Monday, ClickUp, Coda |
| Design & creative | `creative/` | Figma, Canva, Framer, Webflow, Excalidraw |
| Admin & identity | `identity/` | Okta, Auth0, Clerk, Keycloak, JumpCloud |
| Fintech & billing | `fintech/` | Stripe, Wise, Revolut, Plaid, Brex, Ramp, Mercury |
| Commerce admin | `commerce/` | Shopify, BigCommerce, Squarespace, Wix |
| Infrastructure & cloud | `cloud/` | AWS, GCP, Azure, Cloudflare, Netlify, Fly |
| Design-system standards | `system-docs/` | Fluent 2, Spectrum, Uber Base, Gestalt, Lightning (SLDS), Geist, Wise |
