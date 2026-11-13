"""Render the menu wall page. usage: python3 render.py <kitdir> <out.html>
Reads <kitdir>/template.html and <kitdir>/data.json (keys: flower, prerolls, vapes, ticker).
Also writes data.json next to <out.html> (the TVs poll it every 3 minutes)."""
import json, sys, os
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
assert isinstance(d['ticker'], list)
data = {c: d[c] for c in ('flower', 'prerolls', 'vapes')}
html = t.replace('__DATA__', json.dumps(data)).replace('__TICKER__', json.dumps(d['ticker'], ensure_ascii=False))
if not html.lstrip().lower().startswith('<!doctype'):
    html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '</head><body>\n' + html + '\n</body></html>\n')
open(out, 'w', encoding='utf-8').write(html)
json.dump({**data, 'ticker': d['ticker']}, open(os.path.join(os.path.dirname(os.path.abspath(out)), 'data.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', {c: len(d[c]) for c in data}, len(d['ticker']), 'ticker lines')
