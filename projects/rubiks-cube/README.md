# Rubik's Cube Guides

Printable picture guides for kids (German): **Schicht für Schicht** (Layer-by-Layer) and **CFOP** (with 2-look OLL and PLL).

Published guides are in `guides/` (HTML and PDF). The web page is `index.html`.

## Layout

```
src/
  cube.py                      cube simulator + SVG renderer (3x3, wide moves, slices)
  build_layer_by_layer.py      builds guides/schicht-fuer-schicht.html
  build_cfop.py                builds guides/cfop.html
  render_pdf.py                renders both HTML guides to A4 PDFs
  style.css                    print styles shared by both guides
  checks/                      scripts that verify the algorithms in the simulator
guides/                        generated output, committed so the site works without a build
```

## Rebuild

```bash
pip install playwright && playwright install chromium   # only for the PDFs
cd projects/rubiks-cube/src
python3 build_layer_by_layer.py
python3 build_cfop.py
python3 render_pdf.py
```

## Verify the algorithms

```bash
cd projects/rubiks-cube/src/checks
PYTHONPATH=.. python3 verify_cfop.py        # OLL algorithms
PYTHONPATH=.. python3 pll_strategy.py       # all 288 last-layer states
```

## Notes

- Orientation in all pictures: yellow up, white down, blue front, red right.
- The guides use the font Inter if installed and fall back to a system sans-serif otherwise.
