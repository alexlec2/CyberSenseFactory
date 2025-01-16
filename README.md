---

# Projet Arduino avec PyFirmata

Ce projet utilise Python pour communiquer avec une carte Arduino via la bibliothèque `pyfirmata2`. Vous pouvez utiliser ce code pour contrôler ou interagir avec votre Arduino à partir de votre ordinateur.

---

## Prérequis

1. **Python**  
   Assurez-vous d'avoir Python 3.x installé sur votre machine.

2. **Matériel**  
   - Une carte Arduino UNO WiFi R4.  
   - Un câble USB-C pour connecter la carte Arduino à votre ordinateur.

---

## Installation

1. Installez les dépendances python dans un virtual environment en exécutant les commandes suivantes dans votre terminal :
   ```bash
   python3 -m venv ./venv
   source venv/bin/activate
   pip install -r requirements.txt

   # On mac
   brew install python-tk
   pip install tk
   ```
   Avec Windows remplacer "source venv/bin/activate" par :
   ```bash
   .\venv\Scripts\Activate
   ```

---

## Utilisation Code

Il existe 3 cas d'utilisation pour controler les éléments electroniques via l'activation des relais:
- via le keyboard avec le code `keyboard_control.py` avec l'arduino connecté
```bash
python3 keyboard_control.py
```

- via l'interface graphique avec l'arduino connecté (version finale) avec `ui_control.py`
```bash
python3 ui_control.py
```

- via l'interface graphique sans l'arduino connecté (pour faire des tests) avec `withoutArduino/ui_control_withoutArduino.py`
```bash
cd withoutArduino
python3 ui_control_withoutArduino.py
```
- via le keyboard sans l'arduino connecté (pour faire des tests) avec `withoutArduino/keyboard_control_withoutArduino.py`
```bash
cd withoutArduino
python3 keyboard_control_withoutArduino.py
```

---


## Utilisation Focus

La touche <Tab> permet de naviguer entre les trois élements (les 2 boutons et le slider).   
Une fois le focus dessus, la touche <Return> ou "Entrée" permet de changer sa valeur.  
Par défaut le focus est de base sur le bouton n1 (Aiguillage 1).  


---

## Connexion et Configuration du Port Série

Le code `control.py` utilise la fonction `find_arduino()` pour trouver le port de connexion avec l'Arduino et ainsi établir la connexion automatiquement.

Cependant, si cela échoue, vous pouvez définir manuellement le port de connexion avec l'Arduino. 
Pour vérifier les ports série disponibles, utilisez la commande suivante dans votre terminal :
```bash
# MacOS
ls -l /dev/tty.usb*

# Windows
mode

# Powershell
Get-WmiObject Win32_SerialPort
```

### Exemple d'utilisation
Une fois que vous avez identifié le port correct (par exemple `/dev/tty.usbmodem14201` ou `COM3`), vous pouvez configurer votre script Python comme suit :
```python
from pyfirmata2 import Arduino

board = Arduino('/dev/tty.usbmodem14201')  # Remplacez par votre port
```

---
## Installation board Arduino R4 Wifi

Après avoir installé l'IDE Arduino ---> installer depuis le "board manager" la carte Arduino R4 Wifi


## Libraries uploaded on Arduino UNO R4 WiFi

- Firmata (tuto upload [ici](https://roboticsbackend.com/arduino-standard-firmata-tutorial/))
   - Problème dans `Boards.h` --> ajouter le bloc de définiton de la cart UNO R4 WiFi (bloc ici ligne 457 à 475 : https://github.com/firmata/arduino/blob/main/Boards.h#L457)


## Train 
Recepteur est sur le 1.

# Connexion filaire

Relai 1 connecté à l'output 13 de l'arduino et le + de la batterie.
Relai 2 connecté à l'output 12 de l'arduino et le - de la batterie.

| Fil          | Input       | Output      | 
| ------------ | ----------- | ----------- |
| Rouge        | Arduino 5 V | + Relai 1   |
| Orange       | + Relai 1   | + Relai 2   |
| Noir         | GND Arduino | - Relai 1   |
| Gris         | - Relai 1   | - Relai 2   |
| Cyan         | Arduino D13 | S relai 1   |
| Bleu         | Arduino D12 | S relai 2   |
| Violet       | + Batterie  | COM Relai 1 |
| Rose         | - Batterie  | COM Relai 2 |
| Marron foncé | NC Relai 1  | Moteur +    |
| Marron clair | NO Relai 1  | Moteur -    |
| Vert         | NC Relai 2  | Moteur +    |
| Jaune        | NO Relai 2  | Moteur -    |

| Arduino Output  | Relai 1 | Relai 2 | 
| --------------- | ------- | ------- |
| 13       | 12   | NC | NO | NC | NO |
| -------- | ---- | -- | -- | -- | -- |
| 1        | 0    | 0  | 1  | 1  | 0  |
| 0        | 1    | 1  | 0  | 0  | 1  |



## Build exe
```bash
pyinstaller --onefile --add-data "images/position_1.png;images/" --add-data "images/position_2.png;images/" -w ui_control.py --name Scada --icon images/icon.png

pyinstaller --onefile --add-data "images/position_1.png;images/" --add-data "images/position_2.png;images/" --add-data "images/position_3.png;images/" --add-data "images/position_4.png;images/" -w ui_control_withoutArduino.py --name ScadaWithoutArduino --icon images/icon.png
```
