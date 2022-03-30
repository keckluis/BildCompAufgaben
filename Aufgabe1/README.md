# Aufgabe 1
## Zweck des Projekts
Ziel dieses Projekts ist es die Verzerrung einer Kamera zu ermitteln um diese anschließend auszugleichen und ein unverzerrtes Bild zu erhalten.
Dazu soll ein Set von Kalibrationsbildern dienen, dass Nutzer für ihre Kamera mit diesem Programm aufnehmen können. Mit diesen Kalibrationsbilder wird die Verzerrung der Kamera ermittelt und kann in Echtzeit aus einem Live-Bild dieser Kamera entfernt werden.

Grundlage für dieses Projekt bildet die OpenCV-Dokumentation zum Thema Kamera-Kalibration:
https://docs.opencv.org/4.5.5/dc/dbb/tutorial_py_calibration.html

## Workflow
### CaptureCalibrationImages.py
Um ein Set an Kalibrationsbildern für die eigene Kamera aufzunehmen wird zunächst das Skript 'CaptureCalibrationImages.py' ausgeführt. Ein Fenster öffnet sich, in dem das Live-Bild der Kamera angezeigt wird. 
Mit der Taste 'C' wird der Aufnahmemodus gestartet. Nun wird pro Sekunde ein Bild aufgenommen. Für Kalibrationsbilder wird ein ausgedrucktes Schachbrettmuster (min. 8x8 Felder) in die Kamera gehalten. Dabei sollte die Position angepasst werden, sodass die Sammlung an aufgenommen Schachbrett-Bildern möglichst den ganzen Bildbereich abdeckt. Schnelle Bewegungen sollten vermieden werden, um Bewegungsunschärfe zu vermeiden. Mit erneutem drücken von 'C' wird der Aufnahmemodus beendet.
Nicht alle aufgenommen Bilder werden sich für die Kalibration eignen, da nicht immer das Schachbrettmuster erkannt wird. Um die ungeeignetet Bilder auszusortieren wird mit der Taste 'E' der Evaluationsmodus gestartet. Jedes aufgenommene Bild wird ausgewertet und die geeigneten werden in neuen Fenstern zu r Betrachtung geöffnet. Sollte auffallen, dass darunter immer noch Bilder sind die aussortiert werden sollten, kann man sich den Namen des Fensters merken um diese Bilder später wieder zu löschen. OpenCV empfiehlt mindestens 10 Kalibrationsbilder für ein gutes Ergebnis. Ist diese Zahl noch nicht erreicht sollten zusätzliche Bilder aufgenommen und evaluiert werden.
Sind genug Kalibrationsbilder vorhanden kann das Programm mit der Taste 'Q' beendet werden. Die Kalibrationsbilder werden im Ordner 'CalibrationImages' gespeichert.

### CameraCalibration.py
Mit den aufgenommenen Kalibrationsbildern kann nun das Kamerabild entzerrt werden. Dazu wird das Skript 'CameraCalibration.py' gestartet. Das Skript lädt die zuvor aufgenommenen Kalibrationsbilder und ermittelt anhand dieser die Verzerrung der Kamera. 
Zwei Fenster werden geöffnet. Das Fenster 'webcam original' zeigt das unveränderte Live-Bild der Kamera. 'webcam undistorted' zeigt ein Live-Bild bei dem für jeden Frame mit Hilfe der ermittelten Kameraverzerrung das Bild wieder entzerrt wurde. 
Mit der Taste 'Q' lässt sich das Programm wieder beenden.
