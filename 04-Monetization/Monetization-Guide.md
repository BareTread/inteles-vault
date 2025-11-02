# Monetization Guide — 2Performant (Abordare Echilibrată)

Filozofie: încrederea pe primul loc. 1–2 linkuri afiliate contextuale > spam. Plasează linkul în caseta verde „Resurse", aproape de final sau în secțiunea în care chiar ajută.

## Link2 Plugin (Recommended — Automatic)

**Setup (One-Time):**
1. Add this script to WordPress footer (Appearance > Theme File Editor > footer.php, before `</body>`):
   ```html
   <script src="https://cdn.2performant.com/l2/link2.js" id="linkTwoPerformant" data-id="l2/0/4/4/7/3/3/7/9/4/0" data-api-host="https://cdn.2performant.com"></script>
   ```
2. Configure target merchants in 2Performant dashboard (Tools > Link2)
3. Done! Link2 auto-converts regular merchant URLs → affiliate links

**Writer Workflow:**
- Use [[04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED]] to choose products
- Paste the **regular merchant URL** (e.g., `https://intimax.ro/product`)
- Link2 automatically adds your `aff_code=80f42fe2f` when visitors click
- NO manual quicklink generation needed!

## Manual Quicklink Format (Fallback)

Only if Link2 is not available:

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
- Ghiduri premium (PDF scurt) — „Top 50 simboluri onirice” (fără a canibaliza conținutul existent).

Testare & tracking:

- Folosește `unique=` descriptiv (ex. `art_3875_dictionar_vise`)
- Verifică săptămânal CTR și conversii în 2Performant

Atribute recomandate link: `rel="nofollow sponsored noopener"`

Snippets utile: vezi [[07-Templates/HTML-Resource-Box]] și [[07-Templates/HTML-Resource-Box-2Links]]

Inventar complet de produse/URL‑uri: [[11-Source-Docs/links]] (copiat din repo). Creează o notă „Quicklist” din produsele folosite des și insereaz-o în articole prin caseta verde.

Automatizare (API 2Performant) — One‑Click:

- Rulează: `bash scripts/monetization-refresh.sh`
  - actualizează programele acceptate (API)
  - regenerează linkuri curate auto
  - creează liste ACCEPTED doar cu comercianții din CSV
  - scrie rapoarte de verificare (audit)
- Folosește pentru publicare: [[04-Monetization/MASTER-PRODUCTS-LIST.ACCEPTED]]
- Homepages rapide: [[04-Monetization/Approved-Merchant-Homepages]]
