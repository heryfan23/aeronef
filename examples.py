"""
EXEMPLES DE DÉPLOIEMENT ET TESTS DU SYSTÈME
============================================

Fichier avec exemples pratiques d'utilisation du système d'automatisation
"""

# =============================================================================
# EXEMPLE 1: TEST SIMPLE - Vérifier les alertes
# =============================================================================

def exemple_1_test_simple():
    """Test simple pour vérifier si le système fonctionne"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    # Initialiser
    db = DatabaseManager()
    maintenance = MaintenanceAutomationSystem(db)
    
    # Simulerun aéronef avec 25 heures
    immat = "N-12345"
    heures = 25.5
    
    print("🧪 TEST 1: Création d'alerte à 25h")
    print(f"   Aéronef: {immat}")
    print(f"   Heures: {heures}h")
    
    # Déclencher les alertes
    alertes = maintenance.check_and_trigger_alerts(immat, heures)
    
    print(f"\n   ✓ {len(alertes)} alerte(s) créée(s)")
    for alerte in alertes:
        print(f"      - {alerte['type']}: {alerte['description']}")
    
    # Afficher le calendrier
    schedule = maintenance.get_next_maintenance_schedule(immat, heures)
    print(f"\n   Calendrier des prochaines révisions:")
    for item in schedule[:3]:
        print(f"      - {item['seuil']}: {item['heures_restantes']:.1f}h restantes")
    
    db.close()


# =============================================================================
# EXEMPLE 2: SIMULATION DE VOL COMPLET
# =============================================================================

def exemple_2_simulation_complete():
    """Simule plusieurs  vols et génère des alertes progressives"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    db = DatabaseManager()
    maintenance = MaintenanceAutomationSystem(db)
    
    print("\n" + "="*60)
    print("🛫 SIMULATION: VOL D'UN CESSNA 172")
    print("="*60)
    
    # Aéronef
    immat = "N-CESSNA-172"
    heures_progression = [5, 15, 25, 35, 50, 75, 100, 150, 200]
    
    for heures in heures_progression:
        print(f"\n📊 Heures cumulées: {heures}h")
        
        # Vérifier alertes
        alertes = maintenance.check_and_trigger_alerts(immat, float(heures))
        
        if alertes:
            print(f"   🚨 {len(alertes)} nouvelles alerte(s):")
            for alerte in alertes:
                print(f"      ⚠️  {alerte['type']} - Sévérité: {alerte['severity']}")
        else:
            existing = db.get_alerts_for_aircraft(immat)
            if existing:
                print(f"   ℹ️  {len(existing)} alerte(s) existante(s) toujours active(s)")
            else:
                print(f"   ✓ Pas d'alerte")
    
    db.close()


# =============================================================================
# EXEMPLE 3: GÉNÉRATION DE RAPPORT
# =============================================================================

def exemple_3_generer_rapport():
    """Génère un rapport complet de maintenance"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    db = DatabaseManager()
    maintenance = MaintenanceAutomationSystem(db)
    
    print("\n" + "="*60)
    print("📄 RAPPORT DE MAINTENANCE")
    print("="*60)
    
    immat = "N-REPORT-001"
    
    # Générer le rapport
    rapport = maintenance.generate_maintenance_report(immat)
    print(rapport)
    
    db.close()


# =============================================================================
# EXEMPLE 4: EXPORT ET STATISTIQUES
# =============================================================================

def exemple_4_statistiques():
    """Affiche les statistiques globales"""
    
    from database_manager import DatabaseManager
    
    db = DatabaseManager()
    
    print("\n" + "="*60)
    print("📈 STATISTIQUES GLOBALES")
    print("="*60)
    
    # Aéronefs
    aircrafts = db.get_all_aircraft()
    print(f"\n✈️  Aéronefs enregistrés: {len(aircrafts)}")
    for immat in aircrafts[:5]:
        info = db.get_aircraft_info(immat)
        print(f"    - {immat}: {info.get('marque', 'N/A')}")
    
    # Alertes actives
    all_alerts = db.get_active_alerts()
    print(f"\n⚠️  Alertes actives: {len(all_alerts)}")
    
    alert_types = {}
    for alerte in all_alerts:
        alert_type = alerte['type_alerte']
        alert_types[alert_type] = alert_types.get(alert_type, 0) + 1
    
    for alert_type, count in sorted(alert_types.items()):
        print(f"    - {alert_type}: {count}")
    
    # Historique
    history = db.get_maintenance_history()
    print(f"\n📋 Maintenances enregistrées: {len(history)}")
    
    if history:
        print(f"    Dernière maintenance:")
        last = history[0]
        print(f"    - {last['immatriculation']}: {last['type_maintenance']}")
        print(f"      Date: {last['date_execution']}")
    
    db.close()


# =============================================================================
# EXEMPLE 5: INTÉGRATION PYQT6
# =============================================================================

def exemple_5_integration_pyqt():
    """Exemple d'intégration dans une classe PyQt6"""
    
    code = """
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem
from alertes_dashboard import AlertesDashboard

class MainWindowAvecAlertes(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Initialiser le système
        self.db = DatabaseManager()
        self.maintenance = MaintenanceAutomationSystem(self.db)
        
        # Créer le dashboard
        self.dashboard = AlertesDashboard()
        self.setCentralWidget(self.dashboard)
        
        self.setWindowTitle("Gestion de Vol - Avec Alertes")
        self.setGeometry(0, 0, 1400, 800)
    
    def afficher_alertes(self):
        # Charger les données
        self.dashboard.load_all_data()
        self.show()

# Utilisation
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = MainWindowAvecAlertes()
    window.afficher_alertes()
    sys.exit(app.exec())
    """
    
    print("\n" + "="*60)
    print("💻 EXEMPLE D'INTÉGRATION PYQT6")
    print("="*60)
    print(code)


# =============================================================================
# EXEMPLE 6: CONFIGURATION PERSONNALISÉE
# =============================================================================

def exemple_6_configuration_personnalisee():
    """Exemple de configuration pour une flotte spécifique"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    db = DatabaseManager()
    
    print("\n" + "="*60)
    print("⚙️  CONFIGURATION PERSONNALISÉE")
    print("="*60)
    
    # Ajouter des seuils personnalisés
    seuils_custom = {
        'HELICOPTER_500H': 500,      # Hélicoptère spécial
        'ULTRALIGHT_100H': 100,      # Ultraléger
        'COMMERCIAL_1500H': 1500,    # Commercial long-courrier
    }
    
    print("\n🔧 Seuils personnalisés:")
    for seuil, heures in seuils_custom.items():
        print(f"   - {seuil}: {heures}h")
    
    # Récupérer les seuils standard
    seuils_standard = db.get_maintenance_thresholds()
    
    print(f"\n📋 Seuils standard disponibles:")
    for seuil in seuils_standard[:5]:
        print(f"   - {seuil['component_type']}: {seuil['threshold_hours']}h")
        print(f"     {seuil['description']}")
    
    db.close()


# =============================================================================
# EXEMPLE 7: ALERTES CRITIQUES ET URGENTES
# =============================================================================

def exemple_7_alertes_critiques():
    """Affiche uniquement les alertes critiques"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    db = DatabaseManager()
    maintenance = MaintenanceAutomationSystem(db)
    
    print("\n" + "="*60)
    print("🚨 ALERTES CRITIQUES ET URGENTES")
    print("="*60)
    
    # Récupérer les alertes critiques
    critiques = maintenance.get_critical_alerts()
    
    print(f"\n⚠️  Alertes critiques (> 7 jours): {len(critiques)}")
    
    if critiques:
        for alerte in critiques:
            urgence_emoji = {
                'CRITIQUE': '🔴',
                'URGENT': '🟠',
                'IMPORTANT': '🟡'
            }
            emoji = urgence_emoji.get(alerte.get('urgence', 'NORMALE'), '⚪')
            
            print(f"\n{emoji} {alerte['immatriculation']} - {alerte['type_alerte']}")
            print(f"   Urgence: {alerte.get('urgence', 'N/A')}")
            print(f"   Depuis: {alerte['date_creation'][:10]}")
    else:
        print("   ✓ Aucune alerte critique")
    
    db.close()


# =============================================================================
# EXEMPLE 8: ESTIMATION DES DATES DE MAINTENANCE
# =============================================================================

def exemple_8_estimation_dates():
    """Estime les dates des prochaines maintenances"""
    
    from database_manager import DatabaseManager
    from maintenance_system import MaintenanceAutomationSystem
    
    db = DatabaseManager()
    maintenance = MaintenanceAutomationSystem(db)
    
    print("\n" + "="*60)
    print("📅 ESTIMATION DES DATES DE MAINTENANCE")
    print("="*60)
    
    immat = "N-ESTIMATION-001"
    heures_actuelles = 15.0
    heures_par_mois = 50  # Aéronef à 50h/mois
    
    estimations = maintenance.estimate_inspection_date(immat, heures_actuelles, heures_par_mois)
    
    print(f"\nAéronef: {immat}")
    print(f"Heures actuelles: {heures_actuelles}h")
    print(f"Moyenne: {heures_par_mois}h/mois")
    print(f"\n Estimations:")
    
    for seuil, data in sorted(estimations.items(), key=lambda x: x[1]['mois_estime']):
        print(f"\n   📊 {seuil}")
        print(f"      Heures restantes: {data['heures_restantes']:.1f}h")
        print(f"      Mois estimés: {data['mois_estime']:.1f}")
        print(f"      Date estimée: {data['date_estimee']}")
    
    db.close()


# =============================================================================
# SCRIPT DE TEST PRINCIPAL
# =============================================================================

def run_all_demos():
    """Exécute tous les exemples"""
    
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   DÉMONSTRATION DU SYSTÈME DE MAINTENANCE AUTOMATISÉ       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    try:
        exemple_1_test_simple()
        exemple_2_simulation_complete()
        exemple_3_generer_rapport()
        exemple_4_statistiques()
        exemple_5_integration_pyqt()
        exemple_6_configuration_personnalisee()
        exemple_7_alertes_critiques()
        exemple_8_estimation_dates()
        
        print("\n" + "="*60)
        print("✅ TOUS LES EXEMPLES EXÉCUTÉS AVEC SUCCÈS")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")


# =============================================================================
# TESTS UNITAIRES
# =============================================================================

class TestMaintenanceSystem:
    """Tests unitaires du système"""
    
    @staticmethod
    def test_conversion_temps():
        """Test la conversion de temps"""
        from maintenance_system import MaintenanceAutomationSystem
        
        maintenance = MaintenanceAutomationSystem()
        
        assert maintenance.convert_time_to_hours("25:30") == 25.5
        assert maintenance.convert_time_to_hours("1:00") == 1.0
        assert maintenance.convert_time_to_hours("10:00") == 10.0
        assert maintenance.convert_time_to_hours("100") == 100.0
        
        print("   ✓ Test conversion temps: OK")
    
    @staticmethod
    def test_seuils():
        """Test les seuils de maintenance"""
        from maintenance_system import MaintenanceAutomationSystem
        
        maintenance = MaintenanceAutomationSystem()
        
        # Vérifier que les seuils existent
        assert 25 in maintenance.STANDARD_THRESHOLDS.values()
        assert 50 in maintenance.STANDARD_THRESHOLDS.values()
        assert 100 in maintenance.STANDARD_THRESHOLDS.values()
        
        print("   ✓ Test seuils: OK")
    
    @staticmethod
    def test_severite():
        """Test le calcul de sévérité"""
        from maintenance_system import MaintenanceAutomationSystem
        
        maintenance = MaintenanceAutomationSystem()
        
        # Critique (dépassé de 20%)
        assert maintenance._calculate_severity(30, 25) == "CRITIQUE"
        
        # Urgent (atteint)
        assert maintenance._calculate_severity(25, 25) == "URGENT"
        
        # Haute (90%)
        assert maintenance._calculate_severity(90, 100) == "HAUTE"
        
        # Normale (moins de 90%)
        assert maintenance._calculate_severity(50, 100) == "NORMALE"
        
        print("    ✓ Test sévérité: OK")
    
    @staticmethod
    def run_tests():
        """Exécute tous les tests"""
        print("\n" + "="*60)
        print("🧪 TESTS UNITAIRES")
        print("="*60 + "\n")
        
        try:
            TestMaintenanceSystem.test_conversion_temps()
            TestMaintenanceSystem.test_seuils()
            TestMaintenanceSystem.test_severite()
            
            print("\n✅ Tous les tests passés avec succès!")
        except AssertionError as e:
            print(f"\n❌ Test échoué: {e}")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")


# =============================================================================
# POINT D'ENTRÉE
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        commande = sys.argv[1].lower()
        
        if commande == "demo":
            run_all_demos()
        elif commande == "test":
            TestMaintenanceSystem.run_tests()
        elif commande == "exemple1":
            exemple_1_test_simple()
        elif commande == "exemple2":
            exemple_2_simulation_complete()
        elif commande == "exemple3":
            exemple_3_generer_rapport()
        elif commande == "exemple4":
            exemple_4_statistiques()
        elif commande == "exemple5":
            exemple_5_integration_pyqt()
        elif commande == "exemple6":
            exemple_6_configuration_personnalisee()
        elif commande == "exemple7":
            exemple_7_alertes_critiques()
        elif commande == "exemple8":
            exemple_8_estimation_dates()
        else:
            print("Commandes disponibles:")
            print("  python examples.py demo          # Tous les exemples")
            print("  python examples.py test          # Tests unitaires")
            print("  python examples.py exemple1      # Test simple")
            print("  python examples.py exemple2      # Simulation vol")
            print("  python examples.py exemple3      # Générer rapport")
            print("  python examples.py exemple4      # Statistiques")
            print("  python examples.py exemple5      # Intégration PyQt")
            print("  python examples.py exemple6      # Configuration")
            print("  python examples.py exemple7      # Alertes critiques")
            print("  python examples.py exemple8      # Estimation dates")
    else:
        # Exécuter tout par défaut
        run_all_demos()
        TestMaintenanceSystem.run_tests()
