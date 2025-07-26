# Pro Evolution Skill Generator

Ein interaktives Tool zur Erstellung von Skill-Hexagon-Diagrammen mit Drag-and-Drop Funktionalität und Custom Skills.

## Features

- 🎯 Interaktive Skill-Konfiguration mit modernen Slidern
- 🔄 Drag-and-Drop zum Neuanordnen der Skills (Uhrzeigersinn im Hexagon)
- ➕ Custom Skills hinzufügen
- 📊 Live Chart-Updates
- 📋 GitHub-Style Copy-to-Clipboard Funktionalität
- 🎨 Pro Evolution Gaming-Design

## Lokale Entwicklung

### Voraussetzungen
- Python 3.11+
- pip

### Installation
```bash
git clone <repository-url>
cd skillhexagon
pip install -r requirements.txt
python app.py
```

Die Anwendung ist dann unter `http://localhost:5000` verfügbar.

## Docker Deployment

### Lokales Testen mit Docker
```bash
# Docker Image bauen
docker build -t skillhexagon .

# Container starten
docker run -p 5000:5000 skillhexagon

# Oder mit Docker Compose
docker-compose up --build
```

### V-Server Deployment über GitHub Actions

#### 1. GitHub Secrets konfigurieren
Fügen Sie folgende Secrets in Ihrem GitHub Repository hinzu (`Settings > Secrets and variables > Actions`):

- `HOST`: IP-Adresse oder Domain Ihres V-Servers
- `USERNAME`: SSH-Benutzername für den V-Server
- `PRIVATE_KEY`: Ihr privater SSH-Schlüssel (gesamter Inhalt der .pem/.key Datei)
- `PORT`: SSH-Port (normalerweise 22)

#### 2. V-Server vorbereiten
Auf Ihrem V-Server müssen Docker und Docker Compose installiert sein:

```bash
# Docker installieren (Ubuntu/Debian)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose installieren
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 3. Automatisches Deployment
Das Deployment erfolgt automatisch bei jedem Push zum `main` Branch:

1. Code wird in GitHub Container Registry (ghcr.io) als Docker Image gebaut
2. Image wird auf den V-Server deployed
3. Alte Container werden gestoppt und durch neue ersetzt
4. Anwendung läuft unter Port 5000

#### 4. Reverse Proxy (optional)
Für Produktionsumgebungen empfiehlt sich ein Reverse Proxy (nginx):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Konfiguration

Die Skill-Konfiguration erfolgt über `config.yml`:

```yaml
app:
  max_skills: 6
  default_chart_title: "Pro Evolution Skills"

skills:
  shooting:
    label: "Shooting"
    description: "Ability to score goals..."
    default_value: 50
```

## Architektur

- **Backend**: Flask 3.0 mit matplotlib für Chart-Generierung
- **Frontend**: Vanilla JavaScript mit modernem CSS
- **Deployment**: Docker + GitHub Actions
- **Storage**: YAML-basierte Konfiguration

## Lizenz

MIT License
