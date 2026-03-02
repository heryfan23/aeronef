"""
MODÈLE INTÉGRATION: heures_vol_NEW.py

Ce fichier montre EXACTEMENT ce qu'il faut modifier dans heures_vol.py
pour intégrer le système d'automatisation des alertes.

INSTRUCTION: 
1. Ouvrir heures_vol.py existant
2. Ajouter les imports du système
3. Initialiser les gestionnaires dans __init__
4. Remplacer check_maintenance_alert() et save_heures()

Ou: Utiliser ce fichier comme référence pour les modifications.
"""

from PyQt6.QtWidgets import (QLineEdit, QWidget, QLabel, QPushButton, QFrame,
                             QTableWidget, QTableWidgetItem, QComboBox, 
                             QDateEdit, QMessageBox, QAbstractItemView, 
                             QMenu, QDialog, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

# ===== NOUVEAUX IMPORTS À AJOUTER =====
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem
# =====================================


class HeuresVol(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)
            
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        # ===== INITIALISER LES NOUVEAUX GESTIONNAIRES =====
        # Garder aussi self.conn et self.cursor pour compatibilité
        try:
            self.conn = sqlite3.connect("aviation.db")
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Erreur connexion BD: {e}")
        
        # Ajouter les gestionnaires du sistema d'automatisation
        self.db_manager = DatabaseManager()
        self.maintenance_automation = MaintenanceAutomationSystem(self.db_manager)
        # ===================================================
        
        # ... RESTE DU __init__ INCHANGÉ ...
        self.titre = QLabel("heures de vol", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        # ... tout le code UI reste identique ...
        # (ne pas copier toute la fonction, juste montrer les ajouts)
    
    # ========================================================================
    # MÉTHODE À REMPLACER: check_maintenance_alert
    # ========================================================================
    
    def check_maintenance_alert(self, immat, temps_cumul_str):
        """
        Vérifie si les heures de révision sont atteintes et déclenche les alertes automatiques
        VERSION AMÉLIORÉE avec système d'automatisation complet
        """
        try:
            # Convertir le temps cumul en heures décimales
            current_hours = self.maintenance_automation.convert_time_to_hours(temps_cumul_str)
            
            # Vérifier et créer les alertes automatiquement
            new_alerts = self.maintenance_automation.check_and_trigger_alerts(immat, current_hours)
            
            if new_alerts:
                # Construire le message d'alerte professionnel
                alert_text = f"""⚠️  ALERTES DE MAINTENANCE DÉTECTÉES

AÉRONEF: {immat}
HEURES ACCUMULÉES: {temps_cumul_str}
═══════════════════════════════════════════

"""
                
                # Ajouter chaque alerte avec ses détails
                for alert in new_alerts:
                    alert_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 {alert['type'].replace('MAINTENANCE_', '')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Seuil: {alert['hours']}h
Sévérité: {alert['severity']}
Description: {alert['description']}
"""
                
                # Ajouter le calendrier des prochaines maintenances
                schedule = self.maintenance_automation.get_next_maintenance_schedule(immat, current_hours)
                
                alert_text += f"""

═══════════════════════════════════════════
CALENDRIER DES PROCHAINES MAINTENANCES
═══════════════════════════════════════════
"""
                
                # Afficher les 5 prochaines révisions
                for item in schedule[:5]:
                    alert_text += f"""

📅 {item['seuil']}
   Heures totales: {item['heures_totales']}h
   Heures restantes: {item['heures_restantes']:.1f}h ({item['pourcentage']:.1f}%)
   {item['description']}
"""
                
                # Afficher le message d'alerte
                alert_msg = QMessageBox(self)
                alert_msg.setIcon(QMessageBox.Icon.Warning)
                alert_msg.setWindowTitle("⚠️  ALERTES DE MAINTENANCE AUTOMATIQUES")
                alert_msg.setText(alert_text)
                alert_msg.setStyleSheet("""
                    QMessageBox { 
                        background-color: #2d2d69; 
                    }
                    QMessageBox QLabel { 
                        color: white; 
                        font-weight: bold; 
                        font-family: 'Courier New';
                    }
                """)
                alert_msg.setMinimumWidth(700)
                alert_msg.setMinimumHeight(500)
                alert_msg.exec()
                
                return True
            else:
                # Vérifier s'il y a une alerte existante (pas de nouvelle)
                existing_alerts = self.db_manager.get_alerts_for_aircraft(immat)
                if existing_alerts:
                    # Afficher un message informatif
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setWindowTitle("ℹ️  Statut Maintenance")
                    msg.setText(f"""Aéronef: {immat}
Heures cumulées: {temps_cumul_str}

Alertes actives: {len(existing_alerts)}

Consultez le tableau de bord "Alertes & Maintenance" 
pour plus de détails et pour planifier les révisions.""")
                    msg.setStyleSheet("""
                        QMessageBox { 
                            background-color: #2d2d69; 
                        }
                        QMessageBox QLabel { 
                            color: white; 
                        }
                    """)
                    msg.exec()
                    return True
            
            return False
        
        except Exception as e:
            print(f'Erreur vérification maintenance automatique: {e}')
            QMessageBox.critical(self, "Erreur", f"Erreur système d'alertes: {e}")
            return False
    
    # ========================================================================
    # MÉTHODE À REMPLACER: save_heures
    # ========================================================================
    
    def save_heures(self):
        """
        Sauvegarde les heures de vol et déclenche automatiquement les alertes
        VERSION AMÉLIORÉE avec système d'automatisation
        """
        immat = self.immatriculation_input.currentText().strip()
        date_vol = self.date_vol.date().toString("yyyy-MM-dd")
        temps_vol = self.temps_vol.text().strip()
        temps_cumul = self.temps_cumul.text().strip()
        
        # Validation des champs obligatoires
        if not immat or not temps_vol:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur - Champs obligatoires")
            msg.setText("Veuillez remplir au moins l'immatriculation et le temps de vol.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        # Sauvegarder dans la BD (ancien système)
        try:
            self.cursor.execute(
                'INSERT INTO heures_vol (immatriculation, date_vol, temps_vol, temps_cumul) VALUES (?, ?, ?, ?)',
                (immat, date_vol, temps_vol, temps_cumul)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur insertion DB:', e)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Erreur")
            msg.setText(f"Erreur lors de l'enregistrement: {str(e)}")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        # ===== DÉCLENCHER AUTOMATIQUEMENT LES ALERTES (NOUVEAU) =====
        heures_check = temps_cumul if temps_cumul else temps_vol
        
        # Appeler la nouvelle méthode avec alertes automatiques
        alert_triggered = self.check_maintenance_alert(immat, heures_check)
        
        # Valider les changements dans la BD d'automatisation
        self.db_manager.commit()
        # =============================================================
        
        # Nettoyer les champs de saisie
        self.temps_vol.clear()
        self.temps_cumul.clear()
        self.date_vol.setDate(QDate.currentDate())
        
        # Recharger le tableau d'affichage
        self.load_heures()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_ajout_heure.hide()
        
        # Message de confirmation avec info sur les alertes
        confirme_text = f"✓ Heures de vol enregistrées pour {immat}\n\n"
        
        if alert_triggered:
            confirme_text += "Une ou plusieurs alertes de maintenance ont été détectées!\n\n"
            confirme_text += "Consultez le tableau de bord 'Alertes & Maintenance'\n"
            confirme_text += "pour planifier les révisions.\n"
        else:
            confirme_text += "Les alertes seront affichées automatiquement\n"
            confirme_text += "lorsque les seuils de maintenance seront atteints."
        
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("✓ Enregistrement Réussi")
        msg.setText(confirme_text)
        msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
        msg.exec()
    
    # ========================================================================
    # AUTRES MÉTHODES - KEEP EXISTING CODE (pas de modification nécessaire)
    # ========================================================================
    
    def load_immatriculations(self):
        """Charge tous les matricules depuis la table aircrafts - UNCHANGED"""
        try:
            self.cursor.execute('SELECT immatriculation FROM aircrafts ORDER BY immatriculation')
            immatriculations = self.cursor.fetchall()
            self.immatriculation_input.clear()
            for immat in immatriculations:
                self.immatriculation_input.addItem(immat[0])
        except Exception as e:
            print('Erreur chargement immatriculations:', e)
    
    # ... AUTRES MÉTHODES INCHANGÉES ...
    # load_heures(), calculate_totals(), validate_time_format(), etc.
    # (copier du fichier original)


# ========================================================================
# RÉSUMÉ DES MODIFICATIONS REQUISES
# ========================================================================

"""
✓ ÉTAPE 1: Ajouter les imports (ligne 4-5)
  from database_manager import DatabaseManager
  from maintenance_system import MaintenanceAutomationSystem

✓ ÉTAPE 2: Dans __init__, après la connection SQLite existante
  self.db_manager = DatabaseManager()
  self.maintenance_automation = MaintenanceAutomationSystem(self.db_manager)

✓ ÉTAPE 3: Remplacer complètement la méthode check_maintenance_alert()
  (Voir ci-dessus pour la nouvelle version)

✓ ÉTAPE 4: Remplacer complètement la méthode save_heures()
  (Voir ci-dessus pour la nouvelle version)

✓ ÉTAPE 5: Garder toutes les autres méthodes inchangées
  - load_immatriculations()
  - load_heures()
  - calculate_totals()
  - validate_time_format()
  - on_row_selected()
  - show_action_menu()
  - etc.

⚠️  IMPORTANT: 
  - Ne pas supprimer self.conn et self.cursor (toujours utilisés)
  - Garder toute l'interface UI inchangée
  - Le système d'automatisation fonctionne EN PARALLÈLE
  - Pas de refactoring majeur, juste des ajouts
"""
