# GeekMagic Hello Cubic lite / Crystal Cube
Simple ESPHome Code for HelloCubic in Home Assistant

<img width="48%" height="auto" alt="image" src="https://github.com/jayjojayson/Sun-Position-Card/blob/main/images/geekmagic-crystal-cube.jpeg" /> 


It's more for me to keep the code it in Mind. But if you like it, you can use it of course.
In Attach is a simple ESPHome Code for the crystal Cube / hello cubic lite. Simply follow the Steps below.

- Create a new ESPHome Device in Home Assistant
- change the Sensors inside the Code to your ones
- Copy the code into the new ESPHome Device
- Uploaded it
- Have fun


<img width="48%" height="auto" alt="image" src="https://github.com/jayjojayson/Sun-Position-Card/blob/main/images/geekmagic-crystal-cube-ha.png" /> 


```yaml
esphome:
  name: "giftv2"
  friendly_name: GifTV2
  platformio_options: 
    board_build.f_cpu: 160000000L

esp8266:
  board: esp12e

# Enable logging
logger:

# Enable Home Assistant API
api:
  encryption:
    key: "DeinKEY="

ota:
  - platform: esphome
    password: "password"
wifi:
  ssid: "WiFi"
  password: "1234"
  min_auth_mode: WPA2

  ap:
    ssid: "giftv Fallback Hotspot"
    password: "12345678"

substitutions:
  icon_battery: "\U000F058E"
  icon_thermometer: "\U000F050F"

spi:
  clk_pin: GPIO14
  mosi_pin: GPIO13
  interface: hardware
  id: spihwd

output:
  - platform: esp8266_pwm
    pin: GPIO05
    frequency: 1000 Hz
    id: pwm_output
    inverted: true

light:
  - platform: monochromatic
    name: "Backlight"
    output: pwm_output
    restore_mode: RESTORE_AND_ON

font:
  - file: "gfonts://Roboto"
    id: font_large
    size: 55
  - file: "gfonts://Roboto"
    id: font_medium  
    size: 35   
  - file: "gfonts://Roboto"
    id: font_small
    size: 25

time:
  - platform: sntp
    id: esptime
    timezone: Europe/Berlin
    servers:
      - pool.ntp.org


# GLOBALE VARIABLEN 
# ---------------------------------------------------------
globals:
  - id: current_page_index
    type: int
    initial_value: '0'


# SENSOREN 
# ---------------------------------------------------------
sensor:
  - platform: homeassistant
    id: aussen_temp
    entity_id: sensor.aussentemperatur_temperatur
    internal: false
    unit_of_measurement: "°C"

  - platform: homeassistant
    id: battery_soc
    entity_id: sensor.victron_system_battery_soc
    internal: false
    unit_of_measurement: "%"

  - platform: homeassistant
    id: daily_pv_energy
    entity_id: sensor.erzeugzung_taglich_kombination_solaranlagen
    internal: false
    unit_of_measurement: "kWh"

  - platform: homeassistant
    id: aktuell_pv_energy
    entity_id: sensor.total_solar_power_kombiniert
    internal: false
    unit_of_measurement: "W"

  - platform: homeassistant
    id: total_grid_power_w
    entity_id: sensor.total_power
    internal: false
    unit_of_measurement: "W"
  
  - platform: homeassistant
    id: daily_house_consumption
    entity_id: sensor.stromverbrauch_taglich
    internal: false
    unit_of_measurement: "kWh"

  - platform: wifi_signal
    id: wifi_strength
    name: "WiFi Signalstärke"
    unit_of_measurement: "dBm"
    update_interval: 60s


# SCHALTER (Auto-Rotate)
# ---------------------------------------------------------
switch:
  - platform: template
    name: "Automatisch Wechseln"
    id: switch_auto_rotate
    icon: "mdi:autorenew"
    optimistic: true
    restore_mode: RESTORE_DEFAULT_OFF


# INTERVAL (Auto-Rotate)
# ---------------------------------------------------------
interval:
  - interval: 5s
    then:
      - if:
          condition:
            switch.is_on: switch_auto_rotate
          then:
            - lambda: |-
                id(current_page_index) += 1;                
                // 5 Optionen (0 bis 4: Solar W, Solar kWh, Netz W, Netz kWh, Temp)
                // Batterie und Wifi sind raus.
                if (id(current_page_index) > 4) {
                  id(current_page_index) = 0;
                }

# SELECT (Konfig Home Assistant)
# ---------------------------------------------------------
select:
  - platform: template
    name: "Anzeige Zeile 1"
    id: disp_select_line1
    optimistic: true
    restore_value: true
    initial_option: "Solar kW"
    options:
      - "Solar kW"
      - "Solar kWh"
      - "Netz kW"
      - "Netz kWh"
      - "Batterie"
      - "Temperatur"
      - "WiFi"
      - "Leer"

  - platform: template
    name: "Anzeige Zeile 2"
    id: disp_select_line2
    optimistic: true
    restore_value: true
    initial_option: "Solar kWh"
    options:
      - "Solar kW"
      - "Solar kWh"
      - "Netz kW"
      - "Netz kWh"
      - "Batterie"
      - "Temperatur"
      - "WiFi"
      - "Leer"

# DISPLAY
# ---------------------------------------------------------
display:
  - id: my_display
    platform: mipi_spi
    model: st7789v
    spi_id: spihwd
    dimensions:
      height: 240
      width: 240
    update_interval: 1s 
    buffer_size: 12.5%
    invert_colors: true
    dc_pin: GPIO00
    reset_pin: GPIO02
    color_depth: 16
    spi_mode: mode3
    data_rate: 40000000
    auto_clear_enabled: false

    transform:
      swap_xy: false
      mirror_x: true
      mirror_y: false

    lambda: |-
        it.fill(Color(0, 0, 0));

        // --- DEFINITIONEN ---
        int box_x = 30;
        int box_y = 105;
        int box_w = 90;
        int box_h = 30;

        int r1_lbl_y = box_y + box_h + 25; 
        int r1_val_y = box_y + box_h + 20; 
        int r1_lbl_x = box_x - 20;
        int r1_val_x = box_x + 135;

        int r2_lbl_y = box_y + box_h + 68; 
        int r2_val_y = box_y + box_h + 63; 
        int r2_lbl_x = box_x - 20;
        int r2_val_x = box_x + 135;

        
        // LOGIK AUTO-ROTATE
        // -----------------------------------------------------------
        // Batterie entfernt
        std::string options[] = {"Solar kW", "Solar kWh", "Netz kW", "Netz kWh", "Temperatur"};
        int options_count = 5;

        // *** FIX: Klammern () hinzugefügt ***
        std::string val_s1 = id(disp_select_line1).current_option();
        std::string val_s2 = id(disp_select_line2).current_option();
        
        std::string s1 = val_s1;
        std::string s2 = val_s2;

        if (id(switch_auto_rotate).state) {
            int idx1 = id(current_page_index) % options_count;
            int idx2 = (id(current_page_index) + 1) % options_count;
            
            s1 = options[idx1];
            s2 = options[idx2];
        }

        
        // 1. HEADER BEREICH 
        // -----------------------------------------------------------
        float temp = id(aussen_temp).state;
        Color temp_color = Color(200, 220, 255);
        if (!isnan(temp)) {
            it.printf(5, 5, id(font_small), temp_color, "%.1f°C", temp);
        } else {
            it.print(5, 5, id(font_small), Color(100, 100, 100), "--°C");
        }

        it.strftime(120, 65, id(font_large), Color(0, 0, 255), TextAlign::CENTER, "%H:%M", id(esptime).now());

        if (!global_api_server->is_connected()) {
             it.filled_circle(230, 230, 3, Color(255, 0, 0));
        }

        int rssi = WiFi.RSSI();
        int bars = 0;
        if (rssi > -50) bars = 3;
        else if (rssi > -60) bars = 2;
        else if (rssi > -70) bars = 1;
        
        int bx = 200; int by = 15; int bar_w = 6; int bar_gap = 5;
        for (int i = 0; i < 3; i++) {
            int h = (i + 1) * 3;
            Color col = (i < bars) ? Color(0, 255, 0) : Color(40, 40, 40);
            it.filled_rectangle(bx + i * (bar_w + bar_gap), by - h, bar_w, h, col);
        }

        
        // 2. BATTERIE
        // -----------------------------------------------------------
        float soc = id(battery_soc).state;
        if (isnan(soc)) { soc = 0; }

        int red = (int)(255 * (100 - soc) / 100);
        int green = (int)(255 * soc / 100);
        
        Color soc_color;
        if (soc == 0 && isnan(id(battery_soc).state)) {
            soc_color = Color(100, 100, 100);
        } else {
            soc_color = Color(red, green, 0);
        }

        it.rectangle(box_x, box_y, box_w, box_h, Color(255, 255, 255));
        it.rectangle(box_x + box_w, box_y + 7, 6, box_h - 14, Color(255, 255, 255));

        int fill_width = (int)(box_w * soc / 100.0);
        if (fill_width > 0) {
            it.filled_rectangle(box_x + 1, box_y + 1, fill_width - 2, box_h - 2, soc_color);
        }

        if (!isnan(id(battery_soc).state)) {
            it.printf(box_x + box_w + 25, box_y - 2, id(font_medium), soc_color, "%.0f%%", soc);
        } else {
            it.print(box_x + box_w + 25, box_y - 2, id(font_medium), Color(100,100,100), "--%");
        }

        
        // 3. VARIABLE ZEILEN
        // -----------------------------------------------------------

        // --- ZEILE 1 RENDER ---
        if (s1 == "Solar kW") {
             float val = id(aktuell_pv_energy).state / 1000.0;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Solar kW:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), Color(211, 117, 17), "%.1f", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        } 
        else if (s1 == "Solar kWh") {
             float val = id(daily_pv_energy).state;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Solar kWh:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), Color(72, 211, 17), "%.1f", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s1 == "Netz kW") {
             float val = id(total_grid_power_w).state / 1000.0;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Netz kW:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), Color(0, 255, 255), "%.1f", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s1 == "Netz kWh") {
             float val = id(daily_house_consumption).state;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Haus kWh:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), Color(255, 0, 255), "%.1f", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s1 == "Batterie") {
             float val = id(battery_soc).state;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Akku SoC:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), soc_color, "%.0f%%", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s1 == "Temperatur") {
             float val = id(aussen_temp).state;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "Aussen:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), temp_color, "%.1f", val);
             else it.print(r1_val_x, r1_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s1 == "WiFi") {
             float val = id(wifi_strength).state;
             it.print(r1_lbl_x, r1_lbl_y, id(font_small), Color::WHITE, "WiFi Signal:");
             if (!isnan(val)) it.printf(r1_val_x, r1_val_y, id(font_medium), Color::WHITE, "%.0f", val);
        }

        // --- ZEILE 2 RENDER ---
        if (s2 == "Solar kW") {
             float val = id(aktuell_pv_energy).state / 1000.0;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Solar kW:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), Color(211, 117, 17), "%.1f", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        } 
        else if (s2 == "Solar kWh") {
             float val = id(daily_pv_energy).state;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Solar kWh:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), Color(72, 211, 17), "%.1f", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s2 == "Netz kW") {
             float val = id(total_grid_power_w).state / 1000.0;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Netz kW:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), Color(0, 255, 255), "%.1f", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s2 == "Netz kWh") {
             float val = id(daily_house_consumption).state;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Haus kWh:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), Color(255, 0, 255), "%.1f", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s2 == "Batterie") {
             float val = id(battery_soc).state;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Akku SoC:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), soc_color, "%.0f%%", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s2 == "Temperatur") {
             float val = id(aussen_temp).state;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "Aussen:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), temp_color, "%.1f", val);
             else it.print(r2_val_x, r2_val_y, id(font_medium), Color(100,100,100), "--");
        }
        else if (s2 == "WiFi") {
             float val = id(wifi_strength).state;
             it.print(r2_lbl_x, r2_lbl_y, id(font_small), Color::WHITE, "WiFi Signal:");
             if (!isnan(val)) it.printf(r2_val_x, r2_val_y, id(font_medium), Color::WHITE, "%.0f", val);
        }
```
