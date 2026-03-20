#!/usr/bin/env python3
"""
Script de diagnostic pour les alertes de maintenance
Vérifie l'état de la base de données et identifie les problèmes
"""

import sqlite3
import os
from datetime import datetime
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem

def main():
    """Lance le diagnostic complet des alertes"""
    print("=" * 80)
    print("🔍 DIAGNOSTIC DES ALERTES DE MAINTENANCE")
    print("=" * 80)
    print()
    
    # 1. Vérifier la connexion à la base de données
    print("1️⃣  VÉRIFICATION DE LA BASE DE DONNÉES")
    print("-" * 80)
    try:
        db = DatabaseManager()
        print("✓ Connexion à la base de données établie")
        print(f"  Chemin: {db.db_path}")
        print(f"  Existe: {os.path.exists(db.db_path)}")
    except Exception as e:
        print(f"❌ Erreur connexion BD: {e}")
        return
    
    print()
    
    # 2. Vérifier la table des alertes de maintenance
    print("2️⃣  VÉRIFICATION DE LA TABLE 'maintenance_alerts'")
    print("-" * 80)
    try:
        db.cursor.execute("SELECT COUNT(*) FROM maintenance_alerts")
        count = db.cursor.fetchone()[0]
        print(f"✓ Nombre d'alertes dans la table: {count}")
        
        if count > 0:
            print("\n  Aperçu des alertes:")
            db.cursor.execute("""
                SELECT id, immatriculation, type_alerte, seuil_heures, 
                       statut, date_creation FROM maintenance_alerts LIMIT 5
            """)
            for row in db.cursor.fetchall():
                print(f"    ID:{row[0]} | {row[1]} | {row[2]} | "
                      f"Seuil:{row[3]}h | Status:{row[4]} | "
                      f"Créée:{row[5]}")
        else:
            print("⚠️  Aucune alerte détectée dans la table!")
    
    except sqlite3.OperationalError as e:
        print(f"❌ Table 'maintenance_alerts' n'existe pas: {e}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # 3. Vérifier les aéronefs
    print("3️⃣  VÉRIFICATION DES AÉRONEFS")
    print("-" * 80)
    try:
        aircraft = db.get_all_aircraft()
        print(f"✓ Nombre d'aéronefs enregistrés: {len(aircraft)}")
        
        if aircraft:
            print("  Aéronefs:")
            for immat in aircraft[:10]:
                print(f"    - {immat}")
            if len(aircraft) > 10:
                print(f"    ... et {len(aircraft) - 10} autres")
        else:
            print("⚠️  Aucun aéronef enregistré!")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # 4. Tester la récupération des alertes
    print("4️⃣  TEST DE RÉCUPÉRATION DES ALERTES")
    print("-" * 80)
    try:
        alerts = db.get_active_alerts()
        print(f"✓ Alertes actives récupérées: {len(alerts)}")
        
        if alerts:
            print("\n  Détails des alertes:")
            for i, alert in enumerate(alerts[:3], 1):
                print(f"\n  Alerte {i}:")
                for key, value in alert.items():
                    print(f"    {key}: {value}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # 5. Tester le système de maintenance
    print("5️⃣  TEST DU SYSTÈME DE MAINTENANCE AUTOMATISÉ")
    print("-" * 80)
    try:
        maintenance_system = MaintenanceAutomationSystem(db)
        
        # Tester la récupération des alertes critiques
        critiques = maintenance_system.get_critical_alerts()
        print(f"✓ Alertes critiques: {len(critiques)}")
        
        if critiques:
            print("\n  Alertes critiques détaillées:")
            for i, alert in enumerate(critiques[:3], 1):
                print(f"\n  Alerte {i}:")
                for key, value in alert.items():
                    print(f"    {key}: {value}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # 6. Vérifier l'historique des maintenances
    print("6️⃣  VÉRIFICATION DE L'HISTORIQUE DES MAINTENANCES")
    print("-" * 80)
    try:
        history = db.get_maintenance_history()
        print(f"✓ Entrées d'historique: {len(history)}")
        
        if history:
            print("\n  Dernières maintenances:")
            for i, maintenance in enumerate(history[:3], 1):
                print(f"\n  Maintenance {i}:")
                for key, value in maintenance.items():
                    print(f"    {key}: {value}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    print("=" * 80)
    print("✓ DIAGNOSTIC TERMINÉ")
    print("=" * 80)

if __name__ == "__main__":
    main()
