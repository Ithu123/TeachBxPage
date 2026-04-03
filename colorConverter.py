import json
import os

def json_to_gpl(json_file, output_name="MaterialTheme"):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        # Falls die JSON vom Material Theme Builder kommt, 
        # liegen die Farben meist unter 'schemes' (light/dark) oder 'palettes'
        colors = {}
        
        # Rekursive Suche nach Hex-Codes
        def find_colors(d, prefix=""):
            for key, value in d.items():
                new_key = f"{prefix} {key}".strip()
                if isinstance(value, dict):
                    find_colors(value, new_key)
                elif isinstance(value, str) and value.startswith("#"):
                    colors[new_key] = value

        find_colors(data)

        if not colors:
            print("Keine Farben im JSON gefunden.")
            return

        # GPL Datei schreiben
        with open(f"{output_name}.gpl", "w") as gpl:
            gpl.write("GIMP Palette\n")
            gpl.write(f"Name: {output_name}\n")
            gpl.write("Columns: 4\n")
            gpl.write("#\n")

            for name, hex_val in colors.items():
                # Hex zu RGB konvertieren
                h = hex_val.lstrip('#')
                r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
                
                # Format: R G B Name (Tab-getrennt)
                gpl.write(f"{r:3} {g:3} {b:3}\t{name}\n")
        
        print(f"Erfolg! '{output_name}.gpl' wurde mit {len(colors)} Farben erstellt.")

    except Exception as e:
        print(f"Fehler: {e}")

# Beispielaufruf
if __name__ == "__main__":
    # Pfad zu deiner exportierten JSON Datei anpassen
    json_to_gpl('material-theme.json', 'MyMaterialPalette')