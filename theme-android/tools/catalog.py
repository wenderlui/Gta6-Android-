"""Gera appfilter.xml, drawable.xml e Catalog.kt a partir de icons.ICONS e wallpapers.SCENES.

Uso: python3 tools/catalog.py
"""
import os
from xml.sax.saxutils import quoteattr
import icons
import wallpapers

ROOT = os.path.join(os.path.dirname(__file__), "..", "app", "src", "main")
LABELS = {
    "wall_sunset_shore": "Pôr do sol na orla", "wall_neon_grid": "Grade neon", "wall_skyline": "Cidade ao entardecer",
    "wall_palm_night": "Noite de palmeiras", "wall_highway": "Estrada infinita", "wall_waves": "Ondas pastel",
    "wall_neon_sign": "Letreiro neon", "wall_pastel_shore": "Calçadão",
}


def main():
    lines = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>",
             '    <iconback img1="iconback" />', '    <scale factor="0.62" />']
    for name, (_, _, comps) in icons.ICONS.items():
        for c in comps:
            lines.append(f"    <item component={quoteattr('ComponentInfo{' + c + '}')} drawable=\"ic_{name}\" />")
    lines.append("</resources>\n")
    appfilter = "\n".join(lines)
    os.makedirs(os.path.join(ROOT, "res", "xml"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    for p in (os.path.join(ROOT, "res", "xml", "appfilter.xml"), os.path.join(ROOT, "assets", "appfilter.xml")):
        open(p, "w").write(appfilter)

    dl = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>", '    <version>1</version>', '    <category title="Neon Shore" />']
    dl += [f'    <item drawable="ic_{n}" />' for n in icons.ICONS]
    dl.append("</resources>\n")
    for p in (os.path.join(ROOT, "res", "xml", "drawable.xml"), os.path.join(ROOT, "assets", "drawable.xml")):
        open(p, "w").write("\n".join(dl))

    kt = ["// Arquivo gerado por tools/catalog.py — não edite à mão.", "package com.wenderlui.neonshore", "",
          "object Catalog {", "    val icons = intArrayOf("]
    kt += [f"        R.drawable.ic_{n}," for n in icons.ICONS]
    kt += ["    )", "", "    val wallpapers = listOf("]
    for name, _ in wallpapers.SCENES:
        kt.append(f'        Wallpaper(R.drawable.{name}, R.drawable.{name}_thumb, "{LABELS[name]}"),')
    kt += ["    )", "}", "", "data class Wallpaper(val full: Int, val thumb: Int, val title: String)", ""]
    kt_dir = os.path.join(ROOT, "java", "com", "wenderlui", "neonshore")
    os.makedirs(kt_dir, exist_ok=True)
    open(os.path.join(kt_dir, "Catalog.kt"), "w").write("\n".join(kt))
    total = sum(len(c) for _, _, c in icons.ICONS.values())
    print(f"{len(icons.ICONS)} ícones, {total} componentes mapeados, {len(wallpapers.SCENES)} wallpapers")


if __name__ == "__main__":
    main()
