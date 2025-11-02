# SOP: Înteles.ro — Content, SEO, MCP & Monetizare (Balanced, Mobile‑First)

Ultima actualizare: 2025‑11‑02

Scop: un ghid autosuficient pe care îl poți da unui agent AI pentru a crea/actualiza articole world‑class în română, cu SEO sănătos, monetizare echilibrată, imagini premium și HTML modern, optimizat mobil. Include filozofie, pași concreți, componente HTML reutilizabile și comenzi MCP (WordPress + Pexels) la nivel practic.

—

## Principii De Bază (Filozofie 80/20)

- Satisface intenția utilizatorului rapid: în primele 2–3 paragrafe oferă răspunsul clar.
- Calitate > cantitate de linkuri: 1–2 linkuri afiliate contextuale bine plasate bat 15 linkuri „stridente”.
- Curat și modern: design discret, lizibil, cu spațiere, umbre fine, colțuri rotunjite; fără „curcubeu” gratuit.
- Mobile‑first: paragrafe scurte, subtitluri dese, liste; 97.5% trafic mobil.
- Credibilitate (E‑E‑A‑T): citează surse (OMS/WHO, Jung, Freud, Wikipedia RO), explică pe scurt de ce contează.
- Fără „formule” inflexibile: componentele vizuale sunt sugestii — adaptează pentru fiecare articol.

—

## Tipuri De Articole & Șabloane De Conținut

### A. Interpretare de vis (format standard)
- Titlu clar + răspuns rapid (2–3 paragrafe)
- H2: Semnificația de bază (explică simbolul pe înțelesul tuturor)
- H2: Perspectivă psihologică (Carl Jung / Sigmund Freud)
- H2: Scenarii frecvente (3–6 scenarii concrete, concise, nu generice)
- H2: Tradiții românești / superstiții (acolo unde e relevant)
- H2: Resurse pentru aprofundare (o casetă verde, max 1–2 linkuri afiliate)
- H2: Întrebări frecvente (FAQ, minim 6 întrebări cu schema.org)
- Secțiune scurtă de concluzie + referințe

### B. „Ce înseamnă X” (explicativ, non‑vis)
- Răspuns scurt/definiție + context (2–3 paragrafe)
- H2: Utilizare și exemple concrete
- H2: Diferențe / confuzii comune
- H2: Implicații practice / când folosești / ce să eviți
- H2: Resurse (max 1–2 linkuri afiliate, dacă e logic)
- H2: FAQ (6+ întrebări)
- Referințe credibile

—

## Stil & Voce (Română naturală)

- Profesional, empatic, informat; evită limbajul agresiv sau manipulator.
- Variază ritmul propozițiilor; folosește diacritice; evită clișeele de AI („În concluzie putem spune că…”, „Este important de menționat că…”).
- Integrează cuvinte‑cheie natural (0.5–1% pentru principalul termen), niciodată „stuffing”.

—

## Design Language (inspirație din site)

- Vibe: pastel cald (fundal crem/galben pal), badge‑uri albastre, imagini mari, carduri cu colțuri rotunjite și umbre fine.
- Token‑uri orientative (nu reguli dure):
  - Radii: 8–12–16px
  - Umbre: 0 3–6px 16–24px rgba(0,0,0,0.08–0.15)
  - Culori: text #333; gri deschis #FAFAFA; linii #E0E0E0; verde #4CAF50; portocaliu #FF6F00; albastru badge ~#1976D2; accente închise #2E7D32, #E65100
  - Spațiere: 16–24px interior; 24–32px între blocuri
- Emojis doar în titluri/ancore vizuale discrete (unde sprijină scanarea).

—

## Componente HTML (reutilizabile, mobile‑friendly)

Observație: sunt exemple cu inline CSS, gândite simplu pentru editorul WordPress. Ajustează culori/tonuri/spacing în funcție de articol. Evită gradientul excesiv; folosește‑l doar când clarifică structura.

### 1) Info Box (învățare, portocaliu)
```html
<div style="background:#FFF3E0;border-left:4px solid #FF6F00;padding:20px;margin:25px 0;border-radius:8px;box-shadow:0 3px 12px rgba(0,0,0,0.06)">
  <h3 style="margin:0 0 10px;color:#E65100">📋 Ce vei afla</h3>
  <ul style="margin:0;line-height:1.8">
    <li>Punct 1</li>
    <li>Punct 2</li>
    <li>Punct 3</li>
  </ul>
  <p style="margin:10px 0 0;font-size:.9rem;color:#666">Sfat: păstrează paragrafele scurte pentru mobil.</p>
  </div>
```

### 2) Resource Box (verde, monetizare echilibrată)
```html
<div style="background:#E8F5E9;border-left:4px solid #4CAF50;padding:20px;margin:25px 0;border-radius:8px;box-shadow:0 3px 12px rgba(0,0,0,0.06)">
  <h3 style="margin:0 0 8px;color:#2E7D32">📚 Resurse pentru aprofundare</h3>
  <p style="margin:0 0 6px">Pentru cei interesați să aprofundeze [subiectul],
    <a href="https://event.2performant.com/events/click?ad_type=quicklink&aff_code=80f42fe2f&unique=[eticheta]&redirect_to=[URL_ENCODAT]" target="_blank" rel="noopener">[Numele resursei]</a>
    oferă explicații și exemple utile.</p>
  <p style="font-size:.85rem;color:#666;margin:10px 0 0"><em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em></p>
</div>
```

### 3) Freud / Jung (accente subtile)
```html
<!-- Freud -->
<div style="background:#FFF3E0;border-left:5px solid #FF9800;padding:18px 20px;margin:22px 0;border-radius:8px">
  <h3 style="margin:0 0 8px;color:#E65100">🔥 Perspectiva lui Freud</h3>
  <ul style="margin:0;line-height:1.8;color:#444">
    <li><strong>Punct cheie</strong> — explicație concisă</li>
  </ul>
</div>

<!-- Jung -->
<div style="background:#E8F5E9;border-left:5px solid #4CAF50;padding:18px 20px;margin:22px 0;border-radius:8px">
  <h3 style="margin:0 0 8px;color:#2E7D32">🌿 Perspectiva lui Carl Jung</h3>
  <ul style="margin:0;line-height:1.8;color:#444">
    <li><strong>Punct cheie</strong> — explicație concisă</li>
  </ul>
</div>
```

### 4) Card Scenariu (folosește doar când ajută)
```html
<div style="background:linear-gradient(135deg,#f6f9ff 0%,#eef4ff 100%);border-radius:12px;padding:18px 20px;box-shadow:0 4px 16px rgba(0,0,0,0.08);margin:22px 0">
  <h3 style="margin:0 0 6px;color:#20304a">🎭 Scenariul: [Titlu scurt]</h3>
  <p style="margin:0;color:#333;line-height:1.7"><strong>Semnificație:</strong> [fraza‑cheie] — explicație scurtă.</p>
  <p style="margin:8px 0 0;color:#4a6ea9;font-style:italic">💡 <strong>Cheie:</strong> [insight aplicabil]</p>
</div>
```

### 5) FAQ Schema (bloc unic + secțiune completă)
```html
<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question" style="background:#FAFAFA;padding:18px 20px;margin:14px 0;border-radius:8px;border:1px solid #eee">
  <h3 itemprop="name" style="margin:0 0 6px;color:#424242">[Întrebare clară]</h3>
  <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer">
    <div itemprop="text">
      <p style="margin:0;line-height:1.7">[Răspuns 150–250 cu detalii concrete]</p>
    </div>
  </div>
</div>
```

—

## Imagini (Pexels MCP + WordPress Media)

- Când: ~la 400–600 de cuvinte sau la tranziții vizuale firești; nu umple doar ca „decorație”.
- Ce: relevant, credibil, non‑clișeu; caută emoție + claritate (ex.: simbolul on‑topic, nu stock generic). 
- Alt text: în română, descriptiv + cuvânt‑cheie natural; fără „stuffing”.
- Denumire fișier: `slug-scurt-descriptor-pexelsID.jpg`
- Plasare: după intro, la mijloc, înainte de FAQ; spațiere consistentă.

Flux (indicativ):
1. Căutare: „Găsește 3–6 imagini Pexels pentru [subiect] (orientare landscape, ton natural, compoziție clară).”
2. Selectează 2–4; notează ID‑urile.
3. Încarcă prin WordPress MCP (media) + setează alt/caption.
4. Plasează imaginile în conținut unde sprijină înțelegerea.

Optimizare (ulterior / lot):
- Redimensionează max 1200px lățime; JPEG 75–80%.
- Menține consistență cromatică cu articolul.

—

## Monetizare (2Performant) — Abordare echilibrată

- Max 1 link afiliat / articol standard (2 dacă articolul e „resource‑heavy”).
- Plasare optimă: în caseta verde „Resurse”, aproape de final (înainte de FAQ) sau într‑o secțiune în care linkul chiar ajută.
- Ton: „Pentru cei interesați…”; zero presiune sau urgență falsă.
- Disclosure obligatoriu ANPC (vezi caseta verde de mai sus).
- Format link:
```
https://event.2performant.com/events/click?ad_type=quicklink&aff_code=80f42fe2f&unique=[eticheta]&redirect_to=[URL_ENCODED]
```
- Inventar recomandat (căi rapide): cărți Jung/Freud, dicționare de vise (Libris), jurnale (Librex), somn/stres (SpringFarma). Vezi „links.md” pentru exemple de URL‑uri produs + linkuri pre‑compuse.

—

## SEO Esențial (pe scurt)

- Titluri: clare, cu intenție; fără clickbait.
- Headere: H2/H3 dese, expresive; fără emoji‑spam; cuvinte‑cheie naturale.
- Conținut: 2.000–2.500 de cuvinte, fără „puf”; răspunsuri specifice, exemple reale.
- Imagini: alt descriptiv și on‑topic; încărcare rapidă (limitează dimensiunile).
- Schema: 6+ întrebări FAQ cu block‑urile de mai sus.
- Legături interne: întărește clustere (simboluri înrudite); ancore descriptive.
- Surse externe: OMS/Jung/Freud/Wikipedia‑RO; evită domenii slabe.

—

## Flux Operațional — Actualizare Articol Existent

1) Identifică candidatul
- Short (<1000w), fără FAQ, subțire sau nealiniat intenției.

2) Preia conținutul (WordPress MCP)
- „Adu postarea ID [id] (conținut complet).”

3) Plan & outline
- Mapează secțiunile conform tipului de articol; listează legături interne utile.

4) Scriere & extindere
- Intro cu răspuns; adâncime (Jung/Freud sau utilizare); scenarii concrete; tradiții românești unde se potrivește; 6 întrebări FAQ.
- Paragrafe scurte, H2/H3 frecvente, 1–2 imagini ajutătoare.

5) Monetizare echilibrată
- Inserează caseta verde cu 1 (max 2) linkuri relevante; adaugă disclosure.

6) Polish
- 1–2 linkuri interne; 1–2 citări externe credibile; verifică diacritice & AI‑tells.

7) Publicare
- Actualizează prin MCP; vizualizează și testează pe mobil.

8) Tracking
- Notează în „Systematic Article Upgrades.md”: rând în Master List (titlu, ID, înainte/după, % creștere, temă), plus agregate.

—

## Flux Operațional — Articol Nou

1) Alegere subiect
- Interpretabile (moarte, animale, familie, bani etc.) sau „ce înseamnă” cu volum căutări.

2) Cercetare
- SERP + „People also ask”, Wikipedia‑RO, OMS, lucrări Jung/Freud.

3) Draft (2.000–2.500w)
- Urmează șablonul corespunzător + 6 FAQ.

4) Imagini
- 1–2 imagini (Pexels MCP), alt optimizat.

5) Monetizare
- 1 casetă verde cu 1 link; eventual al doilea dacă e justificat.

6) Publicare & tracking
- Publică (draft→review→public); loghează în Master List.

—

## MCP — WordPress & Pexels (practic)

WordPress MCP (prin @instawp/mcp‑wp sau configurarea locală existentă):
- Listează/filtrează: „Afișează postări din categoria 5 (<1000w), ordonate descrescător după ID).”
- Citește: „Arată postarea ID [id], conținut + yoast_head_json/wordCount.”
- Actualizează: „Actualizează postarea [id] cu [HTML] și setează status [publish|draft].”
- Media: „Încarcă imaginea [fișier] cu alt ‘[text]’; atașează la postarea [id].”

REST fallback (dacă e nevoie):
- GET/POST `/wp-json/wp/v2/posts` (list, get, update), POST `/media` (upload). Autentificare Basic cu Application Password.

Pexels MCP:
- Caută: „Găsește imagini pentru [subiect], ton natural, landscape, 3–6 rezultate.”
- Selectează cele mai relevante (evită clișee); descarcă; apoi upload în WordPress Media.

—

## Snippet‑uri „Ready To Paste”

### Întrebări frecvente (secțiune completă — repetă blocul de mai sus de 6+ ori)
```html
<section>
  <h2>Întrebări frecvente (FAQ)</h2>
  <!-- Inserează 6+ blocuri "Question/Answer" din snippetul FAQ -->
</section>
```

### Ancoră internă utilă
```html
<p>Vezi și <a href="/ce-inseamna-cand-visezi-…/" rel="internal">interpretarea visului [temă înrudită]</a> pentru context suplimentar.</p>
```

### Referințe credibile (exemplu)
```html
<ul style="line-height:1.9">
  <li><a href="https://ro.wikipedia.org/wiki/[TEMA]" target="_blank" rel="nofollow">Wikipedia — [Tema]</a></li>
  <li>Organizația Mondială a Sănătății (OMS) — materiale despre [subiect]</li>
  <li>C.G. Jung / S. Freud — lucrări de referință</li>
  </ul>
```

—

## Controale De Calitate — Checklist Rapid

- [ ] 2.000–2.500 de cuvinte, cu răspuns rapid în introducere
- [ ] Structură clară (H2/H3 la 300–400 cuvinte)
- [ ] 6+ întrebări FAQ cu schema.org
- [ ] 1 (max 2) linkuri afiliate + disclosure
- [ ] 1–2 imagini cu alt corect, plasate util
- [ ] 1–2 legături interne + 1–2 citări externe credibile
- [ ] Ton profesional, fără „AI‑tells”, cu diacritice
- [ ] HTML curat, închis corect; aspect mobil verificat
- [ ] Publicat + testat pe mobil; trecut în Master List

—

## Note De Design (Sleek Flair fără excese)

- Un singur „hook” box la început doar dacă aduce claritate.
- Freud/Jung: accente cromatice subtile, nu „blocuri stridente”.
- Carduri scenariu: maxim 6, fiecare scurt și cu insight practic.
- Spațiere aerisită, umbre discrete, colțuri rotunjite; păstrează coerența cu badge‑urile albastre și fundalul cald al site‑ului.
- Evită tabele complexe pe mobil; convertește în liste când se poate.

—

## Ce Să Eviți (derapaje comune)

- Monetizare agresivă (multe linkuri, limbaj presant, CTA repetitiv)
- Gradient‑spam / emoji‑spam / vizual „țipător”
- Paragrafe lungi, blocuri de text fără respiro
- Afirmații fără surse, generalități vagi
- „Umplutură” care nu adaugă sens sau claritate

—

## Mini‑Workflow De Decizie (3 pași)

1) Intenție: ce vrea concret cititorul? (definiție, semnificație, aplicare, interpretare vis) → scrie răspunsul scurt întâi.
2) Profunzime: prin ce lentile adaugi valoare? (Jung/Freud, scenarii, tradiții, exemple practice, surse)
3) Monetizare: un singur bloc „Resurse” acolo unde chiar ajută; altfel, nimic.

—

## Unde Actualizezi Metadatele De Progres

- Fișier: `Systematic Article Upgrades.md` → adaugă rând în „MASTER LIST” (titlu, ID, înainte/după, % creștere, temă, status) și actualizează statisticile agregate + rezumat sesiune.

—

## Gata De Folosit

1) Alege articolul (candidați subțiri / oportunități mari)
2) Aplică șablonul potrivit + componentele HTML de mai sus
3) Adaugă 1 resursă afiliată bine aleasă
4) Pune 6+ întrebări FAQ cu schema
5) Publică, testează pe mobil, loghează progresul

Acest SOP este autosuficient: conține filozofie, structură, componente, monetizare echilibrată, imagini, SEO și pași MCP pentru a produce articole „banger” — curate, rapide, frumoase, care câștigă încredere și convertesc pe termen lung.

