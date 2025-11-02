# HTML — Minimal Snippets Only

Info Box (orange)
```html
<div style="background:#FFF3E0;border-left:4px solid #FF6F00;padding:20px;margin:25px 0;border-radius:8px">
  <h3 style="margin:0 0 10px;color:#E65100">📋 Ce vei afla</h3>
  <ul style="margin:0;line-height:1.8"><li>Punct 1</li><li>Punct 2</li></ul>
</div>
```

Resource Box (green, with disclosure)
```html
<div style="background:#E8F5E9;border-left:4px solid #4CAF50;padding:20px;margin:25px 0;border-radius:8px">
  <h3 style="margin:0 0 8px;color:#2E7D32">📚 Resurse</h3>
  <p style="margin:0 0 6px">Pentru aprofundare, <a href="[2P_LINK]" target="_blank" rel="noopener">[Resursă]</a>.</p>
  <p style="font-size:.85rem;color:#666;margin:10px 0 0"><em>Link afiliat — câștigăm un mic comision fără costuri pentru tine.</em></p>
</div>
```

FAQ Block
```html
<div itemscope itemprop="mainEntity" itemtype="https://schema.org/Question" style="background:#FAFAFA;padding:18px 20px;margin:14px 0;border-radius:8px;border:1px solid #eee">
  <h3 itemprop="name" style="margin:0 0 6px;color:#424242">[Întrebare]</h3>
  <div itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">
    <p style="margin:0;line-height:1.7">[Răspuns 150–250]</p>
  </div></div>
</div>
```

