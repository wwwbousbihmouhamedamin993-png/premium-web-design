#!/usr/bin/env python3
"""
Local Screenshot Ingestion Bridge Server (premium-web-design)
Listens on http://127.0.0.1:3848
Receives ZIP payloads directly from browser bookmarklets (Mobbin web screens)
and automatically extracts screens into design-systems/{category}/{app}/screens/

Runs alongside the premium-mobile-design bridge (port 3847) — this one serves
the WEB design system library only.
"""

import http.server
import json
import os
import sys
import zipfile
import io
import urllib.parse
import urllib.request
import concurrent.futures
import threading
import collections
import hashlib
import shutil
import re

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

PORT = 3848
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_FILE = os.path.join(BASE_DIR, 'scripts', 'app_registry.json')

# Thread locks per app slug to prevent race conditions during concurrent requests / double clicks
APP_LOCKS = collections.defaultdict(threading.Lock)

# Canonical categories mirror design-systems/README.md
CATEGORY_ALIASES = {
    # Developer tools & CI
    'developer_tools': 'devtools',
    'developer-tools': 'devtools',
    'developers': 'devtools',
    'devtools': 'devtools',
    'development': 'devtools',
    'coding': 'devtools',
    'code': 'devtools',
    'git': 'devtools',
    'ci_cd': 'devtools',
    'cicd': 'devtools',
    'open_source': 'devtools',
    # Observability
    'observability': 'observability',
    'monitoring': 'observability',
    'logs': 'observability',
    'logging': 'observability',
    'apm': 'observability',
    'tracing': 'observability',
    # Data & BI
    'data-bi': 'data-bi',
    'data_bi': 'data-bi',
    'data': 'data-bi',
    'analytics': 'data-bi',
    'business_intelligence': 'data-bi',
    'bi': 'data-bi',
    'big_data': 'data-bi',
    'dashboards': 'data-bi',
    # Databases & backend
    'backend': 'backend',
    'database': 'backend',
    'databases': 'backend',
    'db': 'backend',
    'sql': 'backend',
    'api': 'backend',
    'apis': 'backend',
    'server': 'backend',
    # CRM & sales
    'crm': 'crm',
    'crm_and_sales': 'crm',
    'sales': 'crm',
    'marketing': 'crm',
    'customer_relationship': 'crm',
    # Support
    'support': 'support',
    'customer_support': 'support',
    'customer_service': 'support',
    'helpdesk': 'support',
    'help_desk': 'support',
    'ticketing': 'support',
    # Project & knowledge
    'workspace': 'workspace',
    'productivity': 'workspace',
    'project_management': 'workspace',
    'collaboration': 'workspace',
    'notes': 'workspace',
    'documents': 'workspace',
    'knowledge': 'workspace',
    'knowledge_management': 'workspace',
    'tasks': 'workspace',
    # Design & creative
    'creative': 'creative',
    'design': 'creative',
    'design_tools': 'creative',
    'design-tool': 'creative',
    'video': 'creative',
    'photo': 'creative',
    'graphics': 'creative',
    # Admin & identity
    'identity': 'identity',
    'auth': 'identity',
    'authentication': 'identity',
    'security': 'identity',
    'sso': 'identity',
    'access_management': 'identity',
    'admin': 'identity',
    # Fintech & billing
    'fintech': 'fintech',
    'finance': 'fintech',
    'financial': 'fintech',
    'payments': 'fintech',
    'payment': 'fintech',
    'banking': 'fintech',
    'billing': 'fintech',
    'invoicing': 'fintech',
    'crypto': 'fintech',
    'investing': 'fintech',
    'accounting': 'fintech',
    # Commerce admin
    'commerce': 'commerce',
    'ecommerce': 'commerce',
    'e-commerce': 'commerce',
    'e_commerce': 'commerce',
    'shopping': 'commerce',
    'retail': 'commerce',
    'store': 'commerce',
    # Infrastructure & cloud
    'cloud': 'cloud',
    'cloud_and_infrastructure': 'cloud',
    'infrastructure': 'cloud',
    'hosting': 'cloud',
    'serverless': 'cloud',
    'devops': 'cloud',
    'containers': 'cloud',
    'kubernetes': 'cloud',
    'networking': 'cloud',
    'web_hosting': 'cloud',
    # Design-system standards
    'design_system': 'system-docs',
    'design_systems': 'system-docs',
    'design-systems': 'system-docs',
    'system-docs': 'system-docs',
    'standards': 'system-docs',
}

def load_registry():
    if os.path.exists(REGISTRY_FILE):
        try:
            with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_registry(registry):
    # Ensure components/ paths are never saved into registry
    clean_registry = {
        k: v for k, v in registry.items()
        if not v.startswith("components/")
    }
    with open(REGISTRY_FILE, 'w', encoding='utf-8') as f:
        json.dump(clean_registry, f, indent=2)

def normalize_category(category):
    if not category:
        return 'misc'

    cat_str = str(category).strip()
    if not cat_str:
        return 'misc'

    # Get existing categories in design-systems
    ds_path = os.path.join(BASE_DIR, 'design-systems')
    existing_cats = set()
    if os.path.exists(ds_path):
        existing_cats = {d.name.lower() for d in os.scandir(ds_path) if d.is_dir()}

    # 1. Split compound categories (e.g. "Development, Design Tools" or "Finance & Billing")
    parts = re.split(r'[,;/|]|\band\b', cat_str, flags=re.IGNORECASE)
    for part in parts:
        p_clean = part.lower().strip().replace('&', 'and').replace(' ', '_').replace('-', '_')
        p_clean = re.sub(r'[^a-z0-9_-]+', '', p_clean).strip('_-')
        if not p_clean:
            continue
        if p_clean in CATEGORY_ALIASES:
            return CATEGORY_ALIASES[p_clean]
        if p_clean in existing_cats:
            return p_clean
        p_hyphen = p_clean.replace('_', '-')
        p_underscore = p_clean.replace('-', '_')
        if p_hyphen in existing_cats:
            return p_hyphen
        if p_underscore in existing_cats:
            return p_underscore

    # 2. Check whole cleaned string
    c_clean = cat_str.lower().strip().replace('&', 'and').replace(' ', '_').replace('-', '_')
    c_clean = re.sub(r'[^a-z0-9_-]+', '', c_clean).strip('_-')
    if c_clean in CATEGORY_ALIASES:
        return CATEGORY_ALIASES[c_clean]

    if c_clean in existing_cats:
        return c_clean
    c_hyphen = c_clean.replace('_', '-')
    c_underscore = c_clean.replace('-', '_')
    if c_hyphen in existing_cats:
        return c_hyphen
    if c_underscore in existing_cats:
        return c_underscore

    # 3. Substring check against canonical aliases (longest alias wins for precision)
    matches = [a for a in CATEGORY_ALIASES if a in c_clean]
    if matches:
        best = max(matches, key=len)
        return CATEGORY_ALIASES[best]

    return c_hyphen or 'misc'

def resolve_target_dir(app_slug, registry, category=None):
    slug_clean = app_slug.lower().strip().replace(' ', '_').replace('-', '_')
    slug_clean = re.sub(r'[^a-z0-9_]+', '', slug_clean).strip('_')
    if not slug_clean or slug_clean in {'app', 'apps', 'screens', 'browse', 'web', 'loading'}:
        slug_clean = 'app'
    slug_hyphen = slug_clean.replace('_', '-')

    # 1. Check registry exact match (excluding any legacy components/ path)
    for k in (slug_clean, slug_hyphen):
        if k in registry:
            current_path = registry[k]
            if not current_path.startswith("components/"):
                # If currently in misc but real category provided, migrate to real category
                if current_path.startswith("design-systems/misc/") and category:
                    break
                return os.path.join(BASE_DIR, current_path), current_path

    # 2. Check disk in design-systems and design-systems-plus
    for section in ['design-systems', 'design-systems-plus']:
        section_dir = os.path.join(BASE_DIR, section)
        if not os.path.exists(section_dir):
            continue
        for cat in os.listdir(section_dir):
            cat_path = os.path.join(section_dir, cat)
            if not os.path.isdir(cat_path):
                continue
            if cat == 'system-docs':
                # Standards-reference category — never auto-route Mobbin harvests here
                continue
            app_dir = os.path.join(cat_path, slug_hyphen)
            if os.path.isdir(app_dir):
                # If found in misc but real category provided, migrate!
                if cat == 'misc' and category:
                    new_cat = normalize_category(category)
                    new_app_dir = os.path.join(BASE_DIR, 'design-systems', new_cat, slug_hyphen)
                    os.makedirs(os.path.dirname(new_app_dir), exist_ok=True)
                    shutil.move(app_dir, new_app_dir)
                    new_rel = f"design-systems/{new_cat}/{slug_hyphen}/screens"
                    registry[slug_clean] = new_rel
                    registry[slug_hyphen] = new_rel
                    save_registry(registry)
                    return os.path.join(new_app_dir, 'screens'), new_rel
                rel_path = f"{section}/{cat}/{slug_hyphen}/screens"
                return os.path.join(app_dir, 'screens'), rel_path

    # 3. Dynamic category resolution: NEVER route to components/, ALWAYS to design-systems/
    cat_dir = normalize_category(category)
    new_rel_path = f"design-systems/{cat_dir}/{slug_hyphen}/screens"
    new_abs_path = os.path.join(BASE_DIR, new_rel_path)
    os.makedirs(new_abs_path, exist_ok=True)

    # Starter README if not present
    app_root = os.path.join(BASE_DIR, f"design-systems/{cat_dir}/{slug_hyphen}")
    readme_path = os.path.join(app_root, "README.md")
    design_path = os.path.join(app_root, "DESIGN.md")
    if not os.path.exists(readme_path) and not os.path.exists(design_path):
        cat_display = category.strip() if category else cat_dir.title()
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(f"# {app_slug.title()} — Web design spec\n\n**Category:** {cat_display}\n\nAuto-created via Ingestion Bridge.\n\n## Files\n\n- [`screens/`](screens/)\n")

    # Register in lookup table
    registry[slug_clean] = new_rel_path
    registry[slug_hyphen] = new_rel_path
    save_registry(registry)
    print(f"✨ Registered new app '{app_slug}' in category '{cat_dir}' -> {new_rel_path}")
    return new_abs_path, new_rel_path

def get_existing_screen_hashes(target_abs_path):
    """Returns set of SHA256 hashes of all existing screens in target_abs_path and max numeric index."""
    hashes = set()
    max_idx = 0
    if not os.path.exists(target_abs_path):
        return hashes, max_idx

    for fname in os.listdir(target_abs_path):
        fpath = os.path.join(target_abs_path, fname)
        if not os.path.isfile(fpath):
            continue
        m = re.match(r'screen_(\d+)\.(webp|png|jpg|jpeg)', fname, re.IGNORECASE)
        if m:
            idx = int(m.group(1))
            if idx > max_idx:
                max_idx = idx
        try:
            with open(fpath, 'rb') as f:
                h = hashlib.sha256(f.read()).hexdigest()
                hashes.add(h)
        except Exception:
            pass
    return hashes, max_idx

def ingest_screen_data(target_abs_path, image_bytes, existing_hashes, next_idx):
    """
    Saves image_bytes if its SHA256 hash is not already present in existing_hashes.
    Names the file screen_{next_idx:03d}.webp.
    Returns (saved: bool, next_idx: int)
    """
    if not image_bytes or len(image_bytes) < 1000:
        return False, next_idx

    img_hash = hashlib.sha256(image_bytes).hexdigest()
    if img_hash in existing_hashes:
        return False, next_idx

    os.makedirs(target_abs_path, exist_ok=True)
    target_fname = f"screen_{next_idx:03d}.webp"
    target_fpath = os.path.join(target_abs_path, target_fname)

    temp_fpath = target_fpath + f".tmp.{os.getpid()}"
    try:
        with open(temp_fpath, 'wb') as f:
            f.write(image_bytes)
        os.replace(temp_fpath, target_fpath)
    except Exception:
        if os.path.exists(temp_fpath):
            os.remove(temp_fpath)
        raise

    existing_hashes.add(img_hash)
    return True, next_idx + 1

class IngestionHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stdout.write(f"[{self.log_date_time_string()}] {args[0]} {args[1]} -> {args[2]}\n")
        sys.stdout.flush()

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == '/' or self.path == '/health':
            registry = load_registry()
            self.send_response(200)
            self.send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            resp = {
                "status": "online",
                "service": "Mobbin Web Ingestion Bridge (premium-web-design)",
                "registered_apps": len(registry)
            }
            self.wfile.write(json.dumps(resp, indent=2).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        is_flow_dest = (
            parsed.path.startswith('/save-flow') or
            params.get('dest', [''])[0] == 'flows' or
            params.get('target', [''])[0] == 'flows'
        )

        if is_flow_dest:
            app_param = params.get('app', [''])[0] or self.headers.get('X-App-Slug', 'app')
            cat_param = params.get('category', [''])[0] or params.get('cat', [''])[0] or self.headers.get('X-Category', 'general')

            app_clean = app_param.lower().strip().replace(' ', '_').replace('-', '_')
            cat_clean = cat_param.lower().strip().replace(' ', '_').replace('-', '_')

            target_rel_path = f"flows/{cat_clean}/{app_clean}"
            target_abs_path = os.path.join(BASE_DIR, "flows", cat_clean, app_clean)
            os.makedirs(target_abs_path, exist_ok=True)

            readme_path = os.path.join(target_abs_path, "README.md")
            if not os.path.exists(readme_path):
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(f"# {app_param.title()} — {cat_param.title()} Flow\n\nCaptured from web bookmarklet.\n")

        elif parsed.path.startswith('/save'):
            app_param = params.get('app', [''])[0]
            if not app_param:
                app_param = self.headers.get('X-App-Slug', 'unknown_app')

            cat_param = params.get('category', [''])[0] or params.get('cat', [''])[0] or self.headers.get('X-Category', '')
            flow_param = params.get('flow', [''])[0] or self.headers.get('X-Flow-Name', '')

            registry = load_registry()
            target_abs_path, target_rel_path = resolve_target_dir(app_param, registry, category=cat_param)

            if flow_param:
                flow_clean = flow_param.lower().strip().replace(' ', '_').replace('-', '_')
                target_abs_path = os.path.join(target_abs_path, flow_clean)
                target_rel_path = f"{target_rel_path}/{flow_clean}"

            os.makedirs(target_abs_path, exist_ok=True)
        else:
            self.send_response(404)
            self.end_headers()
            return

        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            self.send_response(400)
            self.send_cors_headers()
            self.end_headers()
            self.wfile.write(b'{"error": "Empty body"}')
            return

        content_type = self.headers.get('Content-Type', '')

        # Acquire per-app lock to prevent race conditions from concurrent clicks / requests
        lock = APP_LOCKS[app_param]
        with lock:
            existing_hashes, max_idx = get_existing_screen_hashes(target_abs_path)
            next_idx = max_idx + 1

            # Fast JSON Mode
            if 'application/json' in content_type:
                try:
                    raw_data = self.rfile.read(content_length)
                    payload = json.loads(raw_data.decode('utf-8'))
                    screens = payload.get('screens', [])
                    if not screens:
                        self.send_response(400)
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(b'{"error": "No screens in payload"}')
                        return

                    def fetch_screen(item):
                        url = item.get('url')
                        if not url:
                            return None
                        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        try:
                            with urllib.request.urlopen(req, timeout=12) as resp:
                                return resp.read()
                        except Exception as e:
                            print(f"Error downloading {url}: {e}")
                            return None

                    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                        fetched_bytes_list = list(pool.map(fetch_screen, screens))

                    saved_count = 0
                    skipped_count = 0
                    for img_bytes in fetched_bytes_list:
                        if not img_bytes:
                            skipped_count += 1
                            continue
                        saved, next_idx = ingest_screen_data(target_abs_path, img_bytes, existing_hashes, next_idx)
                        if saved:
                            saved_count += 1
                        else:
                            skipped_count += 1

                    print(f"🎉 Saved {saved_count} new web screens ({skipped_count} skipped/duplicates) into {target_rel_path}")
                    self.send_response(200)
                    self.send_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    res = {
                        "status": "success",
                        "app": app_param,
                        "count": saved_count,
                        "skipped": skipped_count,
                        "total": len(existing_hashes),
                        "target": target_rel_path
                    }
                    self.wfile.write(json.dumps(res).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"❌ Error in JSON download: {e}")
                    self.send_response(500)
                    self.send_cors_headers()
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                    return

            # ZIP Mode
            zip_bytes = self.rfile.read(content_length)
            try:
                saved_count = 0
                skipped_count = 0
                with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
                    for filename in z.namelist():
                        basename = os.path.basename(filename)
                        if not basename or basename.startswith('.') or basename.startswith('__MACOSX'):
                            continue
                        with z.open(filename) as source:
                            img_data = source.read()
                        saved, next_idx = ingest_screen_data(target_abs_path, img_data, existing_hashes, next_idx)
                        if saved:
                            saved_count += 1
                        else:
                            skipped_count += 1

                print(f"🎉 Saved {saved_count} new web screens ({skipped_count} skipped/duplicates) into {target_rel_path}")
                self.send_response(200)
                self.send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                res = {
                    "status": "success",
                    "app": app_param,
                    "count": saved_count,
                    "skipped": skipped_count,
                    "total": len(existing_hashes),
                    "target": target_rel_path
                }
                self.wfile.write(json.dumps(res).encode('utf-8'))
            except Exception as e:
                print(f"❌ Error extracting ZIP: {e}")
                self.send_response(500)
                self.send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

def run_server():
    try:
        from watch_downloads import watch_loop
        watcher = threading.Thread(target=watch_loop, daemon=True)
        watcher.start()
        print("👀 Background Downloads Watcher active (auto-ingesting *__webscreens.zip).")
    except Exception as e:
        print(f"⚠️ Could not start watcher thread: {e}")

    server = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), IngestionHandler)
    print(f"🚀 Web Ingestion Bridge Server active on http://127.0.0.1:{PORT}")
    print(f"📁 Target Base: {BASE_DIR}")
    print("Ready to receive web screenshots from the Mobbin web bookmarklet.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Web Ingestion Bridge.")
        server.server_close()

if __name__ == '__main__':
    run_server()
