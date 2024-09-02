# Automatic Skeleton Marker Relation

### Luke Mikat, Abraham Neme Alvarez, Valdone Zabutkaite

## Poster

## Problemstellung

Beim markerbasierten Motion Capturing (MoCap) werden Marker auf den Körper platziert. Es ist jedoch nicht immer möglich, alle Marker genau dort zu platzieren, wo sie idealerweise hingehören. Dadurch fehlt die Relation zwischen den Markern und dem Skelett, was bedeutet, dass man nicht mehr von den Markern auf das Skelett zurückschließen kann.

## Lösungsansatz

Um die Relation zwischen den MoCap-Markern und dem Skelett zu verbessern, wird vorgeschlagen, auf bestehende Forschungsarbeiten zurückzugreifen, die parametrische Menschenmodelle wie [SMPL (Skinned Multi-Person Linear Model)](https://smpl.is.tue.mpg.de/) verwenden. Diese Modelle können in Tiefenaufnahmen von RGBD-Kameras, beispielsweise der Kinect, eingebettet werden. 

Die Hauptidee besteht darin, zunächst das SMPL-Modell auf die Tiefenaufnahmen zu fitten und in einem zweiten Schritt die MoCap-Marker zu erkennen und deren Relation zum SMPL-Modell herzustellen. Durch die Verwendung des SMPL-Modells könnte man eine präzisere Positionierung der Marker erreichen, da das Modell detaillierte Informationen über die Körperform und -struktur liefert. Sobald das Modell angepasst ist, könnte die Position der Marker relativ zum Modell berechnet werden. Das würde eine genaue Relation zwischen den Markern und dem Skelett ermöglichen.

## Vorgehensweise

1. **Untersuchung bestehender Ansätze:**
   - [Avatar Project](https://github.com/sxyu/avatar) - Anpassung von 3D-Modellen an reale Personen
   - [RVH Mesh Registration](https://github.com/bharat-b7/RVH_Mesh_Registration?tab=readme-ov-file) - Registrierung von 3D-Meshes auf reale Personen

2. **Nutzung und Testen eines SMPL-Renderers:**
   - Die vorhandenen Ansätze zum Rendern von SMPL 3D-Modellen sollen zum Laufen gebracht und mittels Tiefenaufnahmen von RGBD-Kameras getestet werden.

3. **Markererkennung und Zuordnung:**
   - Im nächsten Schritt wird die Erkennung der MoCap-Marker in den Tiefenaufnahmen vorgenommen. Diese Marker werden dann dem SMPL-Modell zugeordnet, um deren genaue Position relativ zum Skelett zu bestimmen.

4. **Evaluierung des SMPL-Modells:**
   - Nach der erfolgreichen Implementierung des SMPL-Modells wird dessen Performance in Bezug auf das Fitting in Kinect-Videos evaluiert. Dabei wird darauf geachtet, wie gut das Modell die Bewegungen der erfassten Person nachbilden kann und wie genau das resultierende Skelett ist.

## Avatar Project

### Dependencies

[cmake](https://cmake.org/download/) installieren

vcpkg installieren:

```bash
   git clone https://github.com/microsoft/vcpkg.git
   cd vcpkg
   ./bootstrap-vcpkg.bat     # For Windows
   ./bootstrap-vcpkg.sh      # For Linux/macOS
   ./vcpkg integrate install
```
Bei Bedarf glfw3 installieren:

```bash
   ./vcpkg install glfw3
```

Dependencies installieren über vcpkg:

```bash
   ./vcpkg install azure-kinect-sensor-sdk
   ./vcpkg install opencv3
   ./vcpkg install opencv3[openexr]
   ./vcpkg install eigen3
   ./vcpkg install zlib
   ./vcpkg install boost
   ./vcpkg install ceres
```

### Datensätze 

Die Model-Daten und Datasets aus dem [originalen Repo](https://github.com/sxyu/avatar/releases/) waren nicht mehr verfügbar, wodurch man [dieser Anleitung](https://github.com/augcog/OpenARK/tree/master/data/avatar-model) folgen musste um die notwendigen Dateien zu erhalten.

Notwendig für das Ausführen der Live-Demo:

data/avatar-model:

- model.pcd
- skeleton.txt
- joint_regressor.txt
- pose_prior.txt
- tree.150k.refine.srtr
- tree.150k.refine.srtr.partmap

Notwendig für das Ausführen der Demo (OpenARK Dataset):

Herunterladen und in den Ordner data/avatar-dataset extrahieren:

https://github.com/sxyu/OpenARK-Deps/releases/download/0.0.1/avatar-dataset.zip

### Build

Replace the path to vcpkg:

```bash
   cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:\path\to\vcpkg\scripts\buildsystems\vcpkg.cmake
   cd build
   cmake --build build --config Release
   cd Release
```

### Live-Demo

TODO 

Die Live-Demo zeigt eine Echtzeitdarstellung von einer Kinect-Kamera und visualiesiert einen 3D-Avatar auf die im Bild stehende Person.

```bash
./live-demo.exe --rtree ./tree.150k.refine.srtr
```

### Demo

TODO 

Die Demo zeigt die Verarbeitung und Animation eines 3D-Avatars basierend auf voraufgezeichneten Tiefen-Bildern. Diese Demo dient dazu, die Ergebnisse der Pipeline zu veranschaulichen, ohne dass Echtzeit-Daten erforderlich sind.

```bash
cd build/Release
./demo --rtree tree.150k.refine.srtr --dataset_path ../../data/avatar-dataset/human-dance-random --image 351 --background 351
```

Optional arguments:

TODO (alle optionalen Arguments auflisten/austesten)

-T
-M
...

### Evaluierung

#### Live-Demo 
   ![Avatar Project Evaluation](./images/avatar-project-evaluation.png) -
#### Demo
 TODO

## RVH Mesh Registration

TODO

### Dependencies

### Build

### Datensätze

...


## Ablauf des Projektes

TODO 

Die Reproduktion des Repositories erwies sich als eine anspruchsvolle Aufgabe, da die verwendeten C++-Bibliotheken veraltet waren und es zu Abhängigkeitskonflikten kam. Zudem fehlten sowohl die Datensätze als auch die Demos, und die im Repository angegebenen Links waren nicht mehr verfügbar. So mussten wir die Datensätze teilweise selbst zusammenzustellen, was zeitaufwändig war. Schließlich konnten wir die Live-Demo und die Demo zum Laufen bringen und evaluieren.

## Aufgabenteilung

TODO

## Reflexion

TODO

Abraham(943567)

Valdone()

Luke(@s82765)
