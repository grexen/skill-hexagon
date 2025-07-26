import matplotlib.pyplot as plt
import numpy as np

# Skill-Daten
skills = {
    "Frontend": 85,
    "DevOps \n& Infrastructure": 25,
    "Netzwerk \n& Sicherheit": 25,
    "Backend": 50,
    "Zusammenarbeit \n& Kommunikation": 90,
    "Testing & QA": 70
}

# Extrahiere Labels und Werte aus dem Dictionary
labels = list(skills.keys())
values = list(skills.values())

# Setup für Hexagon
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False) + np.pi/2  # +90° Drehung

# Hexagon Chart Setup (kartesisches Koordinatensystem)
fig, ax = plt.subplots(figsize=(8, 8))

# Konvertiere polare zu kartesische Koordinaten für die Skill-Werte
x_values = []
y_values = []
for i, value in enumerate(values):
    x = value * np.cos(angles[i])
    y = value * np.sin(angles[i])
    x_values.append(x)
    y_values.append(y)

# Schließe das Polygon
x_values.append(x_values[0])
y_values.append(y_values[0])

# Zeichne das Skill-Polygon
ax.plot(x_values, y_values, color="tab:green", linewidth=2)
ax.fill(x_values, y_values, color="tab:green", alpha=0.25)

# Hexagon-Gitterlinien zeichnen
for value in [20, 40, 60, 80, 100]:
    hex_x = []
    hex_y = []
    for angle in angles:
        x = value * np.cos(angle)
        y = value * np.sin(angle)
        hex_x.append(x)
        hex_y.append(y)
    # Schließe das Hexagon
    hex_x.append(hex_x[0])
    hex_y.append(hex_y[0])
    
    # Äußerste Linie dicker zeichnen
    if value == 100:
        ax.plot(hex_x, hex_y, color="lightgray", linewidth=1.5)
    else:
        ax.plot(hex_x, hex_y, color="lightgray", linewidth=0.5)

# Radiale Linien von der Mitte zu den Ecken
for angle in angles:
    x_end = 100 * np.cos(angle)
    y_end = 100 * np.sin(angle)
    ax.plot([0, x_end], [0, y_end], color="lightgray", linewidth=0.5)

# Achsen konfigurieren
ax.set_xlim(-120, 120)
ax.set_ylim(-120, 120)
ax.set_aspect('equal')
ax.axis('off')  # Entfernt alle Achsen und Rahmen

# Titel
ax.set_title("Skill Hexagon: Web Developer (Profil 2)", size=14, weight="bold", pad=20)

# Eigene Label-Positionierung außerhalb des Diagramms
label_padding = 1.15  # Abstand von der Mitte
for i, label in enumerate(labels):
    angle = angles[i]
    x = 100 * label_padding * np.cos(angle)
    y = 100 * label_padding * np.sin(angle)
    
    # Horizontale Ausrichtung basierend auf Position
    if x > 10:
        ha = "left"
    elif x < -10:
        ha = "right"
    else:
        ha = "center"
    
    # Vertikale Ausrichtung basierend auf Position
    if y > 10:
        va = "bottom"
    elif y < -10:
        va = "top"
    else:
        va = "center"
    
    ax.text(x, y, label, size=10, horizontalalignment=ha, verticalalignment=va, 
            multialignment='left')

plt.tight_layout()
plt.show()