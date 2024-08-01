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

## Dependencies

- **Boost 1.58:** Boost C++ Bibliothek ist eine Sammlung von hochqualitativen, plattformübergreifenden C++ Bibliotheken, die oft als Erweiterungen der Standardbibliothek dienen. Sie bietet Lösungen für eine Vielzahl von Programmieraufgaben, darunter Datenstrukturen, Algorithmen, Multithreading, und vieles mehr. Boost wird häufig als Grundlage für die Entwicklung von C++ Projekten verwendet und ist bekannt für seine robuste und gut getestete Implementierung.

- OpenCV 3.3+ (OpenCV 4 wird nicht unterstützt)
- Eigen 3.3.4
- Ceres Solver 1.14 (Ceres 2 wird nicht unterstützt)

Dies ist sehr leistungsrelevant, und es wird dringend empfohlen, Ceres manuell mit LAPACK- und OpenMP-Unterstützung zu bauen. Wenn Sie einen Intel-Prozessor verwenden, wird ebenfalls empfohlen, MKL als BLAS/LAPACK zu verwenden. Andernfalls wird ATLAS empfohlen. Stellen Sie außerdem sicher, dass Sie Ceres im Release-Modus bauen.

- zlib, für das Lesen des SMPL npz-Modells

Eine der folgenden (optional, aber erforderlich für Live-Demo):
- K4A (Azure Kinect SDK)
- libfreenect2
- PCL 1.8+, optional
