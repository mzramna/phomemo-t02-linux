"""Teste do suporte a Markdown do t02 (self-check ponytail, sem framework)."""
import os
import shutil
import sys
import tempfile
from importlib.machinery import SourceFileLoader

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

if not any(shutil.which(c) for c in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")):
    print("sem chrome/chromium instalado, pulando teste de markdown")
    sys.exit(0)

t02 = SourceFileLoader("t02", os.path.join(HERE, "t02")).load_module()

with tempfile.TemporaryDirectory() as tmp:
    png_path = os.path.join(tmp, "dot.png")
    Image.new("RGB", (50, 50), "black").save(png_path)

    md_path = os.path.join(tmp, "test.md")
    md_path_obj = md_path
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"""# Titulo

**b** *i* ++u++

- item 1
- item 2

> citacao

```
a++; b++
```

| A | B | C |
|---|---|---|
| aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | x | y |

![dot]({os.path.basename(png_path)})
""")

    img = t02.render_md(md_path)

    assert img.width == 384, f"largura esperada 384, veio {img.width}"
    assert 20 < img.height < 16384, f"altura fora do esperado: {img.height}"

    gray = img.convert("L")
    pixels = gray.getdata()
    assert any(p < 50 for p in pixels), "esperava pixels pretos (texto/tabela/imagem)"

    # as 3 colunas mais a direita devem ser brancas (sem overflow do texto)
    for x in range(img.width - 3, img.width):
        col_pixels = [gray.getpixel((x, y)) for y in range(img.height)]
        assert all(p > 200 for p in col_pixels), f"coluna {x} nao esta branca (overflow horizontal)"

    t02.to_bitmap(img)  # so precisa rodar sem erro

    out_png = "/tmp/claude-1000/-home-mzramna/84ca9cc8-6c90-4dff-a549-e5261d65b2b0/scratchpad/md_test.png"
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    img.save(out_png)
    print(f"OK: {img.width}x{img.height}, salvo em {out_png} ({os.path.getsize(out_png)} bytes)")
