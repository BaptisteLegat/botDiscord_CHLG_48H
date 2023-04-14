
# Challenge 48h - YBOT

Ybot est un bot discord prévu pour faciliter les échanges entre étudiants ainsi qu'avec la pédagogie.  

Il est connecté à Hyperplanning pour donner aux étudiants qui le souhaitent leur emploi du temps quand ils le demandent.

Il dispose aussi d'un accès à l'API de ChatGPT pour que l'on puisse lui poser des questions directement sur Discord.
## Installation

Lien d'invitation du bot : https://discord.com/api/oauth2/authorize?client_id=1095987420555644978&permissions=8&scope=bot%20applications.commands  
  
Ces commandes doivent être exécutée sur un OS Linux

```bash
$ sudo apt install pip
$ pip install python3

$ pip install discord.py re sqlite3 pytz icalendar openai asyncio
```

    
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
Pose une question à choix multiple avec des réactions pour y répondre, n'est pas limité au nombre de réponse possible, les guillemets sont indispensables
```bash
  !sondage "Question à choix multiple" "Réponse 1" "Réponse2" "Réponse 3"
```
Envoie l'emploi du temps du jour même (Intervenant, Salle, Heures)
```bash
  !ajrd
```
De même pour le lendemain
```bash
  !demain
```
De même pour toute la semaine actuelle
```bash
  !semaine
```
Ouvre un channel privé accessible uniquement par son auteur et par le rôle qu'il souhaitera mentionner, toutes les instructions sont contenues dans le message qu'envoie le bot dans le channel
```bash
  !ticket
```
Envoie un rappel d'une tâche à la date indiquée
```bash
  !rappel [AAAA-MM-DD] [HH:MM] [Ce qui doit être rappelé]
```
Envoie la liste des rappels en sommeil pour l'utilisateur
```bash
!mes_rappels
```
Stock l'ical de l'étudiant dans une base de donnée locale au bot pour qu'il puisse lui envoyer son emploi du temps quotidiennement | Commande uniquement disponible en mp
```bash
!verify [lien_ical] 
```
Renvoie l'ical de l'étudiant qui envoie le message | Commande uniquement disponible en mp
```bash
!get_ical
```
Pose une question à ChatGPT, le bot renvoie la réponse
La réponse n'est pas bridée, le bot peut partir en roue libre
Les réponses sont limités en mot (100 tokens = 3500 mots)
```bash
!gpt [Question]
```
Envoie une citation de motivation
```bash
!citation
```
## Authors

- [@Baptiste Legat](https://github.com/BaptisteLegat)
- [@Léonard Bensimon](https://github.com/Lbensimo)
- [@Quentin Saillard](https://github.com/QuentinSAIL)
- [@Mathieu Bouchon](https://github.com/FrenchAdmin)
- [@Tommy Arias](https://github.com/TommyArias)
- [@Alexis Poinsignon](https://github.com/AlexisP69)  

![Logo](https://www.ynov-lyon.com/app/uploads/2021/10/Informatique.png)

