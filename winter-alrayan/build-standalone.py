"""Inline fonts and images into one self-contained HTML file (standalone.html)."""
import base64, pathlib, re
root = pathlib.Path(__file__).parent
s = (root / 'index.html').read_text(encoding='utf-8')
mime = {'.woff2': 'font/woff2', '.jpg': 'image/jpeg'}
def data(rel):
    p = root / rel
    return 'data:%s;base64,%s' % (mime[p.suffix], base64.b64encode(p.read_bytes()).decode())
s = re.sub(r'<link rel="preload"[^>]*>\n', '', s)
s = s.replace('url(assets/glass.jpg)', 'var(--glass)').replace(':root{', ':root{--glass:url(%s);' % data('assets/glass.jpg'), 1)
s = re.sub(r'assets/[\w./-]+\.(?:woff2|jpg)', lambda m: data(m.group(0)), s)
(root / 'standalone.html').write_text(s, encoding='utf-8')
print('standalone.html', len(s))
