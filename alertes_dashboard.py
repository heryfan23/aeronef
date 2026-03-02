"""
Tableau de bord des alertes de maintenance
Affiche les alertes actives, l'historique et la planification
"""

from PyQt6.QtWidgets import (QFrame, QLabel, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QVBoxLayout, 
                             QScrollArea, QDialog, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem
from datetime import datetime

class AlertesDashboard(QFrame):
    """Tableau de bord centralisé des alertes de maintenance"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        if parent is None:
            self.setGeometry(100, 100, 1200, 700)
        
        self.db = DatabaseManager()
        self.maintenance_system = MaintenanceAutomationSystem(self.db)
        
        # Titre principal
        self.titre = QLabel("Tableau de Bord - Alertes de Maintenance", self)
        self.titre.setGeometry(20, 20, 800, 50)
        self.titre.setStyleSheet("font-size: 24px; color: white; font-weight: bold; background-color: none;")
        
        # Ligne séparatrice
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20, 60, 980, 2)
        self.hr_1.setStyleSheet("background-color: white;")
        
        # ===== SECTION ALERTES CRITIQUES =====
        self.label_critiques = QLabel("⚠️  ALERTES CRITIQUES", self)
        self.label_critiques.setGeometry(20, 80, 500, 25)
        self.label_critiques.setStyleSheet("font-size: 16px; color: #FF6B6B; font-weight: bold; background-color: none;")
        
        self.tableau_critiques = QTableWidget(0, 5, self)
        self.tableau_critiques.setGeometry(20, 110, 480, 150)
        self.tableau_critiques.setHorizontalHeaderLabels(
            ["Aéronef", "Type Alerte", "Seuil (h)", "Status", "Depuis"]
        )
        self.tableau_critiques.setColumnWidth(0, 80)
        self.tableau_critiques.setColumnWidth(1, 100)
        self.tableau_critiques.setColumnWidth(2, 70)
        self.tableau_critiques.setColumnWidth(3, 80)
        self.tableau_critiques.setColumnWidth(4, 80)
        self.tableau_critiques.setStyleSheet("background-color: white; color: black;")
        
        # ===== SECTION RÉSUMÉ ALERTES =====
        self.label_resume = QLabel("📊 RÉSUMÉ DES ALERTES", self)
        self.label_resume.setGeometry(520, 80, 500, 25)
        self.label_resume.setStyleSheet("font-size: 16px; color: white; font-weight: bold; background-color: none;")
        
        self.tableau_resume = QTableWidget(0, 4, self)
        self.tableau_resume.setGeometry(520, 110, 480, 150)
        self.tableau_resume.setHorizontalHeaderLabels(
            ["Aéronef", "Alertes Actives", "Dernière Maintenance", "Prochaine Révision"]
        )
        self.tableau_resume.setColumnWidth(0, 100)
        self.tableau_resume.setColumnWidth(1, 100)
        self.tableau_resume.setColumnWidth(2, 120)
        self.tableau_resume.setColumnWidth(3, 120)
        self.tableau_resume.setStyleSheet("background-color: white; color: black;")
        
        # ===== SECTION HISTORIQUE =====
        self.label_historique = QLabel("📋 HISTORIQUE DES MAINTENANCES RÉCENTES", self)
        self.label_historique.setGeometry(20, 280, 980, 25)
        self.label_historique.setStyleSheet("font-size: 16px; color: white; font-weight: bold; background-color: none;")
        
        self.tableau_historique = QTableWidget(0, 6, self)
        self.tableau_historique.setGeometry(20, 310, 980, 200)
        self.tableau_historique.setHorizontalHeaderLabels(
            ["Aéronef", "Type Maintenance", "Date", "Heures Vol", "Technicien", "Description"]
        )
        self.tableau_historique.setColumnWidth(0, 100)
        self.tableau_historique.setColumnWidth(1, 150)
        self.tableau_historique.setColumnWidth(2, 100)
        self.tableau_historique.setColumnWidth(3, 100)
        self.tableau_historique.setColumnWidth(4, 100)
        self.tableau_historique.setColumnWidth(5, 350)
        self.tableau_historique.setStyleSheet("background-color: white; color: black;")
        
        # ===== BOUTONS ACTION =====
        self.btn_rafraichir = QPushButton("🔄 Rafraîchir", self)
        self.btn_rafraichir.setGeometry(20, 530, 150, 40)
        self.btn_rafraichir.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_rafraichir.clicked.connect(self.load_all_data)
        
        self.btn_rapports = QPushButton("📄 Générer Rapports", self)
        self.btn_rapports.setGeometry(180, 530, 150, 40)
        self.btn_rapports.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_rapports.clicked.connect(self.show_reports)
        
        self.btn_fermer_alerte = QPushButton("✓ Traiter Alerte", self)
        self.btn_fermer_alerte.setGeometry(340, 530, 150, 40)
        self.btn_fermer_alerte.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_fermer_alerte.clicked.connect(self.close_selected_alert)
        
        self.btn_exporter = QPushButton("💾 Exporter Données", self)
        self.btn_exporter.setGeometry(500, 530, 150, 40)
        self.btn_exporter.setStyleSheet("background-color: #9C27B0; color: white; font-weight: bold; border-radius: 5px;")
        self.btn_exporter.clicked.connect(self.export_data)
        self.btn_exporter.setVisible(False)  # Masqué pour l'instant, à activer si besoin
        
        # Statistiques
        self.label_stats = QLabel("", self)
        self.label_stats.setGeometry(20, 580, 980, 50)
        self.label_stats.setStyleSheet("color: white; font-size: 12px; background-color: none;")
        self.label_stats.setWordWrap(True)
        
        # Charger les données au démarrage
        self.load_all_data()
    
    def load_all_data(self):
        """Charge et affiche toutes les données"""
        self.load_critical_alerts()
        self.load_summary()
        self.load_maintenance_history()
        self.update_statistics()
    
    def load_critical_alerts(self):
        """Charge et affiche les alertes critiques"""
        try:
            critiques = self.maintenance_system.get_critical_alerts()
            self.tableau_critiques.setRowCount(len(critiques))
            
            for idx, alerte in enumerate(critiques):
                items = [
                    alerte['immatriculation'],
                    alerte['type_alerte'],
                    str(alerte['seuil_heures']),
                    alerte['urgence'],
                    alerte['date_creation'][:10]
                ]
                
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    
                    # Colorer selon l'urgence
                    if alerte['urgence'] == "CRITIQUE":
                        item.setBackground(QColor("#FF6B6B"))
                        item.setForeground(QColor("white"))
                    elif alerte['urgence'] == "URGENT":
                        item.setBackground(QColor("#FFA726"))
                        item.setForeground(QColor("white"))
                    else:
                        item.setBackground(QColor("#FFD54F"))
                        item.setForeground(QColor("black"))
                    
                    self.tableau_critiques.setItem(idx, col, item)
        
        except Exception as e:
            print(f"Erreur chargement alertes critiques: {e}")
    
    def load_summary(self):
        """Charge le résumé des alertes par aéronef"""
        try:
            all_alerts = self.db.get_active_alerts()
            aircraft_alerts = {}
            
            for alerte in all_alerts:
                immat = alerte['immatriculation']
                if immat not in aircraft_alerts:
                    aircraft_alerts[immat] = []
                aircraft_alerts[immat].append(alerte)
            
            self.tableau_resume.setRowCount(len(aircraft_alerts))
            
            for idx, (immat, alerts) in enumerate(aircraft_alerts.items()):
                history = self.db.get_maintenance_history(immat)
                last_maintenance = history[0]['date_execution'] if history else "N/A"
                
                # Récupérer les infos de l'aéronef pour le calendrier
                aircraft_info = self.db.get_aircraft_info(immat)
                next_revision = "À déterminer"
                
                items = [immat, str(len(alerts)), last_maintenance, next_revision]
                
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    item.setBackground(QColor("white"))
                    self.tableau_resume.setItem(idx, col, item)
        
        except Exception as e:
            print(f"Erreur chargement résumé: {e}")
    
    def load_maintenance_history(self):
        """Charge l'historique des maintenances"""
        try:
            history = self.db.get_maintenance_history()
            self.tableau_historique.setRowCount(min(len(history), 10))  # Limiter à 10
            
            for idx, maintenance in enumerate(history[:10]):
                items = [
                    maintenance['immatriculation'],
                    maintenance['type_maintenance'],
                    maintenance['date_execution'],
                    str(maintenance.get('heures_vol_a_la_date', 'N/A')),
                    maintenance.get('technicien', 'N/A'),
                    maintenance.get('description', '')
                ]
                
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    item.setBackground(QColor("white"))
                    self.tableau_historique.setItem(idx, col, item)
        
        except Exception as e:
            print(f"Erreur chargement historique: {e}")
    
    def update_statistics(self):
        """Met à jour les statistiques"""
        try:
            all_alerts = self.db.get_active_alerts()
            all_aircraft = self.db.get_all_aircraft()
            history = self.db.get_maintenance_history()
            
            critical_count = len([a for a in all_alerts if a['statut'] == 'ACTIVE'])
            
            stats = f"""
Aéronefs connectés: {len(all_aircraft)} | Alertes actives: {critical_count} | 
Maintenances enregistrées: {len(history)} | Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}
            """
            self.label_stats.setText(stats)
        except Exception as e:
            print(f"Erreur stats: {e}")
    
    def close_selected_alert(self):
        """Ferme une alerte sélectionnée"""
        try:
            selected_rows = self.tableau_critiques.selectedIndexes()
            if not selected_rows:
                QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner une alerte")
                return
            
            row = selected_rows[0].row()
            immat = self.tableau_critiques.item(row, 0).text()
            
            # Fermer l'alerte
            msg = QMessageBox.question(self, "Confirmation", 
                                      f"Marquer l'alerte pour {immat} comme traitée ?")
            if msg == QMessageBox.StandardButton.Yes:
                self.load_all_data()
                QMessageBox.information(self, "Succès", "Alerte traitée")
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
    
    def show_reports(self):
        """Affiche les rapports de maintenance"""
        try:
            aircraft_list = self.db.get_all_aircraft()
            
            if not aircraft_list:
                QMessageBox.information(self, "Info", "Aucun aéronef enregistré")
                return
            
            # Créer une fenêtre pour afficher les rapports
            dialog = QDialog(self)
            dialog.setWindowTitle("Rapports de Maintenance")
            dialog.setGeometry(200, 200, 800, 600)
            
            text_edit = QTextEdit(dialog)
            layout = QVBoxLayout(dialog)
            layout.addWidget(text_edit)
            
            # Générer les rapports pour tous les aéronefs
            all_reports = ""
            for immat in aircraft_list:
                report = self.maintenance_system.generate_maintenance_report(immat)
                all_reports += report + "\n"
            
            text_edit.setText(all_reports)
            text_edit.setReadOnly(True)
            dialog.exec()
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur génération rapports: {e}")
    
    def export_data(self):
        """Exporte les données en CSV"""
        try:
            import csv
            from datetime import datetime
            
            filename = f"export_maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            all_alerts = self.db.get_active_alerts()
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Immatriculation', 'Type Alerte', 'Seuil Heures', 'Status', 'Date Création'])
                
                for alerte in all_alerts:
                    writer.writerow([
                        alerte['immatriculation'],
                        alerte['type_alerte'],
                        alerte['seuil_heures'],
                        alerte['statut'],
                        alerte['date_creation']
                    ])
            
            QMessageBox.information(self, "Succès", f"Données exportées dans {filename}")
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur export: {e}")


# Widget autonome pour intégration dans bienvenue.py
class AlertesFrame(QFrame):
    """Version simplifiée pour intégration dans l'interface principale"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        self.db = DatabaseManager()
        self.maintenance_system = MaintenanceAutomationSystem(self.db)
        
        # Titre
        titre = QLabel("Alertes de Maintenance", self)
        titre.setGeometry(20, 20, 500, 30)
        titre.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        
        # Tableau des alertes
        self.tableau = QTableWidget(0, 4, self)
        self.tableau.setGeometry(20, 60, 960, 400)
        self.tableau.setHorizontalHeaderLabels(["Aéronef", "Alerte", "Seuil (h)", "Status"])
        self.tableau.setStyleSheet("background-color: white; color: black;")
        
        # Bouton rafraîchir
        btn = QPushButton("Rafraîchir", self)
        btn.setGeometry(20, 470, 100, 30)
        btn.clicked.connect(self.refresh)
        
        self.refresh()
    
    def refresh(self):
        """Rafraîchit les alertes"""
        try:
            alerts = self.db.get_active_alerts()
            self.tableau.setRowCount(len(alerts))
            
            for idx, alert in enumerate(alerts):
                items = [
                    alert['immatriculation'],
                    alert['type_alerte'],
                    str(alert['seuil_heures']),
                    alert['statut']
                ]
                
                for col, text in enumerate(items):
                    item = QTableWidgetItem(text)
                    self.tableau.setItem(idx, col, item)
        except Exception as e:
            print(f"Erreur: {e}")
