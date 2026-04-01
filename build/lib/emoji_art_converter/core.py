from PIL import Image
import numpy as np
from .palette import load_palette

def _closest_emoji(r, g, b, palette):
    """Finde das Emoji mit der geringsten euklidischen Distanz im RGB-Raum."""
    best_char = palette[0]["char"]
    min_dist = float("inf")
    for em in palette:
        dr = em["r"] - r
        dg = em["g"] - g
        db = em["b"] - b
        dist = dr*dr + dg*dg + db*db
        if dist < min_dist:
            min_dist = dist
            best_char = em["char"]
    return best_char

def image_to_emoji(image_path, width=80, height=None, palette=None):
    """
    Konvertiert ein Bild in eine Emoji-Kunst.
    
    :param image_path: Pfad zum Bild (str) oder PIL.Image-Objekt
    :param width: Anzahl der Spalten (int)
    :param height: Anzahl der Zeilen (int, optional – wird aus Seitenverhältnis berechnet)
    :param palette: Liste von Emoji-Dicts mit "char", "r", "g", "b". Falls None, wird Standardpalette geladen.
    :return: Mehrzeiliger String mit Emoji-Kunst
    """
    if palette is None:
        palette = load_palette()
    
    # Bild laden
    if isinstance(image_path, str):
        img = Image.open(image_path)
    else:
        img = image_path
    
    # Größe berechnen
    orig_w, orig_h = img.size
    if height is None:
        height = int(width * orig_h / orig_w)
    # Begrenzung der Höhe (optional)
    if height > 150:
        height = 150
    
    # Bild skalieren
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    # In RGB konvertieren (falls RGBA)
    if img.mode == "RGBA":
        # Hintergrund schwarz oder weiß? Wir nehmen schwarz, um Transparenz zu vermeiden
        background = Image.new("RGB", img.size, (0, 0, 0))
        background.paste(img, mask=img.split()[3])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")
    
    pixels = np.array(img)
    rows = []
    for y in range(height):
        row_chars = []
        for x in range(width):
            r, g, b = pixels[y, x]
            row_chars.append(_closest_emoji(r, g, b, palette))
        rows.append("".join(row_chars))
    return "\n".join(rows)

def get_emoji_palette():
    """Gibt die Standard-Emoji-Palette zurück."""
    return load_palette()