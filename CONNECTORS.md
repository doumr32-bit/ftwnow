# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. FTWNOW describes workflows in terms of categories rather than specific products, so you can use your preferred tools.

## Connectors for this plugin

| Category | Placeholder | Default Server | Other Options |
|----------|-------------|----------------|---------------|
| Docs | `~~docs` | Notion | Confluence, Google Docs, Coda |
| Project Tracker | `~~project tracker` | Linear | Jira, Asana, Monday, Shortcut |
| Design Tool | `~~design tool` | Figma | Sketch, Penpot, Adobe XD |
| Deploy Platform | `~~deploy platform` | Vercel | Netlify, Cloudflare Pages, Railway |

## Fixed connectors (not swappable)

These tools are core to the FTWNOW methodology and cannot be replaced:

| Tool | Reason |
|------|--------|
| **Supabase** | Backend infrastructure — migrations, RLS policies, Edge Functions, DB auditing are deeply integrated into Phase 4-6 |
| **GitHub** | Source control — branching strategy, PR workflow, dev log storage, auto-commit are built into the methodology |

## Customization

After installing this plugin, use the `cowork-plugin-customizer` skill to swap default connectors for your preferred tools. For example, replace Linear with Jira, or Notion with Confluence.
