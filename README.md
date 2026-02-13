# Formatif F4 — Threading et Callbacks Python

**Cours** : 243-413-SH — Introduction aux objets connectes
**Semaine** : 4
**Type** : Formative (non notee)
**Retries** : Illimites - poussez autant de fois que necessaire!

---

> **Pratique autonome** -- Ce formatif est une evaluation formative (non notee). Contrairement au laboratoire guide, vous devez completer les taches de maniere autonome. Les tests automatiques vous donnent une retroaction immediate a chaque push.

## Ce que vous avez appris en labo

Le laboratoire de la semaine 4 vous a guide a travers :

- Structuration d'un script Python avec fonctions et main guard
- Creation de threads pour lectures de capteurs en arriere-plan
- Utilisation de `queue.Queue` pour communication thread-safe
- Gestion d'un bouton avec callbacks gpiozero
- Arret propre d'un programme multi-threade

Ce formatif vous demande d'appliquer ces competences de maniere autonome.

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script main.py, garde `__main__`, fonctions, constantes |
| **Milestone 2** | 35 pts | Imports threading/queue, utilisation Queue et Thread |
| **Milestone 3** | 40 pts | gpiozero callbacks, Event pour arret, gestion erreurs |

**Chaque test echoue vous dit**:
- Ce qui etait attendu
- Ce qui a ete trouve
- Une suggestion pour corriger

---

## Objectif

Ce formatif vise a verifier que vous etes capable de :
1. Structurer du code Python avec des fonctions et un garde main
2. Utiliser le threading pour des lectures de capteurs non-bloquantes
3. Utiliser Queue pour la communication thread-safe
4. Implementer des callbacks de bouton avec gpiozero
5. Gerer proprement l'arret du programme (Ctrl+C)

---

## Le probleme a resoudre

**Scenario**: Votre superviseur a remarque un probleme avec votre code de la semaine 3:

> "Quand tu appuies sur le bouton pendant que le capteur est en lecture,
> rien ne se passe. Le programme est bloque par `time.sleep(5)`!"

**Solution**: Le threading permet de:
- Lire les capteurs en arriere-plan (thread producteur)
- Traiter les donnees dans un autre thread (thread consommateur)
- Repondre aux boutons immediatement (callbacks)

---

## Workflow de soumission

```
+-------------------------------------------------------------+
|                    WORKFLOW FORMATIF F4                     |
+-------------------------------------------------------------+
|                                                             |
|  1. Creer main.py avec la structure de base                 |
|     +-- Imports (threading, queue, gpiozero)                |
|     +-- Constantes de configuration                         |
|     +-- Fonctions (read_sensor, publish_data)               |
|     +-- Garde __main__                                      |
|                                                             |
|  2. Ajouter le pattern producteur-consommateur              |
|     +-- Queue pour les donnees                              |
|     +-- Thread producteur (lecture capteur)                 |
|     +-- Thread consommateur (traitement/publication)        |
|     +-- Event pour l'arret propre                           |
|                                                             |
|  3. Ajouter les callbacks gpiozero                          |
|     +-- Bouton avec when_pressed                            |
|     +-- Gestion d'erreurs dans les callbacks                |
|     +-- Gestion de KeyboardInterrupt                        |
|                                                             |
|  4. Tester sur Raspberry Pi                                 |
|     +-- python3 validate_pi.py                              |
|                                                             |
|  5. Pousser vers GitHub                                     |
|                                                             |
+-------------------------------------------------------------+
```

---

## Structure de code recommandee

```python
# /// script
# requires-python = ">=3.9"
# dependencies = ["gpiozero"]
# ///
"""Programme principal avec threading et callbacks."""

import threading
import queue
import time
from gpiozero import Button

# Configuration
SENSOR_INTERVAL = 5  # secondes entre lectures
BUTTON_PIN = 17      # GPIO pour le bouton

# Communication inter-threads
data_queue = queue.Queue()
stop_event = threading.Event()


def read_sensor(sensor):
    """Thread producteur: lit le capteur periodiquement."""
    while not stop_event.is_set():
        try:
            data = sensor.read()
            data_queue.put(data)
            print(f"Lecture: {data}")
        except Exception as e:
            print(f"Erreur lecture: {e}")
        time.sleep(SENSOR_INTERVAL)


def process_data():
    """Thread consommateur: traite les donnees de la queue."""
    while not stop_event.is_set():
        try:
            data = data_queue.get(timeout=1)
            # Traiter/publier les donnees
            print(f"Traitement: {data}")
        except queue.Empty:
            continue  # Pas de donnees, continuer


def on_button_press():
    """Callback du bouton - TOUJOURS avec try/except!"""
    try:
        print("Bouton appuye!")
        # Lecture immediate du capteur
    except Exception as e:
        print(f"Erreur callback: {e}")


def main():
    """Fonction principale."""
    # Setup button
    button = Button(BUTTON_PIN, bounce_time=0.1)
    button.when_pressed = on_button_press

    # Creer et demarrer les threads
    producer = threading.Thread(target=read_sensor, args=(sensor,))
    consumer = threading.Thread(target=process_data)

    producer.start()
    consumer.start()

    # Attendre la fin (ou Ctrl+C)
    try:
        producer.join()
        consumer.join()
    except KeyboardInterrupt:
        print("Arret demande...")
        stop_event.set()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Programme termine.")
        stop_event.set()
```

---

## Points cles

### Pourquoi `queue.Queue`?

Les variables partagees entre threads peuvent causer des "race conditions".
`Queue` est thread-safe: plusieurs threads peuvent faire `.put()` et `.get()`
sans risque de corruption de donnees.

### Pourquoi `threading.Event`?

Pour signaler aux threads de s'arreter proprement. Chaque thread verifie
`stop_event.is_set()` dans sa boucle et sort quand c'est `True`.

### Pourquoi try/except dans les callbacks?

**IMPORTANT**: gpiozero execute les callbacks dans des threads en arriere-plan.
Les exceptions dans les callbacks sont **SILENCIEUSEMENT IGNOREES**!
Votre bouton semble "arreter de fonctionner" sans message d'erreur.

### Pourquoi gpiozero?

- Plus simple que RPi.GPIO
- Fonctionne sur Raspberry Pi 5
- API Pythonique avec callbacks

---

## Livrables

Dans ce depot, vous devez avoir :

- [ ] `main.py` — Script principal avec threading
- [ ] `.test_markers/` — Dossier cree par `validate_pi.py`

---

Bonne chance!
