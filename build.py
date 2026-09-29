#!/usr/bin/env python3
"""Builds dist/index.html (a single self-contained file) from src/.
   - dist/index.html      → publish as-is (GitHub Pages, Netlify, your own server)
   - dist/artifact.html   → same page without <!doctype>/<html> wrapper (for Claude artifacts)
"""
import pathlib
root = pathlib.Path(__file__).parent
src = root / "src"
order = ["config.js", "ui.js", "shared.js", "bank.js", "bank2.js"]
scripts = [(src / f).read_text(encoding="utf-8") for f in order]
scripts.append("const MODS_LANG = {}; const DEEP = {};")
# QR code for the PayPal.Me link (generated at build time; needs `pip install qrcode`)
import re, json
qr_svg = ""
m = re.search(r'paypalMe:\s*"([^"]*)"', (src / "config.js").read_text(encoding="utf-8"))
if m and m.group(1):
    try:
        import qrcode
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
        q.add_data("https://paypal.me/" + m.group(1)); q.make(fit=True)
        mat = q.get_matrix(); n = len(mat)
        d = "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(mat) for x, v in enumerate(row) if v)
        qr_svg = (f'<svg viewBox="-2 -2 {n+4} {n+4}" role="img" aria-label="QR code paypal.me/{m.group(1)}" '
                  f'shape-rendering="crispEdges"><rect x="-2" y="-2" width="{n+4}" height="{n+4}" fill="#fff"/>'
                  f'<path d="{d}" fill="#16213A"/></svg>')
    except ImportError:
        print("qrcode not installed: skipping QR code (pip install qrcode)")
scripts.append("const QR_SVG = " + json.dumps(qr_svg) + ";")
for l in ["pt", "en", "fr"]:
    scripts.append((src / f"mods.{l}.js").read_text(encoding="utf-8"))
    scripts.append((src / f"deep.{l}.js").read_text(encoding="utf-8"))
scripts.append((src / "app.js").read_text(encoding="utf-8"))
js = "\n;\n".join(scripts).replace("</script", "<\\/script")
body = (src / "template.html").read_text(encoding="utf-8")
body = body.replace("/*STYLE*/", (src / "style.css").read_text(encoding="utf-8")).replace("/*SCRIPTS*/", js)
dist = root / "dist"; dist.mkdir(exist_ok=True)
(dist / "artifact.html").write_text(body, encoding="utf-8")
i = body.index("<header")
head, rest = body[:i], body[i:]
full = ('<!doctype html>\n<html lang="pt">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
        + head + '</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
(dist / "index.html").write_text(full, encoding="utf-8")
print("built", len(full)//1024, "KB")
