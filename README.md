# Projet de reconnaissance visuelle des élèves d'une classe

## Description

L'application est un système de reconnaissance visuelle, qui détecte automatiquement les élèves lorsqu'ils se situent en face de la caméra dans la classe. Cela permet par exemple de faire l'appel en notant les élèves absents ainsi que ceux ayant été en retard. L'application est également dotée d'une fonctionnalité envoyant un mail aux parents des élèves absents et en retard ainsi qu'à l'administration de l'école ou un responsable.

## Membres du projet

Wolf Maxime <br/>
Boulet Timothé <br/>
Tonetto Léo-Paul <br/>
Battach Marouane

### Jalons

Jour 1 : <br/>
• Gitlab bien organisé <br/>
• Récupérer les fonctions utiles de la semaine dernière et éventuellement les adapter à notre cas de figure <br/>
• Commencer les nouveaux programmes dont celui de lecture et de récupération des images de la vidéo <br/>
• Créer l’IA

Jour 2 : <br/>
• Terminer les nouveaux programmes dont celui de lecture et de récupération des images de la vidéo <br/>
• Partie avec l’envoie d’email aux personnes concernées et lancement de la vidéo par le prof

Jour 3 : <br/>
• Partie avec l’envoie d’email aux personnes concernées et lancement de la vidéo par le prof <br/>
• Mise en forme des données renvoyées au professeur

Jour 4 : <br/>
• Finaliser l’application avec argparse <br/>
• Finaliser le Gitlab

## Installation

On précise ici les bibliothèques qui sont nécessaires au bon fonctionnement des programmes.

```bash
pip install opencv-python
pip install numpy
pip install matplotlib
pip install tkinter
pip install git+https://github.com/rcmalli/keras-vggface.git
pip install email
pip install smtplib
pip install PIL

```

## Exemple d'utilisation

La commande suivante permet d'éxecuter le script python de principale.py qui ouvre ensuite une fenêtre dans laquelle il faut préciser la valeur de la durée de la capture voulue. En éxecutant ce script, on parcourt une vidéo test (dans laquelle apparaît plusieurs personnalités) images par images et les programmes permettent d'en déduire quelles personnes arrivent en retard, quelles personnes sont absentes. Ensuite, un mail est envoyé au responsable et aux "élèves" comme précisé dans la description du projet. (Remarque : ici on a utilisé nos adresses mails pour modéliser celles des personnes présentes sur la vidéo)


```bash
python principale.py
```

## Support

Pour plus d'informations/questions : <br/>
maxime.wolf@student-cs.fr <br/>
lp.tonetto@student-cs.fr <br/>
timothe.boulet@student-cs.fr <br/>
marouane.battach@student-cs.fr
