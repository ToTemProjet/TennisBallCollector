# Debrief du 25/01/2022

PO: Florian Gaurier


## Bilan

Pourcentage de tâches réalisées: 60 %

### Ce qui a fonctionné

- Xacro : l'architecture globale est faite, reste à tester l'articulation et spawn dans gazebo
- Mapping : création de zones : 4 zones possibles (mur, goal, balle, robot) >> Implémentations zone = boîte qui vient bloquer ou non. >> Architecture logicielle faite
- Traitement d'images : HSV (H et S).


### Ce qui n'a pas fonctionné

- 3 personnes en présentiel : contact par conversation messenger. (COVID)


### Retour d'expérience du PO

Le backlog doit être raffiné pour avoir des fonctionnalité plus proches du "client" et plus simples (Ex.: aller à la balle >> détecter 1/des balles + avancer le robot etc) et ensuite ajouter les tasks


### Conseils pour le prochain PO

- Faire les user story plus "primitives"/petites
- En déduire les tasks


## Nouvelles mesures

Pour mettre à jour depuis le github penser  ajouter l'upstream avec :
```bash 
git remote add upstream https://github.com/JmichPalten/TennisBallCollector
```
Ènsuite faire :
```bash
git fetch upstream
git rebase upstream/<nom_de_la_branche>
```

Pour la prochaine fois :
	- Faire 2 .launch pour spawn le robot d'un côté et le robot + la scène de l'autre