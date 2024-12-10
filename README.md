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

1. Installez les dépendances python en exécutant la commande suivante dans votre terminal :
   ```bash
   pip install -r requirements.txt
   ```

---

## Utilisation

1. Lancez le script Python :
```bash
python3 control.py
```

2. Appuyez sur les touches définies pour contrôler les fonctionnalités.

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







