# 𖣘 Fan Control ESP Home for Huawei R4850

## Fan Control with ESP Home for Huawei R4850 for Home Assistant

📌 Das ist eine einfach Lüftersteuerung für das Huawei R4850, kann aber natürlich auch für andere Projekte genutzt werden. Es wird in ESPHome ein Gerät angelegt und das lässt hinterher die Steurung (on/off) in Home Assistant zu. 
Den Schaltplan findest du im beigefügtem Bild Schaltplan.png (liegt im Ornder)

## Voraussetzungen

1. Home Assistant mit ESPHome Add-on installiert 
2. ESP8266-Gerät (z. B. ESP-01, NodeMCU, Wemos D1 mini) 
3. USB-Kabel zum Flashen 


## 📁 Schritt 1: YAML-Code in ESPHome einfügen

1. Öffne in Home Assistant das **ESPHome Add-on**.
2. Klicke auf **"Neu erstellen"** oder den **+ Button**.
3. Gib deinem Projekt einen Namen (z. B. `huawei-lufter`) und wähle **ESP8266** als Chip.
4. Ersetze den automatisch erzeugten Code durch deinen:

yaml

```yaml
esphome:
  name: huawei-lufter
  friendly_name: Huawei-Lüfter

esp8266:
  board: esp01_1m

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "your key"

ota:
  - platform: esphome
    password: "your password"

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

  # Enable fallback hotspot (captive portal) in case wifi connection fails
  ap:
    ssid: "Huawei-Lufter Fallback Hotspot"
    password: "kY3UmzlpLsKD"

captive_portal:
  
output:
  - platform: esp8266_pwm
    id: motor_forward_pin
    pin: GPIO5
  - platform: esp8266_pwm
    id: motor_reverse_pin
    pin: GPIO4

fan:
  - platform: hbridge
    id: my_fan
    name: "Living Room Fan"
    pin_a: motor_forward_pin
    pin_b: motor_reverse_pin
    decay_mode: slow  
```

5. Achte darauf, deine **WLAN-Daten** in den Secrets (`wifi_ssid` und `wifi_password`) korrekt zu hinterlegen.
6. Ebenso muss der api Key mit dem von euch erzeugtem Gerät ausgetauscht werden.
7. Jetzt speichern.



## ⚡ Schritt 2: ESP zum ersten Mal flashen

Da OTA (Over-the-Air) erst nach dem ersten Flash funktioniert, musst du das Gerät einmalig **per Kabel** flashen.

### So geht's:

1. **Verbinde den ESP8266 mit dem USB-SKabel.**
2. **Schließe den Adapter an deinen PC an.**
3. Im ESPHome-Interface:
  * Klicke auf **"Installieren" → "Manuell über USB"**.
  * Wähle **"Plug into this computer"** (wenn lokal über Web-UI) oder alternativ „Legacy upload method“.
  * ESPHome kompiliert die Firmware und lädt sie auf dein Gerät.

📌 Alternativ kannst du die .bin-Datei auch herunterladen und mit **ESPHome Web flasher** oder **ESPTool** flashen. Den Web flasher nutze ich auch oft für die Erstinstallation.



## 🌐 Schritt 3: Gerät verbindet sich mit WLAN

Nach dem ersten Flash:

1. Der ESP startet neu und verbindet sich mit deinem WLAN.
2. In ESPHome taucht das Gerät nun **online** auf.
3. Ab jetzt kannst du jederzeit **OTA** verwenden.
4. Die IP des Gerätes findest du über deinen Router heraus (Name: Huaweii XX)



## ✅ Schritt 4: Integration in Home Assistant

Wenn `api: key` korrekt gesetzt ist:

1. Home Assistant erkennt das neue Gerät automatisch.
2. Du bekommst eine **Benachrichtigung** zur Integration.
3. Klicke auf „Gerät hinzufügen“ und du kannst den Lüfter anschließend steuern.
