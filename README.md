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
