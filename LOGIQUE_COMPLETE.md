# 📊 LOGIQUE COMPLÈTE DU SYSTÈME DE GESTION DE VOL AÉRONEF

## 🎯 Vue d'ensemble générale

Ce logiciel est un système complet de gestion de maintenance aéronautique qui automatise les alertes de révision basées sur les heures de vol cumulées.

### Architecture du système:

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION PYQT6                        │
│                    (Interface Graphique)                     │
├─────────────────────────────────────────────────────────────┤
│   main.py ──→ login.py ──→ bienvenue.py (Écran Principal)  │
└──────────────────────────┬──────────────────────────────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    │                      │                      │
    ▼                      ▼                      ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ Modules      │    │ Maintenance  │    │ Alertes      │
│ Métier:      │    │ System:      │    │ Dashboard:   │
│              │    │              │    │              │
│ • ajout_info │    │ • database_  │    │ • alertes_   │
│ • heures_vol │    │   manager.py │    │   dashboard. │
│ • moteurs    │    │ • maintenance│    │   py         │
│ • helices    │    │   _system.py │    │              │
│ • travaux    │    │              │    │ (Tableau de  │
│ • ...autres  │    │              │    │  bord visuel)│
└──────────────┘    └──────────────┘    └──────────────┘
    │                      │                      │
    └──────────────────────┼──────────────────────┘
                           │
                           ▼
                ┌────────────────────────┐
                │  Base de Données       │
                │   (aviation.db)        │
                │                        │
                │ • aircrafts            │
                │ • heures_vol           │
                │ • moteurs              │
                │ • helices              │
                │ • maintenance_alerts   │
                │ • maintenance_history  │
                │ • maintenance_thresholds│
                └────────────────────────┘
```

---

## 🔄 Flux de Travail Principal

### Étape 1: Enregistrement d'un aéronef
```
Opérateur saisit:
├─ Immatriculation (ex: N-12345)
├─ Marque/Modèle (ex: CESSNA 172)
├─ Numéro de série
├─ Date de fabrication
├─ Propriétaire
└─ Heures totales

↓ Stockage dans: TABLE "aircrafts"
```

### Étape 2: Saisie des heures de vol
```
Opérateur saisit:
├─ Aéronef (sélection)
├─ Date du vol
├─ Temps de vol (25h30 = 25:30)
└─ Temps cumulé (ex: 25:30)

↓ Insertion dans: TABLE "heures_vol"

↓ DÉCLENCHE AUTOMATIQUEMENT (NEW):
  check_maintenance_alert(immatriculation, heures)
```

### Étape 3: Système d'alerte automatique (NOUVEAU)
```
convert_time_to_hours("25:30") → 25.5h

↓

check_and_trigger_alerts(immatriculation, 25.5)
│
├─ Vérifie 25h ✓ Alerte créée
├─ Vérifie 50h ✗ Pas atteint
├─ Vérifie 100h ✗ Pas atteint
├─ Vérifie 200h ✗ Pas atteint
└─ ...autres seuils

↓ Chaque alerte créée est enregistrée dans:
  TABLE "maintenance_alerts"
  
Location:
├─ id: 1
├─ immatriculation: N-12345
├─ type_alerte: MAINTENANCE_25H
├─ seuil_heures: 25
├─ statut: ACTIVE
├─ date_creation: 2024-02-25 14:30:00
└─ description: "Inspection de 25h..."
```

### Étape 4: Affichage des alertes
```
L'interface affiche IMMÉDIATEMENT:

⚠️  POP-UP ALERT MESSAGE:
   "L'aéronef N-12345 a atteint les révisions suivantes..."
   
   Seuil 25h → URGENT
   
   Calendrier des prochaines:
   ├─ 50h: 24.5h restantes
   ├─ 100h: 74.5h restantes
   └─ 200h: 174.5h restantes
```

### Étape 5: Tableau de bord de suivi
```
AlertesDashboard affiche 4 sections:

1️⃣  ALERTES CRITIQUES
   • Affiche les alertes > 7 jours
   • Code couleur (Rouge = CRITIQUE)
   
2️⃣  RÉSUMÉ PAR AÉRONEF
   • Nombre d'alertes actives
   • Dernière maintenance
   • Prochaine révision prévue
   
3️⃣  HISTORIQUE MAINTENANCES
   • Toutes les révisions effectuées
   • Dates, techniciens, descriptions
   
4️⃣  STATISTIQUES GLOBALES
   • Aéronefs connectés
   • Alertes actives totales
   • Maintenances enregistrées
```

---

## 📋 Seuils de Maintenance Standard

Automatiquement déclenchés selon les heures:

| Seuil | Nom | Description | Composants |
|-------|-----|-------------|-----------|
| **25h** | 25H_CHECK | Inspection légère | Moteur, Transmission |
| **50h** | 50H_CHECK | Révision moteur | Moteur, Hélice |
| **100h** | 100H_CHECK | Révision majeure | Tous systèmes |
| **200h** | 200H_CHECK | Révision complète | Tous systèmes |
| **500h** | PROPELLER | Révision hélice | Hélice uniquement |
| **600h** | 600H_CHECK | Grande révision | Tous systèmes |
| **1200h** | 1200H_OVERHAUL | Grand révision | Moteurs - Révision générale |

---

## 🚀 Système d'Étapes de Maintenance

### Pour Moteurs:
```
MAINTENANCE_25H
    ↓
MAINTENANCE_50H  ← Révision complète moteur
    ↓
MAINTENANCE_100H ← Inspection approfondie
    ↓
MAINTENANCE_600H ← Replacement potentiel
    ↓
MAINTENANCE_1200H ← Grand révision / Overhaul
```

### Pour Hélices:
```
MAINTENANCE_50H
    ↓
MAINTENANCE_200H ← Révision hélice
    ↓
MAINTENANCE_600H
```

---

## 💾 Structure de la Base de Données

### Table: aircrafts
```
┌──────────┬──────────────┬────────┬───────────────┐
│ COLONNE  │ TYPE         │ CLÉS   │ DESCRIPTION   │
├──────────┼──────────────┼────────┼───────────────┤
│ id       │ INTEGER      │ PK     │ Auto-incrément│
│ immat... │ TEXT         │ UNIQUE │ N-12345       │
│ marque   │ TEXT         │        │ CESSNA 172    │
│ serie    │ TEXT         │        │ Serial number │
│ date...  │ TEXT         │        │ YYYY-MM-DD    │
│ proprio  │ TEXT         │        │ Nom           │
│ heures.. │ TEXT         │        │ HH:MM         │
└──────────┴──────────────┴────────┴───────────────┘
```

### Table: heures_vol
```
┌──────────┬──────────────┬────────┬───────────────┐
│ COLONNE  │ TYPE         │ CLÉS   │ DESCRIPTION   │
├──────────┼──────────────┼────────┼───────────────┤
│ id       │ INTEGER      │ PK     │ Auto-incrément│
│ immat..  │ TEXT         │ FK     │ Lien aircraft │
│ date_vol │ TEXT         │        │ YYYY-MM-DD    │
│ temps_vol│ TEXT         │        │ HH:MM         │
│ temps... │ TEXT         │        │ Cumulé HH:MM  │
└──────────┴──────────────┴────────┴───────────────┘
```

### Table: maintenance_alerts (NOUVELLE)
```
┌──────────────┬──────────────┬────────┬────────────────────┐
│ COLONNE      │ TYPE         │ CLÉS   │ DESCRIPTION        │
├──────────────┼──────────────┼────────┼────────────────────┤
│ id           │ INTEGER      │ PK     │ Auto-incrément     │
│ immatr...    │ TEXT         │ FK     │ Lien aircraft      │
│ type_alerte  │ TEXT         │        │ MAINTENANCE_25H    │
│ seuil_heures │ INTEGER      │        │ 25, 50, 100, etc   │
│ statut       │ TEXT         │        │ ACTIVE/TRAITEE     │
│ date_creat.. │ TEXT         │        │ Timestamp création │
│ date_prog... │ TEXT         │        │ Programmé pour ..  │
│ description  │ TEXT         │        │ Détails révision   │
└──────────────┴──────────────┴────────┴────────────────────┘
```

### Table: maintenance_history (NOUVELLE)
```
┌──────────────┬──────────────┬────────┬────────────────────┐
│ COLONNE      │ TYPE         │ CLÉS   │ DESCRIPTION        │
├──────────────┼──────────────┼────────┼────────────────────┤
│ id           │ INTEGER      │ PK     │ Auto-incrément     │
│ immatr...    │ TEXT         │ FK     │ Lien aircraft      │
│ type_maint.. │ TEXT         │        │ Type de maintenance│
│ date_exec... │ TEXT         │        │ Quand fait         │
│ heures_vol   │ INTEGER      │        │ Heures à ce moment │
│ description  │ TEXT         │        │ Détails            │
│ technicien   │ TEXT         │        │ Nom du mécanicien  │
│ proch_alerte │ TEXT         │        │ Prochaine alerte   │
└──────────────┴──────────────┴────────┴────────────────────┘
```

---

## 🎓 Exemple Pratique Complet

### Scénario: Vol d'un Cessna 172

```
┌─────────────────────────────────────────────┐
│ JOUR 1: Enregistrement                      │
└─────────────────────────────────────────────┘

Saisir:
  Immatriculation: N-12345
  Marque: CESSNA 172
  Heures totales: 0h
  
→ Stocké dans TABLE "aircrafts"

┌─────────────────────────────────────────────┐
│ JOUR 30: Premier vol de 5 heures           │
└─────────────────────────────────────────────┘

Saisir:
  Aéronef: N-12345
  Date: 2024-01-15
  Temps vol: 5:00
  Temps cumulé: 5:00
  
→ Stocké dans TABLE "heures_vol"
→ Aucune alerte (5h < 25h)

┌─────────────────────────────────────────────┐
│ JOUR 60: Vol de 20 heures (cumulé: 25h)   │
└─────────────────────────────────────────────┘

Saisir:
  Temps cumulé: 25:00
  
↓ SYSTÈME DÉCLENCHE:

check_maintenance_alert("N-12345", 25.0)

  ✓ ALERTE_25H créée
  ✗ 50h pas atteint
  ✗ 100h pas atteint
  
↓ POP-UP AUTOMATIQUE:

⚠️  ALERTES DE MAINTENANCE - AÉRONEF N-12345
HEURES ACCUMULÉES: 25:00

━━━━━━━━━━━━━━━━━━━━━
🔧 MAINTENANCE_25H
━━━━━━━━━━━━━━━━━━━━━
Seuil: 25h
Sévérité: URGENT
Description: Inspection de 25h

CALENDRIER DES PROCHAINES MAINTENANCES:

📅 50H
   Total: 50h
   Restante: 25.0h (50.0%)
   Révision 50h - Inspection complète

📅 100H
   Total: 100h
   Restante: 75.0h (25.0%)
   Révision 100h - Révision majeure

↓ Alerte enregistrée dans TABLE "maintenance_alerts"
  [id: 1, immat: N-12345, type: MAINTENANCE_25H, 
   statut: ACTIVE, date: 2024-02-01 10:30:00]

┌─────────────────────────────────────────────┐
│ JOUR 70: Cumulé: 40h                       │
└─────────────────────────────────────────────┘

Saisir temps = 40:00

→ Vérifie: 25h ← Alerte existe déjà
         → Pas de nouvelle alerte
         
→ Affiche info: "Alerte 25h active depuis X jours"

┌─────────────────────────────────────────────┐
│ JOUR 85: Cumulé: 50.5h                     │
└─────────────────────────────────────────────┘

Saisir temps = 50:30

↓ SYSTÈME DÉCLENCHE:

check_maintenance_alert("N-12345", 50.5)

  ✓ ALERTE_25H (existante)
  ✓ ALERTE_50H créée  ← NOUVELLE !
  ✗ 100h pas atteint
  
↓ POP-UP:

⚠️  ALERTES DE MAINTENANCE

ALERTE NOUVELLE: MAINTENANCE_50H
Sévérité: URGENT
"Révision 50h - Inspection complète moteurs"

CALENDRIER:
  📅 100H: 49.5h restantes (49.5%)
  📅 200H: 149.5h restantes (25.2%)

↓ TABLE "maintenance_alerts" mise à jour:
  [id: 2, immat: N-12345, type: MAINTENANCE_50H, 
   statut: ACTIVE]

┌─────────────────────────────────────────────┐
│ TABLEAU DE BORD - Vue d'ensemble           │
└─────────────────────────────────────────────┘

ALERTES CRITIQUES:
┌─────────────┬────────────────┬─────────────┐
│ Aéronef     │ Type Alerte    │ Depuis (j)  │
├─────────────┼────────────────┼─────────────┤
│ N-12345     │ MAINTENANCE_25H│ 85 jours    │
│ N-12345     │ MAINTENANCE_50H│ 1 jour      │
└─────────────┴────────────────┴─────────────┘

RÉSUMÉ:
┌─────────────┬──────────┬──────────────┬──────────────┐
│ Aéronef     │ Actives  │ Dernière M.  │ Prochaine M. │
├─────────────┼──────────┼──────────────┼──────────────┤
│ N-12345     │ 2 alertes│ 2024-02-01   │ 50h (URGENT) │
└─────────────┴──────────┴──────────────┴──────────────┘
```

---

## 🔧 Configuration et Personnalisation

### Modifier les seuils (maintenance_system.py):

```python
STANDARD_THRESHOLDS = {
    '25H': 25,    # ← Modifier ici
    '50H': 50,
    '100H': 100,
    # Ajouter des seuils custom
    '1500H': 1500,  # Pour un aéronef spécifique
}
```

### Ajouter des seuils personnalisés par type:

```python
MAINTENANCE_PLANS = {
    'MOTEUR': [25, 50, 100, 200, 600, 1200],
    'HELICE': [50, 100, 200, 600],
    'CUSTOM_HYDRAULIQUE': [150, 300, 600],  # ← Ajout
}
```

---

## 📊 Rapports et Exports

Le système génère automatiquement:

1. **Rapports de maintenance** par aéronef
   - Alertes actives
   - Historique complet
   - Prochaines échéances

2. **Export CSV** des alertes
   - Pour statistiques externes
   - Compliance documentation

3. **Estimation de dates**
   - Basée sur heures par mois
   - Calendrier estimé jusqu'à 1200h

---

## ⚙️ Comment Intégrer le Système

### Fichiers à modifier:

1. **heures_vol.py** - Ajouter imports + modifier save_heures()
2. **bienvenue.py** - Ajouter AlertesDashboard + bouton
3. **Tous les modules** - Utiliser database_manager.py

### Étapes rapides:

```
1. Copier dans le dossier /aviation:
   ✓ database_manager.py
   ✓ maintenance_system.py
   ✓ alertes_dashboard.py

2. Modifier heures_vol.py (voir INTEGRATION_GUIDE.py)

3. Modifier bienvenue.py pour ajouter le bouton "Alertes"

4. Exécuter main.py

5. Tester: Créer un aéronef → Saisir heures → Voir alerte
```

---

## 📈 Bénéfices du Système

✅ **Automatisation complète** des alertes
✅ **Traçabilité** de tous les vols et maintenances
✅ **Prévention** des accidents par maintenance préventive
✅ **Conformité** aux normes aéronautiques
✅ **Rapports** détaillés pour audit
✅ **Alertes intelligentes** avec sévérité
✅ **Calendrier estimé** des prochaines révisions
✅ **Historique** complet de chaque aéronef

---

## 🎯 Cas d'Usage Avancés

### Alertes intelligentes:
```python
# Auto-génération de 25h, 50h, 100h, etc.
# Basée sur les heures réelles de vol saisies
# Sans intervention manuelle
```

### Gestion de flotte:
```python
# Tableau de bord centralisé de tous les aéronefs
# Vue des alertes prioritaires
# Planification automatique de maintenance
```

### Conformité aéronautique:
```python
# Suivi de chaque révision obligatoire
# Documentation imprimable/exportable
# Historique immuable
```

---

**Document créé le: 2024-02-25**
**Version: 1.0 - Système Automatisé Complet**
