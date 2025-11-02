# `unique=` Tagging — Best Practices

Obiectiv: etichete `unique=` scurte, descriptive, utile pentru A/B testing și raportare.

## Format recomandat

`a[POSTID]_[topic|slug]_[placement]_[variant]`

Exemple:
- `a2015_jung_box_btm_v1`
- `a3856_dic_vise_box_btm_green`
- `a7395_sleep_box_mid_v2`

## Câmpuri
- `a[POSTID]` — ID WordPress, prefix „a” pentru ușurință vizuală.
- `[topic|slug]` — scurt (ex. `jung`, `dic_vise`, `somn`).
- `[placement]` — `box_top`, `box_mid`, `box_btm`.
- `[variant]` — `v1`, `v2_blue`, `v3_two_links`.

## Reguli
- Max 32 caractere (practic), fără spații.
- Fără diacritice, doar litere/cifre/underscore.
- Menține consecvent pentru comparații corecte.

## Unde treci eticheta
În URL-ul 2Performant: `...&unique=a2015_jung_box_btm_v1&redirect_to=...`

## Tracking
- Notează eticheta în [[09-Tracking/Monetization-Tracker]].
- Săptămânal: compară CTR/conversii per etichetă și mută plasarea câștigătoare.

