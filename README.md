# AutomaticSkeletonMarkerRelation

## Gruppe: Abraham Neme Alvarez, Luke Mikat, Valdone Zabutkaite

## Problemstellung

Beim markerbasierten Motion Capturing (MoCap) werden Marker auf den Körper platziert. Es ist jedoch nicht immer möglich, alle Marker genau dort zu platzieren, wo sie idealerweise hingehören. Dadurch fehlt die Relation zwischen den Markern und dem Skelett, was bedeutet, dass man nicht mehr von den Markern auf das Skelett zurückschließen kann.

## Lösungsansatz

Um die Relation zwischen den MoCap-Markern und dem Skelett zu verbessern, wird vorgeschlagen, auf bestehende Forschungsarbeiten zurückzugreifen, die parametrische Menschenmodelle wie SMPL (Skinned Multi-Person Linear Model) verwenden. Diese Modelle können in Tiefenaufnahmen von RGBD-Kameras, beispielsweise der Kinect, eingebettet werden. 

Die Hauptidee besteht darin, zunächst das SMPL-Modell auf die Tiefenaufnahmen zu fitten und in einem zweiten Schritt die MoCap-Marker zu erkennen und deren Relation zum SMPL-Modell herzustellen. Durch die Verwendung des SMPL-Modells könnte man eine präzisere Positionierung der Marker erreichen, da das Modell detaillierte Informationen über die Körperform und -struktur liefert. Sobald das Modell angepasst ist, könnte die Position der Marker relativ zum Modell berechnet werden. Das würde eine genaue Relation zwischen den Markern und dem Skelett ermöglichen.

## Vorgehensweise

1. **Untersuchung bestehender Ansätze:**
   - Avatar Project - Anpassung von 3D-Modellen an reale Personen
   - RVH Mesh Registration - Registrierung von 3D-Meshes auf reale Personen

2. **Nutzung und Testen eines SMPL-Renderers:**
   - Die vorhandenen Ansätze zum Rendern von SMPL 3D-Modellen sollen zum Laufen gebracht und mittels Tiefenaufnahmen von RGBD-Kameras getestet werden.

3. **Markererkennung und Zuordnung:**
   - Im nächsten Schritt wird die Erkennung der MoCap-Marker in den Tiefenaufnahmen vorgenommen. Diese Marker werden dann dem SMPL-Modell zugeordnet, um deren genaue Position relativ zum Skelett zu bestimmen.

4. **Evaluierung des SMPL-Modells:**
   - Nach der erfolgreichen Implementierung des SMPL-Modells wird dessen Performance in Bezug auf das Fitting in Kinect-Videos evaluiert. Dabei wird darauf geachtet, wie gut das Modell die Bewegungen der erfassten Person nachbilden kann und wie genau das resultierende Skelett ist.
