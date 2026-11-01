# File upload

Applies to: avatar and logo upload, CSV import, attachments on tickets and records, bulk document upload,
exports.

## Dropzone vs button

Both are always available in a well-built surface. GOV.UK: "To upload a file, the user can either use the
'Choose file' button [or] drag and drop a file into the file upload input area"
(https://design-system.service.gov.uk/components/file-upload/).

The drop zone's properties are the design decision:

- GOV.UK's **improved** File upload component (March 2025, opt-in feature flag) exists to make the
drop zone "**bigger**, **visible at all times**, and **more visually responsive to user interactions**". The
previous component did not solve it: the earlier version "does not show a visual target area when dragging
and dropping a file. The component inherits and uses the browser's default behaviour" — tracked as GOV.UK
Frontend issue #3685.
- The improved component also replaced the 'Choose file' button styling "to be more consistent with
the secondary button in the Button component", and made all component text translatable.

**The architectural note that bites:** the improved component is built by JavaScript. "JavaScript creates
the improved version of the component out of the input (`<input type="file">`) and then **hides the input
from the user**. The improved version consists of a `<button>` with a few `<span>` elements inside." So
every attribute has a defined destination:

| Attribute | Where it must live | Why |
|---|---|---|
| `id` | input — and is **renamed** on the input | "added to the button and renamed on the input" |
| `disabled` | input | "copied and synchronised with any changes that happen on the input" |
| `aria-describedby` | input | copied |
| `name`, `accept`, `capture`, `accesskey` | input | "they only work in the input (and not the button)" |
| `multiple` | input | "also changes the behaviour of the button as text is added when multiple files are selected" |
| anything else | parent `<div>` or JS onto the button | "you'll have to add them either to the parent `<div>` or through JavaScript to the button" |

*(all from https://design-system.service.gov.uk/components/file-upload/)*

One gap to carry into review: "Screen readers will not read out the `required` attribute in the improved
version" — consistent with GOV.UK's own recommendation not to use `required`
(https://design-system.service.gov.uk/patterns/validation/).

## Drag-and-drop accessibility

Drag-and-drop is an enhancement layered over a real button. GOV.UK's own research identifies the failure mode:

> "Users of Dragon, a speech recognition tool, **cannot activate their browser's native file inputs**
> by using commands for interacting with web page controls. They have to rely on mouse commands or
> keyboard commands, which take multiple steps to activate the component."

*(https://design-system.service.gov.uk/components/file-upload/, citing GOV.UK Frontend issue #3686)*

So:

- The clickable button is the primary path; the drop zone is never the only path.
- Do not make the dropzone a `div` with a click handler and no keyboard equivalent.
- GOV.UK's improved component exists partly to fix this — "users can say commands for interacting
with web page controls to choose files" — but notes a residual limit: "due to browser security features,
this may not work right away or on subsequent interactions on the same page. If users cannot interact with
the component, they'll first need to perform another action, such as a mouse click." (That page links MDN's
User Activation documentation.)

**Not found:** WCAG success-criterion numbers or conformance levels for drag-and-drop file upload in
the sources consulted. What would settle it: a W3C technique page specific to drag-and-drop file upload.
Until then, treat keyboard-operability of the button as the non-negotiable and log the dropzone as
progressive enhancement.

## File type and size validation

**Client-side `accept` filters the picker; it does not validate.** MDN: the `accept` value is "a
comma-separated list of unique file type specifiers", each of which may be a case-insensitive file extension
(`.jpg`, `.pdf`), a MIME type string, or one of `audio/*`, `video/*`, `image/*`. MDN warns: "Because a given
file type may be identified in more than one manner, it's useful to provide a thorough set of type
specifiers when you need files of a given format"
(https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file).

Also from MDN: `multiple` permits more than one selection; `capture` (`user` / `environment`) requests a
camera; and the input's `value` is "always the file's name prefixed with `C:\fakepath\`, which isn't the
real path of the file".

Validation is server-side, and every failure gets a specific message. GOV.UK's templates, verbatim
(https://design-system.service.gov.uk/components/file-upload/):

| State | Message |
|---|---|
| nothing selected | `Select a [thing]` — e.g. "Select a report" |
| wrong type | `The selected file must be a [list]` — e.g. "must be a CSV or ODS" |
| too large | `The selected file must be smaller than [size]` — e.g. "smaller than 2MB" |
| empty file | `The selected file is empty` |
| virus | `The selected file contains a virus` |
| password protected | `The selected file is password protected` |
| transport failure | `The selected file could not be uploaded – try again` |
| too many files | `You can only select up to [n] files at the same time` |
| wrong template | `The selected file must use the template` |

"Make sure errors … have **specific error messages for specific error states**." A generic "Upload failed"
is the failure mode this table exists to prevent.

Also: only ask for an upload "if it's critical to the delivery of your service", and let users reuse a
previously uploaded file "within a single journey, unless doing so would be a major security or privacy
concern" — while considering shared-device exposure before previewing or downloading it.

## Progress

**Not found:** MDN's `XMLHttpRequest` upload-progress documentation at both URLs consulted
(`/Web/API/XMLHttpRequest/upload_event` and `/Web/API/XMLHttpRequestUploadEvent`) returned HTTP 404 on
2026-10-05, and GOV.UK's file upload guidance contains no progress-bar pattern. What would settle it: the
MDN page documenting `XMLHttpRequest`'s `upload` property and the `ProgressEvent` it fires, or an equivalent
Fetch Streams / upload-progress reference. No attribute names or numeric thresholds for progress are
asserted here as a result.

What is sourced, and therefore binding:

- Any size or count limit must be **stated before** selection — GOV.UK's own messages are "must be
smaller than 2MB" and "up to 10 files at the same time", so the limit is part of the field's hint, not a
surprise discovered after selection.
- Failure must be recoverable: the message is "could not be uploaded – **try again**", not a dead end.
- Per-file state must be visible for multi-file selection, because `multiple` changes the button's
text as files are added (GOV.UK: `multiple` "also changes the behaviour of the button as text is added when
multiple files are selected").

Decide progress thresholds per surface and record them; do not attribute numbers to a source.

## Resumable upload

**Not found:** no resumable or chunked-upload guidance exists in GOV.UK Design System, the ARIA APG,
or MDN's file-input reference. What would settle it: an authoritative protocol specification (e.g. the tus
resumable-upload spec) or a design system with published large-file guidance. Treat the following as
judgement, not sourced fact:

- Progress must be real. A simulated progress bar that stalls is worse than no bar.
- Resuming requires persisted state keyed to file identity (name, size, last-modified), so the
surface can show "Paused — 60% — Resume / Cancel".
- Large-file flows need a resume affordance **before** the user leaves, not only after a failure.
- Never lose the user's other form data when an upload fails.

## The state list

Use this as the row-state model for any file list. Every state needs a visible label and an available
action; a spinner with no text is a state nobody can act on.

| # | State | What the user sees | Action available |
|---|---|---|---|
| 0 | **idle** | dropzone + button; accepted types and limits in the hint | choose file |
| 1 | **dragging** | dropzone highlight — "more visually responsive to user interactions" | — |
| 2 | **validating** (client-side) | inline spinner on the row | cancel |
| 3 | **chosen** | filename + size; `multiple` accumulates rows | remove, re-choose |
| 4 | **rejected — client-side** | specific error: type, size, count, empty | correct and re-choose |
| 5 | **rejected — server-side** | the GOV.UK error table, including virus / password / template | try again |
| 6 | **uploading** | progress with percentage and bytes; row must not vanish | cancel |
| 7 | **paused** (if resumable) | "Paused at 60%" | resume, cancel |
| 8 | **uploaded** | persisted filename, size, and a remove control | remove (before submit) |
| 9 | **processing** (post-upload) | "Processing…" when the server needs time beyond transport | — |
| 10 | **failed** | "could not be uploaded – try again" | retry, cancel |

States 3 → 6 are the ones most often skipped: a chosen-but-not-yet-transferred file needs a visible row and
a remove control, or the user has no way back. State 8's remove control matters most in settings and
checkout, where an uploaded attachment must be revocable before final submit.

## Review checklist

- [ ] Choose-file button is the primary path; dropzone is enhancement.
- [ ] Dropzone is visible at rest, not only on dragover.
- [ ] Every attribute in the table above sits on the input, not the shadow button.
- [ ] `accept` uses a thorough set of specifiers (extensions **and** MIME types).
- [ ] Accepted types and size limits stated in the hint before selection.
- [ ] Each rejection has its own specific message, from the table above.
- [ ] Every row state has a visible label; chosen files are removable.
- [ ] Failure offers retry, not just an error.
- [ ] Shared-device exposure considered before showing a preview/download of an uploaded file.

## Sources

- File upload — GOV.UK Design System — https://design-system.service.gov.uk/components/file-upload/ — accessed 2026-10-05
- Help users to recover from validation errors — GOV.UK Design System — https://design-system.service.gov.uk/patterns/validation/ — accessed 2026-10-05
- `<input type="file">` — MDN Web Docs — https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/file — accessed 2026-10-05
