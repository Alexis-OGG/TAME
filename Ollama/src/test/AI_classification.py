import random
import re
from collections import Counter
import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report, accuracy_score
from pathlib import Path
import json

# ============================================================
# 1. Données synthétiques par sous-catégorie
# ============================================================

SEEDS = {
    "RES": [
        "RES SMD 100K OHM 1% 1/10W 0603",
        "RESISTANCE 10K 1% 0805",
        "RES 4K7 0.1W 5% CMS",
        "RES 220R 1/4W AXIAL",
        "RESISTOR 47K 1% 1206",
    ],
    "POT": [
        "POT 10K LINEAIRE",
        "POTENTIOMETRE 100K",
        "TRIMMER 50K 10 TOURS",
        "POT AJUSTABLE 1K",
        "POTENTIOMETRE ROTATIF 470K",
    ],
    "VARISTANCE": [
        "VARISTANCE 275VAC",
        "MOV 14D471K",
        "VARISTOR 470V",
        "VARISTANCE 320V 14MM",
    ],
    "THERMISTANCE": [
        "THERMISTANCE NTC 10K 3950",
        "NTC 100K 1%",
        "PTC 1K",
        "THERMISTOR NTC 10K 0603",
    ],

    "COND_ALUM": [
        "COND ALU 100UF 25V RADIAL",
        "CAP ELECTROLYTIQUE 470UF 35V",
        "CAP ALUMINIUM 1000UF 16V",
        "ELCO 22UF 50V",
    ],
    "COND_TANT": [
        "COND TANTALE 47UF 16V",
        "CAP TANT 10UF 25V SMD",
        "TANTALUM CAP 100UF 10V",
    ],
    "COND_CERAM": [
        "COND CERAM 100NF 50V X7R 0603",
        "CAP MLCC 1UF 25V X5R 0805",
        "CERAMIC CAP 10PF C0G",
        "CAP 4.7UF X7R 16V 1206",
    ],
    "COND_AJUSTABLE": [
        "COND AJUSTABLE 5 30PF",
        "TRIMMER CAPACITOR 20PF",
        "VARIABLE CAP 2 10PF",
    ],
    "COND_EDLC": [
        "SUPERCAP 1F 5.5V",
        "EDLC 10F 2.7V",
        "SUPER CAPACITOR 100F 2.7V",
    ],

    "DIODE_DE_REDRESS": [
        "DIODE REDRESSEMENT 1N4007",
        "RECTIFIER DIODE 1A 1000V",
        "1N5408 3A 1000V",
    ],
    "DIODE_ZENER": [
        "DIODE ZENER 5V1 500MW",
        "ZENER 12V SOD123",
        "BZX84C3V3 SOT23",
    ],
    "DIODE_DE_SIGNAL": [
        "DIODE SIGNAL 1N4148",
        "1N4148WS SOD323",
        "SMALL SIGNAL DIODE 100V",
    ],
    "DIODE_SCHOTTKY": [
        "DIODE SCHOTTKY BAT54",
        "SCHOTTKY 1A 40V SOD123",
        "SS14 40V 1A",
        "MBR0520 20V 500MA",
    ],
    "DIODE_TRANSIL": [
        "TVS 24V BIDIRECTIONNELLE",
        "TRANSIL 5V SMB",
        "SMBJ24CA TVS",
        "TVS DIODE 12V",
    ],
    "PONT_DE_DIODE": [
        "PONT DIODE 2A 600V",
        "BRIDGE RECTIFIER 4A 1000V",
        "DF06M PONT REDRESSEUR",
    ],
    "DIODE_ESD": [
        "PROTECTION ESD USB 5V",
        "ESD DIODE SOT23",
        "TVS ESD ARRAY 4 CHANNEL",
    ],

    "SELF": [
        "SELF 10UH 3A SMD",
        "INDUCTOR 47UH 2A",
        "BOBINE 100UH 1A",
        "POWER INDUCTOR 22UH",
    ],
    "SELF_MODE_COMMUN": [
        "SELF MODE COMMUN 2X10MH",
        "COMMON MODE CHOKE 90 OHM",
        "CMC USB 2 LIGNES",
    ],
    "FERRITES": [
        "FERRITE BEAD 600R 100MHZ",
        "FERRITE 0805 1A",
        "BEAD 120R 0603",
    ],
    "TRANSFO_ISOLEMENT": [
        "TRANSFO ISOLEMENT 230V 12V",
        "ISOLATION TRANSFORMER 1KV",
        "TRANSFORMATEUR ISOLE 24V",
    ],
    "TRANSFO_DE_COURANT": [
        "TRANSFO COURANT 100A 50MA",
        "CURRENT TRANSFORMER 20A",
        "CT SENSOR TRANSFORMER 50A",
    ],
    "TRANSFO_ETHERNET": [
        "TRANSFO ETHERNET 10 100",
        "LAN TRANSFORMER 1 PORT",
        "ETHERNET MAGNETICS 100BASE-T",
    ],

    "CI_AOP_COMPAR": [
        "LM358 DUAL OP AMP SOIC8",
        "AMPLIFICATEUR OPERATIONNEL TL072",
        "COMPARATEUR LM393",
        "MCP6002 OPAMP",
    ],
    "CI_REGUL": [
        "REGULATEUR LDO 3V3 500MA",
        "AMS1117 3.3V SOT223",
        "LM7805 REGULATEUR 5V",
        "TPS7A02 LDO 3V3",
    ],
    "CI_LOGIQUE": [
        "74HC00 QUAD NAND",
        "74HC14 HEX SCHMITT",
        "LOGIC GATE AND 74LVC",
        "74HC595 SHIFT REGISTER",
    ],
    "CI_MEMOIRE": [
        "EEPROM I2C 256KBIT",
        "FLASH SPI 16MB",
        "W25Q128JV SPI FLASH",
        "24LC256 EEPROM",
    ],
    "CI_PROC": [
        "STM32F405RGT6 LQFP64",
        "STM32L476 ARM CORTEX M4",
        "MICROCONTROLEUR 32BIT 512KB",
        "ATSAMD21G18 MCU",
        "PIC18F4550 MICROCONTROLEUR",
    ],
    "CI_CONVERT": [
        "ADC 16BIT 8 CHANNEL SPI",
        "DAC 12BIT I2C",
        "ADS1115 ADC 16BIT",
        "MCP4725 DAC I2C",
    ],
    "CI_DRIVER": [
        "DRIVER MOTEUR DC DOUBLE PONT H",
        "DRV8833 MOTOR DRIVER",
        "DRIVER MOSFET HIGH SIDE",
        "ULN2003 DRIVER DARLINGTON",
    ],
    "CI_REF_DE_TENSION": [
        "REFERENCE TENSION 2V5",
        "TL431 2.5V REFERENCE",
        "ADR4525 VOLTAGE REFERENCE",
    ],
    "CI_RTC": [
        "RTC DS3231 I2C",
        "HORLOGE TEMPS REEL PCF8563",
        "REAL TIME CLOCK I2C",
    ],
    "CI_CHARGEUR": [
        "TP4056 CHARGEUR LI ION",
        "BATTERY CHARGER IC 1A",
        "BQ24075 CHARGER IC",
    ],
    "CI_CAPTEUR_TEMP": [
        "TMP117 CAPTEUR TEMPERATURE",
        "TEMPERATURE SENSOR IC I2C",
        "LM75 DIGITAL TEMP SENSOR",
    ],

    "OSCIL": [
        "OSCILLATEUR 16MHZ CMOS",
        "OSCILLATOR 25MHZ 3V3",
        "TCXO 10MHZ",
    ],
    "RESON": [
        "RESONATEUR CERAMIQUE 8MHZ",
        "CERAMIC RESONATOR 16MHZ",
        "RESONATOR 4MHZ",
    ],
    "QUARTZ": [
        "QUARTZ 16MHZ 20PF",
        "CRYSTAL 32.768KHZ",
        "XTAL 24MHZ SMD",
    ],
    "BUZZER": [
        "BUZZER PIEZO 5V",
        "PIEZO BUZZER 12V",
        "AVERTISSEUR PIEZO 85DB",
    ],

    "BOUTON_POUSSOIR": [
        "BOUTON POUSSOIR MOMENTANE NO",
        "PUSH BUTTON SMD",
        "TACT SWITCH 6X6",
    ],
    "INTERRUPTEUR": [
        "INTERRUPTEUR ON OFF SPST",
        "TOGGLE SWITCH 2 POSITIONS",
        "ROCKER SWITCH 250V",
    ],
    "RELAIS": [
        "RELAIS 12V SPDT 10A",
        "RELAY 5V 2RT",
        "RELAIS 24VDC 250VAC",
    ],
    "FUSIBLE": [
        "FUSIBLE 2A 250V",
        "FUSE SMD 1A 0603",
        "FAST FUSE 5A",
    ],
    "DISJONCTEUR": [
        "DISJONCTEUR 10A",
        "CIRCUIT BREAKER 16A",
        "DISJONCTEUR THERMIQUE 5A",
    ],

    "TRANSISTOR_BIP": [
        "TRANSISTOR NPN BC547",
        "PNP TRANSISTOR BC557",
        "2N3904 NPN SOT23",
        "BC817 45V 500MA",
    ],
    "TRANSISTOR_MOS": [
        "MOSFET N 60V 5A",
        "BSS138 N MOS SOT23",
        "IRLZ44N MOSFET",
        "MOS P CHANNEL 30V",
    ],
    "TRANSISTOR_IGBT": [
        "IGBT 600V 30A",
        "IGBT TRANSISTOR TO247",
        "650V 40A IGBT",
    ],
    "TRIAC": [
        "TRIAC 600V 16A",
        "BTA16 600B TRIAC",
        "TRIAC SMD 4A",
    ],
    "THYRISTOR": [
        "THYRISTOR SCR 800V",
        "SCR 12A 600V",
        "THYRISTOR 25A TO220",
    ],

    "CONNECT": [
        "CONNECTEUR 4 POSITIONS 2.54MM",
        "HEADER 10 PIN",
        "CONNECTOR 6P SMD",
    ],
    "CONNECT_COAX": [
        "CONNECTEUR SMA FEMELLE",
        "COAX CONNECTOR BNC",
        "UFL RF CONNECTOR SMD",
    ],
    "BORNIER": [
        "BORNIER 3 POSITIONS 5.08MM",
        "TERMINAL BLOCK 2P",
        "BORNIER PCB A VIS",
    ],
    "FICHE_BANANE": [
        "FICHE BANANE ROUGE 4MM",
        "BANANA PLUG 4MM",
        "FICHE BANANE NOIRE",
    ],
    "POINTE_TEST": [
        "POINTE TEST ROUGE",
        "TEST PROBE 2MM",
        "POINTE MESURE MULTIMETRE",
    ],

    "BOITIER": [
        "BOITIER ABS IP65",
        "ENCLOSURE PLASTIC 120X80",
        "BOITIER ALUMINIUM IP67",
    ],
    "DISSIPATEUR": [
        "DISSIPATEUR TO220",
        "HEATSINK ALUMINIUM 25MM",
        "RADIATEUR THERMIQUE",
    ],
    "VENTILATEUR": [
        "VENTILATEUR 24V 40X40MM",
        "FAN 12VDC 80MM",
        "VENTILATEUR AXIAL 5V",
    ],
    "MOTEUR": [
        "MOTEUR DC 12V",
        "STEPPER MOTOR 24V",
        "MOTEUR PAS A PAS",
    ],
    "RESSORT": [
        "RESSORT COMPRESSION INOX",
        "SPRING 10MM",
        "RESSORT TRACTION",
    ],

    "PILE": [
        "PILE CR2032 3V",
        "PILE ALCALINE AA 1V5",
        "COIN CELL CR2450",
    ],
    "BATTERIE": [
        "BATTERIE LI ION 3V7 2600MAH",
        "BATTERY LIPO 1000MAH",
        "BATTERIE NIMH 12V",
    ],

    "FIL": [
        "FIL CUIVRE 0.5MM2 ROUGE",
        "WIRE AWG22 BLACK",
        "FIL ELECTRIQUE AWG18",
    ],
    "CABLE": [
        "CABLE USB A USB C 1M",
        "CABLE ALIMENTATION 2 CONDUCTEURS",
        "CORDON USB 2M",
    ],
    "CABLE_ETHERNET": [
        "CABLE ETHERNET CAT6 2M",
        "RJ45 PATCH CABLE CAT5E",
        "CORDON RESEAU CAT6",
    ],
    "CABLE_PLAT": [
        "CABLE PLAT 20 CONDUCTEURS",
        "RIBBON CABLE 10 WAY",
        "NAPPE FFC 20P",
    ],
    "GAINE": [
        "GAINE THERMO 5MM",
        "HEAT SHRINK TUBE",
        "GAINE ISOLANTE NOIRE",
    ],

    "DIODE_LED": [
        "LED ROUGE 0603",
        "DIODE LED BLEUE 3MM",
        "LED VERTE 0805",
        "WHITE LED SMD",
    ],
    "OPTOCOUPLEUR": [
        "OPTOCOUPLEUR PC817",
        "OPTOISOLATOR 5KV DIP4",
        "6N137 HIGH SPEED OPTOCOUPLER",
    ],
    "PHOTODIODE": [
        "PHOTODIODE SILICIUM",
        "PHOTO DIODE IR",
        "PHOTODIODE 900NM",
    ],
    "PHOTOTRANSISTOR": [
        "PHOTOTRANSISTOR IR",
        "PHOTO TRANSISTOR 940NM",
        "NPN PHOTOTRANSISTOR",
    ],
    "AFFICHEUR": [
        "AFFICHEUR LCD 20X4",
        "DISPLAY OLED 128X64",
        "AFFICHEUR 7 SEGMENTS",
    ],
    "CAMERA": [
        "CAMERA CMOS 2MP",
        "CAMERA MODULE 5MP",
        "IMAGE SENSOR CAMERA",
    ],

    "VIS": [
        "VIS M3X10 INOX",
        "SCREW M4X20",
        "VIS CHC M5X16",
    ],
    "ECROU": [
        "ECROU M3 INOX",
        "NUT M4",
        "ECROU FREIN M5",
    ],
    "ROND": [
        "RONDELLE M3",
        "WASHER M4 INOX",
        "RONDELLE EVENTAIL M5",
    ],
    "ENTRETOISE": [
        "ENTRETOISE M3 10MM",
        "STANDOFF M3 15MM",
        "ENTRETOISE HEXAGONALE M4",
    ],

    "CARTE_MEM": [
        "CARTE MEMOIRE MICRO SD 32GB",
        "SD CARD 64GB",
        "MICROSD INDUSTRIELLE 16GB",
    ],
    "DISQUE_DUR": [
        "SSD SATA 500GB",
        "DISQUE DUR 1TB",
        "SSD NVME 1TB",
    ],
    "PC": [
        "PC INDUSTRIEL FANLESS",
        "ORDINATEUR INDUSTRIEL EMBARQUE",
        "MINI PC 16GB RAM",
    ],
    "MONITEUR_PC": [
        "MONITEUR PC 24 POUCES",
        "ECRAN HDMI 22 POUCES",
        "DISPLAY PC FULL HD",
    ],

    "CARTE_PC": [
        "CARTE ELECTRONIQUE ASSEMBLEE",
        "PCBA CONTROLEUR MOTEUR",
        "CARTE PCB EQUIPEE",
    ],
    "MODULE": [
        "MODULE ELECTRONIQUE ASSEMBLE",
        "MODULE BLUETOOTH COMPLET",
        "MODULE WIFI PCB",
    ],

    "CAPTEUR_TEMP": [
        "CAPTEUR TEMPERATURE PT100",
        "SONDE TEMP PT1000",
        "TEMPERATURE SENSOR 10K NTC ASSEMBLY",
    ],
    "CAPTEUR_COURANT": [
        "CAPTEUR COURANT HALL 20A",
        "CURRENT SENSOR 50A",
        "SONDE COURANT 100A",
    ],
    "CAPTEUR_PROXIMITE": [
        "CAPTEUR PROXIMITE INDUCTIF",
        "PROXIMITY SENSOR 10MM",
        "DETECTEUR PROXIMITE 24V",
    ],
}


    
    
# ============================================================
# 2. Augmentation légère
# ============================================================

PACKAGES = [
    "", " SMD", " CMS", " 0603", " 0805", " 1206",
    " SOT23", " SOIC8", " THT", " ROHS"
]

PREFIXES = [
    "", "COMP ", "PART ", "ELEC ", "REF "
]


def augment(text):
    """
    Génère une variation raisonnable d'une désignation.
    Le but n'est pas de transformer totalement le texte.
    """
    result = text.upper()

    # Suppression aléatoire de ponctuation
    if random.random() < 0.35:
        result = re.sub(r"[-_/]", " ", result)

    # Espaces multiples
    result = re.sub(r"\s+", " ", result).strip()

    # Ajout éventuel d'un préfixe ou boîtier
    if random.random() < 0.25:
        result = random.choice(PREFIXES) + result

    if random.random() < 0.30:
        result += random.choice(PACKAGES)

    # Suppression occasionnelle d'un token non essentiel
    tokens = result.split()

    if len(tokens) >= 4 and random.random() < 0.20:
        index = random.randrange(1, len(tokens))
        tokens.pop(index)

    return " ".join(tokens)


# ============================================================
# 3. Construction du dataset
# ============================================================

random.seed(42)

X = []
y = []

EXAMPLES_PER_SEED = 40

with open(Path("C:/Users/alexis.auger/Documents/GitHub/Ollama/digikey_leaves_167.json"),newline='',encoding='utf-8') as fichier:
    lecteur = json.load(fichier)
    for index,ligne in enumerate(lecteur): 
        if index != 0 :
            ligne_info= ligne["valeur"]
        # for label, descriptions in SEEDS.items():
            label = ligne["label"]
            description = ligne_info
            # Toujours conserver l'original
            X.append(description.upper())
            y.append(label)

            # Variantes
            for _ in range(EXAMPLES_PER_SEED - 1):
                X.append(augment(description))
                y.append(label)


print(f"Nombre total d'exemples : {len(X)}")
print(f"Nombre de labels : {len(set(y))}")

print("\nRépartition :")
for label, count in sorted(Counter(y).items()):
    print(f"{label:25} {count}")


# ============================================================
# 4. Train / Test
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ============================================================
# 5. Modèle TF-IDF + LinearSVC
# ============================================================

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 6),
            lowercase=True,
            min_df=1,
            sublinear_tf=True,
        )
    ),
    (
        # "classifier",
        # LinearSVC(
        #     C=2.0,
        #     class_weight="balanced"
        # )
        "classifier",
        KNeighborsClassifier(
            n_neighbors=len(set(y))
        )
    )
])


# ============================================================
# 6. Entraînement
# ============================================================

model.fit(X_train, y_train)


# ============================================================
# 7. Évaluation
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n==============================")
print(f"ACCURACY : {accuracy:.2%}")
print("==============================\n")

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ============================================================
# 8. Tests manuels
# ============================================================

tests = [
    "RES SMD 100K OHM 1% 1/10W",
    "CAP CER 100NF 50V X7R 0603",
    "BSS138LT1G 50V 200MA SOT23",
    "STM32F405RGT6 LQFP64",
    "BAT54C SCHOTTKY SOT23",
    "PC817 DIP4",
    "CR2032 3V LITHIUM",
    "MOSFET N CHANNEL 60V",
    "RJ45 PATCH CABLE CAT6 5M",
    "VIS CHC M3X12 INOX",
]

results = model.predict(tests)

print("\nTESTS :")

for description, label in zip(tests, results):
    print(f"{description:45} -> {label}")


# ============================================================
# 9. Sauvegarde
# ============================================================

import joblib

joblib.dump(model, "component_classifier.joblib")

print("\nModèle sauvegardé : component_classifier.joblib")