"""
Module d'intégration du système de maintenance automatisé
À ajouter dans les fichiers existants pour automatiser les alertes
"""

# ============================================================
# À AJOUTER AU DÉBUT DE heures_vol.py 
# ============================================================

# Ajouter ces imports au fichier heures_vol.py:
"""
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem
"""

# ============================================================
# À REMPLACER DANS heures_vol.py - Classe HeuresVol.__init__
# ============================================================

# Après le setStyleSheet, ajouter:
"""
        # ... code existant ...
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        # Initialiser les gestionnaires
        self.db_manager = DatabaseManager()
        self.maintenance_automation = MaintenanceAutomationSystem(self.db_manager)
        
        # ... reste du code ...
"""

# ============================================================
# À REMPLACER DANS heures_vol.py - Méthode check_maintenance_alert
# ============================================================

# Remplacer la méthode check_maintenance_alert existante par:
"""
    def check_maintenance_alert(self, immat, temps_cumul_str):
        \"\"\"
        Vérifie si les heures de révision sont atteintes et déclenche les alertes automatiques
        Version améliorée avec système d'automatisation complet
        \"\"\"
        try:
            # Convertir le temps cumul en heures décimales
            current_hours = self.maintenance_automation.convert_time_to_hours(temps_cumul_str)
            
            # Vérifier et créer les alertes
            new_alerts = self.maintenance_automation.check_and_trigger_alerts(immat, current_hours)
            
            if new_alerts:
                # Générer un message d'alerte complet
                alert_text = f\"\"\"⚠️  ALERTES DE MAINTENANCE - AÉRONEF {immat}

HEURES ACCUMULÉES: {temps_cumul_str}

\"\"\"
                
                for alert in new_alerts:
                    alert_text += f\"\"\"
━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 {alert['type'].replace('MAINTENANCE_', '')}
━━━━━━━━━━━━━━━━━━━━━━━━━
Seuil:  {alert['hours']}h
Sévérité: {alert['severity']}
Description: {alert['description']}
\"\"\"
                
                # Récupérer le calendrier des prochaines maintenances
                schedule = self.maintenance_automation.get_next_maintenance_schedule(immat, current_hours)
                
                alert_text += f\"\"\"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CALENDRIER DES PROCHAINES MAINTENANCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
\"\"\"
                
                for item in schedule[:5]:  # Afficher les 5 prochaines
                    alert_text += f\"\"\"

📅 {item['seuil']}
   Total: {item['heures_totales']}h
   Restante: {item['heures_restantes']:.1f}h ({item['pourcentage']:.1f}%)
   {item['description']}
\"\"\"
                
                # Afficher l'alerte
                alert_msg = QMessageBox(self)
                alert_msg.setIcon(QMessageBox.Icon.Warning)
                alert_msg.setWindowTitle("⚠️  ALERTES DE MAINTENANCE")
                alert_msg.setText(alert_text)
                alert_msg.setStyleSheet(\"\"\"
                    QMessageBox { background-color: #2d2d69; }
                    QMessageBox QLabel { color: white; font-weight: bold; }
                \"\"\")
                alert_msg.setMinimumWidth(600)
                alert_msg.exec()
                
                return True
            else:
                # Vérifier s'il y a une alerte existante
                existing_alerts = self.db_manager.get_alerts_for_aircraft(immat)
                if existing_alerts:
                    # Afficher un message informatif sur les alertes existantes
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Information)
                    msg.setWindowTitle("ℹ️  Statut Maintenance")
                    msg.setText(f\"Aéronef: {immat}\\n\\nAlertes actives: {len(existing_alerts)}\\n\\n\" +
                               \"Veuillez consulter le tableau de bord pour plus de détails.\")
                    msg.exec()
                    return True
            
            return False
        except Exception as e:
            print(f'Erreur vérification maintenance: {e}')
            return False
\"\"\"

# ============================================================
# À REMPLACER DANS heures_vol.py - Méthode save_heures
# ============================================================

# Remplacer la méthode save_heures existante par:
"""
"""
    def save_heures(self):
        Sauvegarde les heures de vol et déclenche les alertes automatiques 
        immat = self.immatriculation_input.currentText().strip()
        date_vol = self.date_vol.date().toString("yyyy-MM-dd")
        temps_vol = self.temps_vol.text().strip()
        temps_cumul = self.temps_cumul.text().strip()
        
        if not immat or not temps_vol:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir au moins l'immatriculation et le temps de vol.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
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
        
        # AUTOMATISATION DES ALERTES
        heures_check = temps_cumul if temps_cumul else temps_vol
        self.check_maintenance_alert(immat, heures_check)
        
        # Enregistrer l'alerte dans la base de données
        self.db_manager.commit()
        
        # Nettoyer les champs
        self.temps_vol.clear()
        self.temps_cumul.clear()
        self.date_vol.setDate(QDate().currentDate())
        
        # Recharger le tableau
        self.load_heures()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_ajout_heure.hide()
        
        # Message de confirmation
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("✓ Succès")
        msg.setText(f\"Heures de vol enregistrées pour {immat}\\n\\nVeuillez consulter le tableau de bord pour les alertes.\")
        msg.setStyleSheet(\"QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }\")
        msg.exec()
"\"\"\"

# ============================================================
# À AJOUTER À bienvenue.py POUR AFFICHER LE TABLEAU DE BORD
# ============================================================

# Au début du fichier bienvenue.py, ajouter:
"""
from alertes_dashboard import AlertesDashboard
"""

# Dans la méthode __init__ de la classe Bienvenue, ajouter après les autres frames:

        # Frame Alertes Dashboard
        self.alertes_frame = AlertesDashboard(self)
        self.alertes_frame.setGeometry(270, 70, 1070, 620)
        self.alertes_frame.hide()
"""

# Ajouter un bouton pour accéder au tableau de bord:
"""
        self.alertes = QPushButton("Alertes & Maintenance",self.dashboard)
        self.alertes.setGeometry(25,420,200,40)
        self.alertes.setStyleSheet(\"\"\"
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        \"\"\")
        self.alertes.setCursor(Qt.CursorShape.PointingHandCursor)
        self.alertes.clicked.connect(self.show_alertes)
"""

# Ajouter les méthodes:
"""
    def show_alertes(self):
        self.hide_all_frames(self.alertes_frame)
        self.alertes_frame.load_all_data()
    
    def hide_alertes(self):
        self.alertes_frame.hide()
"""

# ============================================================
# EXEMPLE D'UTILISATION DIRECTE
# ============================================================
"""
# Dans n'importe quel script:

from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem

db = DatabaseManager()
maintenance = MaintenanceAutomationSystem(db)

# Vérifier les alertes pour un aéronef
immatriculation = "N-12345"
current_hours = 25.5  # 25h30

alerts = maintenance.check_and_trigger_alerts(immatriculation, current_hours)
print(f"Alertes créées: {len(alerts)}")

for alert in alerts:
    print(f\"  - {alert['type']}: {alert['description']}\")

# Obtenir le calendrier de maintenance
schedule = maintenance.get_next_maintenance_schedule(immatriculation, current_hours)
for item in schedule:
    print(f\"  - {item['seuil']}: {item['heures_restantes']:.1f}h restantes\")

# Générer un rapport complet
report = maintenance.generate_maintenance_report(immatriculation)
print(report)

db.close()
"""