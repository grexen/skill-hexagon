from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
import matplotlib
import yaml
import os
matplotlib.use('Agg')  # Non-interactive backend

app = Flask(__name__)

# Lade Konfiguration
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yml')
    with open(config_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

config = load_config()

# Konstanten aus Konfiguration
DEFAULT_TITLE = config['app']['default_chart_title']

def create_skill_hexagon(skills_data, title="Skill Hexagon"):
    # Labels aus Konfiguration mit Zeilenumbrüchen für bessere Darstellung
    display_labels = {}
    for key, skill in config['skills'].items():
        label = skill['label']
        # Füge Zeilenumbrüche für lange Labels hinzu
        if len(label) > 15:
            words = label.split(' ')
            if len(words) > 1:
                mid = len(words) // 2
                label = ' '.join(words[:mid]) + ' \n' + ' '.join(words[mid:])
        display_labels[skill['label']] = label
    
    # Extrahiere Labels und Werte aus dem Dictionary
    labels = [display_labels.get(key, key) for key in skills_data.keys()]
    values = list(skills_data.values())
    
    # Setup für Hexagon
    num_vars = len(labels)
    # Für Uhrzeigersinn: Starte bei 90° (oben) und gehe im Uhrzeigersinn (-2π statt +2π)
    angles = np.pi/2 - np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

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

    # Titel mit Gaming-Font
    ax.set_title(title, size=16, weight="bold", pad=20, family='monospace', 
                style='normal', variant='normal')

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
    
    # Konvertiere zu Base64 für Web-Display
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/')
def index():
    # Standard Skills aus Konfiguration laden (erste 6 als Default)
    max_skills = config['app']['max_skills']
    default_skill_keys = config['default_skills'][:max_skills]  # Limitiere auf max_skills
    default_skills = {}
    all_skills = {}
    
    # Alle verfügbaren Skills sammeln
    for key, skill in config['skills'].items():
        all_skills[key] = {
            'label': skill['label'],
            'description': skill['description'],
            'default_value': skill['default_value']
        }
        
        # Default Skills für initial angezeigtes Hexagon
        if key in default_skill_keys:
            default_skills[skill['label']] = skill['default_value']
    
    plot_url = create_skill_hexagon(default_skills, DEFAULT_TITLE)
    return render_template('index.html', 
                         plot_url=plot_url, 
                         skills=default_skills, 
                         default_title=DEFAULT_TITLE,
                         config=config,
                         all_skills=all_skills,
                         default_skill_keys=default_skill_keys,
                         max_skills=max_skills)

@app.route('/update_chart', methods=['POST'])
def update_chart():
    data = request.json
    skills = data.get('skills', {})
    title = data.get('title', DEFAULT_TITLE)
    
    # Konvertiere String-Werte zu Integers
    try:
        skills = {k: int(v) for k, v in skills.items()}
    except (ValueError, TypeError):
        skills = {k: 50 for k in skills.keys()}  # Fallback-Werte
    
    plot_url = create_skill_hexagon(skills, title)
    return jsonify({'image': plot_url})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
