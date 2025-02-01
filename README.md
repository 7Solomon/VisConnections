# VisConnect - 3D Strukturtechnik-Visualisierung

Eine Python Anwendung zur Visualisierung und Analyse von Bauteilen und Verbindungen im Stahlbau.

## Funktionen

- 3D-Visualisierung von Standard-Stahlbauteilen:
  - HEA-Träger 
  - IPE-Träger (geplant)
  - Verbindungsplatten
![HEA](/assets/HEA.png | width=300)
![HEA](/assets/add_menu.png | width=300)

- Interaktive Objektmanipulation:
  - Rotation um X-, Y-, Z-Achsen
  - Veränderung der Position
  - Sichtbar/ nicht Sichtbar
![InteractionsMenu](/assets/interaction_menu.png | width=300)

- Verbindungspunkt-Visualisierung und -Verwaltung
- Benutzeroberfläche mit:
  - Objektlisten-Overlay
  - Kontextmenüs
  - Anpassbare Ansichten
![ObjectMenu](/assets/object_menu.png | width=300)


## Technische Details

Erstellt mit:
- PyQt6 für die Benutzeroberfläche
- PyVista für 3D-Visualisierung
- NumPy für Berechnungen
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