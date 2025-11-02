# WordPress REST API — Cheat Sheet (fallback)

Endpoint de bază: `https://inteles.ro/wp-json/wp/v2`

Listare (ultimele 10):
```bash
curl "https://inteles.ro/wp-json/wp/v2/posts?per_page=10&order=desc"
```

Filtrare categorie (vise = 5):
```bash
curl "https://inteles.ro/wp-json/wp/v2/posts?categories=5&per_page=50&order=desc"
```

Obține postare:
```bash
curl "https://inteles.ro/wp-json/wp/v2/posts/{id}"
```

Actualizează postare (Basic Auth cu Application Password):
```bash
curl -u "username:app_password" -X POST \
  -H "Content-Type: application/json" \
  -d '{"content":"<p>HTML</p>","status":"publish"}' \
  "https://inteles.ro/wp-json/wp/v2/posts/{id}"
```

Upload media:
```bash
curl -u "username:app_password" -X POST \
  -H "Content-Disposition: attachment; filename=img.jpg" \
  -H "Content-Type: image/jpeg" \
  --data-binary @img.jpg \
  "https://inteles.ro/wp-json/wp/v2/media"
```

Note:
- Nu stoca parole în această notă — folosește manager securizat.

