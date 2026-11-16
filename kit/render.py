"""Render the menu wall page and the lounge TV page. usage: python3 render.py <kitdir> <out.html>
Reads <kitdir>/template.html, <kitdir>/lounge.html and <kitdir>/data.json (keys: flower, prerolls, vapes,
edibles, ticker). Writes <out.html> (menu wall), lounge.html next to it (lounge TV), and data.json
next to them (the TVs poll it every few minutes)."""
import json, sys, os, hashlib
k, out = sys.argv[1], sys.argv[2]
t = open(os.path.join(k, 'template.html'), encoding='utf-8').read()
d = json.load(open(os.path.join(k, 'data.json'), encoding='utf-8'))
for cat in ('flower', 'prerolls', 'vapes'):
    for it in d[cat]:
        for f in ('n', 'b', 't', 'thc', 'fl', 'ef', 'img', 'sizes'):
            assert f in it, (cat, it.get('n'), f)
        assert it['sizes'], (cat, it['n'])
        img = os.path.join(os.path.dirname(os.path.abspath(out)), it['img'])
        if not os.path.exists(img): print('WARNING missing image', it['img'])
d.setdefault('edibles', [])
for it in d['edibles']:                       # lounge TV only; t/thc optional, dose e.g. "200mg · 10mg each"
    for f in ('n', 'b', 'img', 'sizes'):
        assert f in it, ('edibles', it.get('n'), f)
    assert it['sizes'], ('edibles', it['n'])
    img = os.path.join(os.path.dirname(os.path.abspath(out)), it['img'])
    if not os.path.exists(img): print('WARNING missing image', it['img'])
assert isinstance(d['ticker'], list)
lt = open(os.path.join(k, 'lounge.html'), encoding='utf-8').read()
data = {c: d[c] for c in ('flower', 'prerolls', 'vapes')}
build = hashlib.sha1((t + lt).encode('utf-8')).hexdigest()[:10]   # changes only when a design (template) changes
theme = d.get('theme') or ''
bezel = d.get('bezel', 40)
html = t.replace('__BUILD__', build).replace('__THEME__', json.dumps(theme)).replace('__BEZEL__', json.dumps(bezel)).replace('__DATA__', json.dumps(data)).replace('__TICKER__', json.dumps(d['ticker'], ensure_ascii=False))
if not html.lstrip().lower().startswith('<!doctype'):
    html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '</head><body>\n' + html + '\n</body></html>\n')
open(out, 'w', encoding='utf-8').write(html)
lounge = {**data, 'edibles': d['edibles']}
lhtml = lt.replace('__BUILD__', build).replace('__THEME__', json.dumps(theme)).replace('__DATA__', json.dumps(lounge)).replace('__TICKER__', json.dumps(d['ticker'], ensure_ascii=False))
open(os.path.join(os.path.dirname(os.path.abspath(out)), 'lounge.html'), 'w', encoding='utf-8').write(lhtml)
json.dump({**lounge, 'ticker': d['ticker'], 'theme': theme, 'bezel': bezel, 'build': build}, open(os.path.join(os.path.dirname(os.path.abspath(out)), 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', {c: len(d[c]) for c in lounge}, len(d['ticker']), 'ticker lines')
