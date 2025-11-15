def darken_color(hex_color, factor=0.8):
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    darkened = [max(0, int(c * factor)) for c in rgb]
    return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"

def lighten_color(hex_color, factor=0.8):
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    lightened = [min(255, int(c + (255 - c) * factor)) for c in rgb]
    return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"