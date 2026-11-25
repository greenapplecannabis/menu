import json,sys,collections

THC_KEYS=('Total % THC','% THC')

def _thc(fields):
    f={x['name']:x['value'] for x in fields or [] if x.get('value') not in (None,'')}
    for k in THC_KEYS:
        if k in f: return f[k]
    return None

def product_thc(paths):
    """Saved manage_products get results -> {productId: THC} (product fields first, then variant fields)."""
    out={}
    for p in paths:
        prod=json.load(open(p))['data']['product']
        t=_thc(prod.get('fields'))
        if t is None:
            for var in prod.get('variants') or []:
                t=_thc(var.get('fields'))
                if t is not None: break
        if t is not None: out[prod['id']]=t
    return out

SPECIES={'indica':'Indica','sativa':'Sativa','50/50':'Hybrid','hybrid':'Hybrid',
         'indica-dom':'Indica Dom. Hybrid','sativa-dom':'Sativa Dom. Hybrid'}

def species(paths):
    """Saved manage_products list results (return_fields id, name, brand, variants { fields { name value } })
    -> {productId: menu type} from the variant field 'Strain Species'. A file may instead hold a plain
    JSON object {productId: "Indica-dom", ...}. Unknown or blank values are left out."""
    out={}
    for p in paths:
        j=json.load(open(p))
        if 'data' in j:
            for prod in j['data']['products']:
                for var in prod.get('variants') or []:
                    v={x['name']:x['value'] for x in var.get('fields') or []}.get('Strain Species')
                    if v and v.strip().lower() in SPECIES:
                        out[prod['id']]=SPECIES[v.strip().lower()]; break
        else:
            for pid,v in j.items():
                if v and v.strip().lower() in SPECIES: out[pid]=SPECIES[v.strip().lower()]
    return out

def agg(path, product_paths=(), species_paths=()):
    """In-stock variants. THC comes from the batch's 'Total % THC'; when blank, from the product page's
    '% THC' (pass saved manage_products get results for those products as product_paths)."""
    rows=json.load(open(path))['data']['inventory']
    v=collections.OrderedDict()
    for r in rows:
        q=sum(x['quantity'] for x in r['quantities'] or [] if x['room'] and x['room']['isForSale'] and x['room']['name']=='For Sale')
        e=v.setdefault(r['variantId'],dict(name=r['productName'],var=r['variantName'],brand=r['productBrand'],q=0,price=None,w=r['weightVolume'],desc=r['productDescription'],thc=None,pid=r['productId']))
        e['q']+=q
        if q>0:
            e['price']=r['pricing']['preTaxPrice'] if r.get('pricing') else e['price']
            e['thc']=_thc(r['fields']) or e['thc']
    pt=product_thc(product_paths)
    sp=species(species_paths)
    for e in v.values():
        if e['thc'] is None: e['thc']=pt.get(e['pid'])
        e['type']=sp.get(e['pid'])          # menu `t` from Flowhub Strain Species (None if not set)
    return {k:x for k,x in v.items() if x['q']>0}

def missing_thc(path):
    """Product IDs of in-stock items with no batch THC: look these up with manage_products get."""
    return sorted({x['pid'] for x in agg(path).values() if x['thc'] is None})
