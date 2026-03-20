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
    """Tableau de bord centralisé des alertes de maintenance
    
    Affiche les alertes critiques, le résumé des alertes par aéronef,
    l'historique des maintenances et les statistiques générales.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuration du style du widget
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        if parent is None:
            self.setGeometry(100, 100, 1200, 700)
        
        # Initialisation des gestionnaires de base de données
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
        """Charge et affiche toutes les données du tableau de bord"""
        print("🔄 Actualisation des données du tableau de bord...")
        
        # 1️⃣  Vérifier les alertes depuis moteurs et hélices
        print("🔧 Vérification des alertes moteurs/hélices...")
        try:
            moteurs_helices_alerts = self.maintenance_system.check_moteurs_helices_alerts()
            if moteurs_helices_alerts:
                print(f"✓ {len(moteurs_helices_alerts)} alerte(s) moteurs/hélices créée(s)")
        except Exception as e:
            print(f"⚠️  Erreur vérification moteurs/hélices: {e}")
        
        # 2️⃣  Charger les alertes critiques
        self.load_critical_alerts()
        self.load_summary()
        self.load_maintenance_history()
        self.update_statistics()
    
    def load_critical_alerts(self):
        """Charge et affiche les alertes critiques dans le tableau
        
        Les alertes sont classées par urgence (CRITIQUE, URGENT, IMPORTANT)
        selon leur ancienneté et leur statut d'activation.
        """
        try:
            # Récupérer les alertes critiques du système de maintenance
            critiques = self.maintenance_system.get_critical_alerts()
            print(f"📊 Alertes critiques trouvées: {len(critiques)}")
            
            # Configurer le nombre de lignes du tableau
            self.tableau_critiques.setRowCount(len(critiques))
            
            if len(critiques) == 0:
                print("⚠️  Aucune alerte critique détectée")
            
            # Remplir chaque ligne avec les données d'alerte
            for idx, alerte in enumerate(critiques):
                # Préparer les colonnes: Aéronef, Type Alerte, Seuil (h), Status, Depuis
                items = [
                    alerte['immatriculation'],
                    alerte['type_alerte'],
                    str(alerte['seuil_heures']),
                    alerte['urgence'],
                    alerte['date_creation'][:10]
                ]
                
                # Ajouter chaque colonne et appliquer les couleurs selon l'urgence
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    
                    # Colorer selon le niveau d'urgence
                    if alerte['urgence'] == "CRITIQUE":
                        # Rouge vif pour CRITIQUE
                        item.setBackground(QColor("#FF6B6B"))
                        item.setForeground(QColor("white"))
                    elif alerte['urgence'] == "URGENT":
                        # Orange pour URGENT
                        item.setBackground(QColor("#FFA726"))
                        item.setForeground(QColor("white"))
                    else:
                        # Jaune pour IMPORTANT
                        item.setBackground(QColor("#FFD54F"))
                        item.setForeground(QColor("black"))
                    
                    self.tableau_critiques.setItem(idx, col, item)
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement des alertes critiques: {e}")
            import traceback
            traceback.print_exc()
    
    def load_summary(self):
        """Charge et affiche le résumé des alertes par aéronef
        
        Pour chaque aéronef, affiche le nombre d'alertes actives,
        la date de la dernière maintenance et la prochaine révision prévue.
        """
        try:
            # Récupérer toutes les alertes actives
            all_alerts = self.db.get_active_alerts()
            print(f"📋 Alertes actives totales: {len(all_alerts)}")
            
            # Regrouper les alertes par immatriculation
            aircraft_alerts = {}
            for alerte in all_alerts:
                immat = alerte['immatriculation']
                if immat not in aircraft_alerts:
                    aircraft_alerts[immat] = []
                aircraft_alerts[immat].append(alerte)
            
            print(f"✈️  Aéronefs avec alertes: {len(aircraft_alerts)}")
            
            # Configurer le nombre de lignes du tableau résumé
            self.tableau_resume.setRowCount(len(aircraft_alerts))
            
            # Remplir le tableau avec les données de chaque aéronef
            for idx, (immat, alerts) in enumerate(aircraft_alerts.items()):
                # Récupérer l'historique des maintenances pour cet aéronef
                history = self.db.get_maintenance_history(immat)
                last_maintenance = history[0]['date_execution'] if history else "N/A"
                
                # Récupérer les informations de l'aéronef
                aircraft_info = self.db.get_aircraft_info(immat)
                next_revision = "À déterminer"  # Valeur par défaut
                
                # Préparer les colonnes: Aéronef, Alertes Actives, Dernière Maintenance, Prochaine Révision
                items = [immat, str(len(alerts)), last_maintenance, next_revision]
                
                # Ajouter chaque colonne au tableau
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    item.setBackground(QColor("white"))
                    self.tableau_resume.setItem(idx, col, item)
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement du résumé: {e}")
            import traceback
            traceback.print_exc()
    
    def load_maintenance_history(self):
        """Charge et affiche l'historique des maintenances récentes
        
        Affiche les 10 dernières interventions de maintenance effectuées
        avec les détails complets (aéronef, date, type, technicien, etc.).
        """
        try:
            # Récupérer tout l'historique des maintenances
            history = self.db.get_maintenance_history()
            print(f"📜 Entrées d'historique trouvées: {len(history)}")
            
            # Limiter l'affichage aux 10 dernières maintenances
            display_count = min(len(history), 10)
            self.tableau_historique.setRowCount(display_count)
            
            # Remplir le tableau avec les données d'historique
            for idx, maintenance in enumerate(history[:10]):
                # Préparer les colonnes: Aéronef, Type Maintenance, Date, Heures Vol, Technicien, Description
                items = [
                    maintenance['immatriculation'],
                    maintenance['type_maintenance'],
                    maintenance['date_execution'],
                    str(maintenance.get('heures_vol_a_la_date', 'N/A')),
                    maintenance.get('technicien', 'N/A'),
                    maintenance.get('description', '')
                ]
                
                # Ajouter chaque colonne au tableau
                for col, item_text in enumerate(items):
                    item = QTableWidgetItem(item_text)
                    item.setBackground(QColor("white"))
                    self.tableau_historique.setItem(idx, col, item)
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement de l'historique: {e}")
            import traceback
            traceback.print_exc()
    
    def update_statistics(self):
        """Met à jour les statistiques générales du tableau de bord
        
        Affiche le nombre d'aéronefs connectés, d'alertes actives,
        de maintenances enregistrées et l'heure de la dernière actualisation.
        """
        try:
            # Récupérer les données pour les statistiques
            all_alerts = self.db.get_active_alerts()
            all_aircraft = self.db.get_all_aircraft()
            history = self.db.get_maintenance_history()
            
            # Compter les alertes actives (toutes les alertes retournées sont actives)
            critical_count = len(all_alerts)
            
            print(f"📈 Statistiques: {len(all_aircraft)} aéronefs, {critical_count} alertes, {len(history)} maintenances")
            
            # Formater le texte des statistiques
            stats = f"""
Aéronefs connectés: {len(all_aircraft)} | Alertes actives: {critical_count} | 
Maintenances enregistrées: {len(history)} | Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}
            """
            self.label_stats.setText(stats)
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des statistiques: {e}")
            import traceback
            traceback.print_exc()
    
    def close_selected_alert(self):
        """Marque une alerte sélectionnée comme traitée
        
        - Récupère les données de l'alerte
        - Demande confirmation
        - Enregistre la maintenance dans l'historique
        - Marque l'alerte comme TRAITEE
        - Actualise l'affichage
        """
        try:
            # Récupérer la ligne sélectionnée dans le tableau
            selected_rows = self.tableau_critiques.selectedIndexes()
            if not selected_rows:
                QMessageBox.warning(self, "Avertissement", "Veuillez sélectionner une alerte")
                return
            
            # Extraire les données de la ligne sélectionnée
            row = selected_rows[0].row()
            immat = self.tableau_critiques.item(row, 0).text()
            type_alerte = self.tableau_critiques.item(row, 1).text()
            seuil_heures = self.tableau_critiques.item(row, 2).text()
            
            # Récupérer l'ID de l'alerte dans la base de données
            self.db.cursor.execute(
                'SELECT id FROM maintenance_alerts WHERE immatriculation=? AND type_alerte=? AND statut=?',
                (immat, type_alerte, 'ACTIVE')
            )
            result = self.db.cursor.fetchone()
            if not result:
                QMessageBox.warning(self, "Erreur", "Alerte non trouvée")
                return
            
            alert_id = result[0]
            print(f"📋 Traitement de l'alerte ID={alert_id}")
            
            # Demander une confirmation avant la fermeture
            msg = QMessageBox.question(self, "Confirmation", 
                                      f"Enregistrer la maintenance pour {immat} ?\n"
                                      f"Alerte: {type_alerte}\n"
                                      f"Seuil: {seuil_heures}h")
            if msg != QMessageBox.StandardButton.Yes:
                return
            
            # Récupérer les heures actuelles de l'aéronef
            try:
                self.db.cursor.execute(
                    'SELECT SUM(CAST(temps_vol AS FLOAT)) as total_heures FROM heures_vol WHERE immatriculation=?',
                    (immat,)
                )
                row_heures = self.db.cursor.fetchone()
                heures_vol = int(row_heures[0]) if row_heures and row_heures[0] else 0
            except:
                heures_vol = None
            
            # Enregistrer la maintenance dans l'historique
            date_execution = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            description = f"Maintenance effectuée suite à alerte: {type_alerte}"
            
            self.db.cursor.execute(
                'INSERT INTO maintenance_history '
                '(immatriculation, type_maintenance, date_execution, heures_vol_a_la_date, description) '
                'VALUES (?, ?, ?, ?, ?)',
                (immat, type_alerte, date_execution, heures_vol, description)
            )
            print(f"  ✓ Maintenance enregistrée dans l'historique")
            
            # Marquer l'alerte comme TRAITEE
            self.db.cursor.execute(
                'UPDATE maintenance_alerts SET statut=?, date_programmation=? WHERE id=?',
                ('TRAITEE', date_execution, alert_id)
            )
            print(f"  ✓ Alerte marquée comme TRAITEE")
            
            self.db.conn.commit()
            print(f"  ✓ Données sauvegardées")
            
            # Vérifier que l'alerte est bien TRAITEE
            self.db.cursor.execute(
                'SELECT statut FROM maintenance_alerts WHERE id=?',
                (alert_id,)
            )
            check = self.db.cursor.fetchone()
            print(f"  Vérification: alerte ID={alert_id} statut={check[0] if check else 'NOT FOUND'}")
            
            # Actualiser l'affichage
            print(f"🔄 Rafraîchissement de l'affichage...")
            self.load_all_data()
            
            QMessageBox.information(
                self, 
                "✓ Succès", 
                f"Maintenance enregistrée :\n"
                f"- Aéronef: {immat}\n"
                f"- Type: {type_alerte}\n"
                f"- Date: {date_execution}\n"
                f"- Heures: {heures_vol}h\n\n"
                f"L'alerte a été supprimée de la liste."
            )
        
        except Exception as e:
            print(f"❌ Erreur lors de la fermeture de l'alerte: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Erreur", f"Erreur: {e}")
    
    def show_reports(self):
        """Affiche les rapports de maintenance détaillés pour tous les aéronefs
        
        Génère et affiche un rapport complet pour chaque aéronef connecté
        incluant l'état des maintenances, les alertes et les révisions prévues.
        """
        try:
            # Récupérer la liste de tous les aéronefs
            aircraft_list = self.db.get_all_aircraft()
            print(f"📄 Génération de rapports pour {len(aircraft_list)} aéronef(s)")
            
            if not aircraft_list:
                QMessageBox.information(self, "Info", "Aucun aéronef enregistré")
                return
            
            # Créer une fenêtre de dialogue pour afficher les rapports
            dialog = QDialog(self)
            dialog.setWindowTitle("Rapports de Maintenance")
            dialog.setGeometry(250, 80, 800, 600)
            dialog.setStyleSheet("background-color: white;")
            
            # Ajouter un zone de texte pour afficher les rapports
            text_edit = QTextEdit(dialog)
            layout = QVBoxLayout(dialog)
            layout.addWidget(text_edit)
            
            # Générer les rapports pour tous les aéronefs
            all_reports = ""
            for immat in aircraft_list:
                print(f"  Génération du rapport pour {immat}...")
                report = self.maintenance_system.generate_maintenance_report(immat)
                all_reports += report + "\n" + "="*80 + "\n\n"
            
            # Afficher les rapports dans la zone de texte
            text_edit.setText(all_reports)
            text_edit.setReadOnly(True)
            dialog.exec()
            print("✓ Rapports générés avec succès")
        
        except Exception as e:
            print(f"❌ Erreur lors de la génération des rapports: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur génération rapports: {e}")
    
    def export_data(self):
        """Exporte les données des alertes actives en format CSV
        
        Crée un fichier CSV contenant toutes les alertes actives
        avec leurs détails complets pour analyse externe.
        """
        try:
            import csv
            from datetime import datetime
            
            # Créer le nom du fichier avec timestamp
            filename = f"export_maintenance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            print(f"💾 Exportation des données vers {filename}")
            
            # Récupérer toutes les alertes actives
            all_alerts = self.db.get_active_alerts()
            print(f"  {len(all_alerts)} alerte(s) à exporter")
            
            # Écrire les données dans le fichier CSV
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Écrire l'en-tête du CSV
                writer.writerow(['Immatriculation', 'Type Alerte', 'Seuil Heures', 'Status', 'Date Création'])
                
                # Écrire chaque alerte dans le CSV
                for alerte in all_alerts:
                    writer.writerow([
                        alerte['immatriculation'],
                        alerte['type_alerte'],
                        alerte['seuil_heures'],
                        alerte['statut'],
                        alerte['date_creation']
                    ])
            
            print(f"✓ Export terminé avec succès")
            QMessageBox.information(self, "✓ Succès", f"Données exportées dans {filename}")
        
        except Exception as e:
            print(f"❌ Erreur lors de l'exportation: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur export: {e}")


# Widget autonome pour intégration dans bienvenue.py
class AlertesFrame(QFrame):
    """Version simplifiée du tableau d'alertes pour intégration dans l'interface principale
    
    Affiche un aperçu rapide des alertes actives de maintenance
    avec la possibilité de les actualiser.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configuration du style du widget
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        # Initialisation des gestionnaires de base de données
        self.db = DatabaseManager()
        self.maintenance_system = MaintenanceAutomationSystem(self.db)
        
        # Titre du widget
        titre = QLabel("Alertes de Maintenance", self)
        titre.setGeometry(20, 20, 500, 30)
        titre.setStyleSheet("font-size: 18px; color: white; font-weight: bold;")
        
        # Tableau des alertes (4 colonnes: Aéronef, Alerte, Seuil (h), Status)
        self.tableau = QTableWidget(0, 4, self)
        self.tableau.setGeometry(20, 60, 960, 400)
        self.tableau.setHorizontalHeaderLabels(["Aéronef", "Alerte", "Seuil (h)", "Status"])
        self.tableau.setStyleSheet("background-color: white; color: black;")
        
        # Bouton pour actualiser les alertes
        btn = QPushButton("Rafraîchir", self)
        btn.setGeometry(20, 470, 100, 30)
        btn.clicked.connect(self.refresh)
        
        # Charger les données au démarrage
        self.refresh()
    
    def refresh(self):
        """Actualise les alertes affichées dans le widget
        
        Récupère les alertes actives de la base de données et les affiche
        dans le tableau avec les détails: immatriculation, type d'alerte,
        seuil en heures et statut actuel.
        """
        try:
            # Récupérer toutes les alertes actives
            alerts = self.db.get_active_alerts()
            print(f"🔄 Actualisation des alertes: {len(alerts)} alerte(s) trouvée(s)")
            
            # Configurer le nombre de lignes du tableau
            self.tableau.setRowCount(len(alerts))
            
            if len(alerts) == 0:
                print("✓ Aucune alerte active actuellement")
            
            # Remplir le tableau avec les données des alertes
            for idx, alert in enumerate(alerts):
                # Préparer les colonnes: Aéronef, Alerte, Seuil (h), Status
                items = [
                    alert['immatriculation'],
                    alert['type_alerte'],
                    str(alert['seuil_heures']),
                    alert['statut']
                ]
                
                # Ajouter chaque colonne au tableau
                for col, text in enumerate(items):
                    item = QTableWidgetItem(text)
                    self.tableau.setItem(idx, col, item)
        
        except Exception as e:
            print(f"❌ Erreur lors de l'actualisation des alertes: {e}")
            import traceback
            traceback.print_exc()
