# Aufgabe 4 3D Reconstruction  

Python-Version: 3.9.13  
  
Package-Versionen  
open3d: 0.15.1   
numpy: 1.22.4  
opencv-python: 4.6.0.66  
matplotlib: 3.5.2  
joblib: 1.1.0

## Bedienung
Sobald Open3D installiert ist wird außerdem der Code aus dem Open3D-Repository benötigt. Alternativ befindet sich der Code auch im Open3D-Installationsordner.
Der Pfad zu diesem lässt sich im Terminal mit dem Befehl "pip show open3d" anzeigen.  
Am besten kopiert man jetzt den Ordner "open3d" und fügt ihn zusammen mit dem Skript "mkv_to_ply.py" und der mkv-Datei in einen neuen Ordner.
Dort kann man nun das Skript starten und wird im Terminal aufgefordert den Namen der mkv-Datei (mit Dateiendung) einzugeben. Nach der Bestätigung wird noch nach einem Namen für den Ordner gefragt in dem die Ergebnisse gespeichert werden sollen. Das Skript startet dann den Prozess und verarbeitet die Daten aus der mkv-Datei um ein 3D-Modell im ply-Format zu rekonstruieren. Dieses ist dann im Unterordner "scene" unter dem Namen "integrated.ply" zu finden.
  
Disclaimer: Das Skript dient nur der Zusammenfassung mehrerer Konsolenbefehle, die man für die 3D Rekonstruktion mit Open3D einzeln ausführen müsste.
Der eigentliche Rekonstruktions-Code ist von Open und kann [hier](https://github.com/isl-org/Open3D) gefunden werden.

## .mvk Reader
`azure_kinect_mkv_reader.py --input input.mkv --output outputfolder`
  
Dieser Befehl startet einen mkv-Reader, der die einmzelnen Frames aus der Videodatei extrahiert und in einem Ordner speichert. In einem anderen Ordner werden außerdem Tiefenkarten gespeichert, die aus den in der mvk-Datei vorhandenen Tiefeninformationen erstellt werden.
![mkv_reader](https://github.com/keckluis/BildCompAufgaben/blob/main/Aufgabe4/readme_images/mkv_reader.png)

## Make fragments
`python run_system.py "outputfolder\\config.json" --make`
  
Der erste Schritt erstellt Fragmente (Geometrie) durch Kombination der RGBD-Daten aus den einzelnen Frames. Für diesen Schritt kommen verschiedene Algorithmen zum Einsatz. Dazu zählt "RGBD Odometry", welche die Kamerabewegungen zuwischen 2 Frames berechnet, die "Multiway Registration" welche zum Ziel hat die die Geometrien im Globalen Koordinatensystem anzuordnen, und RGBD Integration.
  
## Register fragments
`python run_system.py "outputfolder\\config.json" --register`
  
Im zweiten Schritt werden die einzelnen Fragmente neu ausgerichtet, damit sie die passende Transformation im globalen Raum einnehmen. HieR kommt Iterative Closest Point (ICP) Registration und Multiway Registration zum Einsatz.
  
## Refine registration
`python run_system.py "outputfolder\\config.json" --refine`
  
In Schritt drei wird die Anordnung der Fragmente weiter verfeinert. Dazu werden mittels ICP Punktewolken  aus verschiedenen Bildern weiter aneinander angenähert. Multiway Registation kommt auch wieder zum Einsatz.
  
## Integrate scene
`python run_system.py "outputfolder\\config.json" --integrate`
  
Im letzten Schritt werden die einzelnen, nun ausgerichteten Fragmente in ein gemeinsames Volume zusammengeführt und als ply-Datei exportiert.
  
## Result
![result](https://github.com/keckluis/BildCompAufgaben/blob/main/Aufgabe4/readme_images/result.png)
