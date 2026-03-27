In der Community war @Schorsch so nett und hat mir alle Spiele zur Verfügung gestellt. Also habe ich mal gebastelt. So hat man ein kleines Game-Center und muss sich nicht für ein Spiel entscheiden bzw. braucht nur eine Datei für alle Spiele. Die HTML Datei fasst also alle Spiele zusammen und die Card ist im Dark-Mode gestaltet. Wenn ihr lieber den Light-Mode habt, könnt ihr die Farben oben im ersten Teil vom HTML anpassen. Die Tastatursteuerung funktioniert überall, bis auf Tetris, aber da hatte ich jetzt noch nicht weiter geschaut.

<img width="45%" alt="image" src="https://github.com/user-attachments/assets/9095ece8-8d76-4225-bf10-e4df6b2f1463" /> <img width="45%" src="https://github.com/user-attachments/assets/3a1bb042-7449-4bb1-b757-242dae6cf7c3" />

> Die games.html einfach in den www-Ordner packen. 

Diesen Teil dann in als neue Card in euer Dashboard einfügen:

```
type: iframe
url: /local/games.html
aspect_ratio: "1:1"
grid_options:
  columns: full
  rows: 9

```

So haben alle Spiele-Fans am Wochenende etwas zu tun. ;)
