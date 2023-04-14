
# Challenge 48h - YBOT

Ybot est un bot discord prévu pour faciliter les échanges entre étudiants ainsi qu'avec la pédagogie.  

Il est connecté à Hyperplanning pour donner aux étudiants qui le souhaitent leur emploi du temps de façon journalière.  

Il dispose aussi d'un accès à l'API de ChatGPT pour que l'on puisse lui poser des questions directement sur Discord.
## Installation

Lien d'invitation du bot : https://discord.com/api/oauth2/authorize?client_id=1095987420555644978&permissions=8&scope=bot%20applications.commands

    
## Fonctionnalités

- Gestion des rôles
- Système de rappel
- Connexion aux emplois du temps
- Sondages
- Proposition d'afterwork
- Envoi de messages officiels
- Questions à ChatGPT


## Liste des commandes

Ces commandes sont à tester sur le serveur discord dans lequel se trouve le bot 

Envoie un message dans le channel de la commande (supprime l'appel à la commande)
```bash
  !send "Message @Pédagogie"
```
Envoie un message dans le channel général pour annoncer un afterwork prévu à la Kolok le soir même avec des réactions pour participer
```bash
  !afterwork
```
Pose une question à choix multiple avec des réactions pour y répondre, n'est pas limité au nombre de réponse possible
```bash
  !sondage "Question à choix multiple" "Réponse 1" "Réponse2" "Réponse 3"
```
Envoie l'emploi du temps du jour même (Intervenant, Salle, Heures)
```bash
  !aujrd
```
De même pour le lendemain
```bash
  !demain
```
De même pour toute la semaine actuelle
```bash
  !semaine
```
Renvoie uniquement l'heure du prochain cours
```bash
!time
```
Ouvre un channel privé accessible uniquement par son auteur et par le rôle qu'il souhaitera mentionner, toutes les instructions sont contenues dans le message qu'envoie le bot dans le channel
```bash
  !ticket
```
Envoie un rappel d'une tâche à la date indiquée
```bash
  !rappel [AAAA-MM-DD] [HH:MM] [Ce qui doit être rappelé]
```
Stock l'ical de l'étudiant dans une base de donnée locale au bot pour qu'il puisse lui envoyer son emploi du temps quotidiennement
```bash
!stocker_ical [lien_ical] 
```
Renvoie l'ical de l'étudiant qui envoie le message
```bash
!get_ical
```
Pose une question à ChatGPT, le bot renvoie la réponse
```bash
!gpt [Question]
```
## Authors

- [@Baptiste Legat](https://github.com/BaptisteLegat)
- [@Léonard Bensimon](https://github.com/Lbensimo)
- [@Quentin Saillard](https://github.com/QuentinSAIL)
- [@Mathieu Bouchon](https://github.com/FrenchAdmin)
- [@Tommy Arias](https://github.com/TommyArias)
- [@Alexis Poinsignon](https://github.com/AlexisP69)  

![Logo](https://www.ynov-lyon.com/app/uploads/2021/10/Informatique.png)

