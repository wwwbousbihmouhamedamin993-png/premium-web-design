# Routing & the navigation model

Route structure is the skeleton of a logged-in app: it decides what a deep link resolves to,
where the layout chrome lives, and whether browser Back means anything. Framework APIs differ;
the invariants do not. Examples use React Router's route config API because it names these
concepts explicitly.

## Rules

- **One layout owns the chrome.** A layout route "create[s] new nesting for their children, but
  they do not add any segments to the URL" (React Router, *Routing*). Put the shell header, the
  sidebar, and the toast region in a layout route, never in a page route.
- **Nested route segments compose.** "The path of the parent is automatically included in the
  child," so `route("dashboard", ...)` with a child `route("settings", ...)` yields both
  `/dashboard` and `/dashboard/settings` (React Router, *Routing*).
- **Index routes are the default child.** They "render into their parent's `<Outlet/>` at their
  parent's URL (like a default child route)" and "can't have children" (React Router, *Routing*).
  A collection URL (`/projects`) therefore needs an index route; `/projects/` with no index route
  is a 404 by construction.
- **Breadcrumbs are secondary, never a replacement.** Carbon: breadcrumbs "are always treated as
  secondary and should never entirely replace the primary navigation," and shouldn't be used for
  single-level products because "they create unnecessary clutter." For a multi-step process, use a
  progress indicator instead.
- **Breadcrumbs state where you are, not how you got here.** Carbon supports two variants:
  *location-based* (illustrate the site's hierarchy) and *path-based* (the actual steps taken,
  always dynamically generated). "The breadcrumb variant used should be consistent across a
  product."
- **Breadcrumb truncation never wraps.** "The first and last two page links should be shown, but
  the remaining breadcrumbs in between are condensed into an overflow menu. Breadcrumbs should
  never wrap onto a second line" (Carbon, *Breadcrumb*).
- **The current page is not a link.** "By default, the current page is not listed in the breadcrumb
  trail." If it is listed, it is last and not interactive.
- **Splat routes carry the 404.** A `*` route is the catchall: React Router's own example throws
  `new Response("Page not found", { status: 404 })` from it. Never redirect an unmatched route to
  app home — a deep link must land on content or on an honest 404, not a silent relocation.
- **Filter and sort state belongs in the URL.** Carbon's global-header pattern recommends
  tracking "the essential state elements in the URL and return the user to that URL automatically
  when they return." Query state is carried by `URLSearchParams`, which defines "utility methods
  to work with the query string of a URL" and exposes `get`/`set`/`delete`/`has`/`getAll` (MDN,
  `URLSearchParams`, accessed 2026-10-05).
- **Use `set()`, not `append()`, for a filter.** `URLSearchParams.set()` "sets the value
  associated with a given parameter"; `append()` "adds a specified key/value pair as a new search
  parameter" (MDN). Appending a filter on every change produces `?status=open&status=failed`
  instead of replacing it.
- **Multi-value state uses `getAll()`.** `get()` "returns the first value associated with the given
  search parameter"; `getAll()` "returns all the values" (MDN).
- **Back and Forward must be real.** `history.pushState()` "adds a new entry to the session
  history" while `replaceState()` "updates the session history entry for the current page" (MDN,
  *Working with the History API*). Use `pushState` for navigations a user would expect to undo,
  `replaceState` for filter/sort refinement of the current view — otherwise Back walks through
  every checkbox click.

## Layout and route skeleton

```
root.tsx                 # shell: header, nav landmarks, toast region — no URL segment
└── layout(app)          # app layout, no segment
    ├── index            # /app → homepage template
    ├── projects         # index route → collection list at /app/projects
    │   └── :projectId   # /app/projects/:projectId → detail
    └── settings         # /app/settings → settings template
*                        # splat → 404
```

| Concept | Route API | URL effect | Use for |
|---|---|---|---|
| Root | `root.tsx` | wraps everything | document, landmarks |
| Layout | `layout()` | none | sidebar, page chrome |
| Index | `index()` | parent's URL | the parent's default view |
| Dynamic | `:param` | one segment | record identity |
| Optional | `:lang?` | segment may be absent | locale / variant |
| Splat | `*` | remainder | 404, file paths |

## Route-level code splitting

Route modules "define: automatic code-splitting, data loading, actions, revalidation, error
boundaries, and more" (React Router, *Route Module*). Consequence for design: the shell must render
before any page chunk resolves, or the frame flickers on every navigation.

- **Every route ships its own error boundary.** `ErrorBoundary` "will render instead of the route
  component" when route APIs throw (React Router). A layout-level boundary preserves the shell.
- **Reserve space for the async chunk.** Polaris's `HydrateFallback` pattern (React Router) renders
  immediately in place of the route component while the client loader runs — the design equivalent
  is a skeleton at the route's own density, never a spinner over a bare page.
- **Rendering strategy is a route-level decision.** React Router exposes three — client-side,
  server-side, and static pre-rendering — with `ssr` set globally but individual routes still free
  to pre-render (React Router, *Rendering Strategies*).

**Not found:** a primary-source consensus on how many nested route levels a B2B console should
tolerate before flattening. Carbon's rule ("The left panel does not support three tiers of
navigation") is a component constraint about the left panel, not a whole-IA depth budget. Settled
by: comparative teardown of several production consoles with per-level click counts.

## Sources

- Routing (route config, layout, index, prefix, dynamic, splat) — React Router. https://reactrouter.com/start/framework/routing — accessed 2026-10-05
- Route Module (code splitting, loaders, ErrorBoundary, HydrateFallback) — React Router. https://reactrouter.com/start/framework/route-module — accessed 2026-10-05
- Rendering Strategies — React Router. https://reactrouter.com/start/framework/rendering — accessed 2026-10-05
- Breadcrumb — Carbon Design System (IBM). https://carbondesignsystem.com/components/breadcrumb/usage/ — accessed 2026-10-05
- Global header (pattern: state in URL) — Carbon Design System (IBM). https://carbondesignsystem.com/patterns/global-header/ — accessed 2026-10-05
- `URLSearchParams` — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams — accessed 2026-10-05
- Working with the History API (`pushState` / `replaceState` / `popstate`) — MDN Web Docs. https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API — accessed 2026-10-05
