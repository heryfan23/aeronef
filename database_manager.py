"""
Gestionnaire centralisé de la base de données pour l'application Aviation
Permet une gestion cohérente et sécurisée de toutes les opérations de base de données
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

class DatabaseManager:
    """Gestionnaire centralisé pour toutes les opérations de base de données"""
    
    def __init__(self, db_path="aviation.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialise la connexion à la base de données et crée les tables si nécessaire"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # enforce fk behavior globally
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self._create_tables_if_not_exist()
            print("✓ Base de données initialisée avec succès")
        except Exception as e:
            print(f"✗ Erreur lors de l'initialisation de la base de données: {e}")
    
    def _create_tables_if_not_exist(self):
        """Crée les tables nécessaires si elles n'existent pas"""
        try:
            # Table des alertes de maintenance
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    type_alerte TEXT NOT NULL,
                    seuil_heures INTEGER NOT NULL,
                    statut TEXT DEFAULT 'ACTIVE',
                    date_creation TEXT DEFAULT CURRENT_TIMESTAMP,
                    date_programmation TEXT,
                    description TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            
            # Table de l'historique des maintenances
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    type_maintenance TEXT NOT NULL,
                    date_execution TEXT NOT NULL,
                    heures_vol_a_la_date INTEGER,
                    description TEXT,
                    technicien TEXT,
                    prochaine_alerte TEXT,
                    date_enregistrement TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            
            # Table des seuils de maintenance standards
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS maintenance_thresholds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    component_type TEXT NOT NULL,
                    threshold_hours INTEGER NOT NULL,
                    description TEXT,
                    is_active INTEGER DEFAULT 1
                )
            ''')
            
            self.conn.commit()
            self._insert_default_thresholds()
            
        except Exception as e:
            print(f"Erreur création des tables: {e}")
    
    def _insert_default_thresholds(self):
        """Insère les seuils de maintenance standard"""
        try:
            self.cursor.execute('SELECT COUNT(*) FROM maintenance_thresholds')
            if self.cursor.fetchone()[0] == 0:
                thresholds = [
                    ('25H_CHECK', 25, 'Inspection à 25 heures - Vérification générale et contrôle moteur'),
                    ('50H_CHECK', 50, 'Inspection à 50 heures - Révision complète moteurs'),
                    ('100H_CHECK', 100, 'Inspection à 100 heures - Révision majeure'),
                    ('200H_CHECK', 200, 'Inspection à 200 heures - Révision complète'),
                    ('600H_CHECK', 600, 'Inspection à 600 heures - Révision majeure'),
                    ('1200H_OVERHAUL', 1200, 'Grande révision 1200 heures'),
                    ('ENGINE_CONDITION', 500, 'Vérification de l\'état moteur'),
                    ('PROPELLER_CHECK', 200, 'Révision des hélices'),
                ]
                
                for component, hours, desc in thresholds:
                    self.cursor.execute(
                        'INSERT INTO maintenance_thresholds (component_type, threshold_hours, description) VALUES (?, ?, ?)',
                        (component, hours, desc)
                    )
                self.conn.commit()
                print("✓ Seuils de maintenance par défaut insérés")
        except Exception as e:
            print(f"Erreur insertion des seuils: {e}")
    
    # ===================== OPÉRATIONS ALERTES =====================
    
    def get_active_alerts(self) -> List[Dict]:
        """Récupère toutes les alertes actives"""
        try:
            self.cursor.execute('''
                SELECT id, immatriculation, type_alerte, seuil_heures, 
                       date_creation, date_programmation, description, statut
                FROM maintenance_alerts
                WHERE statut = 'ACTIVE'
                ORDER BY date_creation DESC
            ''')
            
            columns = ['id', 'immatriculation', 'type_alerte', 'seuil_heures', 
                      'date_creation', 'date_programmation', 'description', 'statut']
            alerts = []
            for row in self.cursor.fetchall():
                alerts.append(dict(zip(columns, row)))
            return alerts
        except Exception as e:
            print(f"Erreur récupération alertes: {e}")
            return []
    
    def get_alerts_for_aircraft(self, immatriculation: str) -> List[Dict]:
        """Récupère les alertes d'un aéronef spécifique"""
        try:
            self.cursor.execute('''
                SELECT id, immatriculation, type_alerte, seuil_heures, 
                       date_creation, date_programmation, description, statut
                FROM maintenance_alerts
                WHERE immatriculation = ?
                ORDER BY date_creation DESC
            ''', (immatriculation,))
            
            columns = ['id', 'immatriculation', 'type_alerte', 'seuil_heures', 
                      'date_creation', 'date_programmation', 'description', 'statut']
            alerts = []
            for row in self.cursor.fetchall():
                alerts.append(dict(zip(columns, row)))
            return alerts
        except Exception as e:
            print(f"Erreur: {e}")
            return []
    
    def create_alert(self, immatriculation: str, type_alerte: str, 
                    seuil_heures: int, description: str = "") -> bool:
        """Crée une nouvelle alerte de maintenance"""
        try:
            # Vérifier s'il existe déjà une alerte similaire active
            self.cursor.execute('''
                SELECT id FROM maintenance_alerts
                WHERE immatriculation = ? AND type_alerte = ? AND statut = 'ACTIVE'
            ''', (immatriculation, type_alerte))
            
            if self.cursor.fetchone():
                print(f"Alerte similaire déjà existante pour {immatriculation}")
                return False
            
            self.cursor.execute('''
                INSERT INTO maintenance_alerts 
                (immatriculation, type_alerte, seuil_heures, description)
                VALUES (?, ?, ?, ?)
            ''', (immatriculation, type_alerte, seuil_heures, description))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur création alerte: {e}")
            return False
    
    def close_alert(self, alert_id: int, date_programmation: str = None) -> bool:
        """Ferme une alerte (la marque comme traitée)"""
        try:
            self.cursor.execute('''
                UPDATE maintenance_alerts
                SET statut = 'TRAITEE', date_programmation = ?
                WHERE id = ?
            ''', (date_programmation or datetime.now().strftime("%Y-%m-%d"), alert_id))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur fermeture alerte: {e}")
            return False
    
    # ===================== OPÉRATIONS MAINTENANCE =====================
    
    def get_maintenance_history(self, immatriculation: str = None) -> List[Dict]:
        """Récupère l'historique des maintenances"""
        try:
            if immatriculation:
                self.cursor.execute('''
                    SELECT id, immatriculation, type_maintenance, date_execution,
                           heures_vol_a_la_date, description, technicien, prochaine_alerte
                    FROM maintenance_history
                    WHERE immatriculation = ?
                    ORDER BY date_execution DESC
                ''', (immatriculation,))
            else:
                self.cursor.execute('''
                    SELECT id, immatriculation, type_maintenance, date_execution,
                           heures_vol_a_la_date, description, technicien, prochaine_alerte
                    FROM maintenance_history
                    ORDER BY date_execution DESC
                ''')
            
            columns = ['id', 'immatriculation', 'type_maintenance', 'date_execution',
                      'heures_vol_a_la_date', 'description', 'technicien', 'prochaine_alerte']
            history = []
            for row in self.cursor.fetchall():
                history.append(dict(zip(columns, row)))
            return history
        except Exception as e:
            print(f"Erreur historique: {e}")
            return []
    
    def record_maintenance(self, immatriculation: str, type_maintenance: str,
                          date_execution: str, heures_vol: int = None,
                          description: str = "", technicien: str = "") -> bool:
        """Enregistre une maintenance effectuée"""
        try:
            self.cursor.execute('''
                INSERT INTO maintenance_history 
                (immatriculation, type_maintenance, date_execution, heures_vol_a_la_date, 
                 description, technicien, prochaine_alerte)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (immatriculation, type_maintenance, date_execution, heures_vol,
                  description, technicien, ""))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Erreur enregistrement maintenance: {e}")
            return False
    
    # ===================== OPÉRATIONS SEUILS =====================
    
    def get_maintenance_thresholds(self) -> List[Dict]:
        """Récupère tous les seuils de maintenance"""
        try:
            self.cursor.execute('''
                SELECT id, component_type, threshold_hours, description
                FROM maintenance_thresholds
                WHERE is_active = 1
                ORDER BY threshold_hours
            ''')
            
            columns = ['id', 'component_type', 'threshold_hours', 'description']
            thresholds = []
            for row in self.cursor.fetchall():
                thresholds.append(dict(zip(columns, row)))
            return thresholds
        except Exception as e:
            print(f"Erreur récupération seuils: {e}")
            return []
    
    # ===================== OPÉRATIONS GÉRÉ AÉRONEFS =====================
    
    def get_all_aircraft(self) -> List[str]:
        """Récupère tous les immatriculationditions"""
        try:
            self.cursor.execute('SELECT DISTINCT immatriculation FROM aircrafts ORDER BY immatriculation')
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Erreur récupération aéronefs: {e}")
            return []
    
    def get_aircraft_info(self, immatriculation: str) -> Optional[Dict]:
        """Récupère les infos d'un aéronef"""
        try:
            self.cursor.execute('''
                SELECT immatriculation, marque, serie, date_fabrication, 
                       proprietaire, heures_total
                FROM aircrafts
                WHERE immatriculation = ?
            ''', (immatriculation,))
            
            row = self.cursor.fetchone()
            if row:
                return {
                    'immatriculation': row[0],
                    'marque': row[1],
                    'serie': row[2],
                    'date_fabrication': row[3],
                    'proprietaire': row[4],
                    'heures_total': row[5]
                }
            return None
        except Exception as e:
            print(f"Erreur récupération info aéronef: {e}")
            return None
    
    # ===================== OPÉRATIONS UTILITAIRES =====================
    
    def execute_query(self, query: str, params: tuple = ()) -> List:
        """Execute une requête SQL personnalisée"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erreur exécution requête: {e}")
            return []
    
    def commit(self):
        """Valide les changements"""
        try:
            self.conn.commit()
        except Exception as e:
            print(f"Erreur commit: {e}")
    
    def close(self):
        """Ferme la connexion à la base de données"""
        try:
            if self.conn:
                self.conn.close()
                print("✓ Connexion base de données fermée")
        except Exception as e:
            print(f"Erreur fermeture BD: {e}")
