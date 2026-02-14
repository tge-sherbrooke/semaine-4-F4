# Formatif F4 — Threading et Bouton Polling Python

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
- Lecture d'un bouton par polling digitalio dans un thread dedie
- Arret propre d'un programme multi-threade

Ce formatif vous demande d'appliquer ces competences de maniere autonome.

---

## Progressive Milestones

Ce formatif utilise des **jalons progressifs** avec retroaction detaillee:

| Jalon | Points | Verification |
|-------|--------|-------------|
| **Milestone 1** | 25 pts | Script main.py, garde `__main__`, fonctions, constantes |
| **Milestone 2** | 35 pts | Imports threading/queue, utilisation Queue et Thread |
| **Milestone 3** | 40 pts | digitalio bouton polling, Event pour arret, gestion erreurs |

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
4. Lire un bouton avec digitalio polling dans un thread dedie
5. Gerer proprement l'arret du programme (Ctrl+C)

---

## Le probleme a resoudre

**Scenario**: Votre superviseur a remarque un probleme avec votre code de la semaine 3:

> "Quand tu appuies sur le bouton pendant que le capteur est en lecture,
> rien ne se passe. Le programme est bloque par `time.sleep(5)`!"

**Solution**: Le threading permet de:
- Lire les capteurs en arriere-plan (thread producteur)
- Traiter les donnees dans un autre thread (thread consommateur)
- Detecter les appuis bouton immediatement (polling dans un thread)

---

## Workflow de soumission

```
+-------------------------------------------------------------+
|                    WORKFLOW FORMATIF F4                     |
+-------------------------------------------------------------+
|                                                             |
|  1. Creer main.py avec la structure de base                 |
|     +-- Imports (threading, queue, digitalio)               |
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
|  3. Ajouter le polling bouton digitalio                     |
|     +-- Thread de polling avec button.value                 |
|     +-- Gestion d'erreurs dans le thread de polling         |
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
# dependencies = ["adafruit-blinka"]
# ///
"""Programme principal avec threading et bouton polling."""

import threading
import queue
import time
import board
import digitalio

# Configuration
SENSOR_INTERVAL = 5  # secondes entre lectures
BUTTON_PIN = board.GP17  # GPIO pour le bouton

# Communication inter-threads
data_queue = queue.Queue()
stop_event = threading.Event()

# Configuration du bouton
button = digitalio.DigitalInOut(BUTTON_PIN)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP


def read_sensor(sensor):
    """Thread producteur: lit le capteur periodiquement."""
    while not stop_event.is_set():
        try:
            temperature = sensor.temperature
            humidity = sensor.relative_humidity
            data = {"temperature": temperature, "humidity": humidity}
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


def button_polling_thread():
    """Thread de polling du bouton -- TOUJOURS avec try/except!"""
    last_value = True
    while not stop_event.is_set():
        try:
            current = button.value
            if last_value and not current:
                print("Bouton appuye!")
            last_value = current
        except Exception as e:
            print(f"Erreur polling: {e}")
        time.sleep(0.05)


def main():
    """Fonction principale."""
    # Initialiser le capteur AHT20
    import adafruit_ahtx0

    i2c = board.I2C()
    sensor = adafruit_ahtx0.AHTx0(i2c)

    # Creer et demarrer les threads
    producer = threading.Thread(target=read_sensor, args=(sensor,))
    consumer = threading.Thread(target=process_data)
    btn_thread = threading.Thread(target=button_polling_thread)

    producer.start()
    consumer.start()
    btn_thread.start()

    # Attendre la fin (ou Ctrl+C)
    try:
        producer.join()
        consumer.join()
        btn_thread.join()
    except KeyboardInterrupt:
        print("Arret demande...")
        stop_event.set()
    finally:
        button.deinit()


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

### Pourquoi try/except dans le thread de polling?

**IMPORTANT**: Le thread de polling du bouton s'execute en arriere-plan.
Les exceptions dans un thread ne sont **PAS AFFICHEES** dans le terminal
principal! Votre bouton peut sembler "arreter de fonctionner" sans message
d'erreur. Toujours entourer le code du thread avec try/except.

### Pourquoi digitalio polling?

digitalio est la bibliotheque standard CircuitPython pour les GPIO.
Le polling dans un thread dedie est simple, fiable, et fonctionne sur
tous les Raspberry Pi sans dependance supplementaire (via adafruit-blinka).

---

## Livrables

Dans ce depot, vous devez avoir :

- [ ] `main.py` — Script principal avec threading
- [ ] `.test_markers/` — Dossier cree par `validate_pi.py`

---

Bonne chance!
