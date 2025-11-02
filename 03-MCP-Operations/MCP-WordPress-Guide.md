# MCP WordPress Guide (inteles.ro)

Scop: comenzi uzuale pentru listare, verificare wordCount, actualizare conținut și media.

Categorii:
- Înțelesul Viselor (ID 5)

Flux uzual:
1) Identifică candidați: „Listează postări în categoria 5, per_page=50, orderby=id desc; arată wordCount; filtrează <1000w.”
2) Verifică dacă nu e deja upgradat (caută elemente vizuale + FAQ).
3) Preia postarea completă (titlu, content, schema/wordCount).
4) Actualizează conținutul (HTML complet) și publică.
5) Încarcă imagini (alt setat), atașează la postare.

Formulări utile (în conversație cu agentul MCP):
- „Listă postări categoria 5 (vise), per_page=50, page=1, orderby=id, order=desc.”
- „Arată postarea ID 3875, vreau detalii și conținut.”
- „Actualizează post ID 3875 cu acest HTML (status publish).”
- „Urcă această imagine cu alt ‘[descriere]’ și atașeaz-o la postarea 3875.”

Notă REST: vezi [[REST-API-CheatSheet]] pentru curl și endpoints.

