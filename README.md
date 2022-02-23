# Tennis Ball Collector

Ceci est un template de dépôt Git pour le cours d'ingénierie système et modélisation robotique à l'ENSTA Bretagne en 2021.

### Dépendences

###### A compléter avec la/les dépendences.

Nécessite d'utiliser :
- Opencv

### Démarrer la simulation

Cloner le repository :
```bash
git clone https://github.com/ToTemProjet/TennisBallCollector.git
```

Se placer dans le dossier "TennisBallCollector"
```bash
cd <your_directory>/TennisBallCollector/
```

Construire l'ensemble du projet :
```bash
colcon build --symlink-install
```

Charger les variables nécessaires au fonctionnement de ROS2 : (Disponible sous galactic & foxy; recquiert l'installation sous /opt/ros/<distro>)
```bash
source setup.sh
```

Lancer le robot ET la scène :
```bash
ros2 launch bot robot.launch.py
```

### Modifier les package

Une erreur connue et non traitée existe concernant le symlink des fichiers en utilisant un setup.py avec le ament_python dans le package.xml. (Source : https://github.com/colcon/colcon-core/issues/407) Il est donc nécessaire de build à nouveau les packages après modification d'un fichier partagé via le setup.py. (Ex.: .launch; .urdf...)

## Groupe

### Membres

Badr MOUTALIB
Baptiste ORLHAC
Enzo ESSONO
Florian GAURIER
Isaac-Andreï WITT
Martin GOUNABOU

### Gestion de projet

Lien vers [Taiga](https://tree.taiga.io/project/andrei54-totem/timeline).
Lien vers les slides de [présentation](https://docs.google.com/presentation/d/1YX5qmtOK7w0YDIIzOg7Bh3UYP3WFRpOGJme5MQlJPwY/edit?fbclid=IwAR04dgeRve3ENqcEQgt61lSeGD0bORqXG570YBEygAEDbzH90c43XUK55cY#slide=id.p).


## Structure du dépôt

Ce dépôt doit être cloné dans le dossier `src` d'un workspace ROS 2.

### Package `tennis_court`

Le dossier `tennis_court` est un package ROS contenant le monde dans lequel le robot ramasseur de balle devra évoluer ainsi qu'un script permettant de faire apparaître des balles dans la simulation.
Ce package ne doit pas être modifié.
Consulter le [README](tennis_court/README.md) du package pour plus d'informations.


### Documents

Le dossier `docs` contient tous les documents utiles au projet:
- Des [instructions pour utiliser Git](docs/GitWorkflow.md)
- Un [Mémo pour ROS 2 et Gazebo](docs/Memo_ROS2.pdf)
- Les [slides de la présentation Git](docs/GitPresentation.pdf)


### Rapports

Le dossier `reports` doit être rempli avec les rapports d'[objectifs](../reports/GoalsTemplate.md) et de [rétrospectives](../reports/DebriefTemplate.md) en suivant les deux templates mis à disposition. Ces deux rapports doivent être rédigés respectivement au début et à la fin de chaque sprint.

