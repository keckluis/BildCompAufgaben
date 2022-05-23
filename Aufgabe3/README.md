# Aufgabe 3 DepthMap Estimation

Bedienung: Beliebige Taste zum durchschalten der Schritte  

Python-Version: 3.10.3  
OpenCV-Version: 4.5.5  
Numpy-Version: 1.22.3  

## Schritt1: Auffinden und Matchen von  Features im Bild mithilfe SIFT
Zuerst versuchen wir identische Features in Bild 1 und Bild 2 zu finden. Dazu benutzen wir den SIFT Algorithmus zusammen dem FLANN Matching. 

## Schritt 2: erzeuge Fundamentalmatrix 
Mit den Matches der Bilder kann nun die Fundamentalmatrix gefunden werden, diese enthält die wie die essentielle Matrix die Translation und Rotation von Bild 1 nach Bild 2, zusätzlich aber auch noch die Intrinsität der beide Kameras. Die Fundamentalmatrix brauchen wir später zur Rectification.

## Schritt 3: finde Epilinien
Wurde die Fundamental Matrix auf Bild 2 angewandt, können wir nun die  Epilinie eines Bildpunktes aus Bild 1 in Bild 2 projizieren. Diese Linie in Bild 1 bildet sich durch ein Feature x und des Epipols, der Epipol ist ein Schnittpunkt auf der Bildebene, der durch eine gerade Linie zwischen den beiden Kameras entsteht. Mithilfe des Epipols und eines Features kann nun die Epilinie auf Bild 1 erzeugt werden. Diese Epilinie können wir nun auch auf Bild 2 übertragen. Durch die Suche nach dem Feature x und des bereits existierenden Epipols e‘ erstellen wir eine Epilinie auf Bildebene 2. Auf dieser Linie suchen wir nun nach weiteren Features des Typs x. Finden wir das Feature x mehrfach auf der Epilinie des zweiten Bildes, so haben wir bereits einen Hinweis auf Tiefeninformationen über das abgelichtete Object erhalten.

## Schritt 4: Rectification
Bei der Rectification (Berichtigung) geht es darum das Bild 2 mittels der Fundamental Matrix zu translatieren und zu rotieren sodass aus beiden Perspektiven eine Tiefenkarte erstellt werden kann. 

## Schritt 5: Erstellung der Tiefenkarte
Mit Hilfe der OpenCV-Funktion 'StereoSGBM_create' wird nun eine Tiefenkarte aus den beiden rektifizierten Bilder erstellt. Da in diesem Programm eine Tiefenkarte aus drei Bildern entstehen soll, wird der gesamte Ablauf dreimal wiederholt, wobei jede mögliche Paar-Kombination aus den drei Bildern genutzt wird.

##Schritt 6: Kombinieren der Tiefenkarten
Aus den drei Bilderkombinationen sind drei Tiefenkarten entstanden, die nun zusammengeführt werden. Dafür wird der Farbwert eines Pixels aus allen drei Karten addiert und durch drei dividiert, um einen durchschnittlichen Farbwert zu erhalten. 
