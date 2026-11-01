@echo off
title Refresh Web App Registry
echo Scanning design-systems for web apps...
set "SKILL_ROOT=%~dp0.."
python -c "import os, json; base = os.path.abspath(os.environ.get('SKILL_ROOT', '..')); registry = {}; [registry.update({app.lower(): f'{r}/{cat}/{app}/screens', app.lower().replace('-', '_'): f'{r}/{cat}/{app}/screens', app.lower().replace('_', '-'): f'{r}/{cat}/{app}/screens', app.lower().replace('-', '').replace('_', ''): f'{r}/{cat}/{app}/screens'}) for r in ['design-systems', 'design-systems-plus'] if os.path.exists(os.path.join(base, r)) for cat in os.listdir(os.path.join(base, r)) if os.path.isdir(os.path.join(base, r, cat)) and cat != 'system-docs' for app in os.listdir(os.path.join(base, r, cat)) if os.path.isdir(os.path.join(base, r, cat, app)) and (os.makedirs(os.path.join(base, r, cat, app, 'screens'), exist_ok=True) or True)]; reg_file = os.path.join(base, 'scripts', 'app_registry.json'); open(reg_file, 'w', encoding='utf-8').write(json.dumps(registry, indent=2, ensure_ascii=False) + '\n'); print(f'Registry updated! Total mapped keys: {len(registry)}')"
pause
