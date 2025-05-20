## 🔋 Energiefluss-Visualisierung mit SVG + Floorplan-Card (Home Assistant)

Dieses Projekt zeigt, wie man mit einer SVG-Grafik und der `floorplan-card` Energieflüsse wie Solar, Batterie, Netz und Hausverbrauch visuell und dynamisch darstellt. Letztendlich müsst ihr im Beispielcode zur Card nur eure Entitäten/Sensoren austauschen und die Card sollte funktionieren. :)


### 🔧 Voraussetzungen

* HACS installiert
* `floorplan-card` Custom Card installiert
* Sensoren mit täglichen Energie-Werten
* CSS-Datei (energy-flow-card.css) zur dynamischen Gestaltung

Die meisten werden keine Sensoren für den realen Solarverbrauch (abzüglich Einspeisung und Batterieladung) haben. Genauso beim Verbrauch, hier wird der Netzbezug plus Batterie plus Erzeugung (erster Sensor) gerechnet, daher habe ich mir dafür zwei Sensoren angelegt. (danke nochmal @dreckfresse für den Gedankenanstoß.) 

```yaml
# Verrechnung für Diagramm Verbrauch und Erzeugung
- sensor:
  - name: "Erzeugzung taglich nach Abzug Einspeisung"
    unique_id: erzeugung_taglich_kWh
    unit_of_measurement: "kWh"
    state_class: total_increasing
    device_class: energy
    state: >
      {% set solar = states('sensor.growatt_todaygenerateenergy') | float(0) %}
      {% set batterie = states('sensor.acpowerzubatterie_energy_today') | float(0) %}
      {% set einspeisung = states('sensor.solar_netzeinspeisung_kwh_taglich') | float(0) %}
      {{ (solar - einspeisung - batterie) | round(2) }}
- sensor:
  - name: "Verbrauch taglich nach Abzug"
    unique_id: verbrauch_taglich_kWh
    unit_of_measurement: "kWh"
    state_class: total_increasing
    device_class: energy
    state: >
      {% set stromverbrauch = states('sensor.stromverbrauch_taglich') | float(0) %}
      {% set batterie = states('sensor.acpowervonbatterie_energy_today') | float(0) %}
      {% set erzeugung = states('sensor.erzeugzung_taglich_nach_abzug_einspeisung') | float(0) %}
      {% set batterieent = states('sensor.acpowerzubatterie_energy_today') | float(0) %}
      {% set einspeisung = states('sensor.solar_netzeinspeisung_kwh_taglich') | float(0) %}
      {{ (stromverbrauch + batterie + erzeugung - einspeisung - batterieent) | round(2) }}

```

---

### Aufbau der Card im Detail

Ihr müsst einfach in der Card eure Entitäten eintragen und könnt im Anschluss die Card nutzen. Alle Animationen und Grenzwerte ich habe soweit eingestellt. Ihr könnt sie natürlich anpassen, aber die Card sollte auf Anhieb funktionieren.

```yaml
type: custom:floorplan-card
grid_options:
  columns: full
config:
  console_log_level: info
  defaults:
    hover_action: hover-info
    tap_action: more-info
  image: /local/energy-flow-card/energy-flow-card-small.svg
  stylesheet: /local/energy-flow-card/energy-flow-card.css
  rules:
    - element: soc
      entity: sensor.batterie_ladezustand
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " %" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: batterie100
      entity: sensor.batterie_ladezustand
      state_action:
        action: call-service
        service: floorplan.style_set
        service_data: |
          ${parseFloat(entity.state) > 100 ? 'display:block' : 'display:none'}
    - element: batterie80
      entity: sensor.batterie_ladezustand
      state_action:
        action: call-service
        service: floorplan.style_set
        service_data: |
          ${parseFloat(entity.state) > 80 ? 'display:block' : 'display:none'}
    - element: batterie60
      entity: sensor.batterie_ladezustand
      state_action:
        action: call-service
        service: floorplan.style_set
        service_data: |
          ${parseFloat(entity.state) > 60 ? 'display:block' : 'display:none'}
    - element: batterie40
      entity: sensor.batterie_ladezustand
      state_action:
        action: call-service
        service: floorplan.style_set
        service_data: |
          ${parseFloat(entity.state) > 40 ? 'display:block' : 'display:none'}
    - element: batterie20
      entity: sensor.batterie_ladezustand
      state_action:
        action: call-service
        service: floorplan.style_set
        service_data: |
          ${parseFloat(entity.state) > 1 ? 'display:block' : 'display:none'}
    - element: dreieckbatteriein
      entity: sensor.acpowerzubatterie_energy_power
      state_action:
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 30) ?
            'display:block' : 'display:none'}
    - element: dreieckbatterieout
      entity: sensor.acpowervonbatterie_energy_power
      state_action:
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0.1) ?
            'opacity:1' : 'opacity:0'}
    - element: batteriein
      entity: sensor.acpowerzubatterie_energy_power
      state_action:
        - service: floorplan.class_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "batteriein" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "display:block" : "display:none"}
    - element: solarin
      entity: sensor.total_solar_power_kombiniert
      state_action:
        - service: floorplan.class_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "solarin" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "display:block" : "display:none"}
    - element: netzin
      entity: sensor.total_power
      state_action:
        - service: floorplan.class_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "netzin" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "display:block" : "display:none"}
    - element: netzout
      entity: sensor.solar_netzeinspeisung_kwh_taglich
      state_action:
        - service: floorplan.class_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "netzout" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "display:block" : "display:none"}
    - element: hausin
      entity: sensor.total_power_kombiniert
      state_action:
        - service: floorplan.class_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "hausin" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 10) ?
            "display:block" : "display:none"}
    - element: hausin
      entity: sensor.acpowervonbatterie_energy_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: >-
          ${(parseFloat(entity.state) > 0) ? 'hausin batteriebetrieb' :
          'hausin'}    
    - element: solarleistung
      entity: sensor.erzeugzung_taglich_kombination_solaranlagen
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: solarleistungwatt
      entity: sensor.total_solar_power_kombiniert
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " W" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: batterie
      entity: sensor.acpowerzubatterie_energy_today
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0.1) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: batterieout
      entity: sensor.acpowervonbatterie_energy_today
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0.1) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: batterieoutwatt
      entity: sensor.acpowervonbatterie_energy_power
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " W" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: hausverbrauchwatt
      entity: sensor.total_power_kombiniert
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " W" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: hausverbrauch
      entity: sensor.verbrauch_taglich_nach_abzug
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: netzbezug
      entity: sensor.stromverbrauch_taglich
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: netztbezugwatt
      entity: sensor.total_power
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " W" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: netzeinspeisung
      entity: sensor.solar_netzeinspeisung_kwh_taglich
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0.1) ?
            (Math.round(entity.state * 10) / 10).toString().replace(".", ",") +
            " kWh" : ""}
        - service: floorplan.style_set
          service_data: >-
            ${(entity.state !== undefined && parseFloat(entity.state) > 0) ?
            'display:block' : 'display:none'}
        - service: floorplan.class_set
          service_data:
            class: static-value
card_mod:
  style: |
    ha-card {
      background: none !important;   
      box-shadow: none !important;
      border: none;
    }

```

---

### Layout & Design

Hier gehe ich nochmal etwas näher auf die einzelnen Funktionen ein. Wie die floorplan-card generell funktioniert habe ich bereits zur Custom Pool-Flow-Card erklärt. Dort erfahrt ihr auch, wie man die ID mit Inkscape setzt.

#### 🧩 1. Floorplan-Card Konfiguration (`energy-flow.yaml`)

Die SVG-Grafik wird mit CSS verknüpft, um je nach Entity-Zustand Animationen oder Farben zu steuern.

```yaml
- type: 'custom:floorplan-card'
  config:
    image: /local/energy-flow.svg
    stylesheet: /local/energy-flow-card.css
    defaults:
      tap_action:
        action: more-info
    rules:
      - entity: sensor.battery_direction
        state: charging
        class: batteriein   # Startet Ladeanimation
      - entity: sensor.solar_power
        state: '> 100'
        class: solarin      # Zeigt Solarstromfluss
```

---

#### 🎨 2. CSS-Stylesheet (`energy-flow-card.css`)

Die CSS-Datei steuert Animationen und Sichtbarkeit innerhalb der SVG.

##### 🔁 Beispiel 1: Animation für Batterie-Ladevorgang

```css
.batteriein {
  animation: batteryFlow 4s infinite;
  transform-box: fill-box;
  transform-origin: center;
}
@keyframes batteryFlow {
  0%   { transform: translate(0, 0); }
  100% { transform: translate(-41px, 5.5px); }
}
```

#### 👻 Beispiel 2: Elemente bei bestimmten Zuständen ausblenden

```css
.entitystate-off {
  display: none !important;
}
```

#### 🌈 Beispiel 3: Farbe ändern bei Batterie-Betrieb

```css
.hausin.batteriebetrieb {
  fill: blue;
}
```

---

#### 📁 Dateien im Projekt

- `energy-flow.yaml` → Konfiguration für die Floorplan-Card
- `energy-flow-card.css` → Animationen & Styles
- `energy-flow.svg` → Die eigentliche Grafik mit IDs/Klassen für Zuordnung

---
