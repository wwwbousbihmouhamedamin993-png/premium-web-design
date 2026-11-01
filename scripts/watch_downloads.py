#!/usr/bin/env python3
"""
Downloads Folder Auto-Ingestion Watcher (premium-web-design)
Monitors ~/Downloads for exported WEB screens ZIP archives
(`*__webscreens.zip` / `webmobbin__*.zip`).
Automatically unpacks them into design-systems/{category}/{app}/screens/
and deletes the ZIP file from Downloads so zero clutter is left behind.

Pattern-safe with the premium-mobile-design watcher: this one only picks up
web archives (`__webscreens` / `webmobbin__`) and ignores mobile ones
(`__screens`, `flow__`, `pageflows__`), so both bridges can run at once.
"""

import os
import sys
import time
import zipfile
import re
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOADS_DIR = os.path.join(os.path.expanduser('~'), 'Downloads')
REGISTRY_FILE = os.path.join(BASE_DIR, 'scripts', 'app_registry.json')

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def resolve_target_dir(app_slug, registry, category=None):
    try:
        from ingest_bridge import resolve_target_dir as bridge_resolve
        return bridge_resolve(app_slug, registry, category=category)
    except Exception:
        slug_clean = app_slug.lower().strip().replace(' ', '_').replace('-', '_')
        slug_hyphen = slug_clean.replace('_', '-')
        cat = category or 'misc'
        new_rel_path = f"design-systems/{cat}/{slug_hyphen}/screens"
        new_abs_path = os.path.join(BASE_DIR, new_rel_path)
        os.makedirs(new_abs_path, exist_ok=True)
        return new_abs_path, new_rel_path

def process_zip(zip_path):
    filename = os.path.basename(zip_path)
    base_name = os.path.splitext(filename)[0]

    # Wait until file is done downloading (size stable, readable)
    for _ in range(10):
        try:
            size1 = os.path.getsize(zip_path)
            time.sleep(0.3)
            size2 = os.path.getsize(zip_path)
            if size1 == size2 and size1 > 0:
                # Test opening zip
                with zipfile.ZipFile(zip_path, 'r') as test_z:
                    _ = test_z.namelist()
                break
        except Exception:
            time.sleep(0.5)
    else:
        print(f"⏳ File {filename} still busy or incomplete, skipping for now...")
        return False

    # Pattern: Mobbin WEB screen bundle: <app>__<category>__webscreens(_N)?.zip,
    # <app>__webscreens(_N)?.zip, webmobbin__<app>.zip
    m_app_cat = re.match(r'^([a-zA-Z0-9_-]+)__([a-zA-Z0-9_-]+)__webscreens(?:_\d+)?$', base_name, re.IGNORECASE)
    m_screens = re.match(r'^([a-zA-Z0-9_-]+)__webscreens(?:_\d+)?$', base_name, re.IGNORECASE)
    m_mobbin = re.match(r'^webmobbin__([a-zA-Z0-9_-]+)$', base_name, re.IGNORECASE)

    app_slug = None
    cat_extracted = None
    if m_app_cat:
        app_slug = m_app_cat.group(1).lower().strip().replace('-', '_')
        cat_extracted = m_app_cat.group(2).lower().strip().replace('-', '_')
    elif m_screens:
        app_slug = m_screens.group(1).lower().strip().replace('-', '_')
    elif m_mobbin:
        app_slug = m_mobbin.group(1).lower().strip().replace('-', '_')

    if not app_slug:
        return False

    registry = load_registry()
    target_abs_path, target_rel_path = resolve_target_dir(app_slug, registry, category=cat_extracted)

    print(f"\n📦 Found ingestion archive: {filename}")
    print(f"📂 Extracting into: {target_rel_path}...")

    extracted = 0
    skipped = 0
    try:
        from ingest_bridge import get_existing_screen_hashes, ingest_screen_data
        existing_hashes, max_idx = get_existing_screen_hashes(target_abs_path)
        next_idx = max_idx + 1
        with zipfile.ZipFile(zip_path, 'r') as z:
            for item in z.namelist():
                base_item = os.path.basename(item)
                if not base_item or base_item.startswith('.') or base_item.startswith('__MACOSX'):
                    continue
                with z.open(item) as src:
                    img_data = src.read()
                saved, next_idx = ingest_screen_data(target_abs_path, img_data, existing_hashes, next_idx)
                if saved:
                    extracted += 1
                else:
                    skipped += 1

        print(f"🎉 Successfully extracted {extracted} new files ({skipped} duplicates skipped) into {target_rel_path}")

        # Remove zip from Downloads folder
        try:
            os.remove(zip_path)
            print(f"🧹 Cleaned up {filename} from Downloads.")
        except Exception as e:
            print(f"⚠️ Could not delete zip: {e}")

        return True
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def is_web_archive(entry):
    """Only match WEB archives — never mobile ones (__screens, flow__, pageflows__)."""
    lower = entry.lower()
    if '__webscreens' in lower or lower.startswith('webscreens__'):
        return True
    if lower.startswith('webmobbin__'):
        return True
    return False

def watch_loop():
    print(f"👀 Watching {DOWNLOADS_DIR} for web screen ZIPs...")
    print(f"📁 Target Base: {BASE_DIR}")
    print("Ready to ingest `*__webscreens.zip` or `webmobbin__*.zip` on download.\n")

    seen_files = set()
    while True:
        try:
            if not os.path.exists(DOWNLOADS_DIR):
                time.sleep(2)
                continue

            entries = os.listdir(DOWNLOADS_DIR)
            for entry in entries:
                if not entry.lower().endswith('.zip'):
                    continue
                if entry in seen_files:
                    continue

                if is_web_archive(entry):
                    full_path = os.path.join(DOWNLOADS_DIR, entry)
                    if os.path.exists(full_path):
                        if process_zip(full_path):
                            seen_files.add(entry)

        except Exception as e:
            print(f"Watcher error: {e}")

        time.sleep(0.5)

if __name__ == '__main__':
    watch_loop()
