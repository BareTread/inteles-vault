# Monetization Guide — 2Performant (Abordare Echilibrată)

Filozofie: încrederea pe primul loc. 1–2 linkuri afiliate contextuale > spam. Plasează linkul în caseta verde „Resurse”, aproape de final sau în secțiunea în care chiar ajută.

Format link (quicklink):

```
https://event.2performant.com/events/click?ad_type=quicklink&aff_code=80f42fe2f&unique=[eticheta]&redirect_to=[URL_ENCODED]
```

Disclosure ANPC (obligatoriu):

```html
<p style="font-size:.85rem;color:#666;margin-top:12px"><em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em></p>
```

Unde funcționează cel mai bine:

- Interpretări de vise → cărți Jung/Freud, dicționare de vise (Libris)
- Somn/stres → suplimente SpringFarma (doar când e relevant)
- Jurnale/mindfulness → Librex

Alte căi (complementare, păstrând echilibrul):

- Publicitate contextuală (AdSense) — densitate redusă, doar între secțiuni mari.
- Newsletter + magnet („Jurnal de vise PDF”) → monetizare pe email cu recomandări discrete.
- Ghiduri premium (PDF scurt) — „Top 50 simboluri onirice” (fără a canibaliza conținutul existent).

Testare & tracking:

- Folosește `unique=` descriptiv (ex. `art_3875_dictionar_vise`)
- Verifică săptămânal CTR și conversii în 2Performant

Atribute recomandate link: `rel="nofollow sponsored noopener"`

Snippets utile: vezi [[07-Templates/HTML-Resource-Box]] și [[07-Templates/HTML-Resource-Box-2Links]]

Inventar complet de produse/URL‑uri: [[11-Source-Docs/links]] (copiat din repo). Creează o notă „Quicklist” din produsele folosite des și insereaz-o în articole prin caseta verde.

Automatizare (API 2Performant):

- Rulează `python scripts/twop/fetch_and_build.py` după ce setezi `.env`.
- Generează [[04-Monetization/Auto-Generated-Affiliate-Links]].
- Surse: Programe acceptate + produse curate (Libris, SpringFarma, etc.).
