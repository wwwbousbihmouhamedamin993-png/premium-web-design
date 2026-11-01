# Offline, stale data, sync

Applies to: desktop web product surfaces in B2B SaaS — laptops on VPN, hotel and conference Wi-Fi, captive portals, spotty enterprise proxies. Not mobile offline.

## Framing

Desktop B2B has a specific offline problem: the network reports "connected" while the application cannot reach its API. MDN is blunt about why the platform signal cannot be trusted — "Browsers and operating systems leverage different heuristics to determine whether the device is online. In general, connection to LAN is considered online, even though the LAN may not have Internet access… On Windows, the online status is determined by whether it can reach a Microsoft home server, which may be blocked by firewalls or VPNs, even if the computer has Internet access. Therefore, this property is inherently unreliable, and you should not disable features based on the online status, only provide hints when the user may seem offline" [S1].

That last sentence is the governing rule. **Detection is a hint for the UI, never a gate on functionality.**

## Detection

| Signal | API | Use | Limit |
|---|---|---|---|
| Connection state hint | `navigator.onLine` — boolean, `true` online | Initial hint, and reacting to change | "inherently unreliable"; do not disable features on it [S1] |
| Change events | `online` / `offline` fired on `window` | Toggle an offline banner; trigger reconnection | Fires on heuristic change, not on API reachability [S1] |
| Connection quality | `navigator.connection` → `NetworkInformation` | Downgrade image and payload weight before a request fails | "Limited availability"; also available in Workers [S2] |
| Real reachability | First-party request outcome | The only signal that reflects your API | You own this; no source prescribes a probe endpoint |
| Deferred retry | `SyncManager` via `ServiceWorkerRegistration.sync` | Queue writes for delivery when connectivity returns | "Limited availability"; **secure context only (HTTPS)** [S3] |

`navigator.onLine` fires `online`/`offline` "when its value changes" [S1]. Note MDN's compatibility caveat: "If the browser doesn't support `navigator.onLine` the above example will always come out as `false`/`undefined`" — a missing feature reads as offline, so do not treat the absence of the event as a positive confirmation [S1].

`NetworkInformation` supplies the general connection type for choosing content weight — "This can be used to select high definition content or low definition content based on the user's connection" — and MDN's example switches on `effectiveType`, testing for `"slow-2g"` to skip preloading a video [S2]. It also fires its own `change` event, so connection type can drive a live quality indicator.

## Background reconnection

The Background Synchronization API "enables a web app to defer tasks so that they can be run in a service worker once the user has a stable network connection" [S3]. MDN's own model is an offline-capable mail client: "the application frontend just registers a sync request and the service worker gets alerted when the network is present again and handles the sync" [S3].

Mechanics: register a tag with `registration.sync.register(tag)`; check pending work with `registration.sync.getTags()`; handle `sync` on `ServiceWorkerGlobalScope` and branch on `event.tag` inside `event.waitUntil()` [S3]. The `sync` event "happens as soon as the network becomes available" [S3].

Constraints that shape the design:

- **"Limited availability"** and **secure context only** [S3]. Gate it, and keep a foreground retry path for browsers without it.
- Service workers "are intended… to enable the creation of effective offline experiences, intercept network requests, and take appropriate action based on whether the network is available" [S4]. They "are only available in secure contexts" [S4].

Design consequence from web.dev: **"Don't block content."** "Avoid network requests that block content. Let the user continue to browse your app and queue tasks that will be performed and synced when the connection has improved" [S5]. A full-screen modal blocking on a sync is the failure they are describing.

## Stale data indication

Two distinct affordances, and they are not interchangeable.

**Current-state notice** — the connection is bad *now*. web.dev's model sentence: "You seem to have a bad network connection. Not to worry! Messages will be sent when the network is restored" [S5]. Two components: the state, and the fact that queued work still lands.

**Age-of-data notice** — the record shown may be out of date. web.dev: "Some apps can always show the last time they were updated" [S5]. Material Money is their worked example: it caches rates and is explicitly out-of-date, versus weather and stock apps that "need to auto-update because old data isn't useful" [S5].

That contrast is the rule: **auto-update where stale data is useless; show the timestamp where the user might act on it.** A B2B record list is the second case.

Additional web.dev requirements:

- "Tell the user both the application's state and the actions they can still take when they have a network failure" [S5].
- "Clearly inform the user when a change in state occurs as soon as possible" [S5].
- On reconnection, apps prioritising current information "should auto-update and tell the user as soon as possible"; others "can show a tap-to-update notification informing the user of new content", because "Auto-updating an article would cause users to lose their place" [S5].
- Say whose fault it is: "make it clear whether a connection problem is on your end (by saying 'The network is down') or their end (by saying 'You are disconnected')" [S5].
- Per-element state, not one global grey-out: "Each UI element can have its own context and behavior that changes depending on if it needs a successful connection" — their example browses offline but disables pricing and the Buy button [S5]. web.dev also cautions that "because web design tends to use gray for disabled elements, using grayed UI to show that your app is offline can cause confusion about what the app can do while offline" [S5].
- Never convey state with colour or an icon alone: "Use language, color, and visual components to show a status or change of state. Using only color to show state can be hard for users to notice, or even completely inaccessible to users with visual disabilities" [S5]. On icons: "Be careful when using icons to demonstrate status that might instead be interpreted as a save or download action" [S5].
- Use "action-based language that your audience can relate to" rather than the word "offline", since "Non-technical audiences often misunderstand the word 'offline'" [S5].

Carbon adds the offline banner to its **system-generated** notification category — listed as a use case alongside planned maintenance and session expiry — because these "provide updates on background system status or out-of-context events that have finished" and are not tied to a user's current action [S6].

## Last-synced timestamps

- Show the sync state persistently where the data is consequential: "Tell the user what state their data is in. For example, you can show whether the app has synced" [S5].
- Back it with a real mechanism. Polaris' `s-progress` carries sync semantics directly — their documented example is `<s-progress accessibilityLabel="Inventory synced" value="30" max="100" tone="info">` — and an indeterminate variant labelled "Importing products" for unknown duration [S7].
- Its accessibility requirement is the model to copy for any custom sync indicator: "Always name what is progressing: Set `accessibilityLabel` to something specific… Assistive technology announces a progress bar by its name, and the component never invents one" [S7].
- Polaris progress "is display-only. It isn't form-associated, has no `name`, and never participates in form submission" and "doesn't advance on its own" — the animation is driven by your `value` updates [S7].
- Announce sync completion as a success notification. Polaris `s-banner` lists "success confirmations" among its use cases, exemplified as "Show success messages for important operations like saves or sync" [S8].

**Not found:** a sourced interval, staleness threshold, or refresh cadence for showing "last synced". web.dev establishes that displaying the time is correct [S5]; no source specifies when the value becomes unacceptable to show.

## Optimistic UI with mandatory reversibility

The rule this file asserts: **an optimistic update is only permissible if the user can get back to the pre-update state without losing work.**

Two of the three legs of this are sourced; the third is not.

**Sourced — preserve the user's input and let them correct rather than restart.** NN/g: "Let users correct errors by editing their original action instead of starting over. For example, display the original text entered into a text field even if it does not match the requirements for that field and allow the user to modify it" [S9]. On effort: "If possible, guess the correct action and let users pick it from a small list of fixes" [S9]. Carbon's inline loading states give an optimistic UI its terminal states — inactive, active, finished, error — with the finished state "active for 1.5 seconds before calling an optional function `onSuccess`", and on error "the inline loading component becomes inactive and an inline notification or error handling within the form should appear" [S10].

**Sourced — offline edits must still feel saved.** web.dev: "If a user is editing a document offline, consider changing the feedback design so it's visibly different from when they're online but still shows that their file was 'saved' and will sync when they have a network connection. This educates the user about how your app works and reassures them that their task or action has been stored, which can make them more confident in using their application" [S5].

**Not found — a source stating reversibility as a mandatory property of optimistic updates.** Nothing in Carbon, Polaris, NN/g, MDN or web.dev in this set frames it as a rule. It is the defensible synthesis of the two sourced legs above plus the destructive-action reversibility your project already applies elsewhere, but it is not cited. Settling it would need a design system that documents an optimistic-update pattern — Material Design's data tables or a Shopify Polaris section on mutation feedback — or a primary source on undo semantics.

## Sync conflict resolution

The clear model in the record is GitLab's, and it generalises because the shape of the problem is the same: two versions of the same content, and a user must choose.

GitLab's framing: "Merge conflicts occur when two branches in a merge request, the source and target, have different changes to the same lines of code. In most cases, GitLab can merge changes together, but when conflicts arise, you must decide which changes to keep" [S11].

Four resolution methods, each matched to conflict severity [S11]:

| Method | GitLab's stated fit |
|---|---|
| GitLab Duo (AI) | "Best for automatic, end-to-end conflict resolution" |
| Interactive mode | "Best for conflicts where you only need to select which version of a line to keep" |
| Inline editor | "Suitable for complex conflicts requiring manual edits to blend changes" |
| Command line | "Provides complete control over complex conflicts" |

The transferable pattern is the escalation ladder keyed to conflict size — a field-level two-choice, escalating to a side-by-side editor, escalating to a raw diff — plus their disclosure that some conflicts cannot be resolved in the UI at all, because the file "is a non-binary text file", "is less than 200 KB in size with conflict markers added", "uses UTF-8 compatible encoding", "doesn't contain conflict markers", and "exists under the same path in both branches" [S11]. Anything failing those criteria "must resolve the conflict manually" [S11].

Two UI rules worth lifting: GitLab resolves into the source branch without merging to target, so the user can "review and test the merge commit to verify it contains no unintended changes and doesn't break your build" [S11] — a conflict resolution that cannot be inspected before it lands is not reviewable. And their per-conflict verbs are literal and paired: "Use ours" / "Use theirs" [S11].

Carbon's equivalent at record level, from its error-management classes: when data cannot be surfaced, explain why and what the user can do, using plain language and no codes [S12]. Its **systems** class prescribes "viewing an activity log" as the diagnostic route [S12].

## State table

| Condition | Indicator | Available actions | Never |
|---|---|---|---|
| Online, data fresh | Nothing | All | — |
| Online, request in flight | Skeleton or inline loading per `loading-skeletons.md` | Scoping per region | Unbounded spinner |
| Offline, data cached | Offline notice + last-synced time | Read cached; queue writes | Disabling features on `navigator.onLine` |
| Offline, data not cached | Per-element unavailable state, not global grey-out | Retry when told; leave | Blanking the route |
| Connection degraded | Reduced payload; `effectiveType` driven [S2] | Continue | Blocking modal on sync |
| Reconnected, sync pending | Indeterminate progress, labelled [S7] | Continue working | Clearing the queue silently |
| Reconnected, conflict | Ladder: two-choice → side-by-side → manual [S11] | Choose ours/theirs; inspect before commit | Auto-resolving over a newer edit |
| Sync failed permanently | Inline notification with error terminal [S10] | Retry; copy reference ID | Stack trace or raw server string |

## Announcing connection state

Connection changes are status messages and WCAG 2.1 SC 4.1.3 (AA) applies — they must be "programmatically determined through role or properties such that they can be presented to the user by assistive technologies without receiving focus" [S13]. Use `aria-live="polite"` [S14]; reserve `assertive` for cases where "an interruption may disorient users or cause them to not complete their current task" and is therefore "imperative" — losing connectivity mid-write is close to that bar [S14]. If a region is being repopulated after reconnection, `aria-busy="true"` until the replacement content is in place [S15].

## Not found

- **A rule that optimistic updates must be reversible.** See above — asserted, not sourced.
- **A staleness threshold or refresh cadence** for the last-synced timestamp.
- **Any sourced offline guidance in IBM Carbon or Shopify Polaris.** Neither system documents an offline pattern; the offline material here is web.dev and MDN. Carbon's pattern index has no offline entry and lists "Error states (future)" and "Onboarding (future)" as planned [S12].
- **A conflict-resolution UI spec from a design system.** GitLab's documentation is a product spec, not a design-system pattern; the four-method ladder is read across, not quoted as guidance.
- **Browser support figures** for Background Sync. MDN marks it "Limited availability" [S3]; caniuse or MDN's browser-compatibility table would settle actual coverage.
- **Whether `navigator.connection` is safe in enterprise managed browsers.** MDN marks it "Limited availability" [S2]; an IT-managed-browser inventory would settle it.

## Sources

- **[S1]** https://developer.mozilla.org/en-US/docs/Web/API/Navigator/onLine — Mozilla Developer Network, "Navigator: onLine property" (last modified Feb 15, 2025). LAN/Windows heuristics; "inherently unreliable"; do-not-disable rule; `online`/`offline` events; unsupported-feature caveat. Accessed 2026-10-05.
- **[S2]** https://developer.mozilla.org/en-US/docs/Web/API/Network_Information_API — Mozilla Developer Network, "Network Information API" (page last modified Apr 13, 2025). Limited availability; `Navigator.connection`; `effectiveType` and `"slow-2g"`; `change` event; available in Workers. Accessed 2026-10-05.
- **[S3]** https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API — Mozilla Developer Network, "Background Synchronization API" (page last modified Apr 22, 2024). Limited availability; secure context only; `SyncManager`, `ServiceWorkerRegistration.sync`, tag registration, `sync` event semantics, offline mail-client example. Accessed 2026-10-05.
- **[S4]** https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API — Mozilla Developer Network, "Service Worker API" (page last modified Aug 15, 2026). Proxy-server role; intercepting requests; secure-context requirement. Accessed 2026-10-05.
- **[S5]** https://web.dev/articles/offline-ux-design-guidelines — Google / web.dev, Mustafa Kurtuldu & Thomas Steiner, "Offline UX design guidelines" (Nov 10, 2016). State notices; last-updated display; auto-update vs tap-to-update; whose-fault wording; per-element state; multi-device signalling; skeleton use; don't-block-content; offline-saved feedback; sync state visibility. Accessed 2026-10-05.
- **[S6]** https://carbondesignsystem.com/building-blocks/core/patterns/notifications/ — IBM Carbon Design System, "Notifications" pattern (last updated Aug 12, 2026). System-generated notifications including "A user loses network connection"; status and type sets; banner rules. Accessed 2026-10-05.
- **[S7]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/progress — Shopify, Polaris web components: Progress (v1.1). Determinate vs indeterminate; `value`/`max`; `accessibilityLabel` requirement; inventory-sync example; display-only limitations. Accessed 2026-10-05.
- **[S8]** https://shopify.dev/docs/api/app-home/latest/web-components/feedback-and-status-indicators/banner — Shopify, Polaris web components: Banner (v1.1). Success confirmations for saves and syncs; tone set. Accessed 2026-10-05.
- **[S9]** https://www.nngroup.com/articles/error-message-guidelines/ — Nielsen Norman Group, Tim Neusesser & Evan Sunwall, "Error-Message Guidelines" (May 14, 2023). Preserve the user's input; reduce error-correction effort; effort accelerators. Accessed 2026-10-05.
- **[S10]** https://carbondesignsystem.com/building-blocks/core/components/inline-loading/guidelines/ — IBM Carbon Design System, "Inline loading" component guidelines (last updated Sep 30, 2026). Four states; 1.5s success state; error terminal routing to an inline notification. Accessed 2026-10-05.
- **[S11]** https://docs.gitlab.com/user/project/merge_requests/conflicts/ — GitLab Docs, "Merge conflicts". Conflict definition; four resolution methods with stated fit; UI-resolvability criteria including the 200 KB limit; "Use ours" / "Use theirs"; review-and-test before merge. Accessed 2026-10-05.
- **[S12]** https://carbondesignsystem.com/building-blocks/core/patterns/empty-states/ — IBM Carbon Design System, "Empty states" pattern (last updated Aug 11, 2026). Four error-management classes; plain-language/no-codes rule; "Error states (future)" and "Onboarding (future)"; pattern index with no offline entry. Accessed 2026-10-05.
- **[S13]** https://www.w3.org/WAI/WCAG21/Understanding/status-messages.html — W3C WAI, Understanding SC 4.1.3 Status Messages (Level AA; page updated May 11, 2026). Programmatic determination without focus. Accessed 2026-10-05.
- **[S14]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-live — Mozilla Developer Network, "ARIA: aria-live attribute" (last modified Sep 23, 2025). polite / assertive / off; interruption warning. Accessed 2026-10-05.
- **[S15]** https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy — Mozilla Developer Network, "ARIA: aria-busy attribute" (last modified Jun 23, 2025). Defer announcements until a region finishes updating. Accessed 2026-10-05.
