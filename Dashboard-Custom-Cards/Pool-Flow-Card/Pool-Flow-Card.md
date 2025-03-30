# 🌅 Pool-Flow-Card

Hi, heute möchte ich mal die ha-floorplan-card vorstellen, mit der man auch wunderbar Custom Kreisläufe von Strom, Wasser, Heizung, Solar usw. darstellen kann. Ich habe mich daran mal versucht und eine Flow-Card für meinen Pool erstellt. So sehe ich direkt, welche Pumpen laufen und welche Kreisläufe gerade aktiv sind.  Durch Nutzung der Card kann eine interaktive Darstellung realisiert werden.​

![image](https://github.com/user-attachments/assets/2b339aff-3de8-4d9d-98ef-00b119002369)


## Erstellung einer individuellen Pool-Karte in Home Assistant

📌 In diesem Tutorial zeige ich dir, wie du eine benutzerdefinierte Pool-Karte in Home Assistant erstellst. Dabei nutzen wir die Floorplan Card, um eine SVG-Grafik deines Pools mit CSS-Animationen zu versehen und mit YAML-Konfigurationen zu steuern.​ Das kann aber genauso gut für alle anderen Kreiläufe ob Strom, Heizung, Strom usw. verwendet werden. Der Kreativtät sind fast keine Grenzen gesetzt.

**Voraussetzungen**

* HACS
* Zugriff auf das Dateisystem von Home Assistant​ (z.B. FileExplorer)
* Inkscape (kann kostenlos im Internet heruntergeladen werden)

### Schritt 1: Installation der Floorplan Card über HACS

📌 Um die Floorplan Card zu nutzen, musst du sie zunächst über den Home Assistant Community Store (HACS) installieren:​

1. Öffne das HACS-Panel in deinem Home Assistant.​
2. Klicke auf "Frontend".​
3. Suche nach "Floorplan Card".​
4. Wähle die Karte aus und klicke auf "Installieren".​
5. Starte Home Assistant neu, um die Installation abzuschließen.​

### Schritt 2: Erstellen der Verzeichnisstruktur und Ablegen der Dateien

1. Navigiere zum `www`-Verzeichnis in deinem Home Assistant Konfigurationsordner. Falls dieses nicht existiert, erstelle es.​
2. Innerhalb des `www`-Verzeichnisses erstelle einen neuen Ordner namens `pool-card`.​
3. Lege die folgenden Dateien in diesem Ordner ab:​
  * `pool-card.svg`: Deine SVG-Grafik des Pools.​
  * `pool-card.css`: Die CSS-Datei für Animationen und Styling.​
  * `pool-card.yaml`: Die YAML-Konfigurationsdatei für die Floorplan Card.​

### Schritt 3: Bearbeiten der SVG-Datei mit Inkscape

📌 Um die einzelnen Elemente in der SVG-Datei später gezielt ansprechen zu können, musst du ihnen eindeutige IDs zuweisen. Dazu eignet sich das Programm Inkscape:​

1. Öffne die Datei `pool-card.svg` mit Inkscape.​
2. Wähle ein Element aus, das du steuern möchtest.​
3. Gehe im Menü auf "Objekt" > "Objekteigenschaften".​
4. Weise dem Element im Feld "ID" einen eindeutigen Namen zu, z.B. `wasserlauf`.​
5. Wiederhole diesen Vorgang für alle relevanten Elemente.​
6. Speichere die Änderungen und schließe Inkscape.​



<details>
  <summary> 📌 <b>Ausführliche Anleitung - Bearbeiten der SVG-Datei mit Inkscape</b></summary>       
    
   Um die interaktiven Elemente in deiner SVG-Datei später in Home Assistant gezielt ansprechen zu können, ist es notwendig, ihnen eindeutige IDs zuzuweisen. Dies ermöglicht es, spezifische Komponenten wie Pumpen oder Ventile individuell zu steuern oder zu visualisieren. Hier ist eine Schritt-für-Schritt-Anleitung, wie du dies mit Inkscape umsetzen kannst:​
   
   1. **Öffnen der SVG-Datei:**
     * Starte Inkscape auf deinem Computer.​
     * Lade die SVG-Datei deines Pool-Layouts, indem du auf **"Datei" > "Öffnen"** gehst und die entsprechende Datei auswählst.​
   2. **Auswählen des zu bearbeitenden Objekts:**
     * Klicke auf das Objekt, dem du eine ID zuweisen möchtest, um es auszuwählen.​
   3. **Zuweisen einer eindeutigen ID:**
     * Gehe im Menü auf **"Objekt" > "Objekteigenschaften"**.​
     * Im sich öffnenden Dialogfeld findest du das Feld **"ID"**. Gib hier einen eindeutigen Namen für das Objekt ein, der dessen Funktion oder Position beschreibt, z.B. `pool_pumpe` für die Poolpumpe oder `ventil_einlass` für das Einlassventil.​
     * Bestätige die Eingabe, indem du auf **"Setzen"** klickst.​
   4. **Wiederholen für weitere Objekte:**
     * Wiederhole die Schritte 2 und 3 für alle weiteren Objekte in deiner SVG-Datei, denen du IDs zuweisen möchtest.​
   5. **Speichern der Änderungen:**
     * Nachdem du allen relevanten Objekten eindeutige IDs zugewiesen hast, speichere die Datei über **"Datei" > "Speichern"**.​
   
   Durch das Zuweisen eindeutiger IDs zu den Objekten in deiner SVG-Datei legst du die Grundlage dafür, diese später in Home Assistant mittels CSS und YAML gezielt anzusprechen und zu steuern. Dies ermöglicht eine interaktive und dynamische Darstellung deines Pools im Home Assistant Dashboard.
</details>

### Schritt 4: Konfiguration der `pool-card.yaml`

📌 Die `pool-card.yaml` definiert die Interaktionen zwischen den Home Assistant Entitäten und den SVG-Elementen. Hier mein Beispiel-Code:

```yaml
type: custom:floorplan-card
config:
  console_log_level: info
  defaults:
    hover_action: hover-info
    tap_action: more-info
  image: /local/pool-card/pool-card.svg
  stylesheet: /local/pool-card/pool-card.css
  rules:
    - element: wasserlauf
      entity: switch.wasserlauf_steckdose_1
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: entitystate-${entity.state}
    - element: abfluss
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"flussH\" : \"\"}"
    - element: abfluss2
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"flussH\" : \"\"}"
    - element: abfluss3
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"flussV\" : \"\"}"
    - element: abfluss4
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"zuflussV\" : \"\"}"
    - element: abfluss5
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"zuflussV\" : \"\"}"
    - element: abfluss6
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"zuflussV\" : \"\"}"
    - element: abfluss7
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"zuflussH\" : \"\"}"
    - element: abfluss7-4
      entity: switch.skimmerpumpe_shelly_plug_switch_0
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state === \"on\") ? \"zuflussH\" : \"\"}"
    - element: zufluss
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"zuflussH\" : \"\"}"
    - element: zufluss2
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"zuflussH\" : \"\"}"
    - element: zufluss3
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"flussV\" : \"\"}"
    - element: zufluss4
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"flussH\" : \"\"}"
    - element: zufluss5
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"flussV\" : \"\"}"
    - element: zufluss6
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(Number(entity.state) > 5) ? \"zuflussV\" : \"\"}"
    - element: zufluss_strom
      entity: sensor.stromungspumpen_leistung
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state > \"10\") ? \"flussH\" : \"\"}"
    - element: zufluss_strom2
      entity: sensor.stromungspumpen_leistung
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state > \"10\") ? \"flussH\" : \"\"}"
    - element: rad
      entity: sensor.stromungspumpen_leistung
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state > \"10\") ? \"rad\" : \"\"}"
    - element: rad2
      entity: sensor.stromungspumpen_leistung
      state_action:
        action: call-service
        service: floorplan.class_set
        service_data: "${(entity.state > \"10\") ? \"rad\" : \"\"}"
    - element: hauptpumpe
      entity: sensor.hauptpumpe_shelly_plug_switch_0_power
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined) ?
            Math.round(entity.state) + "W" : " "}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: skimmer
      entity: sensor.skimmerpumpe_shelly_plug_switch_0_power
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state !== undefined) ?
            Math.round(entity.state) + "W" : " "}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: wasspumpe_leistung
      entity: sensor.wasserlauf_leistung
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state > 5) ? Math.round(entity.state) / 2 + "
            W" : " "}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: stromungspumpe
      entity: sensor.stromungspumpen_leistung
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state > 5) ? Math.round(entity.state) / 2 + "
            W" : " "}
        - service: floorplan.class_set
          service_data:
            class: static-value
    - element: stromungspumpe2
      entity: sensor.stromungspumpen_leistung
      state_action:
        - service: floorplan.text_set
          service_data: >-
            ${(entity.state > 5) ? Math.round(entity.state) / 2 + "
            W" : " "}
        - service: floorplan.class_set
          service_data:
            class: static-value
```

### Schritt 5: Erstellung der `pool-card.css`

📌 Die `pool-card.css` enthält die Stildefinitionen und Animationen für die SVG-Grafik. Meine CSS-Datei sieht so aus.​

```css
/* All good :/ */
.entitystate-on {
  opacity: 0;
}

.entitystate-off {
  display: none !important;
}

.static-value, .static-value tspan {
  fill: #000000;
  font-weight: bold;
}

.zuflussH {
  fill: #3e6dca !important;
  color: #3e6dca !important;
  animation-name: zuflussH;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  transform-box: fill-box;
  transform-origin: 100% 0%;
}

@keyframes zuflussH{
  0% {
    transform: scaleX(0%);
  }

  50% {
    transform: scaleX(50%);
  }
  
  100% {
    transform: scaleX(100%);
  }
}

.zuflussV {
  fill: #3e6dca !important;
  color: #3e6dca !important;
  animation-name: zuflussV;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  transform-box: fill-box;
  transform-origin: 0% 100%;
}

@keyframes zuflussV{
  0% {
    transform: scaleY(0%);
  }

  50% {
    transform: scaleY(50%);
  }
  
  100% {
    transform: scaleY(100%);
  }
}

.rad {
  animation-name: spin;
  animation-duration: 6s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
  transform-origin: 50% 50%;
  transform-box: fill-box;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

  
.rad2 {
  animation-name: spin2;
  animation-duration: 6s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
  transform-origin: 50% 50%;
  transform-box: fill-box;
}

@keyframes spin2 {
  from {
    transform: rotate(360deg);
  }
  to {
    transform: rotate(0deg);
  }
}

.flussH {
  fill: #3e6dca !important;
  color: #3e6dca !important;
  animation-name: abflussH;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  transform-box: fill-box;
  transform-origin: 0% 0%;
}

@keyframes abflussH{
  0% {
    transform: scaleX(0%);
  }

  50% {
    transform: scaleX(50%);
  }
  
  100% {
    transform: scaleX(100%);
  }
}

.flussV {
  fill: #3e6dca !important;
  color: #3e6dca !important;
  animation-name: abflussV;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  transform-box: fill-box;
  transform-origin: 0% 0%;
}

@keyframes abflussV{
  0% {
    transform: scaleY(0%);
  }

  50% {
    transform: scaleY(50%);
  }
  
  100% {
    transform: scaleY(100%);
  }
}

.pumping {
  fill: #3e6dca !important;
  color: #3e6dca !important;
  animation-name: pumping;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
  transform-origin: 50% 50%;
  transform-box: fill-box;
}

@keyframes pump{
  0% {
    transform: translate(0px,0px);
  }

  50% {
    transform: translate(0px, -5px);
  }
  
  100% {
    transform: translate(0px, 0px);
  }
}

.heating {
  animation: heat;
  animation-name: heat;
  animation-duration: 3s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
  transform-box: fill-box;
  transform-origin: 0% 0%;
}

@keyframes heat{
  0% {
    fill: #507eec;
    transform: scaleX(100%);
  }

  50% {
    fill: #ef7e87;
    transform: scaleX(50%);
  }
  
  100% {
    fill: #507eec;
    transform: scaleX(100%);
  }
}
```
📌 Die CSS-Klassen sorgen dafür, dass das entsprechende SVG-Element eine fließende Animation erhält, die bei mir den Wasserfluss simuliert.​

### Schritt 6: Integration der Pool-Karte in das Home Assistant Dashboard

📌 Füge die `pool-card.yaml` zu deinem Dashboard hinzu:​

1. Gehe in Home Assistant zu deinem Dashboard und aktiviere den Bearbeitungsmodus.​
2. Füge eine neue Karte hinzu und wähle den Typ "Manual".​
3. Kopiere den Inhalt der `pool-card.yaml` in das Konfigurationsfeld.​
4. Speichere die Änderungen und verlasse den Bearbeitungsmodus.​

Nun sollte deine individuelle Pool-Karte im Dashboard sichtbar sein und entsprechend der definierten Regeln interaktiv reagieren.
