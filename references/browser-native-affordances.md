# Browser-native affordances

Applies to: every surface. The default instinct in a premium design system is to replace the
browser's controls with a bespoke one. On a B2B console that instinct is usually a mistake, and
the cost lands on keyboard users, screen reader users, and international users first.

## The economics of replacing a native control

WCAG **SC 4.1.2 Name, Role, Value** (Level **A**) is the governing criterion, and its intent text
is the whole argument:

> When standard controls from accessible technologies are used, this process is straightforward.
> If the user interface elements are used according to specification the conditions of this
> provision will be met. … **If custom controls are created**, however, or interface elements are
> programmed … to have a different role and/or function than usual, **then additional measures need
> to be taken** to ensure that the controls provide important and appropriate information to
> assistive technologies and allow themselves to be controlled by assistive technologies. [S1]

The ARIA Authoring Practices Guide says the same about its own reference implementations. On the
select-only combobox example, W3C prints a warning banner above the code: "The code in this example
is not intended for production environments… **There may be support gaps in some browser and
assistive technology combinations, especially for mobile/touch devices.** Testing code based on this
example with assistive technologies is essential before considering use in production systems"
[S2]. It also points at the principle by name: "Robust accessibility can be further optimized by
choosing implementation patterns that maximize use of semantic HTML and heeding the warning that
**No ARIA is better than Bad ARIA**." [S2]

The API surface you inherit for free with a native control is: the accessible name, the role, all
state transitions, the platform keyboard bindings, the touch behaviour, the OS-level text services,
autofill, high-contrast/forced-colors rendering, translation of the built-in UI, and screen-reader
announcement of state changes. A bespoke combobox must re-implement every one of those.

**House rule (judgement, not sourced):** replace a native control only when one of these is true —
(a) the design genuinely cannot be expressed with the native control at any acceptable quality,
(b) you are prepared to test on the assistive technologies you claim to support, or (c) the native
control's own limitations are documented below and accepted. "We couldn't style it" is not a
reason.

## `<select>` vs the custom combobox

MDN: "The `<select>` element represents a control that provides a menu of options" [S3], and it is
Baseline widely available since July 2015 [S3]. It accepts `autocomplete`, `disabled`, `form`,
`multiple`, `name`, `required`, `size` and `open` [S3].

Three facts that should end the debate in most cases:

1. **The native single-select already is a combobox to assistive technology.** APG: "in some
   browsers, an HTML `select` element with `size="1"` is presented to assistive technologies as a
   combobox" [S4].
2. **The custom version is measurably behind, by W3C's own account.** APG's select-only combobox
   example is "functionally similar to an HTML select element", but is used for illustration only
   and carries the support-gap warning above [S2]. The APG pattern's own note for a non-editable
   combobox is that pressing a printable character "optionally moves focus to a value that starts
   with the typed characters" [S4] — *optional*, i.e. not guaranteed, whereas typeahead on a native
   select is the platform's job.
3. **The keyboard contract you must implement by hand.** APG's combobox keyboard interaction, when
   focus is in the combobox [S4]: `Down Arrow` moves focus into the popup; `Up Arrow` (optional)
   places focus on the last focusable element in the popup; `Escape` dismisses the popup and
   optionally clears the combobox if it was already hidden; `Enter` accepts an autocomplete
   suggestion; printable characters type. And: "the popup indicator icon or button (if present),
   the popup, and the popup descendants are **excluded from the page Tab sequence**" [S4]. Every
   one of those is a chance to ship a keyboard trap.

**Where the native control genuinely loses** (house judgement, not sourced): cross-region teams
in a "select all that apply" filter with 40+ options; any listbox needing multi-column layout,
token chips with per-option removal, or rich option descriptions; a list longer than the viewport
with built-in search. If you lose on those, you owe the full APG contract plus assistive-technology
testing — not just a matching visual.

## `<input type="date">` and `<dialog>`

**Date input** (Baseline since April 2021) has two behaviours that matter. **The value is canonical
regardless of locale**: "The value is normalized to the format `yyyy-mm-dd`… includes the year,
month, and day, but not the time" [S5]. **The display follows the user, the parsing does not**: "the
**displayed** date format will differ from the actual value — the displayed date is formatted based
on the **locale of the user's browser**, but the parsed value is always formatted `yyyy-mm-dd`" [S5].
That is a localisation feature, not a limitation (`i18n-rtl.md`), and the platform picker handles
date ranges, non-Gregorian calendars and locale-appropriate field order for free.

Where it genuinely falls short: range selection, inline validation messaging against the control,
and fiscal/period pickers ("Q3 FY26"), which are not calendar dates. Those are reasons to build a
picker — and building a picker means implementing the calendar grid keyboard contract.
**House rule (judgement, not sourced):** for a plain "choose one date" field on a B2B form, ship
`<input type="date">`. It is localisable, accessible, autofillable, and known to the OS user.

**`<dialog>`** (Baseline since March 2022) gives you four things:

- **`showModal()` makes the rest of the document inert.** MDN on `inert`: "Modal `<dialog>`s
  generated with `showModal()` escape inertness, meaning that they don't inherit inertness from
  their ancestors" [S7]. APG from the user's side: "Windows under a modal dialog are inert… modal
  dialogs contain their tab sequence. That is, Tab and Shift+Tab do not move focus outside the
  dialog" [S8].
- **Platform dismiss paths are already defined.** `closedby` documents three methods — light dismiss,
  "a platform-specific user action, such as pressing the **Esc** key on desktop platforms, or a
  'back' or 'dismiss' gesture on mobile platforms", and a developer-specified mechanism [S6]. Values
  `any`, `closerequest`, `none`; the default is `closerequest` for `showModal()`, `none` otherwise [S6].
- **Top-layer rendering.** Popovers when open "will appear above all other elements in the **top
  layer**, and won't be influenced by parent elements' position or overflow styling" [S9] — the
  z-index war in `references/z-index-layers.md` is a problem a native dialog does not have.
- **Two hard rules.** "The `tabindex` attribute **must not** be used on the `<dialog>` element", and
  "It is recommended to use the `.show()` or `.showModal()` methods … rather than the `open`
  attribute", which yields a non-modal dialog [S6].

Still yours: initial focus target, focus restoration to the trigger on close, the heading that names
the dialog, and the destructive-confirm pattern (which wants `alertdialog` — "a special-case dialog
role designed specifically for dialogs that divert users' attention to a brief, important message"
[S8]). `popover` is the sibling for non-modal surfaces: values `auto`, `hint`, `manual`; `auto`
popovers
are light-dismissible and generally close one another, `manual` popovers require explicit show/hide
[S9].

## Autofill and passkeys

**Autofill is a feature you get only by not breaking it.** "The `autocomplete` attribute provides a
hint to the user agent specifying how to, or indeed whether to, prefill a form control. The attribute
value is either the keyword `off` or `on`, or an ordered list of space-separated tokens" [S10]. The
grammar is load-bearing for B2B forms: `autocomplete="section-user1 billing postal-code"` is valid
[S10]. If the same token list appears in more than one control all occurrences get the same value,
while "some autocomplete values may need to be re-used multiple times… such as the `postal-code`
token in a form that contains both shipping and billing addresses" [S10]. The precondition: user
agents "might require `<input>` / `<select>` / `<textarea>` elements to have a `name` and/or `id`
attribute, to be descendants of a `<form>` element, and to be owned by a form with a submit button"
[S10].

**House rules (judgement, not sourced):** never ship `autocomplete="off"` on a first-party account
or billing form; give every account field the right token (`email`, `name`, `given-name`,
`family-name`, `organization`, `new-password`, `current-password`, `one-time-code`) and every field
a `name`, since name/id absence is a documented reason autofill may not fire [S10]; do not rebuild
the password field; and make sure the login form's `type`/`name` and native constraint validation are
correct, because that is what lets the manager offer to fill.

**Passkeys.** WebAuthn is Baseline widely available since September 2021 and "available only in secure
contexts (HTTPS)" [S11]. MDN states why it is the right default: it "enables strong authentication
with public key cryptography, enabling passwordless authentication and secure multi-factor
authentication (MFA) without SMS texts", with "**Protection against phishing**: An attacker who
creates a fake login website can't login as the user because the signature changes with the origin
of the website" [S11]. So offer enrolment and sign-in **as native platform UI** via
`navigator.credentials`, with a password path retained. Do not rebuild the ceremony in your own
modal — the account chooser, transport selection, and cross-device QR/hybrid flow are the platform's
contribution, and re-implementing them degrades the phishing resistance that is the reason to use
passkeys [S11].

## User-preference media features

Five features, all Baseline, all set by the user rather than the brand.

| Feature | Values | Baseline | What the platform does |
|---|---|---|---|
| `prefers-reduced-motion` | `no-preference`, **`reduce`** | Jan 2020 [S12] | Detects a setting "to minimize the amount of non-essential motion… the user prefers an interface that removes, reduces, or replaces motion-based animations. Such animations can trigger discomfort for those with **vestibular motion disorders**. Animations such as scaling or panning large objects can be vestibular motion triggers." |
| `prefers-color-scheme` | `light`, `dark` | Jan 2020 [S13] | `light` means the user prefers a light theme, **or has not expressed an active preference**. |
| `prefers-contrast` | `no-preference`, `more`, `less`, `custom` | May 2022 [S14] | `custom` "will match the color palette specified by users of `forced-colors: active`". |
| `forced-colors` | `none`, **`active`** | Sep 2022 [S15] | "the browser enforces a user-chosen limited color palette"; example is Windows High Contrast. |
| `color-scheme` (property) | `normal`, `light`, `dark`, `light dark`, `only light` | Jan 2022 [S16] | UA recolours **the chrome**: canvas surface, scrollbars and other interaction UI, **form controls**, and other browser-provided UI such as spellcheck underlines. |

Two consequences that are easy to miss. **MDN splits the responsibility explicitly**: `color-scheme`
handles the chrome, and "**Component authors must use the `prefers-color-scheme` media feature** to
support the color schemes on the rest of the elements" [S16] — so `color-scheme: dark` without
`prefers-color-scheme` support is a half-dark page. And **`forced-colors: active` overrides author
colours at paint time, not in the cascade**: affected properties "are treated as if they have no
author-level values specified… The browser-specified values do not affect the style cascade; the
values are instead forced by the browser at paint time", covering `color`, `background-color`,
`border-color`, `outline-color` and others [S15]. The survival strategy is the `<system-color>` type:
"authors should use colors from the `<system-color>` type for all properties that are not in the set
of properties whose colors are overridden" [S17].

**House rules (judgement, not sourced):** `prefers-reduced-motion: reduce` must remove or replace
translation, scale, parallax, and auto-playing carousel motion — not merely shorten durations, since
MDN's phrasing is "removes, reduces, **or replaces**" [S12]. Default to light tokens, override for
`prefers-color-scheme: dark`, and pair with `color-scheme: light dark` so scrollbars, form controls
and the canvas agree [S13][S16]. Every token that must survive forced colors carries a
`<system-color>` fallback, and forced-colors is in the contrast-verification matrix.

## Skinning, download, and print

**`appearance` is the escape hatch *and* the trap.** MDN: "The `appearance` CSS property specifies
the rendered appearance of replaced UI widget elements such as form controls", most commonly native
platform styling "or a primitive appearance with styles that can be overridden using CSS" [S18];
values include `auto`, `none`, `menulist-button`, `textfield`, `base-select` [S18]. The cost of
`appearance: none` is in `accessibility-web.md`: the control stops being exempt from **SC 1.4.11**
(3:1, Level **AA**), because the exemption is for components "whose appearance is determined by the
user agent and **not modified by the author**" [S19]. Skin it and you own every state: default,
hover, focus, active, checked, disabled, invalid, forced-colors. **House rule (judgement, not
sourced):** `appearance: none` only for checkbox, radio and toggle, where the platform affordance
has no acceptable appearance; leave `select`, `date`, `range`, `progress` and `button` alone, or ship
the unskinned state in forced-colors mode.

**Download.** `download` "Causes the browser to treat the linked URL as a download. Can be used with
or without a filename value" [S20]; without a value the name is derived from `Content-Disposition`,
the final URL segment, or the media type, with `/` and `\` converted to underscores [S20]. Two hard
constraints: **`download` only works for same-origin URLs, or the `blob:` and `data:` schemes**, and
"If the header specifies a filename, it takes priority over a filename specified in the `download`
attribute" [S20]. A console's CSV/JSON export must therefore generate through a `blob:` URL, never a
`fetch` to a signed cross-origin URL. And the browser may prompt, save silently, or open the file
elsewhere — "The user may be prompted before a download starts, or the file may be saved
automatically, or it may open automatically" [S20] — so an export must not depend on navigation
happening.

**Print.** MDN lists four reasons a surface cares: "the size and shape of the paper", different styles
for paper, higher-resolution images, and "presenting a specially-formatted version of your content
before printing begins" [S21]. The mechanism is a print stylesheet
(`<link href="/print.css" media="print" rel="stylesheet">`), `@media print` for overrides, and
`@page` for "the page's dimensions, orientation, and margins" [S21]. MDN's caution:
"**specificity and precedence rules still apply**" [S21], so print overrides need weight; browsers also
fire `beforeprint` and `afterprint` [S21]. For a console, print is an export feature — invoice,
invoice schedule, audit-log extract, runbook. **House rule (judgement, not sourced):** a print
stylesheet exists that drops sticky headers, bulk-action bars and column controls, expands collapsed
cells to full values, and prints the current filter state — the user cannot see the on-screen state
and cannot know what they are about to put on paper.

## Decision table

| Need | Use the native | Replace when |
|---|---|---|
| Pick one of ≤40 options | `<select>` | never, for aesthetics |
| Pick several of many | `<select multiple>` or checkboxes | >40 options, or multi-column/rich options, and you will test with AT |
| One date | `<input type="date">` | range, fiscal period, or inline validation messaging |
| Blocking confirmation | `<dialog>` + `showModal()` | never |
| Non-modal surface | `popover` / `<dialog>.show()` | never |
| Login / payment / identity | native inputs + `autocomplete` + `type` | never |
| Authentication | WebAuthn via `navigator.credentials` + password fallback | never |
| Checkbox / radio / toggle | native, `appearance: none` allowed | never |
| Export | `blob:` URL + `download` | never |
| Paper output | `@media print` + `@page` | never |

## Not found

- **A sourced rule for the point at which a native `<select>` becomes unusable.** APG identifies
  the combobox pattern's scenario as "The value must be one of a predefined set of allowed values"
  and notes "the listbox and menu button patterns are also useful in this scenario" [S4], but no
  primary source publishes an option-count threshold. This is a house judgement.
- **Any WCAG success criterion that mandates using native controls.** 4.1.2 mandates the
  *outcome* — programmatically determinable name, role, and settable state [S1]. Nothing in
  WCAG 2.2 says "use `<select>`". The native-control argument is 4.1.2's intent text plus APG's
  support-gap warning [S1][S2], not a normative requirement.
- **A numeric threshold for `prefers-reduced-motion` coverage** — i.e. how much animation may
  remain. MDN specifies the mechanism and the rationale [S12]; no source publishes a permitted
  residue.
- **MDN's `download` attribute page at the canonical Attributes URL returned 404 at time of
  access**; content above is cited from the `<a>` element reference where the attribute is
  documented, which is the same normative text.

## Sources

All W3C and MDN pages **accessed 2026-10-05**. Brackets give the claim each supports.

- **[S1]** https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html — W3C WAI, *SC 4.1.2, Level A*. [standard HTML meets it when used to spec; custom controls need additional measures]
- **[S2]** https://www.w3.org/WAI/ARIA/apg/patterns/combobox/examples/combobox-select-only/ — W3C WAI, ARIA APG, *Select-Only Combobox Example*. ["not intended for production"; support gaps on mobile/touch; AT testing required; "No ARIA is better than Bad ARIA"]
- **[S3]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/select — MDN, *select*, Baseline since Jul 2015. [semantics; attribute set]
- **[S4]** https://www.w3.org/WAI/ARIA/apg/patterns/combobox/ — W3C WAI, ARIA APG, *Combobox Pattern*. [`size="1"` select presented as combobox; select-only vs editable; full keyboard contract; popup excluded from Tab sequence; optional typeahead]
- **[S5]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/date — MDN, *input type="date"*, Baseline since Apr 2021. [`yyyy-mm-dd` normalisation; display vs parse locale split; `min`/`max`; `valueAsNumber`]
- **[S6]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog — MDN, *dialog*, Baseline since Mar 2022. [`showModal()`/`show()`; `closedby` values and defaults; Esc and mobile dismiss gestures; "tabindex must not be used"; `open` yields non-modal]
- **[S7]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert — MDN, *inert*, Baseline since Apr 2023. [removed from tab order and accessibility tree; `showModal()` escapes inherited inertness]
- **[S8]** https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ — W3C WAI, ARIA APG, *Dialog (Modal) Pattern*. [inert windows; Tab contained; no focus escape; `alertdialog`; positive `tabindex` discouraged]
- **[S9]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/popover — MDN, *popover*, Baseline-new since Apr 2024. [`auto`/`hint`/`manual`; light dismiss; top layer independent of parent position/overflow]
- **[S10]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete — MDN, *autocomplete*. [token grammar; `off`/`on`; form-owner inheritance; `name`/`id`/`<form>`/submit preconditions; repeated and sectioned tokens]
- **[S11]** https://developer.mozilla.org/en-US/docs/Web/API/Web_Authentication_API — MDN, *Web Authentication API*, Baseline since Sep 2021, secure contexts only. [public-key auth without SMS; phishing protection via origin-bound signatures]
- **[S12]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion — MDN, *prefers-reduced-motion*, Baseline since Jan 2020. [`reduce`/`no-preference`; vestibular disorders; scaling and panning as triggers]
- **[S13]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme — MDN, *prefers-color-scheme*, Baseline since Jan 2020. [`light`/`dark`; `light` as no-preference default; embedded SVG/iframe; override patterns]
- **[S14]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-contrast — MDN, *prefers-contrast*, Baseline since May 2022. [`no-preference`/`more`/`less`/`custom`; `custom` matches `forced-colors: active`]
- **[S15]** https://developer.mozilla.org/en-US/docs/Web/CSS/@media/forced-colors — MDN, *forced-colors*, Baseline since Sep 2022. [`none`/`active`; forced at paint time not in the cascade; the list of overridden properties]
- **[S16]** https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme — MDN, *color-scheme*, Baseline since Jan 2022. [UA-recoloured chrome list; "authors must use prefers-color-scheme"; `only light`]
- **[S17]** https://developer.mozilla.org/en-US/docs/Web/CSS/system-color — MDN, *system-color*. [system colours for forced colors; use for all non-overridden properties]
- **[S18]** https://developer.mozilla.org/en-US/docs/Web/CSS/appearance — MDN, *appearance*, Baseline since Mar 2022. [native vs overridable primitive; `auto`/`none`/`menulist-button`/`textfield`/`base-select`]
- **[S19]** https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html — W3C WAI, *SC 1.4.11, Level AA*. [3:1; the "not modified by the author" exemption; do-not-round]
- **[S20]** https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a — MDN, *a*, Baseline since Jul 2015, `download` section. [filename derivation and `/`→`_`; same-origin / `blob:` / `data:` only; `Content-Disposition` precedence; browser-dependent prompting]
- **[S21]** https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_media_queries/Printing — MDN, *Printing*. [the four use cases; `media="print"`; `@media print` and `@page`; specificity still applies; `beforeprint`/`afterprint`]