import json,sys,collections
def agg(path):
    rows=json.load(open(path))['data']['inventory']
    v=collections.OrderedDict()
    for r in rows:
        q=sum(x['quantity'] for x in r['quantities'] or [] if x['room'] and x['room']['isForSale'] and x['room']['name']=='For Sale')
        e=v.setdefault(r['variantId'],dict(name=r['productName'],var=r['variantName'],brand=r['productBrand'],q=0,price=None,w=r['weightVolume'],desc=r['productDescription'],thc=None))
        e['q']+=q
        if q>0:
            e['price']=r['pricing']['preTaxPrice'] if r.get('pricing') else e['price']
            f={x['name']:x['value'] for x in r['fields'] or []}; e['thc']=f.get('Total % THC') or e['thc']
    return {k:x for k,x in v.items() if x['q']>0}
