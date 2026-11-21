> LEGACY: describes the old automatic plate pipeline. Do not use it to design icons — see REDESIGN.md.

# Lesson 6 — Hand-built icons

Use this when OVERRIDES cannot fix an app:

* a box/screen inside the tile whose content must be clipped to the plate (Terminal Emulator),
* the mark is cropped by the tile edge (Shizuku),
* figure and ground must be rebuilt (ChatGPT),
* a poster or mascot (Clash Royale, Survivor.io),
* the automatic regions keep picking up noise (Dolby Atmos: the disc's thin rim line).

Hand-built apps are functions in `work/_lib/build_weak.py`. `make_icon.py` uses the
function automatically when one exists for the slug.

## 6.1 The template (Dolby Atmos — copy this)

```python
@build
def dolby_atmos():
    """Source: Dolby's pale disc with the dark double-D (cropped from the phone's app-info
    screen). The pale disc is the TILE (plate/disc colour); the mark is exactly the two
    largest dark components (the Ds) - the disc's thin rim line is not part of the mark."""
    a, s = gt.load(WORK / "dolby_atmos")                 # source.png as float RGBA, s = units per pixel
    dark = (lum(a) < 0.45) & gt.opaque(a)                # 1. a mask by a colour rule
    comps = gt.components(dark)                          # 2. connected pieces, largest first
    ds_src = [trace(comps[0] | comps[1], s)]             # 3. trace -> SVG path in 0..128
    PALE, INKD = "#dae5ea", "#465461"                    # 4. colours measured from the source
    out = {}
    for st, title, base, bx in (("faithful", "Faithful", lambda i: fam.plate(i, PALE), box_c(64, 62, 66, 52)),
                                ("disc", "Sound Disc", lambda i: fam.disc(i, PALE, top_light=0), box_c(64, 63, 70, 54)),
                                ("rimmed", "Rimmed", lambda i: i.rimmed_disc(inner=PALE, rim_face="#f6f5f4"), box_c(64, 63, 60, 46))):
        ic = gk.Icon(f"Dolby Atmos - {title}", note("dolby_atmos", "pale tile + dark double-D"))
        base(ic)                                         # 5. the plate / disc / rim (with chin)
        ds, _ = place(ds_src, bx)                        # 6. scale the mark into a box (aspect kept)
        raised(ic, [(ds[0], INKD)], lift=2)              # 7. the mark with its lift
        out[st] = ic
    ic = gk.Icon("Dolby Atmos - Free Symbol", note("dolby_atmos", "double-D with a pale margin"))
    ds, _ = place(ds_src, box_c(64, 76, 104, 72))
    body = fam.offset_d(ds[0], 4.0)                      # 8. a margin around the mark
    x0, _, x1, _ = gk.bbox_d(body)
    ic.path(gk.translate_d(body, 0, 4), ic.chin_gradient(PALE, x0, x1, 10), layer_id="body-chin")
    ic.path(body, PALE, layer_id="body-face")
    raised(ic, [(ds[0], INKD)], lift=1.5)
    out["symbol"] = ic
    return out
```

Run `python3 tools/make_icon.py dolby_atmos`; adjust the boxes until the gate passes.

## 6.2 Your toolbox

| Helper | Does |
|---|---|
| `gt.load(dir)` | `source.png` → array `a` (H×W×4, 0..1), `s` = 128-units per pixel |
| `gt.near(a, "#hex1", "#hex2")` | mask of pixels closer to hex1 than hex2 |
| `lum(a)`, `gt.opaque(a)` | brightness, alpha mask — build masks with `<`, `>`, `&`, `|`, `~` |
| `gt.components(mask)` | connected pieces, largest first |
| `gt.fill_holes(mask)`, `gt.circle_fit(mask, s)`, `gt.bbox(mask, s)` | measure shapes |
| `trace(mask, s, smooth_u=0.45)` | mask → clean SVG path (0..128) |
| `place(paths, box_c(cx, cy, w, h))` | scale+move paths together into a box (aspect kept) |
| `fam.plate`, `fam.disc`, `fam.rimmed`, `ic.rimmed_disc` | the GNOME bases (with chins) |
| `fam.slab(ic, d, colour, depth=4)` | any shape as an object with a chin (Symbol) |
| `raised(ic, [(d, colour), …], lift=2)` | marks with their lift (sides first) |
| `fam.offset_d(d, 4)` | margin around a mark |
| `poly_of(d)`, `d_of(geom)`, `clip(d, "plate"/"disc"/"rimmed")` | shapely geometry: union, intersection, clipping to the face |
| `tile_to(d, x0, y0, size)` | map source-tile coordinates onto a square (for crops like Shizuku) |
| `ic.linear(stops, x1, y1, x2, y2)` | a gradient (only for curved or brand-gradient faces) |

## 6.3 Patterns from the project (read the functions in `build_weak.py`)

| App | Pattern |
|---|---|
| `terminal_em_lat_r` | the screen becomes the plate; its lime area is clipped to the face with `clip()` |
| `shizuku` | the head is cropped by the tile → crop it by each face the same way (`tile_to` + `clip`); Symbol = the source's hexagon as a badge |
| `chatgpt` (in `build_group1.py`) | figure/ground: the white silhouette is the object, the dark lines are inlaid on it |
| `hesap_makinesi` | keys as raised slabs, the stationery traced by colour standing on them |
| `clash_royale` | free adaptation: two crowns (one measured, one mirrored with the other king's band colour) on the measured blue/red split |
| `survivor_io` | free adaptation from primitives (witch hat + coins) in measured colours |
| `konabess` | measured ring/slash (circle and line fits) + a GNOME chip; unreadable text dropped |
| `walpy`, `bcr` | blurry sources (see R7) |
| `gnomed` | an original logo (our own app, no third-party source) |

## 6.4 Rules for free adaptation

1. Only when tracing cannot produce a clean icon (posters, illustrations, crops).
2. Pick **one** element the users know. Measure its shape and colours from the source
   wherever possible.
3. Primitives (circles, curves, polygons) are allowed for generic objects (a hat, a coin,
   a chip) — **never** to redraw a brand's logo from memory.
4. Document it in the docstring and in the PR.
