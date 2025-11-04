#!/usr/bin/env python3
from scripts.twop.build_category_packs import parse_master_products, MASTER_ALL, MASTER_ACCEPTED
from collections import Counter

prods = parse_master_products([MASTER_ACCEPTED, MASTER_ALL])
print(f'Total products parsed: {len(prods)}')
cats = Counter(p.category for p in prods)
print(f'\nCategories found: {len(cats)}')
for cat, count in cats.most_common():
    print(f'  {cat}: {count}')

print(f'\nFirst 5 products:')
for p in prods[:5]:
    print(f'  - {p.name} ({p.merchant})')
