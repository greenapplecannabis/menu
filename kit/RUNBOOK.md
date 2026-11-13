# Green Apple Menu Wall — automatic update runbook

The menu wall is this GitHub repository, published with GitHub Pages at
https://greenapplecannabis.github.io/menu/ — three Fire TV sticks show it with #left = Vapes,
#center = Prerolls, #right = Flower. The page re-reads `data.json` every 3 minutes, so a push is all
it takes for the TVs to change. This run keeps it in step with Flowhub.

Flowhub is READ ONLY in this job: never create or change deals, products, prices or inventory.

## 1. Get the repo
Call `add_repo` (owner `greenapplecannabis`, repo `menu`, access `push`) and clone it as that tool says
(`git clone --depth 1 https://github.com/greenapplecannabis/menu <dir>`). Work inside the clone.
Files: `index.html` + `data.json` (published, generated), `img/` (product photos), `kit/` (this runbook,
`template.html`, `data.json` = the source data, `render.py`, `agg.py`).

## 2. Read Flowhub (Flowhub tools only)
- `get_own_active_user` first (store: Green Apple Cannabis).
- `manage_inventory` list per category; save each raw result to a file:
  Flower 1009137d-354a-40c4-be74-a7e0473513a7 · Preroll b4e924aa-2e41-445e-9ad3-0470bdf3a1e9 ·
  Vapes fa65853e-c899-45d8-998e-3c06d3a24e70 · Concentrates 9e1725d4-0433-4736-8827-49b9aade175c
- `kit/agg.py`: `from agg import agg; agg(path)` gives in-stock variants (room "For Sale", q>0) with
  name, variant, brand, price (cents, pre-tax), THC.
- `manage_deals` list: the deals that are active today.

## 3. Update kit/data.json
Items: `{n: strain name, b: brand, t: "Indica|Sativa|Hybrid|Indica Dom. Hybrid|Sativa Dom. Hybrid", thc: number,
fl: "Taste • Taste • Taste", ef: "Feel • Feel • Feel", img: "img/<file>", chip: short label or null
(e.g. "2-PACK", "1G CART", "1G DISPOSABLE", "HASH ROSIN DISPOSABLE"), badge: e.g. "40% OFF" or null,
sizes: [{l: label e.g. "3.5g" / "2-Pack 1.5g", p: price cents, s: sale price cents or null}]}`.
Sections: flower (flower jars/bags), prerolls, vapes (vapes + concentrates). Keep the existing order;
put new items where they fit alphabetically.

Rules, in order:
1. **Sold out** (no For Sale stock) → remove that size; remove the item when no sizes are left.
2. **Price** → `p` = Flowhub price. If an active deal covers the product, `s` = discounted price
   (round to whole cents) and `badge` = "NN% OFF"; otherwise `s` = null and `badge` = null.
3. **New in-stock product** not on the menu → add it. Taste/feel/type from the Flowhub description,
   else a quick web search of the strain, best effort, 3 words each. Image: reuse an existing
   `img/` file of the same product line (same brand + package style) if one fits; otherwise
   `img/placeholder.jpg`. Never invent prices or THC.
4. Skip samples, display units, $0 items, accessories, and non-cannabis products.
5. **Ticker** (`ticker` array, HTML allowed: `<b>NN% OFF</b> what`) → one line per active
   customer-facing deal, short and plain, like the existing lines. Remove lines for ended deals.
Change nothing else (layout, titles, wording of untouched items). Keep the `theme` value exactly as it is
(e.g. "green-wednesday" or ""); only the owner switches themes.

## 4. Render and publish (only if something changed)
- `python3 kit/render.py kit index.html` (validates the data, writes index.html and data.json).
- `git add -A && git commit -m "Menu update <date time>"` then
  `git -c push.negotiate=true push origin main`.
- If nothing changed, commit nothing.

## 5. Report
End with a 1–3 line summary: what was added / removed / repriced, or "no changes".
If anything failed, leave the live menu as it was and say what failed.
