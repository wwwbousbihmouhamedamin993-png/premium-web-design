# Mobbin Web Ingestion Bridge — setup & usage

Web-platform twin of the premium-mobile-design harvester. Pulls desktop screenshots
off Mobbin app pages into this skill's library:

```
design-systems/<category>/<app>/screens/screen_001.webp, screen_002.webp, ...
```

Categories are auto-detected from the Mobbin page and normalized to this library's
taxonomy (`devtools`, `observability`, `data-bi`, `backend`, `crm`, `support`,
`workspace`, `creative`, `identity`, `fintech`, `commerce`, `cloud`). Unknown
categories get their own folder; `system-docs/` is never auto-routed.

## 1. Start the bridge

Double-click **`start_bridge.bat`** (or run `python ingest_bridge.py`).
It listens on **http://127.0.0.1:3848** and prints saves as they happen.
The mobile bridge (port 3847) can run at the same time — they don't collide.

Health check: open http://127.0.0.1:3848/health

## 2. Install the bookmarklet

1. Open `mobbin_web_harvester_bookmarklet.txt` and copy the whole
   `javascript:...` one-liner (or build/rebuild it: `python build_bookmarklet.py`).
2. Create a new browser bookmark (Ctrl+D on any page → edit), name it
   e.g. `Mobbin Web → Design System`, paste the one-liner as the URL.

## 3. Harvest

1. Open a Mobbin **web** app page — `https://mobbin.com/apps/<slug>-web`.
2. Click the bookmark. It auto-scrolls the gallery, grabs the highest-res
   (unblurred) `bytescale.mobbin.com` variant of every screen, drops
   placeholders, and POSTs the zip to the bridge.
3. The overlay reports: `Saved N new web screens (M duplicates skipped) into
   design-systems/<category>/<app>/screens`.

Duplicate screens (any bytes already in the folder, including the named
`*.webp` files) are skipped by SHA256 — re-running is always safe.

## Fallback (bridge not running)

If the bridge is down, the bookmarklet downloads
`<app>__<category>__webscreens.zip` to your Downloads folder instead. Next time
the bridge starts, its Downloads watcher auto-extracts any `*__webscreens.zip` /
`webmobbin__*.zip` and deletes the archive. It ignores mobile archives
(`__screens`, `flow__`, `pageflows__`), so the mobile watcher and this one
can watch Downloads simultaneously without stealing each other's files.

## Files

| File | Purpose |
|---|---|
| `ingest_bridge.py` | HTTP bridge on 127.0.0.1:3848 (ZIP + JSON modes) |
| `watch_downloads.py` | Downloads-folder watcher (web archives only) |
| `start_bridge.bat` / `stop_bridge.bat` | Start / stop the bridge |
| `mobbin_web_harvester.js` | Bookmarklet source (readable) |
| `build_bookmarklet.py` | Rebuilds the one-liner from the source |
| `mobbin_web_harvester_bookmarklet.txt` | Installable one-liner |
| `refresh_registry.bat` | Rebuild `app_registry.json` from `design-systems/` |
| `app_registry.json` | app slug → screens path lookup table |
