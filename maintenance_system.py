"""
Système de maintenance automatisé pour la gestion des vols d'aéronefs
Gère les alertes, les seuils et la planification automatique de la maintenance
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from database_manager import DatabaseManager

class MaintenanceAutomationSystem:
    """Système automatisé pour la gestion de la maintenance préventive"""
    
    # Seuils standards en heures
    STANDARD_THRESHOLDS = {
        '25H': 25,
        '50H': 50,
        '100H': 100,
        '200H': 200,
        '500H': 500,  # Pour hélices
        '600H': 600,
        '1200H': 1200,
    }
    
    # Composants et leurs révisions
    MAINTENANCE_PLANS = {
        'MOTEUR': [25, 50, 100, 200, 600, 1200],
        'HELICE': [50, 100, 200, 600],
        'SYSTEME_HYDRAULIQUE': [100, 600],
        'TRAIN_ATTERRISSAGE': [100, 600],
        'SYSTEME_ELECTRIQUE': [200, 600],
        'REVISION_GENERALE': [25, 100, 600, 1200],
    }
    
    def __init__(self, db_manager: DatabaseManager = None):
        self.db = db_manager if db_manager else DatabaseManager()
    
    def convert_time_to_hours(self, time_str: str) -> float:
        
        """Convertit un temps au format hh:mm en heures décimales"""
        try:
            if ':' in time_str:
                hours, minutes = map(int, time_str.split(':'))
                return hours + (minutes / 60)
            else:
                return float(time_str)
        except:
            return 0
    
    def check_and_trigger_alerts(self, immatriculation: str, current_hours: float) -> List[Dict]:
        """
        Vérifie si des seuils de maintenance sont atteints et crée des alertes
        Retourne la liste des nouvelles alertes créées
        """
        alerts_created = []
        
        try:
            # Récupérer les alertes déjà existantes
            existing_alerts = self.db.get_alerts_for_aircraft(immatriculation)
            existing_types = [a['type_alerte'] for a in existing_alerts if a['statut'] == 'ACTIVE']
            
            # Vérifier chaque seuil standard
            for threshold_name, threshold_hours in self.STANDARD_THRESHOLDS.items():
                if current_hours >= threshold_hours:
                    alert_type = f"MAINTENANCE_{threshold_name}"
                    
                    if alert_type not in existing_types:
                        description = self._get_maintenance_description(threshold_hours)
                        
                        if self.db.create_alert(
                            immatriculation, 
                            alert_type, 
                            threshold_hours, 
                            description
                        ):
                            alerts_created.append({
                                'type': alert_type,
                                'hours': threshold_hours,
                                'description': description,
                                'severity': self._calculate_severity(current_hours, threshold_hours)
                            })
            
            return alerts_created
        except Exception as e:
            print(f"Erreur vérification alertes: {e}")
            return []
    
    def _get_maintenance_description(self, hours: int) -> str:
        """Retourne la description de maintenance pour un nombre d'heures"""
        descriptions = {
            25: "Inspection de 25h - Vérification générale et fonctionnement moteur",
            50: "Révision 50h - Inspection complète moteurs et systèmes",
            100: "Révision 100h - Révision majeure et contrôles complets",
            200: "Révision 200h - Maintenance complète de tous les systèmes",
            500: "Révision des hélices - Inspection complète et maintenance TSN",
            600: "Grande révision 600h - Révision majeure système et moteurs",
            1200: "Révision complète 1200h - Maintenance générale approfondie",
        }
        return descriptions.get(hours, f"Révision à {hours}h")
    
    def _calculate_severity(self, current_hours: float, threshold_hours: int) -> str:
        """Calcule la severité d'une alerte"""
        ratio = current_hours / threshold_hours
        
        if ratio >= 1.2:
            return "CRITIQUE"  # Dépassé de 20% ou plus
        elif ratio >= 1.0:
            return "URGENT"  # Atteint mais pas encore dépassé
        elif ratio >= 0.9:
            return "HAUTE"  # À moins de 10%
        else:
            return "NORMALE"
    
    def get_next_maintenance_schedule(self, immatriculation: str, current_hours: float) -> List[Dict]:
        """Retourne le calendrier des prochaines maintenances"""
        schedule = []
        
        for threshold_name, threshold_hours in sorted(self.STANDARD_THRESHOLDS.items(), 
                                                      key=lambda x: x[1]):
            if threshold_hours > current_hours:
                remaining_hours = threshold_hours - current_hours
                schedule.append({
                    'seuil': threshold_name,
                    'heures_totales': threshold_hours,
                    'heures_restantes': remaining_hours,
                    'pourcentage': (current_hours / threshold_hours) * 100,
                    'description': self._get_maintenance_description(threshold_hours)
                })
        
        return schedule
    
    def generate_maintenance_report(self, immatriculation: str) -> str:
        """Génère un rapport complet de maintenance"""
        try:
            aircraft_info = self.db.get_aircraft_info(immatriculation)
            active_alerts = self.db.get_alerts_for_aircraft(immatriculation)
            history = self.db.get_maintenance_history(immatriculation)
            
            report = f"""
╔══════════════════════════════════════════════════════════════╗
║         RAPPORT DE MAINTENANCE AÉRONEF                       ║
╚══════════════════════════════════════════════════════════════╝

━━ INFORMATIONS AÉRONEF ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Immatriculation: {immatriculation}
Marque/Modèle: {aircraft_info.get('marque', 'N/A') if aircraft_info else 'N/A'}
Numéro de série: {aircraft_info.get('serie', 'N/A') if aircraft_info else 'N/A'}
Heures totales: {aircraft_info.get('heures_total', 'N/A') if aircraft_info else 'N/A'}
Date de fabrication: {aircraft_info.get('date_fabrication', 'N/A') if aircraft_info else 'N/A'}
Propriétaire: {aircraft_info.get('proprietaire', 'N/A') if aircraft_info else 'N/A'}

━━ ALERTES ACTIVES ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            if active_alerts:
                for alert in active_alerts:
                    report += f"\n  ⚠️  {alert['type_alerte']}"
                    report += f"\n      Seuil: {alert['seuil_heures']}h"
                    report += f"\n      Status: {alert['statut']}"
                    report += f"\n      Créée le: {alert['date_creation']}\n"
            else:
                report += "\n  ✓ Aucune alerte active\n"
            
            report += f"""
━━ HISTORIQUE MAINTENANCE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            if history:
                for maintenance in history[:5]:  # Dernières 5
                    report += f"\n  • {maintenance['type_maintenance']}"
                    report += f" - {maintenance['date_execution']}"
                    if maintenance.get('description'):
                        report += f"\n    ({maintenance['description']})"
            else:
                report += "\n  Aucune maintenance enregistrée"
            
            report += "\n\n" + "═" * 60 + "\n"
            return report
        
        except Exception as e:
            return f"Erreur génération rapport: {e}"
    
    def estimate_inspection_date(self, immatriculation: str, current_hours: float, 
                                hours_per_month: float = 50) -> Dict:
        """
        Estime la date des prochaines inspections basée sur les heures par mois
        """
        estimations = {}
        
        for threshold_name, threshold_hours in sorted(self.STANDARD_THRESHOLDS.items(), 
                                                      key=lambda x: x[1]):
            if threshold_hours > current_hours:
                remaining_hours = threshold_hours - current_hours
                months_until = remaining_hours / hours_per_month if hours_per_month > 0 else 0
                estimated_date = datetime.now() + timedelta(days=months_until * 30)
                
                estimations[threshold_name] = {
                    'heures_restantes': remaining_hours,
                    'mois_estime': months_until,
                    'date_estimee': estimated_date.strftime("%Y-%m-%d"),
                    'total_heures': threshold_hours
                }
        
        return estimations
    
    def get_critical_alerts(self, immatriculation: str = None) -> List[Dict]:
        """Récupère uniquement les alertes critiques ou urgentes
        
        Exclut les alertes traitées, fermées ou archivées.
        """
        all_alerts = self.db.get_alerts_for_aircraft(immatriculation) if immatriculation \
                     else self.db.get_active_alerts()
        
        critical = []
        for alert in all_alerts:
            # Filtrer les alertes actives (exclure TRAITEE, FERMEE, ARCHIVEE, etc.)
            if alert['statut'] not in ('TRAITEE', 'FERMEE', 'ARCHIVEE', 'SUPPRIMEE'):
                if alert['statut'] == 'ACTIVE':
                    # Une alerte est critique si elle est activée depuis plus de 7 jours sans traitement
                    alert_date = datetime.strptime(alert['date_creation'], "%Y-%m-%d %H:%M:%S")
                    days_old = (datetime.now() - alert_date).days
                    
                    if days_old > 7:
                        alert['urgence'] = "CRITIQUE"
                    elif days_old > 3:
                        alert['urgence'] = "URGENT"
                    else:
                        alert['urgence'] = "IMPORTANT"
                    
                    critical.append(alert)
        
        return critical
    
    def check_future_maintenance_alerts(self, immatriculation: str, current_hours: float, 
                                       current_cycles: int = 0, hours_per_month: float = 50,
                                       cycles_per_month: float = 20) -> List[Dict]:
        """
        NOUVELLE ALERTE: Vérifie les maintenances prévues dans 1 mois
        
        Déclenche une alerte si :
        - Une maintenance sera atteinte dans 30 jours 
        - Les heures restantes <= 20h
        - Les cycles restants <= 20
        
        Args:
            immatriculation: Immatriculation de l'aéronef
            current_hours: Heures actuelles cumulées
            current_cycles: Cycles actuels cumulés
            hours_per_month: Estimation d'heures/mois (défaut 50)
            cycles_per_month: Estimation de cycles/mois (défaut 20)
            
        Returns:
            Liste des alertes futures créées
        """
        future_alerts = []
        
        try:
            # Calculer les heures et cycles prévus dans 30 jours
            estimated_hours_in_30d = current_hours + (hours_per_month)
            estimated_cycles_in_30d = current_cycles + (cycles_per_month)
            
            print(f"📅 Vérification alertes futures pour {immatriculation}")
            print(f"   Heures actuelles: {current_hours:.1f}h, Heures estimées +30j: {estimated_hours_in_30d:.1f}h")
            print(f"   Cycles actuels: {current_cycles}, Cycles estimés +30j: {estimated_cycles_in_30d}")
            
            # Vérifier chaque seuil de maintenance
            for threshold_name, threshold_hours in sorted(self.STANDARD_THRESHOLDS.items(), 
                                                         key=lambda x: x[1]):
                
                # Vérifier si ce seuil sera atteint dans 30 jours
                if current_hours < threshold_hours <= estimated_hours_in_30d:
                    
                    remaining_hours = threshold_hours - current_hours
                    # Estimer les cycles restants (proportionnel aux heures restantes)
                    remaining_cycles = max(0, int(estimated_cycles_in_30d - (threshold_hours - current_hours)))
                    
                    print(f"   ⚠️  Seuil {threshold_hours}h: heures restantes={remaining_hours:.1f}h, cycles restants~{remaining_cycles}")
                    
                    # ALERTE si: heures <= 20 ET cycles <= 20
                    if remaining_hours <= 20 and remaining_cycles <= 20:
                        alert_type = f"FUTURE_MAINTENANCE_{threshold_name}"
                        description = f"""
ALERTE MAINTENANCE FUTURE ({threshold_name})
Maintenance prévue dans ~30 jours
Heures restantes: {remaining_hours:.1f}h ({threshold_hours}h requis)
Cycles restants estimés: {remaining_cycles}
{self._get_maintenance_description(threshold_hours)}
"""
                        
                        # Vérifier que cette alerte n'existe pas déjà
                        existing_alerts = self.db.get_alerts_for_aircraft(immatriculation)
                        existing_types = [a['type_alerte'] for a in existing_alerts if a['statut'] == 'ACTIVE']
                        
                        if alert_type not in existing_types:
                            if self.db.create_alert(
                                immatriculation,
                                alert_type,
                                threshold_hours,
                                description
                            ):
                                future_alerts.append({
                                    'type': alert_type,
                                    'hours': threshold_hours,
                                    'remaining_hours': remaining_hours,
                                    'remaining_cycles': remaining_cycles,
                                    'description': description,
                                    'severity': "URGENTE_FUTURE",
                                    'days_until': 30
                                })
                                print(f"   ✓ Alerte future créée pour {threshold_name}")
                        else:
                            print(f"   → Alerte {alert_type} déjà existante")
            
            return future_alerts
            
        except Exception as e:
            print(f"❌ Erreur vérification alertes futures: {e}")
            return []
    
    def check_moteurs_helices_alerts(self) -> List[Dict]:
        """
        ALERTE MOTEURS/HÉLICES: Génère des alertes depuis les tables moteurs et hélices
        
        Crée une alerte si les critères suivants sont remplis:
        - pot_restant (heures) <= 20h
        - pot_restant_cycles <= 50
        - date_revision dans 30 jours
        
        Returns:
            Liste des alertes créées
        """
        alerts_created = []
        
        try:
            # Vérifier les moteurs
            print("🔧 Vérification des alertes MOTEURS...")
            alerts_created.extend(self._check_component_alerts('moteurs', 'MAINTENANCE_MOTEUR'))
            
            # Vérifier les hélices
            print("✈️  Vérification des alertes HÉLICES...")
            alerts_created.extend(self._check_component_alerts('helices', 'MAINTENANCE_HELICE'))
            
            return alerts_created
            
        except Exception as e:
            print(f"❌ Erreur vérification moteurs/hélices: {e}")
            return []
    
    def _check_component_alerts(self, table_name: str, alert_type_base: str) -> List[Dict]:
        """
        Vérifie les alertes pour un composant (moteur ou hélice)
        
        Args:
            table_name: 'moteurs' ou 'helices'
            alert_type_base: 'MAINTENANCE_MOTEUR' ou 'MAINTENANCE_HELICE'
        """
        alerts = []
        
        try:
            self.db.cursor.execute(f'''
                SELECT immatriculation, pot_restant, pot_restant_cycles, date_revision
                FROM {table_name}
                WHERE pot_restant IS NOT NULL AND pot_restant_cycles IS NOT NULL AND date_revision IS NOT NULL
            ''')
            
            rows = self.db.cursor.fetchall()
            print(f"  → {len(rows)} enregistrements trouvés dans {table_name}")
            
            for row in rows:
                immat = row[0]
                pot_restant = row[1]
                pot_restant_cycles = row[2]
                date_revision = row[3]
                
                # Convertir pot_restant en float
                try:
                    pot_restant_float = float(str(pot_restant).strip()) if pot_restant else 0
                except:
                    pot_restant_float = 0
                
                # Convertir pot_restant_cycles en int
                try:
                    pot_restant_cycles_int = int(str(pot_restant_cycles).strip()) if pot_restant_cycles else 0
                except:
                    pot_restant_cycles_int = 0
                
                # Vérifier si date est dans 30 jours
                is_date_in_30days = False
                try:
                    if date_revision:
                        date_revision_date = datetime.strptime(str(date_revision), "%Y-%m-%d").date()
                        today = datetime.now().date()
                        days_until = (date_revision_date - today).days
                        is_date_in_30days = 0 <= days_until <= 30
                except:
                    pass
                
                # ALERTE si tous les critères sont remplis
                if pot_restant_float <= 20 and pot_restant_cycles_int <= 50 and is_date_in_30days:
                    alert_type = f"{alert_type_base}_{immat}"
                    description = f"""
ALERTE MAINTENANCE {table_name.upper()}
Aéronef: {immat}
Heures restantes: {pot_restant_float:.1f}h (maximum 20h)
Cycles restants: {pot_restant_cycles_int} (maximum 50)
Date révision: {date_revision}
⚠️  MAINTENANCE URGENTE - À programmer immédiatement!
"""
                    
                    # Vérifier l'alerte n'existe pas déjà (y compris les TRAITEE récentes)
                    existing_alerts = self.db.get_alerts_for_aircraft(immat)
                    existing_types = [a['type_alerte'] for a in existing_alerts if a['statut'] in ('ACTIVE', 'TRAITEE')]
                    
                    if alert_type not in existing_types:
                        if self.db.create_alert(
                            immat,
                            alert_type,
                            int(pot_restant_float),
                            description
                        ):
                            alerts.append({
                                'type': alert_type,
                                'immat': immat,
                                'pot_restant': pot_restant_float,
                                'pot_restant_cycles': pot_restant_cycles_int,
                                'date_revision': date_revision,
                                'description': description,
                                'severity': 'CRITIQUE'
                            })
                            print(f"  ✓ Alerte créée pour {immat} ({table_name})")
                    else:
                        print(f"  → Alerte déjà existante pour {immat}")
            
            return alerts
            
        except Exception as e:
            print(f"❌ Erreur vérification {table_name}: {e}")
            return []
