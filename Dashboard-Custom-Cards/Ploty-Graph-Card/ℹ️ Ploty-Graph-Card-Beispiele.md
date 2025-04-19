## 📊 **Plotly Graph Card** – Stromverbrauch & PV-Übersicht

Ich habe eine Weile gesucht, um die gestapelte Balkendiagramme zu realisieren. Mit der apex-chart card habe ich keinen Weg gefunden, daher bin ich jetzt auf die ploty-graph card gewechselt. Das kommt dem Energie Dashboard von HA schon sehr nah, wie ich finde. :)

Die `custom:plotly-graph`-Karte kann dir übersichtlich zeigen, wie sich dein täglicher Stromverbrauch zusammensetzt – inklusive **PV-Erzeugung**, **Netzbezug** und **Batterienutzung**. Ideal zur Visualisierung von Energieflüssen!


### 🔧 Voraussetzungen

* HACS installiert
* `plotly-graph` Custom Card installiert
* Sensoren mit täglichen Energie-Werten

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

```yaml
type: custom:plotly-graph
title: Aufteilung
hours_to_show: 7d
refresh_interval: 10
```

* **title**: Titel der Karte.
* **hours_to_show**: Zeitraum der Anzeige – hier 7 Tage (1m für ein Monat)
* **refresh_interval**: Daten werden alle 10 Sekunden aktualisiert.

---

### Layout & Design

```yaml
layout:
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  barmode: relative
  bargap: 0.2
  barcornerradius: 8
  uniformtext:
    minsize: 10
    mode: show
  modebar:
    orientation: v
    remove: zoom
  margin:
    t: 15
    l: 45
    r: 20
```

* **paper_bgcolor** / **plot_bgcolor**: Transparenter Hintergrund.
* **barmode: relative**: Balken werden übereinandergelegt (stacked).
* **bargap**: Abstand zwischen Balken (0–1).
* **barcornerradius**: Abgerundete Balken.
* **uniformtext**: Einheitliche Textgröße.
* **modebar**: Werkzeugleiste – hier wird Zoom ausgeblendet.
* **margin**: Randabstände (top, left, right).

---

### Globale Einstellungen (defaults)

```yaml
defaults:
  entity:
    period: day
    type: bar
    statistic: state
    filters:
      - filter: i>0
```

* **period: day**: Zeigt Tageswerte.
* **type: bar**: Balkendiagramm.
* **statistic: state**: Nutzt den Zustand des Sensors (z. B. kWh).
* **filter: i>0**: Nur Werte größer 0 werden dargestellt (Filter gegen Nullwerte).

---

### Eingebundene Sensoren


```yaml
entities:
  - entity: sensor.erzeugzung_taglich_nach_abzug_einspeisung
    name: PV
    marker:
      color: green
      opacity: 0.7

  - entity: sensor.stromverbrauch_taglich
    name: Netzbezug
    marker:
      color: darkorange
      opacity: 0.7

  - entity: sensor.acpowervonbatterie_energy_today
    name: Batterie
    marker:
      color: steelblue
      opacity: 0.7
```

Jede **Entität** wird:

* Benannt (`name`)
* Farblich dargestellt (`color`)
* optional mit Transparenz versehen (`opacity`)

---

### ✅ Ergebnis

Modernes, kompaktes und aussagekräftiges Balkendiagramm, das zeigt:

* Wieviel Strom täglich aus dem Netz bezogen wurde
* Wieviel aus der Batterie kam
* Wieviel PV selbst verbraucht wurde (nach Abzug der Einspeisung)
---

## So und nun zu den Beispielen:

📌 einfache Darstellung sehr ähnlich zum Energie-Dashboard

![image](https://github.com/user-attachments/assets/7e8db080-f568-45bd-b385-2f7fe67e8af1)


```yaml
type: custom:plotly-graph
card_mod:
  style: |
    ha-card {
        border-width: 0px;
       }
layout:
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  barmode: relative
  bargap: 0.2
  barcornerradius: 8
  uniformtext:
    minsize: 10
    mode: show
  modebar:
    orientation: v
    remove: zoom
  margin:
    t: 15
    l: 45
    r: 20
defaults:
  entity:
    period: day
    type: bar
    statistic: state
    filters:
      - filter: i>0
entities:
  - entity: sensor.erzeugzung_taglich_nach_abzug_einspeisung
    name: PV
    marker:
      color: green
      opacity: 0.7
  - entity: sensor.stromverbrauch_taglich
    name: Netzbezug
    marker:
      color: darkorange
      opacity: 0.7
  - entity: sensor.acpowervonbatterie_energy_today
    name: Batterie
    marker:
      color: steelblue
      opacity: 0.7
hours_to_show: 7d
refresh_interval: 10
grid_options:
  columns: 24
  rows: 5
title: Aufteilung

```

📌 Das selbe Bespiel etwas erweitert und sortierter. Zusätzlich Zeitauswahl hinzugefügt.

![image](https://github.com/user-attachments/assets/986a78fb-7133-49fb-9d9c-d8825094723f)


```yaml
type: custom:plotly-graph
defaults:
  yaxes:
    fixedrange: true
  entity:
    period: day
    type: bar
    statistic: state
    texttemplate: "%{y:.1f}"
    textposition: auto
    filters:
      - filter: i>0
entities:
  - entity: sensor.erzeugzung_taglich_nach_abzug_einspeisung
    name: Erzeugung
    marker:
      color: green
      opacity: 2
  - entity: sensor.acpowervonbatterie_energy_today
    name: Akku Entladung
    marker:
      color: "#6C9BC4"
      opacity: 2
  - entity: sensor.stromverbrauch_taglich
    name: Bezug
    marker:
      color: "#EE7A06"
      opacity: 2
layout:
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  barmode: stack
  bargap: 0.2
  barcornerradius: 5
  uniformtext:
    minsize: 10
    mode: show
  modebar:
    orientation: v
    remove: zoom
  margin:
    t: 15
    l: 45
    r: 20
  height: 500
  legend:
    "y": -0.25
    x: 0.02
  xaxis:
    rangeselector:
      "y": 1.15
      buttons:
        - count: 1
          step: day
        - count: 7
          step: day
        - count: 10
          step: day
        - count: 30
          step: day
    gridcolor: rgba(238,235,235,0.3)
    autorange: true
    showgrid: true
  yaxis:
    visible: true
    autorange: true
hours_to_show: 7d
refresh_interval: 15
card_mod:
  style: |
    ha-card {
        border-width: 0px;
       }
view_layout:
  position: main
grid_options:
  columns: full

```

📌 Nun kommt das worauf es mir persönlich ankommt. Hier findet eine Aufteilung statt. Man sieht die Solarprognose für den laufenden Tag, im zweiten Balken wie sich der Strom aus Netzbezug, Solar und Batterie zusammensetzt und im dritten Balken wie der Verbrauch sich aufteilt, in Netzeinspeisung, Batterieladung und restlicher Verbrauch.

![image](https://github.com/user-attachments/assets/45d6df8c-2eb7-4714-9a0d-964a20d24932)


```yaml
type: custom:plotly-graph
defaults:
  yaxes:
    fixedrange: true
  entity:
    period: day
    type: bar
    statistic: state
    texttemplate: "%{y:.1f}"
    textposition: auto
entities:
  - entity: sensor.erzeugzung_taglich_nach_abzug_einspeisung
    name: Erzeugung
    marker:
      color: green
      opacity: 1
    textfont:
      color: black
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(0,0,0)],
            ys: [...ys, hass.states['sensor.erzeugzung_taglich_nach_abzug_einspeisung'].state],
          })
  - entity: sensor.acpowervonbatterie_energy_today
    name: Akku Entladung
    marker:
      color: "#6C9BC4"
      opacity: 1
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(0,0,0)],
            ys: [...ys, hass.states['sensor.acpowervonbatterie_energy_today'].state],
          })
  - entity: sensor.stromverbrauch_taglich
    name: Bezug
    marker:
      color: darkorange
      opacity: 1
    textfont:
      color: black
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(0,0,0)],
            ys: [...ys, hass.states['sensor.stromverbrauch_taglich'].state],
          })
  - entity: sensor.verbrauch_taglich_nach_abzug
    name: Verbrauch
    marker:
      color: "#CAD97D"
      opacity: 0.5
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(6,0,0)],
            ys: [...ys, hass.states['sensor.verbrauch_taglich_nach_abzug'].state],
          })
    time_offset: 6h
  - entity: sensor.acpowerzubatterie_energy_today
    name: Akku Beladung
    marker:
      color: "#AAE1FC"
      opacity: 0.5
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(6,0,0)],
            ys: [...ys, hass.states['sensor.acpowerzubatterie_energy_today'].state],
          })
    time_offset: 6h
  - entity: sensor.solar_netzeinspeisung_kwh_taglich
    name: Netzeinspeisung
    marker:
      color: red
      opacity: 0.5
    textfont:
      color: grey
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(6,0,0)],
            ys: [...ys, hass.states['sensor.solar_netzeinspeisung_kwh_taglich'].state],
          })
    time_offset: 6h
  - entity: sensor.solcast_pv_forecast_prognose_heute
    name: Prognose
    marker:
      color: "#45664a"
      opacity: 0.2
    textfont:
      color: white
    filters:
      - filter: i>0 && i < xs.length - 1
      - fn: |
          ({ys,xs,hass}) => ({
            xs: [...xs, new Date().setHours(-6,0,0)],
            ys: [...ys, hass.states['sensor.solcast_pv_forecast_prognose_heute'].state],
          })
    time_offset: "-6h"
layout:
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  barmode: stack
  bargap: 0.05
  barcornerradius: 3
  uniformtext:
    minsize: 10
    mode: show
  modebar:
    orientation: v
    remove: zoom
  margin:
    t: 5
    l: 45
    r: 20
  height: 400
  legend:
    "y": -0.22
    x: 0.1
  xaxis:
    rangeselector:
      "y": 1.05
      buttons:
        - count: 1
          step: day
        - count: 7
          step: day
        - count: 10
          step: day
        - count: 30
          step: day
        - count: 6
          step: month
    gridcolor: rgba(238,235,235,0.3)
    autorange: true
    showgrid: true
  yaxis:
    visible: true
    autorange: true
hours_to_show: 7d
refresh_interval: 360
card_mod:
  style: |
    ha-card {
        border-width: 0px;
       }
view_layout:
  position: main
grid_options:
  columns: full

```
### 🔍 Funktion = `fn`?


```
- fn: |
    ({ys,xs,hass}) => ({
      xs: [...xs, new Date().setHours(0,0,0)],
      ys: [...ys, hass.states['sensor.acpowervonbatterie_energy_today'].state],
    })
```

Die Funktion dient zur manuellen Ergänzung der Datenpunkte im Diagramm. Sie ist sozusagen ein Code, der individuell zusätzliche Werte zu den Achsen (`xs` = X-Achse, `ys` = Y-Achse) hinzufügen kann.


### 🔧 Was passiert genau?

* **`({ys, xs, hass}) => ...`**
Das ist eine Funktion, die entsprechend Dinge aus dem Plotly-Kontext filtert:
  * `xs`: Die bisherigen Zeitstempel (X-Achse)
  * `ys`: Die bisherigen Werte (Y-Achse)
  * `hass`: Zugriff auf den gesamten Home Assistant-Status (`hass.states`)
* **`new Date().setHours(0, 0, 0)`**
Gibt den Zeitpunkt **heute um Mitternacht** zurück, als Millisekunden-Zeitstempel. X-Wert (Zeitachse).
* **`hass.states['sensor.acpowervonbatterie_energy_today'].state`**
Liest den aktuellen Wert **dieses Sensors** direkt aus Home Assistant aus. Y-Wert (Datenwert für die Y-Achse).
* **`xs: [...xs, ...]` und `ys: [...ys, ...]`**
Fügt jeweils einen neuen Eintrag zu den vorhandenen Datenlisten hinzu.
Hieran habe ich ewig gesessen, aber es geht jetzt wie gewünscht.

---

📌 Zur Ergänzung noch ein Liniendiagramm mit Aufteilung des aktuellen Strombezuges inkl. Batterieladung und Vorhersage. Das Diagramm ist immer auf einen Tag fixiert und baut sich über den Tag hinweg auf.

![image](https://github.com/user-attachments/assets/1a6af161-45a9-421f-8b0f-5b012ea0ec20)

```yaml
type: custom:plotly-graph
defaults:
  yaxes:
    fixedrange: true
    range:
      - 0
      - null
card_mod:
  style: |
    ha-card {
      border: none;
    }
entities:
  - entity: sensor.acpowervonbatterie_energy_power
    name: Batterieentladung
    yaxis: y1
    fill: tozeroy
    line:
      shape: spline
      color: "#6C9BC4"
  - entity: sensor.growatt_outpowerwatt
    name: Solarertrag
    yaxis: y1
    fill: tozeroy
    line:
      shape: spline
      color: green
    filters:
      - exponential_moving_average:
          alpha: 0.05
  - entity: sensor.total_power_nur_verbrauch
    name: Netzbezug
    yaxis: y1
    fill: tozeroy
    line:
      shape: spline
      color: orange
    filters:
      - exponential_moving_average:
          alpha: 0.05
  - entity: sensor.solar_einspeisung_normiert_positiver_wert
    name: Netzeinspeisung
    yaxis: y1
    line:
      shape: spline
      color: red
    filters:
      - exponential_moving_average:
          alpha: 0.05
  - entity: sensor.acpowerzubatterie_energy_power
    name: Batterieladung
    yaxis: y1
    fill: tozeroy
    line:
      shape: spline
      color: "#AAE1FC"
    filters:
      - exponential_moving_average:
          alpha: 0.05
  - entity: sensor.solcast_pv_forecast_aktuelle_leistung
    name: Vorhersage
    yaxis: y2
    line:
      color: grey
      dash: dot
      width: 2
hours_to_show: current_day
refresh_interval: 120
min_y_axis: 0
fit_y_data: true
logarithmic_scale: true
max_y_axis: 3000
layout:
  height: 290
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  margin:
    t: 0
    l: 45
    r: 40
grid_options:
  columns: full
```
Die Linien können auch geglättet werden. Dazu einfach einen Filter setzten. Der Filter ist im Beispiel schon gesetzt. Wollt ihr ihn nicht haben, einfach herauslöschen. Kleinere Zahlen bedeuten größere Glättung.

![image](https://github.com/user-attachments/assets/1863f1b2-c398-4932-9f2e-f1798001dcff)


📌 Und zum Schluss noch ein Beispiel für die Summierung über die Monate hinweg.

![image](https://github.com/user-attachments/assets/7c2ff69d-bfc4-4f94-a7fd-3589c352bf3e)


```yaml
type: custom:plotly-graph
defaults:
  yaxes:
    fixedrange: true
  entity:
    period: month
    type: bar
    statistic: sum
    filters:
      - filter: i>0
    texttemplate: "%{y:.1f}"
    textposition: auto
    width: 1200000000
entities:
  - entity: sensor.erzeugzung_taglich_nach_abzug_einspeisung
    name: Erzeugung
    marker:
      color: green
      opacity: 1
    textfont:
      color: black
  - entity: sensor.acpowervonbatterie_energy_today
    name: Akku Entladung
    marker:
      color: "#6C9BC4"
      opacity: 1
  - entity: sensor.stromverbrauch_taglich
    name: Bezug
    marker:
      color: darkorange
      opacity: 1
    textfont:
      color: black
  - entity: sensor.solar_netzeinspeisung_kwh_taglich
    name: Netzeinspeisung
    marker:
      color: red
      opacity: 0.5
    textfont:
      color: grey
layout:
  paper_bgcolor: rgba(0,0,0,0)
  plot_bgcolor: rgba(0,0,0,0)
  barmode: stack
  bargap: 0.05
  barcornerradius: 3
  uniformtext:
    minsize: 10
    mode: show
  modebar:
    orientation: v
    remove: zoom
  margin:
    t: 5
    l: 45
    r: 20
  height: 400
  legend:
    "y": -0.22
    x: 0.1
  xaxis:
    rangeselector:
      "y": 1.05
      buttons:
        - count: 1
          step: month
        - count: 7
          step: month
        - count: 10
          step: month
        - count: 30
          step: month
    gridcolor: rgba(238,235,235,0.3)
    autorange: true
    showgrid: true
  yaxis:
    visible: true
    autorange: true
hours_to_show: 120d
refresh_interval: 360
card_mod:
  style: |
    ha-card {
        border-width: 0px;
       }
view_layout:
  position: main
grid_options:
  columns: full

```
