# VisConnect - 3D Visualisierung von Stahlverbindungen

Eine Python Anwendung zur Visualisierung und Analyse von Bauteilen und Verbindungen im Stahlbau.

## Funktionen

#### 3D-Visualisierung von Standard-Stahlbauteilen:
  - HEA-Träger 
  - IPE-Träger (geplant)
  - Verbindungsplatten
<div style="display: flex; justify-content: center; gap: 20px;">
<img src="/assets/HEA.png" width="300" height="200" alt="HEA">
<img src="/assets/add_menu.png" width="300" height="200" alt="HEA">
</div>

#### Interaktive Objektmanipulation:
  - Rotation um X-, Y-, Z-Achsen
  - Veränderung der Position
  - Sichtbar/ nicht Sichtbar
<img src="/assets/interaction_menu.png" width="300" height="200" alt="InteractionsMenu">


#### Connection point Visualisierung und Verwaltung
  - Management von Mesh clicking
  - Visualisieren von möglichen Verbindungspunkten (und derer Oriantation)

#### Benutzeroberfläche mit:
  - Objektlist-Overlay
  - Kontextmenüs
  - Anpassbare Ansichten
<img src="/assets/object_menu.png" width="300" height="200" alt="ObjectMenu">



## Technische Details

Erstellt mit:
- PyQt6 für die Benutzeroberfläche
- PyVista für 3D-Visualisierung
- Python Dataclasses für Bauteil-Definitionen

## Geplant

Zukünftige Funktionen:
- Berechnung der Festkeitswerte
- Zusätzliche Trägerprofile (alle Standart Träger)
- Erweiterte Verbindungstypen (schweißnähte, angewinkelte Verbindungen)
- Exportmöglichkeiten (Json Format struktur)

## Installation

1. Abhängigkeiten installieren:

```python
pip install PyQt6 pyvista numpy
```