DICTIONNAIRE = {'RESISTIFS': {'REST': ['TECHNO', 'BOITIER', 'STABILITE', None, 'VALEUR', 'PUISSANCE', 'TOLERANCE', 'COURANT ou TENSION', 'T°C FONCT', None], 'POT': ['TECHNO', None, 'STABILITE', None, 'VALEUR', 'PUISSANCE', 'TOLERANCE', None, 'T°C FONCT', None], 'VARISTANCE': ['TECHNO', 'BOITIER', None, None, 'TENSION AC', 'ENERGIE', None, None, 'T°C FONCT', None], 'RES_DE_REST': ['TECHNO', 'BOITIER', 'STABILITE', None, 'VALEUR', 'PUISSANCE', 'TOLERANCE', None, 'T°C FONCT', None], 'THERMISTANCE': ['TYPE', 'TECHNO', 'BOITIER/PTS/FILS', 'LIBRE', 'VALEUR', 'T°Cmin/T°Cmax', 'TOLERANCE', 'VALEUR BETA', None, None], 'LIMITEUR_COURANT': ['TECHNO', None, None, None, 'COURANT MAX', 'TENSION MAX', 'RESISTANCE', 'TOLERANCE', 'T°C FONCT', None]}, 'CAPACITIFS': {'COND_ALUM': ['TECHNO', 'SENS', 'DIAMETRE', None, 'CAPACITE', 'TENSION', 'TOLERANCE', 'ESR', 'T°C FONCT', None], 'COND_TANT': ['TECHNO', 'BOITIER', None, None, 'CAPACITE', 'TENSION', 'TOLERANCE', 'ESR', 'T°C FONCT', None], 'COND_CERAM': ['TECHNO', 'BOITIER', 'DIELECTRIQUE', None, 'CAPACITE', 'TENSION', 'TOLERANCE', None, 'T°C FONCT', None], 'COND_AJUSTABLE': ['TECHNO', 'SENS', None, None, 'CAPACITE min/max', 'TENSION', None, None, 'T°C FONCT', None], 'COND_PLAST': ['TECHNO', 'SENS', 'MATERIAU', None, 'CAPACITE', 'TENSION', 'TOLERANCE', None, 'T°C FONCT', None], 'COND_SILIC': ['TECHNO', 'BOITIER', None, None, 'CAPACITE', 'TENSION', 'TOLERANCE', None, 'T°C FONCT', None], 'COND_EDLC': ['TECHNO', 'SENS', 'DIAMETRE', None, 'CAPACITE', 'TENSION', 'TOLERANCE', 'ESR', 'T°C FONCT', None], 'COND_FILTRE': ['TECHNO', 'BOITIER', 'DIELECTRIQUE', None, 'CAPACITE', 'TENSION', 'TOLERANCE', 'COURANT', 'T°C FONCT', None]}, 'DIODES': {'DIODE_DE_REDRESS': ['TECHNO', 'BOITIER', None, None, 'TENSION VRRM', 'COURANT IF', None, None, 'T°C FONCT', 'T°C STOCK'], 'DIODE_ZENER': ['TECHNO', 'BOITIER', None, None, 'TENSION VZ', 'PUISSANCE', None, None, 'T°C FONCT', 'T°C STOCK'], 'DIODE_DE_SIGNAL': ['TECHNO', 'BOITIER', None, None, 'TENSION VRRM', 'COURANT IF', None, 'TYPE', 'T°C FONCT', 'T°C STOCK'], 'DIODE_SCHOTTKY': ['TECHNO', 'BOITIER', None, None, 'TENSION VRRM', 'COURANT IF', None, 'TYPE', 'T°C FONCT', 'T°C STOCK'], 'DIODE_VARICAP': ['TECHNO', 'BOITIER', None, None, 'TENSION VR', 'CAPACITE CDmax', None, 'TYPE', 'T°C FONCT', 'T°C STOCK'], 'DIAC': ['TECHNO', 'BOITIER', None, None, 'TENSION VBO', 'COURANT', None, None, 'T°C FONCT', 'T°C STOCK'], 'DIODE_TRANSIL': ['TECHNO', 'BOITIER', None, 'SENS', 'TENSION VR', 'PUISSANCE', None, None, 'T°C FONCT', 'T°C STOCK'], 'PONT_DE_DIODE': ['TECHNO', 'BOITIER', None, None, 'TENSION CRETE', 'COURANT', None, 'TYPE', 'T°C FONCT', 'T°C STOCK'], 'DIODE_ESD': ['TECHNO', 'BOITIER', None, 'SENS', 'TENSION ESD', 'PUISSANCE', 'TENSION rwm', 'TYPE', 'T°C FONCT', 'T°C STOCK']}, 'INDUCTIFS': {'TRANSFO_ISOLEMENT': ['TECHNO', 'BOITIER', None, 'PUISSANCE', 'Uprim/Usec/Iac', 'INDUCTANCE', 'RATIO', 'ISOLATION Prim/sec', 'T°C FONCT', 'T°C STOCK'], 'TRANSFO_DE_COURANT': ['TECHNO', 'BOITIER', None, None, 'I SENSE', 'INDUCTANCE', None, 'ISOLATION Prim/sec', 'T°C FONCT', 'T°C STOCK'], 'TRANSFO_IMPULSION': ['TECHNO', 'BOITIER', None, None, 'CONST Et', 'INDUCTANCE', 'RATIO', 'ISOLATION Prim/sec', 'T°C FONCT', 'T°C STOCK'], 'TRANSFO_ETHERNET': ['TECHNO', 'BOITIER', None, None, 'VITESSE', 'INDUCTANCE RX/TX', 'RATIO TX/RX', 'PORT', 'T°C FONCT', 'T°C STOCK'], 'SELF': ['TECHNO', 'BOITIER', None, None, 'INDUCTANCE', 'TOLERANCE', 'COURANT Isat', 'LIBRE', 'T°C FONCT', 'T°C STOCK'], 'SELF_MODE_COMMUN': ['TECHNO', 'BOITIER', None, None, 'VALEUR', 'TOLERANCE', 'COURANT', 'TENSION', 'T°C FONCT', 'T°C STOCK'], 'FERRITES': ['TECHNO', 'BOITIER', None, None, 'IMPED', 'FREQ', 'COURANT', None, 'T°C FONCT', 'T°C STOCK'], 'NOYAU_FERRITE': ['TECHNO', 'DIMENSIONS', None, None, 'MATERIAU', 'PERMEABILITE', 'IMPED', 'FREQ', 'T°C FONCT', 'T°C STOCK'], 'FILTRE': ['TECHNO', 'BOITIER', 'TYPE', None, 'TENSION', 'COURANT', 'FREQUENCE', 'LIBRE', 'T°C FONCT', 'T°C STOCK'], 'HAUT_PARLEUR': ['TECHNO', 'DIMENSIONS EXT', None, None, 'IMPEDANCE', 'PUISSANCE', None, None, 'T°C FONCT', 'T°C STOCK'], 'ANTENNE': ['TECHNO', 'DIMENSIONS EXT', None, None, 'FREQUENCE', None, None, None, 'T°C FONCT', None], 'ELECTROAIMANT': ['TYPE', None, None, None, 'TENSION', 'PUISSANCE', 'FORCE', None, 'T°C FONCT', 'T°C STOCK'], 'BALUN': ['TECHNO', 'BOITIER', None, None, 'IMPEDANCE', 'FREQmin/max', 'PERTE', None, 'T°C FONCT', 'T°C STOCK'], 'TRANSFO_TORIQUE': ['TECHNO', 'BOITIER', None, 'PUISSANCE', 'Uprim/Usec/Iac', None, None, None, 'T°C FONCT', 'T°C STOCK']}, 'ALIMENTATIONS': {'ALIM': ['TYPE', 'TECHNO', None, 'PUISSANCE', 'Vin', 'Vout', 'COURANT', 'RENDEMENT', 'T°C FONCT', 'T°C STOCK'], 'CHARGEUR': ['CHIMIE', None, None, 'PUISSANCE', 'Vin', None, 'COURANT', None, 'T°C FONCT', 'T°C STOCK'], 'BATTERIE': ['CHIMIE', 'DIMENSIONS', None, None, 'TENSION', 'CAPACITE', None, None, 'T°C FONCT', 'T°C STOCK']}, 'CIRCUITS_INTEGRES': {'CI_AOP_COMPAR': ['TECHNO', 'BOITIER', None, None, 'CONFIG', 'TYPE', 'ALIMENTATION', 'DIVERS', 'T°C FONCT', 'T°C STOCK'], 'CI_REGUL': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION IN', 'TENSION / COURANT OUT', 'DIVERS', 'T°C FONCT', 'T°C STOCK'], 'CI_LOGIQUE': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'ALIMENTATION', 'LIBRE', 'LIBRE', 'T°C FONCT', 'T°C STOCK'], 'CI_MEMOIRE': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'ALIMENTATION', 'CAPACITE', 'INTERFACE', 'T°C FONCT', 'T°C STOCK'], 'CI_PROC': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'ALIMENTATION', 'FREQUENCE / DONNEES', 'CAPACITE', 'T°C FONCT', 'T°C STOCK'], 'CI_CONVERT': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'ALIMENTATION', 'RESOLUTION / VOIES', 'INTERFACE', 'T°C FONCT', 'T°C STOCK'], 'CI_DRIVER': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'ALIMENTATION', 'LIBRE', 'LIBRE', 'T°C FONCT', 'T°C STOCK'], 'CI_REF_DE_TENSION': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION Vref', 'PRECISION', None, 'T°C FONCT', 'T°C STOCK'], 'CI_SUPERV_TENSION': ['TECHNO', 'BOITIER', None, None, None, 'ALIMENTATION', 'TENSION Vth', None, 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_TEMP': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', 'PLAGE T°C', 'PRECISION', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_PRESSION': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', 'PLAGE MESURE', 'PRECISION', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_ACCEL': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', 'PLAGE MESURE', 'NBRE AXES', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_COURANT': ['TECHNO', 'BOITIER', None, None, 'FREQUENCE', 'ALIMENTATION', 'PLAGE MESURE', 'PRECISION', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_MAG': ['TECHNO', 'BOITIER', None, None, None, 'ALIMENTATION', 'COURANT SORTIE', 'CHAMP', 'T°C FONCT', 'T°C STOCK'], 'CI_SWITCH_PUISS': ['TECHNO', 'BOITIER', None, None, 'LIBRE', 'TENSION ENTREE', 'COURANT LIMITE max', 'NBRE SORTIES', 'T°C FONCT', 'T°C STOCK'], 'CI_SWITCH_RF': ['TECHNO', 'BOITIER', None, None, None, 'ALIMENTATION', 'PLAGE FREQ', 'NBRE ENTREES', 'T°C FONCT', 'T°C STOCK'], 'CI_MODULE': ['TECHNO', 'BOITIER', 'TYPE', None, 'INTERFACE', 'ALIMENTATION', 'PUISS TX/RX', None, 'T°C FONCT', 'T°C STOCK'], 'CI_CHARGEUR': ['TECHNO', 'BOITIER', 'TYPE BATTERIE', None, 'TYPE', 'TENSION IN', 'TENSION/COURANT CHARGE', 'NB CELLULES', 'T°C FONCT', 'T°C STOCK'], 'CI_RTC': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', None, None, 'T°C FONCT', 'T°C STOCK'], 'CI_RFID': ['TECHNO', 'BOITIER', None, None, None, 'ALIMENTATION', 'FREQUENCE', 'MÉMOIRE', 'T°C FONCT', 'T°C STOCK'], 'CI_POMPE_CHARGE': ['TECHNO', 'BOITIER', None, None, None, 'TENSION IN', 'TENSION/COURANT OUT', None, 'T°C FONCT', 'T°C STOCK'], 'CI_JAUGE': ['TECHNO', 'BOITIER', None, None, 'TYPE BATT', 'ALIMENTATION', 'INTERFACE', None, 'T°C FONCT', 'T°C STOCK'], 'CI_SWITCH': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION ENTREE', None, 'CONFIG', 'T°C FONCT', 'T°C STOCK'], 'CI_SUPERV_WATCHDOG': ['TECHNO', 'BOITIER', None, None, 'NOMBRE VOIES', 'ALIMENTATION', 'ETAT', 'SORTIE', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_HUMID': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', 'PLAGE HUMIDITE', 'PRECISION', 'T°C FONCT', 'T°C STOCK'], 'CI_CAPTEUR_AUDIO': ['TECHNO', 'BOITIER', None, None, 'INTERFACE', 'ALIMENTATION', 'PLAGE FREQ', 'SENSIBILITE', 'T°C FONCT', 'T°C STOCK']}, 'PIEZO': {'OSCIL': ['TECHNO', 'BOITIER', None, None, 'FREQUENCE', 'ALIMENTATION', 'STABILITE', None, 'T°C FONCT', 'T°C STOCK'], 'RESON': ['TECHNO', 'BOITIER', None, None, 'FREQUENCE', None, 'PRECISION', None, 'T°C FONCT', 'T°C STOCK'], 'QUARTZ': ['TECHNO', 'BOITIER', None, None, 'FREQUENCE', None, 'STABILITE', 'CAPACITANCE', 'T°C FONCT', 'T°C STOCK'], 'BUZZER': ['TECHNO', 'DIMENSIONS', None, None, 'TYPE', 'FREQUENCE', 'ALIMENTATION', 'NIVEAU', 'T°C FONCT', 'T°C STOCK']}, 'COMMUTATION': {'BOUTON_POUSSOIR': ['TECHNO', 'NB POINTS', None, None, 'CONFIGURATION', 'ORIENTATION', 'TENSION/COURANT', 'DIVERS', 'T°C FONCT', None], 'INTERRUPTEUR': ['TYPE', 'TECHNO', None, None, 'CONFIGURATION', 'ORIENTATION', 'TENSION/COURANT', 'DIVERS', 'T°C FONCT', 'T°C STOCK'], 'CLAVIER': ['DIMENSIONS', 'NB TOUCHES', None, None, None, 'TENSION', 'COURANT', None, 'T°C FONCT', None], 'RELAIS': ['TYPE', 'TECHNO', None, None, 'CONFIGURATION', 'TENSION BOBINE ou VF', 'TENSION/COURANT', None, 'T°C FONCT', None], 'DISJONCTEUR': ['TYPE', None, None, None, 'POLES', 'COURANT', 'TENSION', None, 'T°C FONCT', None], 'FUSIBLE': ['TYPE', 'TECHNO', 'BOITIER', None, None, 'COURANT', 'TENSION', 'ACTION', 'T°C FONCT', None], 'PROTECTION': ['TECHNO', None, 'TYPE', None, 'TENSION', 'COURANT', None, None, 'T°C FONCT', None], 'CONTACTEUR': [None, 'MONTAGE', 'POLES', None, 'CONFIGURATION', 'COURANT', 'TENSION', None, 'T°C FONCT', None]}, 'TRANSISTORS': {'TRANSISTOR_BIP': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION VCE', 'COURANT IC', None, 'T°C FONCT', 'T°C STOCK'], 'TRANSISTOR_MOS': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION VDS', 'COURANT ID', None, 'T°C FONCT', 'T°C STOCK'], 'TRANSISTOR_IGBT': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION VCE', 'COURANT IC', None, 'T°C FONCT', 'T°C STOCK'], 'TRIAC': ['TECHNO', 'BOITIER', None, None, 'TENSION VDRM', 'COURANT IT', 'COURANT IGT', None, 'T°C FONCT', 'T°C STOCK'], 'THYRISTOR': ['TECHNO', 'BOITIER', None, None, 'TENSION VDRM', 'COURANT IT', 'COURANT IGT', None, 'T°C FONCT', 'T°C STOCK'], 'TRANSISTOR_DARLING': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'TENSION VCE', 'COURANT IC', 'CONFIG', 'T°C FONCT', 'T°C STOCK']}, 'CONNECTIQUE': {'COSSE': ['CONTACT', 'TYPE', 'TAILLE', 'GENRE', 'COULEUR', 'JAUGE', 'ISOLATION', 'ORIENTATION', 'T°C FONCT', None], 'CONTACT': ['CONTACT', 'TYPE', None, 'GENRE', 'FINITION', 'JAUGE', 'SERIE CONNECTEUR', None, 'T°C FONCT', None], 'EMBOUT': ['CONTACT', None, 'TAILLE', 'GENRE', 'COULEUR', 'JAUGE', 'ISOLATION', None, 'T°C FONCT', None], 'FICHE_BANANE': ['CONTACT', None, 'DIAMETRE', 'GENRE', 'COULEUR', None, None, None, 'T°C FONCT', None], 'PLOT': ['CONTACT', 'TYPE', 'DIAMETRE', 'GENRE', 'COULEUR', 'MATIERE', 'FINITION', None, 'T°C FONCT', None], 'PORTE_FUSIBLE': [None, 'CONTACTS', 'TECHNO', None, 'BOITIER', 'TENSION', 'PUISSANCE', 'COURANT', 'T°C FONCT', None], 'CONNECT': ['TYPE/FAMILLE', 'CONTACTS', 'TECHNO', 'NB CONTACTS', 'TYPE', 'FORME', 'GENRE', 'ORIENTATION', 'T°C FONCT', None], 'CONNECT_COAX': ['TYPE', 'CONTACTS', 'TECHNO', 'NB CONTACTS', 'TYPE', 'IMPEDANCE', 'GENRE', 'ORIENTATION', 'T°C FONCT', None], 'CONNECT_VIDE': ['TYPE/SERIE', None, 'TECHNO', 'NB CONTACTS', 'TYPE', 'FORME', 'GENRE', 'TERMINAISON', 'T°C FONCT', None], 'SUPPORT': ['TYPE', 'CONTACTS', 'TECHNO', 'BOITIER / DIMENSIONS', 'NB ELEMENTS', 'MATIERE', None, None, 'T°C FONCT', None], 'BARRETTE': [None, 'GENRE', 'TECHNO', 'NB CONTACTS', 'OPTION', 'ORIENTATION', 'FINITION', 'PAS', 'T°C FONCT', None], 'BORNIER': ['TYPE', None, 'TECHNO', 'NB CONTACTS', 'TYPE', None, 'JAUGE', 'PAS', 'T°C FONCT', None], 'BORNE_A_VIS': ['CONTACTS', None, 'TECHNO', 'NB CONTACTS', 'GENRE', 'DIAMETRE VIS', 'ORIENTATION', None, 'T°C FONCT', None], 'CAPOT': ['TYPE', None, None, 'NB CONTACTS / DIMENSIONS', 'MATIERE', 'COULEUR', 'ORIENTATION', None, 'T°C FONCT', None], 'MODULE_SECTEUR': [None, 'CONTACTS', 'TECHNO', None, 'COURANT', 'INTERRUPTEUR', 'FILTRE', 'FUSIBLE', 'T°C FONCT', None], 'BORNE_BLIND': [None, None, 'TECHNO', 'NB CONTACTS', 'TYPE', 'DIMENSIONS CABLE', None, None, 'T°C FONCT', None], 'POINTE_TEST': [None, None, 'TECHNO', 'DIAMETRE POINTE', None, 'COURANT', 'DIVERS', None, 'T°C FONCT', None], 'EMBASE_BANANE': ['CONTACT', None, 'DIAMETRE', 'GENRE', 'COULEUR', None, None, None, 'T°C FONCT', None]}, 'MECANIQUE': {'PIECE_SUR_PLAN': ['DESIGNATION', None, None, None, 'N° PLAN', None, None, None, None, None], 'BOITIER': ['MATIERE', 'DIMENSIONS EXT', None, None, None, 'COULEUR', None, None, 'T°C FONCT', None], 'CHASSIS': ['MATIERE', 'DIMENSIONS EXT', None, None, None, 'COULEUR', None, None, 'T°C FONCT', None], 'VALISE': ['MATIERE', 'DIMENSIONS EXT', None, None, None, 'COULEUR', None, None, 'T°C FONCT', None], 'DISSIPATEUR': ['DIMENSIONS EXT', 'BOITIER', None, None, 'RES. THERM', None, None, None, None, None], 'VENTILATEUR': ['DIMENSIONS EXT', None, None, None, 'ALIMENTATION', 'BRUIT', None, None, 'T°C FONCT', None], 'MOTEUR': ['TYPE', None, None, None, 'ALIMENTATION', 'PUISSANCE', 'COURANT', None, 'T°C FONCT', 'T°C STOCK'], 'JOINT': ['TYPE', 'FORME', 'DIMENSIONS', None, 'MATIERE', 'ENVELOPPE/QUALITE', 'SHORE', 'COULEUR', 'TENUE EN T°', 'LIBRE'], 'PAD_THERM': ['DIMENSIONS/BOITIER', None, None, None, 'CONDUC. THERM', 'MATERIAU', None, None, 'TENUE EN T°', None], 'RESSORT': ['TYPE', 'DIM ou BOITIER', None, None, 'MATIERE', 'RAIDEUR/FORCE', None, None, None, None], 'PALIER': ['TYPE', 'DIMENSIONS', None, None, 'MATIERE', 'COULEUR', None, None, None, None], 'RES_CHAUFF': ['DIMENSIONS', None, None, None, 'PUISSANCE', 'ALIMENTATION', None, None, None, None], 'PASTILLE': [None, None, 'DIMENSIONS PASTILLE', None, 'LIBRE', None, None, None, None, None], 'BLINDAGE': ['TYPE', 'DIMENSIONS EXT', 'TECHNO', None, 'VENTILATION (capots)', None, None, None, 'T°C FONCT', 'T°C STOCK'], 'POINT_TEST': [None, 'DIAM TROU / CMS', 'DIMENSIONS PASTILLE', None, 'LIBRE', None, None, None, None, None], 'TESTA_PCB': ['TYPE', 'DIAM TROU / CMS', 'DIMENSIONS PASTILLE', None, 'LIBRE', None, None, None, None, None], 'TROU_FIX': ['TYPE', 'DIMENSIONS TROU', 'DIMENSIONS PASTILLE', None, 'FORMAT', None, None, None, None, None], 'ENS_THERM': ['DIMENSIONS EXT', None, None, None, 'TRANSFERT CHALEUR', 'PUISSANCE', 'TENSION MAX', 'COURANT NOM', 'T°C FONCT', None]}, 'PILES': {'PILE': ['CHIMIE', 'FORMAT', None, None, 'TENSION', 'CAPACITE', None, None, 'T°C FONCT', 'T°C STOCK'], 'BATTERIE': ['CHIMIE', 'FORMAT', None, None, 'TENSION', 'CAPACITE', None, None, 'T°C FONCT', 'T°C STOCK']}, 'CABLE_ET_FILAIRE': {'FIL': ['CONFIG BRIN', 'JAUGE/SECTION', None, 'COULEUR', 'MATIERE', 'TYPE', 'TENSION', None, 'T°C FONCT', None], 'CABLE_PLAT': [None, 'JAUGE', 'DIVERS', 'COULEUR', 'MATIERE', 'PAS', None, None, 'T°C FONCT', None], 'NAPPE_EQUIPEE': ['LONGUEUR', 'JAUGE', 'DIVERS', 'COULEUR', 'MATIERE', 'PAS', 'CONNECT A/B', 'GENRE', 'T°C FONCT', None], 'CABLE': ['TYPE', 'JAUGE', 'IMPEDANCE', 'COULEUR', 'MATIERE', 'COULEUR FIL', 'TENSION', 'DIVERS', 'T°C FONCT', None], 'CABLE_ETHERNET': [None, 'JAUGE', None, 'COULEUR', 'MATIERE', 'CATEGORIE', 'BLINDAGE', 'NB PAIRES', 'T°C FONCT', None], 'CORDON': ['TYPE', None, 'LONGUEUR', 'COULEUR', 'MATIERE', 'CONNECT A/B', 'TENSION', 'GENRE', 'T°C FONCT', None], 'GAINE': ['TYPE', None, 'DIAMETRE ou LARGEUR', 'COULEUR', 'MATIERE', 'RATIO', None, None, 'T°C FONCT', None], 'TRESSE': ['TYPE', None, 'LONGUEUR', 'COULEUR', None, None, None, None, 'T°C FONCT', None], 'MANCHON': ['TYPE', None, 'DIAMETRE', 'COULEUR', 'MATIERE', 'RATIO', None, None, 'T°C FONCT', None], 'COLLIER': [None, None, 'DIMENSIONS', 'COULEUR', 'MATIERE', None, None, None, 'T°C FONCT', None], 'GOULOTTE': [None, None, 'DIMENSIONS', 'COULEUR', 'MATIERE', None, None, None, 'T°C FONCT', None], 'EMBASE_COLLIER': [None, 'FIXATION', None, 'COULEUR', 'MATIERE', None, None, None, 'T°C FONCT', None], 'PRESSE_ETOUPE': [None, None, 'DIAMETRE', 'COULEUR', 'MATIERE', 'INDICE IP', None, None, 'T°C FONCT', None]}, 'OPTOELECTRONIQUE': {'DIODE_LED': ['COULEUR', None, 'TECHNO', 'BOITIER', 'L.ONDE', 'PUISS. OPTIQUE', 'TENSION VF', 'COURANT TEST', 'T°C FONCT', 'T°C STOCK'], 'OPTOCOUPLEUR': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'CONFIG', 'ISOLATION', None, 'T°C FONCT', 'T°C STOCK'], 'PHOTODIODE': ['TECHNO', 'BOITIER', None, None, 'TYPE', 'L.ONDE', None, None, 'T°C FONCT', 'T°C STOCK'], 'PHOTOTRANSISTOR': ['TECHNO', 'BOITIER', None, None, None, 'L.ONDE', None, None, 'T°C FONCT', 'T°C STOCK'], 'AFFICHEUR': ['TYPE', None, 'TECHNO', 'DIMENSIONS', 'TYPE ECRAN', 'RESOLUTION', 'COULEUR', 'ALIMENTATION', 'T°C FONCT', 'T°C STOCK'], 'VOYANT': ['TYPE', 'COULEUR', 'TECHNO', 'DIMENSIONS', 'ALIMENTATION', None, None, None, 'T°C FONCT', 'T°C STOCK'], 'LAMPE': ['TYPE', None, None, 'DIMENSIONS', 'ALIMENTATION', 'PUISSANCE', None, None, 'T°C FONCT', 'T°C STOCK'], 'SPECTROMETRE': ['TECHNO', 'BOITIER', None, None, 'P.SPECTRALE', 'RESOLUTION', 'ALIMENTATION', 'INTERFACE', 'T°C FONCT', 'T°C STOCK'], 'GUIDE_LUMIERE': ['TECHNO', 'FORME', None, None, 'DIMENSIONS', 'NB TUBE', 'COULEUR', 'MATIERE', 'T°C FONCT', None], 'DRIVER_FIBRE_OPT': ['TECHNO', 'BOITIER', 'CONNECTEUR', None, 'ALIMENTATION', 'DEBIT', 'SENS', 'LONGUEUR ONDE', 'T°C FONCT', 'T°C STOCK'], 'FIBRE_OPTIQUE': ['MATIERE CŒUR', None, 'LONGUEUR', None, None, 'CONNECT A/B', 'DIAMETRE CŒUR', None, 'T°C FONCT', None], 'CAPTEUR_OPTO': ['TECHNO', 'BOITIER', 'TYPE', None, 'ALIMENTATION', 'SORTIE', 'LIBRE', None, 'T°C FONCT', 'T°C STOCK'], 'FILTRE_OPTIQUE': ['TYPE', None, None, None, 'DIMENSIONS', 'L.ONDE', 'FWHM', 'P.SPECTRALE', 'T°C FONCT', None], 'CAMERA': [None, 'TYPE', None, None, 'RESOLUTION', 'INTERFACE', 'ALIMENTATION', None, 'T°C FONCT', 'T°C STOCK'], 'FENETRE': ['MATIERE', None, None, None, 'DIMENSIONS', 'EPAISSEUR', 'TRAITEMENT', 'LONG. ONDE', 'T°C FONCT', None], 'LENTILLE': ['TYPE', 'MATIERE', None, None, 'DIMENSIONS', 'DIST. FOCALE', 'TRAITEMENT', 'LONG. ONDE', 'T°C FONCT', None]}, 'VISSERIE': {'VIS': ['TYPE', 'FORME TETE', 'FILETAGE', 'DIMENSIONS', 'MATIERE', 'FINITION', None, None, None, None], 'ECROU': ['FORME', 'DIAMETRE', None, None, 'MATIERE', 'FINITION', None, None, None, None], 'ROND': ['FORME', 'TYPE', 'DIAMETRE', None, 'MATIERE', 'FINITION', None, None, None, None], 'ENTRETOISE': ['FORME/LARGEUR', 'GENRE', 'FILETAGE/D INT', 'LONGUEUR', 'MATIERE', 'FINITION', 'DIVERS', None, None, None], 'GOUJON': ['FORME', None, 'FILETAGE/D INT', 'LONGUEUR', 'MATIERE', 'FINITION', None, None, None, None], 'PLOT_ANTIVIB': [None, 'GENRE', 'FILETAGE/D INT', 'LONGUEUR', 'MATIERE', None, None, None, 'T°C FONCT', None], 'CLAVETTE': ['FORME', 'DIMENSIONS', 'TYPE', None, 'MATIERE', 'FINITION', 'LIBRE', None, None, None]}, 'ETIQUETTE': {'ETIQU': ['DESIGNATION', None, None, None, 'DIMENSIONS', 'MATIERE', 'COULEUR', None, None, None]}, 'INFORMATIQUE': {'CARTE_MEM': ['FORMAT', 'TYPE', None, None, 'CAPACITE', 'CLASSE/VITESSE', None, None, 'T°C FONCT', 'T°C STOCK'], 'DISQUE_DUR': ['FORMAT', 'INTERFACE', None, None, 'CAPACITE', 'VITESSE', None, None, 'T°C FONCT', 'T°C STOCK'], 'PC': ['TYPE', None, None, None, 'TYPE_PROC', 'FREQ_PROC', 'RAM/DD', 'OS', 'T°C FONCT', 'T°C STOCK'], 'MONITEUR_PC': ['TAILLE', 'TYPE', None, None, 'RESOLUTION', 'COULEUR', None, None, 'T°C FONCT', 'T°C STOCK'], 'CLAVIER_PC': ['INTERFACE', None, None, None, 'LIBRE', None, None, None, 'T°C FONCT', 'T°C STOCK'], 'SOURIS_PC': ['INTERFACE', None, None, None, 'LIBRE', None, None, None, 'T°C FONCT', 'T°C STOCK'], 'SONDE': ['TYPE', 'INTERFACE PROG', None, None, 'INTERFACE 1', 'INTERFACE 2', None, None, 'T°C FONCT', 'T°C STOCK']}, 'CARTES_EQUIPEES': {'CARTE_PC': ['FORMAT/INTERFACE', None, None, None, 'LIBRE', None, None, None, 'T°C FONCT', 'T°C STOCK'], 'MODULE': ['FONCTION PRINCIPALE', None, None, None, 'LIBRE', None, None, None, 'T°C FONCT', 'T°C STOCK']}, 'CAPTEURS': {'CAPTEUR_TEMP': [None, 'CATEGORIE', None, None, 'TYPE', 'INTERFACE', 'PLAGE T°C', 'PRECISION', None, None], 'CAPTEUR_COURANT': [None, None, None, None, 'FREQUENCE', 'ALIMENTATION', 'PLAGE MESURE', 'PRECISION', 'T°C FONCT', 'T°C STOCK'], 'CAPTEUR_PROXIMITE': [None, 'TYPE', None, None, 'FREQUENCE', 'ALIMENTATION', 'SORTIE', None, 'T°C FONCT', 'T°C STOCK']}}

CATEGORIES = {
    "RESISTIFS": "Composants résistifs",
    "CAPACITIFS": "Composants capacitifs",
    "DIODES": "Diodes électroniques",
    "INDUCTIFS": "Composants inductifs",
    "ALIMENTATIONS": "Sources alimentation",
    "CIRCUITS_INTEGRES": "Circuits intégrés",
    "PIEZO": "Composants piézoélectriques",
    "COMMUTATION": "Composants commutation",
    "TRANSISTORS": "Transistors électroniques",
    "CONNECTIQUE": "Connecteurs électriques",
    "MECANIQUE": "Composants mécaniques",
    "PILES": "Piles batteries",
    "CABLE_ET_FILAIRE": "Câbles fils",
    "OPTOELECTRONIQUE": "Composants optoélectroniques",
    "VISSERIE": "Éléments fixation",
    "ETIQUETTE": "Étiquettes identification",
    "INFORMATIQUE": "Matériel informatique",
    "CARTES_EQUIPEES": "Cartes électroniques",
    "CAPTEURS": "Capteurs mesure"
    }

SUB_CATEGORIES = {
    "RESISTIFS": {
        "RES": "Résistance fixe",
        "POT": "Potentiomètre réglable",
        "VARISTANCE": "Protection surtension",
        "RES_DE_REST": "Résistance restitution",
        "THERMISTANCE": "Résistance thermique",
        "LIMITEUR_COURANT": "Limitation courant"
    },

    "CAPACITIFS": {
        "COND_ALUM": "Condensateur aluminium",
        "COND_TANT": "Condensateur tantale",
        "COND_CERAM": "Condensateur céramique",
        "COND_AJUSTABLE": "Condensateur ajustable",
        "COND_PLAST": "Condensateur plastique",
        "COND_SILIC": "Condensateur silicium",
        "COND_EDLC": "Supercondensateur EDLC",
        "COND_FILTRE": "Condensateur filtrage"
    },

    "DIODES": {
        "DIODE_DE_REDRESS": "Diode redressement",
        "DIODE_ZENER": "Diode Zener",
        "DIODE_DE_SIGNAL": "Diode signal",
        "DIODE_SCHOTTKY": "Diode Schottky",
        "DIODE_VARICAP": "Diode capacité variable",
        "DIAC": "Diode bidirectionnelle",
        "DIODE_TRANSIL": "Protection surtension",
        "PONT_DE_DIODE": "Pont redresseur",
        "DIODE_ESD": "Protection ESD"
    },

    "INDUCTIFS": {
        "TRANSFO_ISOLEMENT": "Transformateur isolement",
        "TRANSFO_DE_COURANT": "Transformateur courant",
        "TRANSFO_IMPULSION": "Transformateur impulsion",
        "TRANSFO_ETHERNET": "Transformateur Ethernet",
        "SELF": "Bobine inductive",
        "SELF_MODE_COMMUN": "Self mode commun",
        "FERRITES": "Ferrite antiparasite",
        "NOYAU_FERRITE": "Noyau magnétique",
        "FILTRE": "Filtre inductif",
        "HAUT_PARLEUR": "Haut-parleur",
        "ANTENNE": "Antenne radio",
        "ELECTROAIMANT": "Actionneur électromagnétique",
        "BALUN": "Adaptateur impédance"
    },

    "ALIMENTATIONS": {
        "ALIM": "Bloc alimentation",
        "CHARGEUR": "Chargeur électrique"
    },

    "CIRCUITS_INTEGRES": {
        "CI_AOP_COMPAR": "Amplificateur comparateur",
        "CI_REGUL": "Régulation tension",
        "CI_LOGIQUE": "Logique numérique",
        "CI_MEMOIRE": "Mémoire électronique",
        "CI_PROC": "Processeur numérique",
        "CI_CONVERT": "Conversion signaux",
        "CI_DRIVER": "Circuit commande",
        "CI_REF_DE_TENSION": "Référence tension",
        "CI_SUPERV_TENSION": "Supervision tension",
        "CI_CAPTEUR_TEMP": "Mesure température",
        "CI_CAPTEUR_PRESSION": "Mesure pression",
        "CI_CAPTEUR_ACCEL": "Mesure accélération",
        "CI_CAPTEUR_COURANT": "Mesure courant",
        "CI_CAPTEUR_MAG": "Mesure magnétique",
        "CI_SWITCH_PUISS": "Commutation puissance",
        "CI_SWITCH_RF": "Commutation radiofréquence",
        "CI_MODULE": "Module intégré",
        "CI_CHARGEUR": "Gestion charge",
        "CI_RTC": "Horloge temps réel",
        "CI_RFID": "Identification radiofréquence",
        "CI_POMPE_CHARGE": "Pompe charge",
        "CI_JAUGE": "Jauge batterie",
        "CI_SWITCH": "Commutateur analogique",
        "CI_SUPERV_WATCHDOG": "Surveillance système",
        "CI_CAPTEUR_HUMID": "Mesure humidité",
        "CI_CAPTEUR_AUDIO": "Acquisition audio"
    },

    "PIEZO": {
        "OSCIL": "Oscillateur électronique",
        "RESON": "Résonateur fréquence",
        "QUARTZ": "Cristal quartz",
        "BUZZER": "Avertisseur sonore"
    },

    "COMMUTATION": {
        "BOUTON_POUSSOIR": "Bouton momentané",
        "INTERRUPTEUR": "Interrupteur électrique",
        "CLAVIER": "Clavier commande",
        "RELAIS": "Relais électrique",
        "DISJONCTEUR": "Protection électrique",
        "FUSIBLE": "Protection surintensité",
        "PROTECTION": "Protection électrique",
        "CONTACTEUR": "Contacteur puissance"
    },

    "TRANSISTORS": {
        "TRANSISTOR_BIP": "Transistor bipolaire",
        "TRANSISTOR_MOS": "Transistor MOSFET",
        "TRANSISTOR_IGBT": "Transistor IGBT",
        "TRIAC": "Commutateur bidirectionnel",
        "THYRISTOR": "Commutateur contrôlé",
        "TRANSISTOR_DARLING": "Transistor Darlington"
    },

    "CONNECTIQUE": {
        "COSSE": "Cosse électrique",
        "CONTACT": "Contact électrique",
        "EMBOUT": "Embout câble",
        "FICHE_BANANE": "Fiche banane",
        "CAPOT": "Capot connecteur",
        "PORTE_FUSIBLE": "Support fusible",
        "CONNECT": "Connecteur générique",
        "CONNECT_COAX": "Connecteur coaxial",
        "CONNECT_VIDE": "Connecteur vide",
        "SUPPORT": "Support composant",
        "BARRETTE": "Barrette connexion",
        "BORNIER": "Bornier électrique",
        "BORNE_A_VIS": "Borne vissée",
        "CAPOT": "Capot connecteur",
        "MODULE_SECTEUR": "Module secteur",
        "BORNE_BLIND": "Borne blindée",
        "POINTE_TEST": "Pointe mesure",
        "EMBASE_BANANE": "Embase banane"
    },

    "MECANIQUE": {
        "PIECE_SUR_PLAN": "Pièce personnalisée",
        "BOITIER": "Boîtier équipement",
        "CHASSIS": "Châssis mécanique",
        "VALISE": "Valise transport",
        "DISSIPATEUR": "Dissipateur thermique",
        "VENTILATEUR": "Ventilateur refroidissement",
        "MOTEUR": "Moteur électrique",
        "JOINT": "Joint étanchéité",
        "PAD_THERM": "Interface thermique",
        "RESSORT": "Ressort mécanique",
        "PALIER": "Palier mécanique",
        "RES_CHAUFF": "Résistance chauffante",
        "PASTILLE": "Pastille mécanique",
        "BLINDAGE": "Blindage électromagnétique",
        "POINT_TEST": "Point test",
        "TESTA_PCB": "Testeur circuit",
        "TROU_FIX": "Trou fixation",
        "ENS_THERM": "Ensemble thermique"
    },

    "PILES": {
        "PILE": "Pile électrique",
        "BATTERIE": "Batterie rechargeable"
    },

    "CABLE_ET_FILAIRE": {
        "FIL": "Fil électrique",
        "CABLE_PLAT": "Câble plat",
        "NAPPE_EQUIPEE": "Nappe assemblée",
        "CABLE": "Câble électrique",
        "CABLE_ETHERNET": "Câble Ethernet",
        "CORDON": "Cordon électrique",
        "GAINE": "Gaine protection",
        "TRESSE": "Tresse conductrice",
        "MANCHON": "Manchon protection",
        "COLLIER": "Collier serrage",
        "GOULOTTE": "Goulotte câblage",
        "EMBASE_COLLIER": "Support collier",
        "PRESSE_ETOUPE": "Presse-étoupe câble"
    },

    "OPTOELECTRONIQUE": {
        "DIODE_LED": "Diode lumineuse",
        "OPTOCOUPLEUR": "Isolation optique",
        "PHOTODIODE": "Détection lumineuse",
        "PHOTOTRANSISTOR": "Transistor photosensible",
        "AFFICHEUR": "Affichage visuel",
        "VOYANT": "Indicateur lumineux",
        "LAMPE": "Source lumineuse",
        "SPECTROMETRE": "Mesure spectrale",
        "GUIDE_LUMIERE": "Guide lumière",
        "DRIVER_FIBRE_OPT": "Commande fibre optique",
        "FIBRE_OPTIQUE": "Transmission optique",
        "CAPTEUR_OPTO": "Capteur optique",
        "FILTRE_OPTIQUE": "Filtre lumineux",
        "CAMERA": "Capture image",
        "LENTILLE": "Lentille optique",
        "FENETRE": "Fenêtre optique"
    },

    "VISSERIE": {
        "VIS": "Vis fixation",
        "ECROU": "Écrou fixation",
        "ROND": "Rondelle fixation",
        "ENTRETOISE": "Entretoise mécanique",
        "GOUJON": "Goujon fixation",
        "PLOT_ANTIVIB": "Plot antivibratoire",
        "CLAVETTE": "Clavette mécanique"
    },

    "ETIQUETTE": {
        "ETIQU": "Étiquette identification"
    },

    "INFORMATIQUE": {
        "CARTE_MEM": "Carte mémoire",
        "DISQUE_DUR": "Stockage informatique",
        "PC": "Ordinateur personnel",
        "MONITEUR_PC": "Écran informatique",
        "CLAVIER_PC": "Clavier informatique",
        "SOURIS_PC": "Souris informatique"
    },

    "CARTES_EQUIPEES": {
        "CARTE_PC": "Carte électronique",
        "MODULE": "Module électronique"
    },

    "CAPTEURS": {
        "CAPTEUR_TEMP": "Capteur température",
        "CAPTEUR_COURANT": "Capteur courant",
        "CAPTEUR_PROXIMITE": "Capteur proximité"
    }
}

# CHAMPS_METADATA = {
#     # ==========================================
#     # 1. COMMON, GENERIC & MECHANICAL
#     # ==========================================
#     "TECHNO": {"description": "Component technology", "unite": None, "exemples": ["SMD", "Through-hole", "Ceramic", "LDO"]},
#     "BOITIER": {"description": "Physical format / Package", "unite": None, "exemples": ["0805", "SOIC-8", "TO-220"]},
#     "BOITIER/PTS/FILS": {"description": "Physical format / Pts / Wires", "unite": None, "exemples": ["Axial", "Radial"]},
#     "BOITIER / DIMENSIONS": {"description": "Package or dimensions", "unite": "mm", "exemples": ["DIP-14", "10x10"]},
#     "DIMENSIONS": {"description": "Overall dimensions", "unite": "mm", "exemples": ["10x10x5"]},
#     "DIMENSIONS EXT": {"description": "External dimensions", "unite": "mm", "exemples": ["120x120x38"]},
#     "DIMENSIONS/BOITIER": {"description": "Dimensions or package", "unite": "mm", "exemples": ["TO-220", "15x15"]},
#     "DIM ou BOITIER": {"description": "Dimensions or package", "unite": "mm", "exemples": []},
#     "TYPE": {"description": "Specific sub-category", "unite": None, "exemples": ["NPN", "Schottky", "Step-Down"]},
#     "LIBRE": {"description": "Free text field", "unite": None, "exemples": ["AEC-Q200", "Low Noise"]},
#     "DIVERS": {"description": "Miscellaneous information", "unite": None, "exemples": []},
#     "T°C FONCT": {"description": "Operating temperature range", "unite": "°C", "exemples": ["-40 to 85"]},
#     "T°C STOCK": {"description": "Storage temperature range", "unite": "°C", "exemples": ["-40 to 105"]},
#     "T°Cmin/T°Cmax": {"description": "Min and max temperature", "unite": "°C", "exemples": ["-55/125"]},
#     "MATIERE": {"description": "Main material", "unite": None, "exemples": ["Plastic", "Brass", "Aluminum"]},
#     "COULEUR": {"description": "Color", "unite": None, "exemples": ["Black", "Red", "Transparent"]},
#     "FINITION": {"description": "Plating / Finish", "unite": None, "exemples": ["Gold (Au)", "Tin (Sn)"]},
#     "FORMAT": {"description": "Standard format", "unite": None, "exemples": ["ATX", "SDHC", "2.5 inches"]},
#     "DESIGNATION": {"description": "Part name or designation", "unite": None, "exemples": []},
#     "N° PLAN": {"description": "Mechanical drawing number", "unite": None, "exemples": []},
#     "CATEGORIE": {"description": "General category", "unite": None, "exemples": ["Cat5e", "Cat6"]},

#     # ==========================================
#     # 2. PASSIVES (Resistors, Capacitors, Inductors)
#     # ==========================================
#     "VALEUR": {"description": "Nominal value", "unite": "Ω, F, H", "exemples": ["10k", "100nF"]},
#     "TOLERANCE": {"description": "Tolerance / Precision", "unite": "%", "exemples": ["1", "5"]},
#     "PUISSANCE": {"description": "Maximum power", "unite": "W", "exemples": ["0.25", "1"]},
#     "STABILITE": {"description": "Stability or drift (TCR)", "unite": "ppm/°C", "exemples": ["50", "100"]},
#     "CAPACITE": {"description": "Capacitance value", "unite": "F", "exemples": ["10u", "100n"]},
#     "CAPACITE min/max": {"description": "Capacitance range (adjustable)", "unite": "F", "exemples": ["5p/30p"]},
#     "TENSION": {"description": "Nominal operating voltage", "unite": "V", "exemples": ["16", "50"]},
#     "ESR": {"description": "Equivalent series resistance", "unite": "Ω or mΩ", "exemples": ["50m"]},
#     "DIELECTRIQUE": {"description": "Dielectric type", "unite": None, "exemples": ["X7R", "C0G"]},
#     "MATERIAU": {"description": "Material", "unite": None, "exemples": ["Polyester", "Ferrite"]},
#     "SENS": {"description": "Polarity or direction", "unite": None, "exemples": ["Polarized", "Non-polarized"]},
#     "DIAMETRE": {"description": "Diameter", "unite": "mm", "exemples": ["5", "8"]},
#     "TENSION AC": {"description": "Max AC voltage", "unite": "Vac", "exemples": ["275", "250"]},
#     "ENERGIE": {"description": "Maximum absorbable energy", "unite": "J (Joule)", "exemples": ["10", "50"]},
#     "VALEUR BETA": {"description": "Beta coefficient (Thermistor)", "unite": "K", "exemples": ["3950", "3435"]},
#     "RESISTANCE": {"description": "Resistance value", "unite": "Ω", "exemples": ["10k"]},

#     # ==========================================
#     # 3. SEMICONDUCTORS & ACTIVES (Diodes, Transistors)
#     # ==========================================
#     "COURANT": {"description": "Nominal current", "unite": "A", "exemples": ["1", "5"]},
#     "COURANT ou TENSION": {"description": "Current or voltage", "unite": "A or V", "exemples": []},
#     "COURANT MAX": {"description": "Maximum current", "unite": "A", "exemples": []},
#     "TENSION MAX": {"description": "Maximum voltage", "unite": "V", "exemples": []},
#     "TENSION VRRM": {"description": "Maximum repetitive peak reverse voltage", "unite": "V", "exemples": ["400", "1000"]},
#     "COURANT IF": {"description": "Forward current", "unite": "A", "exemples": ["1", "0.5"]},
#     "TENSION VZ": {"description": "Zener voltage", "unite": "V", "exemples": ["3.3", "5.1"]},
#     "TENSION VR": {"description": "Reverse voltage", "unite": "V", "exemples": ["5", "12"]},
#     "CAPACITE CDmax": {"description": "Max diode capacitance", "unite": "pF", "exemples": ["15", "30"]},
#     "TENSION VBO": {"description": "Breakover voltage", "unite": "V", "exemples": ["32"]},
#     "TENSION rwm": {"description": "Reverse stand-off voltage", "unite": "V", "exemples": ["5"]},
#     "TENSION CRETE": {"description": "Peak voltage", "unite": "V", "exemples": ["600"]},
#     "TENSION ESD": {"description": "ESD protection voltage", "unite": "kV", "exemples": ["8", "15"]},
#     "TENSION VCE": {"description": "Collector-Emitter voltage", "unite": "V", "exemples": ["45", "60"]},
#     "COURANT IC": {"description": "Collector current", "unite": "A", "exemples": ["0.1", "2"]},
#     "TENSION VDS": {"description": "Drain-Source voltage", "unite": "V", "exemples": ["30", "100"]},
#     "COURANT ID": {"description": "Drain current", "unite": "A", "exemples": ["5", "10"]},
#     "TENSION VDRM": {"description": "Max blocking voltage", "unite": "V", "exemples": ["600"]},
#     "COURANT IT": {"description": "RMS on-state current", "unite": "A", "exemples": ["4"]},
#     "COURANT IGT": {"description": "Gate trigger current", "unite": "mA", "exemples": ["5", "10"]},

#     # ==========================================
#     # 4. INTEGRATED CIRCUITS (ICs)
#     # ==========================================
#     "CONFIG": {"description": "Internal configuration", "unite": None, "exemples": ["Quad", "Dual"]},
#     "ALIMENTATION": {"description": "Supply voltage", "unite": "V", "exemples": ["3.3", "5"]},
#     "TENSION IN": {"description": "Input voltage", "unite": "V", "exemples": ["4.5 to 18"]},
#     "TENSION ENTREE": {"description": "Input voltage", "unite": "V", "exemples": ["3 to 5.5"]},
#     "TENSION / COURANT OUT": {"description": "Output voltage or current", "unite": "V or A", "exemples": ["3.3V / 1A"]},
#     "TENSION/COURANT OUT": {"description": "Output voltage or current", "unite": "V or A", "exemples": []},
#     "INTERFACE": {"description": "Communication interface", "unite": None, "exemples": ["I2C", "SPI", "UART"]},
#     "FREQUENCE / DONNEES": {"description": "Frequency or data rate", "unite": "Hz or bps", "exemples": []},
#     "RESOLUTION / VOIES": {"description": "Resolution and number of channels", "unite": "bits / ch", "exemples": ["12-bit / 4ch"]},
#     "TENSION Vref": {"description": "Reference voltage", "unite": "V", "exemples": ["2.5", "4.096"]},
#     "PRECISION": {"description": "Precision", "unite": "%", "exemples": ["0.1", "1"]},
#     "TENSION Vth": {"description": "Threshold voltage", "unite": "V", "exemples": ["2.93"]},
#     "PLAGE T°C": {"description": "Temperature measurement range", "unite": "°C", "exemples": ["-40 to +125"]},
#     "PLAGE MESURE": {"description": "Overall measurement range", "unite": None, "exemples": []},
#     "NBRE AXES": {"description": "Number of axes", "unite": "Integer", "exemples": ["3", "6"]},
#     "COURANT SORTIE": {"description": "Output current", "unite": "A", "exemples": ["20mA"]},
#     "CHAMP": {"description": "Magnetic field", "unite": "Gauss or T", "exemples": []},
#     "COURANT LIMITE max": {"description": "Current limit", "unite": "A", "exemples": ["1.5"]},
#     "NBRE SORTIES": {"description": "Number of outputs", "unite": "Integer", "exemples": ["1", "4"]},
#     "NBRE ENTREES": {"description": "Number of inputs", "unite": "Integer", "exemples": ["2"]},
#     "PLAGE FREQ": {"description": "Frequency range", "unite": "Hz", "exemples": ["2.4G to 2.5G"]},
#     "PUISS TX/RX": {"description": "Transmit/Receive power", "unite": "dBm", "exemples": ["+4dBm / -90dBm"]},
#     "TYPE BATTERIE": {"description": "Battery type", "unite": None, "exemples": ["Li-Ion"]},
#     "TYPE BATT": {"description": "Battery type", "unite": None, "exemples": []},
#     "TENSION/COURANT CHARGE": {"description": "Charge voltage and current", "unite": "V / A", "exemples": ["4.2V / 1A"]},
#     "NB CELLULES": {"description": "Number of managed cells", "unite": "Integer", "exemples": ["1", "2"]},
#     "MÉMOIRE": {"description": "Memory capacity", "unite": "bits/Bytes", "exemples": ["1kbit"]},
#     "NOMBRE VOIES": {"description": "Number of channels", "unite": "Integer", "exemples": ["1"]},
#     "ETAT": {"description": "Logic state", "unite": None, "exemples": ["Active Low"]},
#     "SORTIE": {"description": "Output type", "unite": None, "exemples": ["Open-Drain", "Push-Pull"]},
#     "PLAGE HUMIDITE": {"description": "Humidity measurement range", "unite": "%RH", "exemples": ["0 to 100"]},
#     "SENSIBILITE": {"description": "Sensitivity", "unite": "dB or mV", "exemples": ["-38dB"]},

#     # ==========================================
#     # 5. INDUCTIVE, MAGNETIC & POWER
#     # ==========================================
#     "INDUCTANCE": {"description": "Inductance value", "unite": "H", "exemples": ["10uH", "2.2mH"]},
#     "Uprim/Usec/Iac": {"description": "Primary / secondary voltage / current", "unite": "V / V / A", "exemples": ["230V/12V/1A"]},
#     "RATIO": {"description": "Transformation ratio", "unite": ":", "exemples": ["1:1", "1:CT"]},
#     "ISOLATION Prim/sec": {"description": "Isolation voltage", "unite": "Vrms or kV", "exemples": ["1500Vrms"]},
#     "I SENSE": {"description": "Sensed current", "unite": "A", "exemples": ["10", "20"]},
#     "CONST Et": {"description": "Voltage-time constant", "unite": "V.us", "exemples": []},
#     "VITESSE": {"description": "Network speed", "unite": "Mbps", "exemples": ["10/100", "1000"]},
#     "INDUCTANCE RX/TX": {"description": "RX/TX line inductance", "unite": "uH", "exemples": ["350uH"]},
#     "RATIO TX/RX": {"description": "TX/RX transformation ratio", "unite": ":", "exemples": ["1:1"]},
#     "PORT": {"description": "Number of ports", "unite": "Integer", "exemples": ["1", "2"]},
#     "COURANT Isat": {"description": "Saturation current", "unite": "A", "exemples": ["3.5"]},
#     "IMPED": {"description": "Impedance", "unite": "Ω", "exemples": ["120", "600"]},
#     "FREQ": {"description": "Test frequency", "unite": "Hz", "exemples": ["100MHz"]},
#     "PERMEABILITE": {"description": "Relative core permeability", "unite": "ui", "exemples": []},
#     "FREQUENCE": {"description": "Operating frequency", "unite": "Hz", "exemples": ["16MHz", "868MHz"]},
#     "IMPEDANCE": {"description": "Characteristic impedance", "unite": "Ω", "exemples": ["50", "8"]},
#     "FORCE": {"description": "Mechanical or attraction force", "unite": "N", "exemples": []},
#     "FREQmin/max": {"description": "Min and max frequency", "unite": "Hz", "exemples": []},
#     "PERTE": {"description": "Insertion loss", "unite": "dB", "exemples": ["-1.5"]},
#     "Vin": {"description": "Input voltage", "unite": "V", "exemples": []},
#     "Vout": {"description": "Output voltage", "unite": "V", "exemples": []},
#     "RENDEMENT": {"description": "Energy efficiency", "unite": "%", "exemples": ["85"]},
#     "CHIMIE": {"description": "Battery chemistry", "unite": None, "exemples": ["Li-Ion", "NiMH"]},

#     # ==========================================
#     # 6. SWITCHING, RELAYS & PIEZO
#     # ==========================================
#     "CAPACITANCE": {"description": "Load capacitance (Crystal)", "unite": "pF", "exemples": ["12.5", "18"]},
#     "NIVEAU": {"description": "Sound pressure level", "unite": "dB", "exemples": ["85"]},
#     "NB POINTS": {"description": "Number of points or contacts (graphics)", "unite": "Integer", "exemples": ["2", "4"]},
#     "CONFIGURATION": {"description": "Switching configuration", "unite": None, "exemples": ["SPST", "DPDT"]},
#     "ORIENTATION": {"description": "Mounting orientation", "unite": None, "exemples": ["Straight", "Right-angle"]},
#     "TENSION/COURANT": {"description": "Switchable voltage and current", "unite": "V / A", "exemples": ["250VAC/10A"]},
#     "NB TOUCHES": {"description": "Number of keys (keypad)", "unite": "Integer", "exemples": ["12", "16"]},
#     "TENSION BOBINE ou VF": {"description": "Coil activation voltage", "unite": "V", "exemples": ["5", "12"]},
#     "POLES": {"description": "Number of poles", "unite": "Integer", "exemples": ["1", "3"]},
#     "ACTION": {"description": "Fuse action", "unite": None, "exemples": ["Fast-acting", "Slow-blow"]},
#     "MONTAGE": {"description": "Mounting type", "unite": None, "exemples": ["DIN Rail", "PCB"]},

#     # ==========================================
#     # 7. CONNECTORS & WIRING
#     # ==========================================
#     "CONTACT": {"description": "Contact type", "unite": None, "exemples": ["Crimp", "Solder"]},
#     "TAILLE": {"description": "Connector size", "unite": None, "exemples": []},
#     "GENRE": {"description": "Gender (Male/Female)", "unite": None, "exemples": ["M", "F"]},
#     "JAUGE": {"description": "Cable section (AWG)", "unite": "AWG or mm²", "exemples": ["24-28"]},
#     "ISOLATION": {"description": "Insulation material", "unite": None, "exemples": ["PVC", "Teflon"]},
#     "SERIE CONNECTEUR": {"description": "Specific series", "unite": None, "exemples": ["Micro-Fit", "JST-XH"]},
#     "CONTACTS": {"description": "Contact finish or material", "unite": None, "exemples": []},
#     "TYPE/FAMILLE": {"description": "Connector family", "unite": None, "exemples": ["RJ45", "USB"]},
#     "TYPE/SERIE": {"description": "Series or type", "unite": None, "exemples": []},
#     "TERMINAISON": {"description": "Termination type", "unite": None, "exemples": ["Solder", "Crimp"]},
#     "NB ELEMENTS": {"description": "Number of elements", "unite": "Integer", "exemples": []},
#     "OPTION": {"description": "Specific options", "unite": None, "exemples": ["With keying / polarizing"]},
#     "OPTIONS": {"description": "Options", "unite": None, "exemples": []},
#     "PAS": {"description": "Pin spacing (Pitch)", "unite": "mm", "exemples": ["2.54", "1.27"]},
#     "DIAMETRE VIS": {"description": "Screw diameter", "unite": "mm or M", "exemples": ["M3", "M4"]},
#     "NB CONTACTS": {"description": "Number of contacts", "unite": "Integer", "exemples": ["10", "40"]},
#     "NB CONTACTS / DIMENSIONS": {"description": "Nb of contacts and dimensions", "unite": None, "exemples": []},
#     "INTERRUPTEUR": {"description": "Switch present", "unite": None, "exemples": ["Yes", "No"]},
#     "FILTRE": {"description": "Filter present (e.g. mains)", "unite": None, "exemples": ["Yes", "No"]},
#     "FUSIBLE": {"description": "Fuse holder present", "unite": None, "exemples": ["Yes", "No"]},
#     "DIMENSIONS CABLE": {"description": "Cable section or diameter", "unite": "mm", "exemples": []},
#     "DIAMETRE POINTE": {"description": "Test probe diameter", "unite": "mm", "exemples": []},
#     "CONFIG BRIN": {"description": "Stranded or solid wire", "unite": None, "exemples": ["Stranded", "Solid"]},
#     "JAUGE/SECTION": {"description": "Cable section", "unite": "AWG or mm²", "exemples": []},
#     "CABLE_PLAT": {"description": "Flat cable", "unite": None, "exemples": ["Yes", "No"]},
#     "LONGUEUR": {"description": "Physical length", "unite": "mm or m", "exemples": ["1000", "500"]},
#     "CONNECT A/B": {"description": "Connectors at ends A and B", "unite": None, "exemples": ["SMA-M / SMA-F"]},
#     "COULEUR FIL": {"description": "Jacket color", "unite": None, "exemples": ["Red", "Black"]},
#     "BLINDAGE": {"description": "Shielding (STP, UTP, FTP)", "unite": None, "exemples": ["STP", "UTP"]},
#     "NB PAIRES": {"description": "Number of twisted pairs", "unite": "Integer", "exemples": ["4"]},
#     "DIAMETRE ou LARGEUR": {"description": "Diameter or width", "unite": "mm", "exemples": []},
#     "RATIO": {"description": "Shrink ratio (Heat shrink)", "unite": ":", "exemples": ["2:1", "3:1"]},
#     "FIXATION": {"description": "Fixing method", "unite": None, "exemples": ["Adhesive", "Screw"]},
#     "INDICE IP": {"description": "Ingress Protection (IP) rating", "unite": None, "exemples": ["IP67", "IP68"]},

#     # ==========================================
#     # 8. OPTOELECTRONICS & FIBER
#     # ==========================================
#     "L.ONDE": {"description": "Dominant wavelength", "unite": "nm", "exemples": ["650"]},
#     "LONGUEUR ONDE": {"description": "Wavelength", "unite": "nm", "exemples": []},
#     "LONG. ONDE": {"description": "Wavelength", "unite": "nm", "exemples": []},
#     "PUISS. OPTIQUE": {"description": "Optical or luminous power", "unite": "mW or mcd", "exemples": []},
#     "TENSION VF": {"description": "Forward Voltage", "unite": "V", "exemples": ["2.1", "3.3"]},
#     "COURANT TEST": {"description": "Test current", "unite": "mA", "exemples": ["20"]},
#     "TYPE ECRAN": {"description": "Display technology", "unite": None, "exemples": ["LCD", "OLED", "TFT"]},
#     "RESOLUTION": {"description": "Spatial resolution", "unite": "Pixels", "exemples": ["128x64"]},
#     "P.SPECTRALE": {"description": "Spectral range", "unite": "nm", "exemples": ["400-700"]},
#     "NB TUBE": {"description": "Number of pipes (light guide)", "unite": "Integer", "exemples": []},
#     "DEBIT": {"description": "Data rate (Fiber)", "unite": "Mbps or Gbps", "exemples": ["1Gbps"]},
#     "MATIERE CŒUR": {"description": "Core material", "unite": None, "exemples": ["Glass", "Plastic (POF)"]},
#     "DIAMETRE CŒUR": {"description": "Optical core diameter", "unite": "um", "exemples": ["50", "9"]},
#     "FWHM": {"description": "Full width at half maximum (FWHM)", "unite": "nm", "exemples": []},
#     "EPAISSEUR": {"description": "Thickness", "unite": "mm", "exemples": []},
#     "TRAITEMENT": {"description": "Surface treatment", "unite": None, "exemples": ["Anti-reflective (AR)"]},
#     "DIST. FOCALE": {"description": "Focal length", "unite": "mm", "exemples": ["10", "25"]},

#     # ==========================================
#     # 9. THERMAL DISSIPATION & PCB MECHANICS
#     # ==========================================
#     "RES. THERM": {"description": "Thermal resistance", "unite": "°C/W", "exemples": ["5", "12"]},
#     "BRUIT": {"description": "Noise level", "unite": "dBA", "exemples": ["25", "40"]},
#     "FORME": {"description": "General shape", "unite": None, "exemples": ["Round", "Square"]},
#     "ENVELOPPE/QUALITE": {"description": "Enclosure type or quality", "unite": None, "exemples": []},
#     "SHORE": {"description": "Hardness (Seals, Pads)", "unite": "Shore A/D", "exemples": ["50A"]},
#     "TENUE EN T°": {"description": "Max temperature resistance", "unite": "°C", "exemples": ["150", "200"]},
#     "CONDUC. THERM": {"description": "Thermal conductivity", "unite": "W/mK", "exemples": ["1.5", "5"]},
#     "RAIDEUR/FORCE": {"description": "Spring stiffness or force", "unite": "N/mm", "exemples": []},
#     "DIMENSIONS PASTILLE": {"description": "PCB pad dimensions", "unite": "mm", "exemples": []},
#     "VENTILATION (capots)": {"description": "Ventilation type (Vented/Solid)", "unite": None, "exemples": ["Vented"]},
#     "DIAM TROU / CMS": {"description": "Hole diameter or SMD", "unite": "mm", "exemples": []},
#     "DIMENSIONS TROU": {"description": "Hole dimensions", "unite": "mm", "exemples": []},
#     "TRANSFERT CHALEUR": {"description": "Heat transfer mode", "unite": None, "exemples": ["Peltier"]},
#     "COURANT NOM": {"description": "Nominal current", "unite": "A", "exemples": []},

#     # ==========================================
#     # 10. FASTENERS & STANDOFFS
#     # ==========================================
#     "FORME TETE": {"description": "Screw head shape", "unite": None, "exemples": ["Cylindrical", "Countersunk", "Hexagonal"]},
#     "FILETAGE": {"description": "Thread type", "unite": "M", "exemples": ["M3", "M4"]},
#     "FILETAGE/D INT": {"description": "Thread or internal diameter", "unite": "mm or M", "exemples": []},
#     "FORME/LARGEUR": {"description": "Shape and width", "unite": "mm", "exemples": ["Hexagonal 5.5"]},

#     # ==========================================
#     # 11. COMPUTING & READY-TO-USE BOARDS
#     # ==========================================
#     "CLASSE/VITESSE": {"description": "Speed class (SD Card)", "unite": None, "exemples": ["Class 10", "UHS-I"]},
#     "TYPE_PROC": {"description": "Processor family", "unite": None, "exemples": ["ARM Cortex-M4", "x86"]},
#     "FREQ_PROC": {"description": "Processor frequency", "unite": "GHz or MHz", "exemples": ["1.2GHz"]},
#     "RAM/DD": {"description": "RAM and Hard Drive", "unite": "GB", "exemples": ["4GB / 32GB"]},
#     "OS": {"description": "Provided Operating System", "unite": None, "exemples": ["Linux", "Windows 10 IoT"]},
#     "INTERFACE PROG": {"description": "Programming interface", "unite": None, "exemples": ["JTAG", "SWD"]},
#     "INTERFACE 1": {"description": "Primary hardware interface", "unite": None, "exemples": ["USB"]},
#     "INTERFACE 2": {"description": "Secondary hardware interface", "unite": None, "exemples": ["Ethernet"]},
#     "FORMAT/INTERFACE": {"description": "Form factor and interface", "unite": None, "exemples": ["PCIe", "M.2"]},
#     "FONCTION PRINCIPALE": {"description": "Module or board role", "unite": None, "exemples": ["Data acquisition", "Relay switching"]},
# }


CHAMPS_METADATA = {
    # ==========================================
    # 1. COMMON, GENERIC & MECHANICAL
    # ==========================================
    "TECHNO": {"description": "Component technology", "unite": None, "exemples": ["SMD", "Through-hole", "Ceramic", "LDO"], "keywords": ["technology", "mounting", "SMT", "THT", "surface mount", "through hole", "type", "construction"]},
    "BOITIER": {"description": "Physical format / Package", "unite": None, "exemples": ["0805", "SOIC-8", "TO-220"], "keywords": ["package", "case", "footprint", "encapsulation", "boitier", "outline"]},
    "BOITIER/PTS/FILS": {"description": "Physical format / Pts / Wires", "unite": None, "exemples": ["Axial", "Radial"], "keywords": ["leads", "terminals", "pins", "wires", "axial", "radial", "lead style"]},
    "BOITIER / DIMENSIONS": {"description": "Package or dimensions", "unite": "mm", "exemples": ["DIP-14", "10x10"], "keywords": ["package size", "dimensions", "size", "footprint", "body size"]},
    "DIMENSIONS": {"description": "Overall dimensions", "unite": "mm", "exemples": ["10x10x5"], "keywords": ["size", "dimensions", "L x W x H", "LxWxH", "outline", "measurements"]},
    "DIMENSIONS EXT": {"description": "External dimensions", "unite": "mm", "exemples": ["120x120x38"], "keywords": ["external dimensions", "outer dimensions", "overall size", "outside dimensions"]},
    "DIMENSIONS/BOITIER": {"description": "Dimensions or package", "unite": "mm", "exemples": ["TO-220", "15x15"], "keywords": ["size/package", "dimensions/case"]},
    "DIM ou BOITIER": {"description": "Dimensions or package", "unite": "mm", "exemples": [], "keywords": ["dim", "case", "package size"]},
    "TYPE": {"description": "Specific sub-category", "unite": None, "exemples": ["NPN", "Schottky", "Step-Down","RF"], "keywords": ["type", "category", "family", "configuration", "classification"]},
    "LIBRE": {"description": "Free text field", "unite": None, "exemples": ["AEC-Q200", "Low Noise"], "keywords": ["features", "notes", "description", "remarks", "special", "characteristics"]},
    "DIVERS": {"description": "Miscellaneous information", "unite": None, "exemples": [], "keywords": ["misc", "other", "additional info", "miscellaneous"]},
    "T°C FONCT": {"description": "Operating temperature range", "unite": "°C", "exemples": ["-40 to 85"], "keywords": ["operating temperature", "temp range", "topr", "operating temp", "ambient temperature", "ta"]},
    "T°C STOCK": {"description": "Storage temperature range", "unite": "°C", "exemples": ["-40 to 105"], "keywords": ["storage temperature", "tstg", "storage temp"]},
    "T°Cmin/T°Cmax": {"description": "Min and max temperature", "unite": "°C", "exemples": ["-55/125"], "keywords": ["temperature min/max", "temp limits", "thermal range"]},
    "MATIERE": {"description": "Main material", "unite": None, "exemples": ["Plastic", "Brass", "Aluminum"], "keywords": ["material", "composition", "body material", "housing material", "base material"]},
    "COULEUR": {"description": "Color", "unite": None, "exemples": ["Black", "Red", "Transparent"], "keywords": ["color", "colour", "finish color", "housing color"]},
    "FINITION": {"description": "Plating / Finish", "unite": None, "exemples": ["Gold (Au)", "Tin (Sn)"], "keywords": ["plating", "finish", "contact plating", "terminal finish", "coating"]},
    "FORMAT": {"description": "Standard format", "unite": None, "exemples": ["ATX", "SDHC", "2.5 inches"], "keywords": ["format", "form factor", "size standard"]},
    "DESIGNATION": {"description": "Part name or designation", "unite": None, "exemples": [], "keywords": ["designation", "part name", "description", "title", "part number description"]},
    "N° PLAN": {"description": "Mechanical drawing number", "unite": None, "exemples": [], "keywords": ["drawing number", "mechanical drawing", "document number", "blueprint"]},
    "CATEGORIE": {"description": "General category", "unite": None, "exemples": ["Cat5e", "Cat6"], "keywords": ["category", "class", "grade", "series type"]},

    # ==========================================
    # 2. PASSIVES (Resistors, Capacitors, Inductors)
    # ==========================================
    "VALEUR": {"description": "Nominal value", "unite": "Ω, F, H", "exemples": ["10k", "100nF"], "keywords": ["value", "resistance", "capacitance", "inductance", "nominal value"]},
    "TOLERANCE": {"description": "Tolerance / Precision", "unite": "%", "exemples": ["1", "5"], "keywords": ["tolerance", "accuracy", "tol", "precision"]},
    "PUISSANCE": {"description": "Maximum power", "unite": "W", "exemples": ["0.25", "1"], "keywords": ["power", "power rating", "wattage", "dissipation", "pd", "rated power"]},
    "STABILITE": {"description": "Stability or drift (TCR)", "unite": "ppm/°C", "exemples": ["50", "100"], "keywords": ["tcr", "temperature coefficient", "stability", "drift", "ppm"]},
    "CAPACITE": {"description": "Capacitance value", "unite": "F", "exemples": ["10u", "100n"], "keywords": ["capacitance", "cap", "c", "value"]},
    "CAPACITE min/max": {"description": "Capacitance range (adjustable)", "unite": "F", "exemples": ["5p/30p"], "keywords": ["capacitance range", "tuning range", "adjustable range", "variable capacitance"]},
    "TENSION": {"description": "Nominal operating voltage", "unite": "V", "exemples": ["16", "50"], "keywords": ["voltage", "rated voltage", "working voltage", "vdc", "wvdc", "ur"]},
    "ESR": {"description": "Equivalent series resistance", "unite": "Ω or mΩ", "exemples": ["50m"], "keywords": ["esr", "equivalent series resistance", "dissipation factor", "df", "tan delta"]},
    "DIELECTRIQUE": {"description": "Dielectric type", "unite": None, "exemples": ["X7R", "C0G"], "keywords": ["dielectric", "temperature characteristic", "ceramic type", "film type", "dielectric material"]},
    "MATERIAU": {"description": "Material", "unite": None, "exemples": ["Polyester", "Ferrite"], "keywords": ["material", "core material", "dielectric material"]},
    "SENS": {"description": "Polarity or direction", "unite": None, "exemples": ["Polarized", "Non-polarized"], "keywords": ["polarity", "polarized", "non-polarized", "direction"]},
    "DIAMETRE": {"description": "Diameter", "unite": "mm", "exemples": ["5", "8"], "keywords": ["diameter", "dia", "ø", "d", "outer diameter"]},
    "TENSION AC": {"description": "Max AC voltage", "unite": "Vac", "exemples": ["275", "250"], "keywords": ["ac voltage", "vac", "rated ac voltage", "ur (ac)"]},
    "ENERGIE": {"description": "Maximum absorbable energy", "unite": "J (Joule)", "exemples": ["10", "50"], "keywords": ["energy", "joule rating", "maximum energy", "wmax", "energy absorption"]},
    "VALEUR BETA": {"description": "Beta coefficient (Thermistor)", "unite": "K", "exemples": ["3950", "3435"], "keywords": ["beta", "b value", "b constant", "thermistor constant", "thermal index"]},
    "RESISTANCE": {"description": "Resistance value", "unite": "Ω", "exemples": ["10k"], "keywords": ["resistance", "r", "ohm", "r25", "dc resistance", "dcr"]},

    # ==========================================
    # 3. SEMICONDUCTORS & ACTIVES (Diodes, Transistors)
    # ==========================================
    "COURANT": {"description": "Nominal current", "unite": "A", "exemples": ["1", "5"], "keywords": ["current", "rated current", "i", "nominal current"]},
    "COURANT ou TENSION": {"description": "Current or voltage", "unite": "A or V", "exemples": [], "keywords": ["current/voltage", "i/v", "ratings"]},
    "COURANT MAX": {"description": "Maximum current", "unite": "A", "exemples": [], "keywords": ["max current", "peak current", "maximum current", "imax", "surge current"]},
    "TENSION MAX": {"description": "Maximum voltage", "unite": "V", "exemples": [], "keywords": ["max voltage", "maximum voltage", "peak voltage", "vmax"]},
    "TENSION VRRM": {"description": "Maximum repetitive peak reverse voltage", "unite": "V", "exemples": ["400", "1000"], "keywords": ["vrrm", "repetitive peak reverse voltage", "peak inverse voltage", "piv", "reverse voltage"]},
    "COURANT IF": {"description": "Forward current", "unite": "A", "exemples": ["1", "0.5"], "keywords": ["if", "forward current", "continuous forward current", "average forward current"]},
    "TENSION VZ": {"description": "Zener voltage", "unite": "V", "exemples": ["3.3", "5.1"], "keywords": ["vz", "zener voltage", "breakdown voltage", "nom zener voltage"]},
    "TENSION VR": {"description": "Reverse voltage", "unite": "V", "exemples": ["5", "12"], "keywords": ["vr", "reverse voltage", "dc blocking voltage", "reverse working voltage"]},
    "CAPACITE CDmax": {"description": "Max diode capacitance", "unite": "pF", "exemples": ["15", "30"], "keywords": ["cd", "diode capacitance", "junction capacitance", "cj", "total capacitance"]},
    "TENSION VBO": {"description": "Breakover voltage", "unite": "V", "exemples": ["32"], "keywords": ["vbo", "breakover voltage"]},
    "TENSION rwm": {"description": "Reverse stand-off voltage", "unite": "V", "exemples": ["5"], "keywords": ["vrwm", "stand-off voltage", "working peak reverse voltage", "reverse standoff"]},
    "TENSION CRETE": {"description": "Peak voltage", "unite": "V", "exemples": ["600"], "keywords": ["peak voltage", "surge voltage", "transient voltage"]},
    "TENSION ESD": {"description": "ESD protection voltage", "unite": "kV", "exemples": ["8", "15"], "keywords": ["esd", "electrostatic discharge", "esd rating", "esd protection", "contact discharge", "air discharge"]},
    "TENSION VCE": {"description": "Collector-Emitter voltage", "unite": "V", "exemples": ["45", "60"], "keywords": ["vce", "collector-emitter voltage", "vceo", "collector to emitter"]},
    "COURANT IC": {"description": "Collector current", "unite": "A", "exemples": ["0.1", "2"], "keywords": ["ic", "collector current", "continuous collector current"]},
    "TENSION VDS": {"description": "Drain-Source voltage", "unite": "V", "exemples": ["30", "100"], "keywords": ["vds", "drain-source voltage", "vdss", "drain to source"]},
    "COURANT ID": {"description": "Drain current", "unite": "A", "exemples": ["5", "10"], "keywords": ["id", "drain current", "continuous drain current", "idrain"]},
    "TENSION VDRM": {"description": "Max blocking voltage", "unite": "V", "exemples": ["600"], "keywords": ["vdrm", "repetitive peak off-state voltage", "blocking voltage"]},
    "COURANT IT": {"description": "RMS on-state current", "unite": "A", "exemples": ["4"], "keywords": ["it(rms)", "on-state current", "rms on-state current"]},
    "COURANT IGT": {"description": "Gate trigger current", "unite": "mA", "exemples": ["5", "10"], "keywords": ["igt", "gate trigger current", "trigger current"]},

    # ==========================================
    # 4. INTEGRATED CIRCUITS (ICs)
    # ==========================================
    "CONFIG": {"description": "Internal configuration", "unite": None, "exemples": ["Quad", "Dual"], "keywords": ["configuration", "channels", "topology", "architecture", "type"]},
    "ALIMENTATION": {"description": "Supply voltage", "unite": "V", "exemples": ["3.3", "5"], "keywords": ["supply voltage", "vcc", "vdd", "operating voltage", "power supply", "vs"]},
    "TENSION IN": {"description": "Input voltage", "unite": "V", "exemples": ["4.5 to 18"], "keywords": ["input voltage", "vin", "input range", "vi"]},
    "TENSION ENTREE": {"description": "Input voltage", "unite": "V", "exemples": ["3 to 5.5"], "keywords": ["input voltage", "vi", "input"]},
    "TENSION / COURANT OUT": {"description": "Output voltage or current", "unite": "V or A", "exemples": ["3.3V / 1A"], "keywords": ["output", "vout/iout", "output ratings", "output specifications"]},
    "TENSION/COURANT OUT": {"description": "Output voltage or current", "unite": "V or A", "exemples": [], "keywords": ["output", "vout/iout", "output ratings"]},
    "INTERFACE": {"description": "Communication interface", "unite": None, "exemples": ["I2C", "SPI", "UART"], "keywords": ["interface", "communication", "bus", "serial interface", "i2c", "spi", "uart", "protocol"]},
    "FREQUENCE / DONNEES": {"description": "Frequency or data rate", "unite": "Hz or bps", "exemples": [], "keywords": ["frequency", "data rate", "speed", "baud rate", "throughput", "clock frequency"]},
    "RESOLUTION / VOIES": {"description": "Resolution and number of channels", "unite": "bits / ch", "exemples": ["12-bit / 4ch"], "keywords": ["resolution", "channels", "bits", "adc resolution", "dac resolution"]},
    "TENSION Vref": {"description": "Reference voltage", "unite": "V", "exemples": ["2.5", "4.096"], "keywords": ["vref", "reference voltage", "internal reference"]},
    "PRECISION": {"description": "Precision", "unite": "%", "exemples": ["0.1", "1"], "keywords": ["precision", "accuracy", "error", "tolerance", "initial accuracy"]},
    "TENSION Vth": {"description": "Threshold voltage", "unite": "V", "exemples": ["2.93"], "keywords": ["vth", "threshold voltage", "reset threshold", "trigger voltage", "detect voltage"]},
    "PLAGE T°C": {"description": "Temperature measurement range", "unite": "°C", "exemples": ["-40 to +125"], "keywords": ["temperature range", "sensing range", "measurement range", "operating temperature"]},
    "PLAGE MESURE": {"description": "Overall measurement range", "unite": None, "exemples": [], "keywords": ["measurement range", "sensing range", "full scale", "dynamic range"]},
    "NBRE AXES": {"description": "Number of axes", "unite": "Integer", "exemples": ["3", "6"], "keywords": ["axes", "axis", "dof", "degrees of freedom"]},
    "COURANT SORTIE": {"description": "Output current", "unite": "A", "exemples": ["20mA"], "keywords": ["output current", "iout", "drive current", "load current", "source/sink current"]},
    "CHAMP": {"description": "Magnetic field", "unite": "Gauss or T", "exemples": [], "keywords": ["magnetic field", "b-field", "operating point", "gauss", "tesla", "magnetic sensitivity"]},
    "COURANT LIMITE max": {"description": "Current limit", "unite": "A", "exemples": ["1.5"], "keywords": ["current limit", "ilim", "overcurrent threshold", "short circuit current"]},
    "NBRE SORTIES": {"description": "Number of outputs", "unite": "Integer", "exemples": ["1", "4"], "keywords": ["outputs", "number of outputs", "channels", "output count"]},
    "NBRE ENTREES": {"description": "Number of inputs", "unite": "Integer", "exemples": ["2"], "keywords": ["inputs", "number of inputs", "channels", "input count"]},
    "PLAGE FREQ": {"description": "Frequency range", "unite": "Hz", "exemples": ["2.4G to 2.5G"], "keywords": ["frequency range", "band", "operating frequency", "bandwidth"]},
    "PUISS TX/RX": {"description": "Transmit/Receive power", "unite": "dBm", "exemples": ["+4dBm / -90dBm"], "keywords": ["tx power", "rx sensitivity", "transmit power", "rf power", "output power"]},
    "TYPE BATTERIE": {"description": "Battery type", "unite": None, "exemples": ["Li-Ion"], "keywords": ["battery type", "chemistry", "cell type", "li-ion", "lipo", "lifepo4"]},
    "TYPE BATT": {"description": "Battery type", "unite": None, "exemples": [], "keywords": ["battery type", "cell type"]},
    "TENSION/COURANT CHARGE": {"description": "Charge voltage and current", "unite": "V / A", "exemples": ["4.2V / 1A"], "keywords": ["charge voltage", "charge current", "charging profile", "fast charge current"]},
    "NB CELLULES": {"description": "Number of managed cells", "unite": "Integer", "exemples": ["1", "2"], "keywords": ["cells", "cell count", "series cells", "s", "number of cells"]},
    "MÉMOIRE": {"description": "Memory capacity", "unite": "bits/Bytes", "exemples": ["1kbit"], "keywords": ["memory", "capacity", "eeprom", "flash", "ram", "storage", "density"]},
    "NOMBRE VOIES": {"description": "Number of channels", "unite": "Integer", "exemples": ["1"], "keywords": ["channels", "ch", "dual", "quad", "number of channels", "ways"]},
    "ETAT": {"description": "Logic state", "unite": None, "exemples": ["Active Low"], "keywords": ["logic state", "active low", "active high", "polarity", "logic level"]},
    "SORTIE": {"description": "Output type", "unite": None, "exemples": ["Open-Drain", "Push-Pull"], "keywords": ["output type", "output topology", "open drain", "push-pull", "open collector"]},
    "PLAGE HUMIDITE": {"description": "Humidity measurement range", "unite": "%RH", "exemples": ["0 to 100"], "keywords": ["humidity range", "rh range", "operating humidity", "relative humidity"]},
    "SENSIBILITE": {"description": "Sensitivity", "unite": "dB or mV", "exemples": ["-38dB"], "keywords": ["sensitivity", "gain", "response", "scale factor"]},

    # ==========================================
    # 5. INDUCTIVE, MAGNETIC & POWER
    # ==========================================
    "INDUCTANCE": {"description": "Inductance value", "unite": "H", "exemples": ["10uH", "2.2mH"], "keywords": ["inductance", "l", "value", "nominal inductance"]},
    "Uprim/Usec/Iac": {"description": "Primary / secondary voltage / current", "unite": "V / V / A", "exemples": ["230V/12V/1A"], "keywords": ["primary voltage", "secondary voltage", "input/output", "turns ratio", "ratings"]},
    "RATIO": {"description": "Transformation ratio", "unite": ":", "exemples": ["1:1", "1:CT"], "keywords": ["turns ratio", "ratio", "n1:n2", "transformation ratio"]},
    "ISOLATION Prim/sec": {"description": "Isolation voltage", "unite": "Vrms or kV", "exemples": ["1500Vrms"], "keywords": ["isolation", "dielectric strength", "hipot", "visol", "breakdown voltage"]},
    "I SENSE": {"description": "Sensed current", "unite": "A", "exemples": ["10", "20"], "keywords": ["sensed current", "current range", "measuring range", "primary current"]},
    "CONST Et": {"description": "Voltage-time constant", "unite": "V.us", "exemples": [], "keywords": ["v-us", "e-t", "voltage-time", "et constant", "volt-time"]},
    "VITESSE": {"description": "Network speed", "unite": "Mbps", "exemples": ["10/100", "1000"], "keywords": ["speed", "data rate", "base-t", "ethernet speed"]},
    "INDUCTANCE RX/TX": {"description": "RX/TX line inductance", "unite": "uH", "exemples": ["350uH"], "keywords": ["rx inductance", "tx inductance", "ocl", "open circuit inductance"]},
    "RATIO TX/RX": {"description": "TX/RX transformation ratio", "unite": ":", "exemples": ["1:1"], "keywords": ["tx/rx ratio", "turns ratio tx/rx"]},
    "PORT": {"description": "Number of ports", "unite": "Integer", "exemples": ["1", "2"], "keywords": ["ports", "number of ports", "single port", "multi-port"]},
    "COURANT Isat": {"description": "Saturation current", "unite": "A", "exemples": ["3.5"], "keywords": ["isat", "saturation current", "saturation", "dc bias current"]},
    "IMPED": {"description": "Impedance", "unite": "Ω", "exemples": ["120", "600"], "keywords": ["impedance", "z", "ac resistance", "z @ 100mhz"]},
    "FREQ": {"description": "Test frequency", "unite": "Hz", "exemples": ["100MHz"], "keywords": ["test frequency", "measurement frequency"]},
    "PERMEABILITE": {"description": "Relative core permeability", "unite": "ui", "exemples": [], "keywords": ["permeability", "ui", "mu", "core material", "initial permeability"]},
    "FREQUENCE": {"description": "Operating frequency", "unite": "Hz", "exemples": ["16MHz", "868MHz"], "keywords": ["frequency", "f", "operating frequency", "resonant frequency"]},
    "IMPEDANCE": {"description": "Characteristic impedance", "unite": "Ω", "exemples": ["50", "8"], "keywords": ["impedance", "z", "characteristic impedance", "z0"]},
    "FORCE": {"description": "Mechanical or attraction force", "unite": "N", "exemples": [], "keywords": ["force", "holding force", "attraction force", "operating force", "mating force"]},
    "FREQmin/max": {"description": "Min and max frequency", "unite": "Hz", "exemples": [], "keywords": ["frequency range", "bandwidth", "passband"]},
    "PERTE": {"description": "Insertion loss", "unite": "dB", "exemples": ["-1.5"], "keywords": ["insertion loss", "loss", "il", "attenuation", "return loss"]},
    "Vin": {"description": "Input voltage", "unite": "V", "exemples": [], "keywords": ["vin", "input voltage", "input range", "input specs"]},
    "Vout": {"description": "Output voltage", "unite": "V", "exemples": [], "keywords": ["vout", "output voltage", "output specs"]},
    "RENDEMENT": {"description": "Energy efficiency", "unite": "%", "exemples": ["85"], "keywords": ["efficiency", "eff", "eta"]},
    "CHIMIE": {"description": "Battery chemistry", "unite": None, "exemples": ["Li-Ion", "NiMH"], "keywords": ["chemistry", "battery type", "system", "technology"]},

    # ==========================================
    # 6. SWITCHING, RELAYS & PIEZO
    # ==========================================
    "CAPACITANCE": {"description": "Load capacitance (Crystal)", "unite": "pF", "exemples": ["12.5", "18"], "keywords": ["load capacitance", "cl", "capacitance", "shunt capacitance"]},
    "NIVEAU": {"description": "Sound pressure level", "unite": "dB", "exemples": ["85"], "keywords": ["spl", "sound pressure level", "acoustic output", "sound level"]},
    "NB POINTS": {"description": "Number of points or contacts", "unite": "Integer", "exemples": ["2", "4"], "keywords": ["contacts", "poles", "throws", "positions", "ways"]},
    "CONFIGURATION": {"description": "Switching configuration", "unite": None, "exemples": ["SPST", "DPDT"], "keywords": ["contact form", "circuit", "spst", "dpdt", "spdt", "arrangement", "switch function"]},
    "ORIENTATION": {"description": "Mounting orientation", "unite": None, "exemples": ["Straight", "Right-angle"], "keywords": ["orientation", "mounting angle", "actuator orientation", "top actuated", "side actuated", "vertical", "horizontal"]},
    "TENSION/COURANT": {"description": "Switchable voltage and current", "unite": "V / A", "exemples": ["250VAC/10A"], "keywords": ["contact rating", "switching rating", "rated load", "electrical rating"]},
    "NB TOUCHES": {"description": "Number of keys (keypad)", "unite": "Integer", "exemples": ["12", "16"], "keywords": ["keys", "buttons", "matrix", "keypad size"]},
    "TENSION BOBINE ou VF": {"description": "Coil activation voltage", "unite": "V", "exemples": ["5", "12"], "keywords": ["coil voltage", "nominal voltage", "control voltage", "rated voltage"]},
    "POLES": {"description": "Number of poles", "unite": "Integer", "exemples": ["1", "3"], "keywords": ["poles", "number of poles"]},
    "ACTION": {"description": "Fuse action", "unite": None, "exemples": ["Fast-acting", "Slow-blow"], "keywords": ["blow characteristic", "opening time", "fusing time", "fast acting", "slow blow", "time delay", "characteristics"]},
    "MONTAGE": {"description": "Mounting type", "unite": None, "exemples": ["DIN Rail", "PCB"], "keywords": ["mounting", "termination", "installation", "mounting type"]},

    # ==========================================
    # 7. CONNECTORS & WIRING
    # ==========================================
    "CONTACT": {"description": "Contact type", "unite": None, "exemples": ["Crimp", "Solder"], "keywords": ["contact type", "termination type", "connection method", "termination style"]},
    "TAILLE": {"description": "Connector size", "unite": None, "exemples": [], "keywords": ["size", "shell size", "dimension"]},
    "GENRE": {"description": "Gender (Male/Female)", "unite": None, "exemples": ["M", "F"], "keywords": ["gender", "male", "female", "plug", "receptacle", "jack"]},
    "JAUGE": {"description": "Cable section (AWG)", "unite": "AWG or mm²", "exemples": ["24-28"], "keywords": ["wire size", "awg", "wire gauge", "cable size", "cross section", "applicable wire"]},
    "ISOLATION": {"description": "Insulation material", "unite": None, "exemples": ["PVC", "Teflon"], "keywords": ["insulation", "jacket material", "dielectric", "insulator material"]},
    "SERIE CONNECTEUR": {"description": "Specific series", "unite": None, "exemples": ["Micro-Fit", "JST-XH"], "keywords": ["series", "product line", "family"]},
    "CONTACTS": {"description": "Contact finish or material", "unite": None, "exemples": [], "keywords": ["contact material", "plating", "contact finish"]},
    "TYPE/FAMILLE": {"description": "Connector family", "unite": None, "exemples": ["RJ45", "USB"], "keywords": ["connector type", "style", "family"]},
    "TYPE/SERIE": {"description": "Series or type", "unite": None, "exemples": [], "keywords": ["type", "series"]},
    "TERMINAISON": {"description": "Termination type", "unite": None, "exemples": ["Solder", "Crimp"], "keywords": ["termination", "mounting style", "connection"]},
    "NB ELEMENTS": {"description": "Number of elements", "unite": "Integer", "exemples": [], "keywords": ["positions", "contacts", "pins", "ways", "circuits", "number of positions"]},
    "OPTION": {"description": "Specific options", "unite": None, "exemples": ["With keying / polarizing"], "keywords": ["features", "options", "keying", "polarization", "latch"]},
    "OPTIONS": {"description": "Options", "unite": None, "exemples": [], "keywords": ["features", "options"]},
    "PAS": {"description": "Pin spacing (Pitch)", "unite": "mm", "exemples": ["2.54", "1.27"], "keywords": ["pitch", "spacing", "centerline", "pin pitch"]},
    "DIAMETRE VIS": {"description": "Screw diameter", "unite": "mm or M", "exemples": ["M3", "M4"], "keywords": ["screw size", "thread size"]},
    "NB CONTACTS": {"description": "Number of contacts", "unite": "Integer", "exemples": ["10", "40"], "keywords": ["number of positions", "contacts", "pins", "poles", "circuits"]},
    "NB CONTACTS / DIMENSIONS": {"description": "Nb of contacts and dimensions", "unite": None, "exemples": [], "keywords": ["contacts/size", "positions/dimensions"]},
    "INTERRUPTEUR": {"description": "Switch present", "unite": None, "exemples": ["Yes", "No"], "keywords": ["switch", "internal switch"]},
    "FILTRE": {"description": "Filter present (e.g. mains)", "unite": None, "exemples": ["Yes", "No"], "keywords": ["filter", "emi filter", "shielded"]},
    "FUSIBLE": {"description": "Fuse holder present", "unite": None, "exemples": ["Yes", "No"], "keywords": ["fuse", "fuse holder", "fused"]},
    "DIMENSIONS CABLE": {"description": "Cable section or diameter", "unite": "mm", "exemples": [], "keywords": ["cable diameter", "outer diameter", "od", "jacket diameter"]},
    "DIAMETRE POINTE": {"description": "Test probe diameter", "unite": "mm", "exemples": [], "keywords": ["tip diameter", "probe diameter", "contact size"]},
    "CONFIG BRIN": {"description": "Stranded or solid wire", "unite": None, "exemples": ["Stranded", "Solid"], "keywords": ["conductor", "stranding", "solid", "stranded"]},
    "JAUGE/SECTION": {"description": "Cable section", "unite": "AWG or mm²", "exemples": [], "keywords": ["awg", "cross section", "wire gauge", "conductor size"]},
    "CABLE_PLAT": {"description": "Flat cable", "unite": None, "exemples": ["Yes", "No"], "keywords": ["flat cable", "ribbon cable", "ffc", "fpc"]},
    "LONGUEUR": {"description": "Physical length", "unite": "mm or m", "exemples": ["1000", "500"], "keywords": ["length", "cable length", "l"]},
    "CONNECT A/B": {"description": "Connectors at ends A and B", "unite": None, "exemples": ["SMA-M / SMA-F"], "keywords": ["connector a", "connector b", "end a", "end b", "connector 1", "connector 2"]},
    "COULEUR FIL": {"description": "Jacket color", "unite": None, "exemples": ["Red", "Black"], "keywords": ["wire color", "jacket color", "insulation color"]},
    "BLINDAGE": {"description": "Shielding (STP, UTP, FTP)", "unite": None, "exemples": ["STP", "UTP"], "keywords": ["shielding", "shield", "screen", "braid", "foil", "shielded"]},
    "NB PAIRES": {"description": "Number of twisted pairs", "unite": "Integer", "exemples": ["4"], "keywords": ["pairs", "twisted pairs", "number of pairs"]},
    "DIAMETRE ou LARGEUR": {"description": "Diameter or width", "unite": "mm", "exemples": [], "keywords": ["diameter", "width", "dia", "w"]},
    "RATIO": {"description": "Shrink ratio (Heat shrink)", "unite": ":", "exemples": ["2:1", "3:1"], "keywords": ["shrink ratio", "recovery ratio"]},
    "FIXATION": {"description": "Fixing method", "unite": None, "exemples": ["Adhesive", "Screw"], "keywords": ["fastening", "mounting method", "attachment"]},
    "INDICE IP": {"description": "Ingress Protection (IP) rating", "unite": None, "exemples": ["IP67", "IP68"], "keywords": ["ip rating", "ingress protection", "protection degree", "environmental rating"]},

    # ==========================================
    # 8. OPTOELECTRONICS & FIBER
    # ==========================================
    "L.ONDE": {"description": "Dominant wavelength", "unite": "nm", "exemples": ["650"], "keywords": ["wavelength", "dominant wavelength", "peak wavelength", "lambda", "wd"]},
    "LONGUEUR ONDE": {"description": "Wavelength", "unite": "nm", "exemples": [], "keywords": ["wavelength", "wave length", "nm"]},
    "LONG. ONDE": {"description": "Wavelength", "unite": "nm", "exemples": [], "keywords": ["wavelength", "nm"]},
    "PUISS. OPTIQUE": {"description": "Optical or luminous power", "unite": "mW or mcd", "exemples": [], "keywords": ["luminous intensity", "radiant intensity", "optical power", "iv", "po", "brightness", "flux"]},
    "TENSION VF": {"description": "Forward Voltage", "unite": "V", "exemples": ["2.1", "3.3"], "keywords": ["forward voltage", "vf", "operating voltage"]},
    "COURANT TEST": {"description": "Test current", "unite": "mA", "exemples": ["20"], "keywords": ["test current", "if", "measurement current"]},
    "TYPE ECRAN": {"description": "Display technology", "unite": None, "exemples": ["LCD", "OLED", "TFT"], "keywords": ["display type", "panel type", "technology", "lcd", "oled", "tft"]},
    "RESOLUTION": {"description": "Spatial resolution", "unite": "Pixels", "exemples": ["128x64"], "keywords": ["resolution", "pixels", "format", "dot matrix"]},
    "P.SPECTRALE": {"description": "Spectral range", "unite": "nm", "exemples": ["400-700"], "keywords": ["spectral range", "bandwidth", "spectral sensitivity"]},
    "NB TUBE": {"description": "Number of pipes (light guide)", "unite": "Integer", "exemples": [], "keywords": ["light pipes", "channels", "ports"]},
    "DEBIT": {"description": "Data rate (Fiber)", "unite": "Mbps or Gbps", "exemples": ["1Gbps"], "keywords": ["data rate", "transmission rate", "bandwidth"]},
    "MATIERE CŒUR": {"description": "Core material", "unite": None, "exemples": ["Glass", "Plastic (POF)"], "keywords": ["core material", "fiber material"]},
    "DIAMETRE CŒUR": {"description": "Optical core diameter", "unite": "um", "exemples": ["50", "9"], "keywords": ["core diameter", "fiber diameter", "cladding"]},
    "FWHM": {"description": "Full width at half maximum (FWHM)", "unite": "nm", "exemples": [], "keywords": ["spectral bandwidth", "half width", "spectral line half width", "delta lambda", "fwhm"]},
    "EPAISSEUR": {"description": "Thickness", "unite": "mm", "exemples": [], "keywords": ["thickness", "depth"]},
    "TRAITEMENT": {"description": "Surface treatment", "unite": None, "exemples": ["Anti-reflective (AR)"], "keywords": ["coating", "ar coating", "surface treatment"]},
    "DIST. FOCALE": {"description": "Focal length", "unite": "mm", "exemples": ["10", "25"], "keywords": ["focal length", "fl"]},

    # ==========================================
    # 9. THERMAL DISSIPATION & PCB MECHANICS
    # ==========================================
    "RES. THERM": {"description": "Thermal resistance", "unite": "°C/W", "exemples": ["5", "12"], "keywords": ["thermal resistance", "rth", "theta", "thermal impedance", "theta ja", "theta jc"]},
    "BRUIT": {"description": "Noise level", "unite": "dBA", "exemples": ["25", "40"], "keywords": ["noise", "acoustic noise", "sound level", "spl"]},
    "FORME": {"description": "General shape", "unite": None, "exemples": ["Round", "Square"], "keywords": ["shape", "form", "profile", "geometry"]},
    "ENVELOPPE/QUALITE": {"description": "Enclosure type or quality", "unite": None, "exemples": [], "keywords": ["enclosure", "housing", "material grade"]},
    "SHORE": {"description": "Hardness (Seals, Pads)", "unite": "Shore A/D", "exemples": ["50A"], "keywords": ["hardness", "shore", "durometer"]},
    "TENUE EN T°": {"description": "Max temperature resistance", "unite": "°C", "exemples": ["150", "200"], "keywords": ["max temperature", "temperature rating", "thermal limit", "withstand temp", "continuous use temperature"]},
    "CONDUC. THERM": {"description": "Thermal conductivity", "unite": "W/mK", "exemples": ["1.5", "5"], "keywords": ["thermal conductivity", "k", "heat transfer coefficient"]},
    "RAIDEUR/FORCE": {"description": "Spring stiffness or force", "unite": "N/mm", "exemples": [], "keywords": ["spring rate", "stiffness", "operating force", "actuation force"]},
    "DIMENSIONS PASTILLE": {"description": "PCB pad dimensions", "unite": "mm", "exemples": [], "keywords": ["pad size", "pad dimension", "footprint size", "recommended pad"]},
    "VENTILATION (capots)": {"description": "Ventilation type (Vented/Solid)", "unite": None, "exemples": ["Vented"], "keywords": ["ventilation", "airflow", "cooling", "vented"]},
    "DIAM TROU / CMS": {"description": "Hole diameter or SMD", "unite": "mm", "exemples": [], "keywords": ["hole size", "drill size", "smd", "smt"]},
    "DIMENSIONS TROU": {"description": "Hole dimensions", "unite": "mm", "exemples": [], "keywords": ["hole dimension", "cutout size", "panel cutout"]},
    "TRANSFERT CHALEUR": {"description": "Heat transfer mode", "unite": None, "exemples": ["Peltier"], "keywords": ["heat transfer", "cooling method", "thermal management"]},
    "COURANT NOM": {"description": "Nominal current", "unite": "A", "exemples": [], "keywords": ["nominal current", "rated current"]},

    # ==========================================
    # 10. FASTENERS & STANDOFFS
    # ==========================================
    "FORME TETE": {"description": "Screw head shape", "unite": None, "exemples": ["Cylindrical", "Countersunk", "Hexagonal"], "keywords": ["head style", "head type", "drive type", "pan head", "flat head"]},
    "FILETAGE": {"description": "Thread type", "unite": "M", "exemples": ["M3", "M4"], "keywords": ["thread", "thread size", "pitch", "metric"]},
    "FILETAGE/D INT": {"description": "Thread or internal diameter", "unite": "mm or M", "exemples": [], "keywords": ["thread size", "inner diameter", "id", "clearance hole"]},
    "FORME/LARGEUR": {"description": "Shape and width", "unite": "mm", "exemples": ["Hexagonal 5.5"], "keywords": ["shape", "width across flats", "wrench size", "hex size"]},

    # ==========================================
    # 11. COMPUTING & READY-TO-USE BOARDS
    # ==========================================
    "CLASSE/VITESSE": {"description": "Speed class (SD Card)", "unite": None, "exemples": ["Class 10", "UHS-I"], "keywords": ["speed class", "uhs", "class", "performance class", "speed rating"]},
    "TYPE_PROC": {"description": "Processor family", "unite": None, "exemples": ["ARM Cortex-M4", "x86"], "keywords": ["processor", "cpu", "mcu", "core", "architecture", "microcontroller"]},
    "FREQ_PROC": {"description": "Processor frequency", "unite": "GHz or MHz", "exemples": ["1.2GHz"], "keywords": ["clock speed", "cpu frequency", "processor speed", "operating frequency"]},
    "RAM/DD": {"description": "RAM and Hard Drive", "unite": "GB", "exemples": ["4GB / 32GB"], "keywords": ["memory", "ram", "storage", "flash", "rom"]},
    "OS": {"description": "Provided Operating System", "unite": None, "exemples": ["Linux", "Windows 10 IoT"], "keywords": ["operating system", "os", "supported os", "software"]},
    "INTERFACE PROG": {"description": "Programming interface", "unite": None, "exemples": ["JTAG", "SWD"], "keywords": ["programming interface", "debug interface", "jtag", "swd", "icsp"]},
    "INTERFACE 1": {"description": "Primary hardware interface", "unite": None, "exemples": ["USB"], "keywords": ["primary interface", "host interface", "port", "usb", "ethernet", "gpio"]},
    "INTERFACE 2": {"description": "Secondary hardware interface", "unite": None, "exemples": ["Ethernet"], "keywords": ["secondary interface", "peripheral interface"]},
    "FORMAT/INTERFACE": {"description": "Form factor and interface", "unite": None, "exemples": ["PCIe", "M.2"], "keywords": ["form factor", "interface", "slot type", "m.2", "pcie"]},
    "FONCTION PRINCIPALE": {"description": "Module or board role", "unite": None, "exemples": ["Data acquisition", "Relay switching"], "keywords": ["function", "application", "description", "features", "module type"]},
}

def get_list_categories():
    
    # return list(DICTIONNAIRE.keys())
    return CATEGORIES

def get_list_subcategories(category:str):

    return SUB_CATEGORIES[category.upper().strip()]


def get_champs(category:str,subcategory:str):
    try:
        liste = list(DICTIONNAIRE[category][subcategory])
        dico=[]
        for index,champs in enumerate(liste):
            if champs==None:
                continue
            ligne = CHAMPS_METADATA[champs]
            ligne["index"]=index+1
            ligne["name"]=champs
            dico.append(ligne)
        return dico
    except Exception as e: 
        return f"Erreur Clé : {e}"

if __name__=="__main__":
    print(get_champs("COMMUTATION","BOUTON_POUSSOIR"))