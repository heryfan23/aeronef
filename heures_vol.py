from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget, QTableWidgetItem, QComboBox, QDateEdit, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os
from database_manager import DatabaseManager
from maintenance_system import MaintenanceAutomationSystem

class HeuresVol(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)
            
        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        # Initialiser les gestionnaires d'automatisation
        try:
            self.db_manager = DatabaseManager()
            self.maintenance_automation = MaintenanceAutomationSystem(self.db_manager)
        except Exception as e:
            print(f"Erreur initialisation système maintenance: {e}")
        
        self.titre = QLabel("heures de vol", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        # Faire une tableau
        # 4 colonnes : immatriculation, date, temps de vol et nombre de cycles
        self.tableau_affichage = QTableWidget(20,4,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels(["Immatriculation","Date de Vol","Temps de vol(h:mm)","Nombre de cycles"])
        self.tableau_affichage.setColumnWidth(0,200)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,250)
        self.tableau_affichage.setColumnWidth(3,250)
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Empêcher l'édition directe des cellules
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.btn_ajout_heures = QPushButton("Nouveaux",self)
        self.btn_ajout_heures.setGeometry(10,10,190,40)
        self.btn_ajout_heures.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_heures.clicked.connect(self.ajouter_heures)
        
        
        self.btn_voir_heures = QPushButton("Voir Listes",self)
        self.btn_voir_heures.setGeometry(230,10,190,40)
        self.btn_voir_heures.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_heures.clicked.connect(self.voir_heures)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        # Frame Total temps de vol
        self.frame_total = QFrame(self)
        self.frame_total.setGeometry(10,510,1000,80)
        self.frame_total.setStyleSheet("background-color:white;border:1px solid black;border-radius:5px")
        
        self.label_total_titre = QLabel("Total Temps de Vol et Cycles par Immatriculation:", self.frame_total)
        self.label_total_titre.setGeometry(20, 10, 300, 25)
        self.label_total_titre.setStyleSheet("color: black; font-size: 14px; font-weight: bold; background-color: none;")
        
        self.label_total_details = QLabel("", self.frame_total)
        self.label_total_details.setGeometry(20, 35, 960, 40)
        self.label_total_details.setStyleSheet("color: black; font-size: 12px; background-color: none;")
        self.label_total_details.setWordWrap(True)
        
        

        # Frame Ajout
        self.frame_ajout_heure = QFrame(self)
        self.frame_ajout_heure.setGeometry(10,110,1000,400)
        self.frame_ajout_heure.setStyleSheet("background-color:white")
        
        self.titre = QLabel("Saisir Heures de vol", self.frame_ajout_heure)
        self.titre.setGeometry(250, 10, 750, 50)
        self.titre.setStyleSheet("font-size: 30px;color:black;background-color:none")
        
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_ajout_heure)
        self.immatriculation_label.setGeometry(20, 80, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_ajout_heure)
        self.immatriculation_input.setGeometry(200, 79, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.date_vol = QLabel("Date de vol:", self.frame_ajout_heure)
        self.date_vol.setGeometry(20, 130, 150, 30)
        self.date_vol.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.date_vol = QDateEdit(self.frame_ajout_heure)
        self.date_vol.setGeometry(200, 129, 300, 35)
        self.date_vol.setDate(QDate.currentDate())
        self.date_vol.setCalendarPopup(True)
        self.date_vol.setDisplayFormat("yyyy-MM-dd")
        self.date_vol.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.temps_vol = QLabel("Temps de Vol \n (h:mm):", self.frame_ajout_heure)
        self.temps_vol.setGeometry(20, 180, 150, 50)
        self.temps_vol.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.temps_vol = QLineEdit(self.frame_ajout_heure)
        self.temps_vol.setGeometry(200, 190, 300, 35)
        self.temps_vol.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        # champ cycles (entier)
        self.cycles_label = QLabel("Nombre de cycles :", self.frame_ajout_heure)
        self.cycles_label.setGeometry(20, 230, 150, 30)
        self.cycles_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.cycles_input = QLineEdit(self.frame_ajout_heure)
        self.cycles_input.setGeometry(200, 230, 300, 35)
        self.cycles_input.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.cycles_input.setPlaceholderText("0")
        
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_ajout_heure)
        self.enregistrer.setGeometry(400,300,200,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_heures)

        self.frame_ajout_heure.hide()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            # on inclut une colonne cycles ; la colonne temps_cumul reste présente pour compatibilité mais n'est plus utilisée
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS heures_vol (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    date_vol TEXT,
                    temps_vol TEXT,
                    cycles INTEGER DEFAULT 0,
                    temps_cumul TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            # si l'ancienne table existait sans cycles, on s'assure d'ajouter la colonne
            try:
                self.cursor.execute("ALTER TABLE heures_vol ADD COLUMN cycles INTEGER DEFAULT 0")
            except Exception:
                # ignore si la colonne existe déjà
                pass
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les heures
        self.load_immatriculations()
        self.load_heures()
        self.selected_rows = []
        
        
    def load_immatriculations(self):
        """Charge tous les matricules depuis la table aircrafts"""
        try:
            self.cursor.execute('SELECT immatriculation FROM aircrafts ORDER BY immatriculation')
            immatriculations = self.cursor.fetchall()
            self.immatriculation_input.clear()
            for immat in immatriculations:
                self.immatriculation_input.addItem(immat[0])
        except Exception as e:
            print('Erreur chargement immatriculations:', e)
    
    def calculate_totals(self):
        """Calcule et affiche le total des temps de vol et des cycles par immatriculation"""
        totals_time = {}
        totals_cycles = {}
        errors = []
        
        # Parcourir le tableau
        for row in range(self.tableau_affichage.rowCount()):
            immat_item = self.tableau_affichage.item(row, 0)
            temps_item = self.tableau_affichage.item(row, 2)
            cycles_item = self.tableau_affichage.item(row, 3)
            
            # Si la ligne est vide, arrêter
            if immat_item is None or immat_item.text().strip() == "":
                break
            
            immat = immat_item.text()
            temps_str = temps_item.text() if temps_item else ""
            cycles_str = cycles_item.text() if cycles_item else "0"
            
            # cycle conversion
            try:
                cycles_val = int(cycles_str) if cycles_str.strip() else 0
            except ValueError:
                cycles_val = 0
            
            # temps validation
            if temps_str.strip():
                if not self.validate_time_format(temps_str):
                    errors.append(f"Format invalide pour {immat}: '{temps_str}'")
                else:
                    hours, minutes = map(int, temps_str.split(":"))
                    total_minutes = hours * 60 + minutes
                    totals_time.setdefault(immat, 0)
                    totals_time[immat] += total_minutes
            
            totals_cycles.setdefault(immat, 0)
            totals_cycles[immat] += cycles_val
        
        # Formater et afficher les résultats
        result_text = ""
        for immat in sorted(set(list(totals_time.keys()) + list(totals_cycles.keys()))):
            hmin = ""
            if immat in totals_time:
                hours = totals_time[immat] // 60
                minutes = totals_time[immat] % 60
                hmin = f"{hours}h{minutes:02d}m"
            cycles = totals_cycles.get(immat, 0)
            result_text += f"  • {immat}: {hmin}  | cycles {cycles}  |  "

        if errors:
            result_text += "\n⚠️ ERREURS: " + " | ".join(errors)
            self.label_total_details.setStyleSheet("color: red; font-size: 12px; background-color: none;")
        else:
            self.label_total_details.setStyleSheet("color: black; font-size: 12px; background-color: none;")
        
        self.label_total_details.setText(result_text if result_text else "Aucune donnée")
    
    def validate_time_format(self, time_str):
        """Valide que le format est hh:mm"""
        try:
            parts = time_str.strip().split(':')
            if len(parts) != 2:
                return False
            hours, minutes = int(parts[0]), int(parts[1])
            if hours < 0 or minutes < 0 or minutes >= 60:
                return False
            return True
        except (ValueError, AttributeError):
            return False
    
    def load_heures(self):
        """Charge les heures de vol depuis la base de données"""
        try:
            self.cursor.execute('SELECT id, immatriculation, date_vol, temps_vol, cycles FROM heures_vol ORDER BY date_vol DESC')
            rows = self.cursor.fetchall()
        except Exception as e:
            print('Erreur lecture DB:', e)
            rows = []
        
        # Ajuster le nombre de lignes du tableau
        row_count = max(20, len(rows))
        self.tableau_affichage.setRowCount(row_count)
        
        # Vider le contenu existant
        self.tableau_affichage.clearContents()
        
        # Remplir avec les données (en sautant la colonne ID)
        for idx, row in enumerate(rows):
            for col, value in enumerate(row[1:]):  # Ignorer l'ID (index 0)
                item = QTableWidgetItem(str(value))
                # Stocker l'ID dans les données de l'item
                item.setData(Qt.ItemDataRole.UserRole, row[0])
                self.tableau_affichage.setItem(idx, col, item)
        
        # Calculer et afficher les totaux
        self.calculate_totals()
    
    def convert_time_to_minutes(self, time_str):
        """Convertit un temps au format hh:mm en minutes"""
        try:
            if not time_str or ':' not in time_str:
                return 0
            parts = time_str.strip().split(':')
            if len(parts) != 2:
                return 0
            hours, minutes = int(parts[0]), int(parts[1])
            return hours * 60 + minutes
        except (ValueError, AttributeError):
            return 0
    
    def check_maintenance_alert(self, immat, temps_cumul_str):
        """Vérifie si les heures de révision sont atteintes et déclenche les alertes automatiques - SYSTÈME AUTOMATISÉ"""
        try:
            # Convertir le temps cumul en heures décimales
            current_hours = self.maintenance_automation.convert_time_to_hours(temps_cumul_str)
            
            # Vérifier et créer les alertes automatiquement
            new_alerts = self.maintenance_automation.check_and_trigger_alerts(immat, current_hours)
            
            if new_alerts:
                # Construire le message d'alerte professionnel
                alert_text = f"""⚠️ ALERTES DE MAINTENANCE DÉTECTÉES

AÉRONEF: {immat}
HEURES ACCUMULÉES: {temps_cumul_str}
═══════════════════════════════════════════

"""
                
                # Ajouter chaque alerte avec ses détails
                for alert in new_alerts:
                    alert_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 {alert['type'].replace('MAINTENANCE_', '')}: RÉVISION {alert['hours']}h
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
   Heures restantes: {item['heures_restantes']:.1f}h ({item['pourcentage']:.1f}%)
   {item['description']}
"""
                
                # Afficher le message d'alerte
                alert_msg = QMessageBox(self)
                alert_msg.setIcon(QMessageBox.Icon.Warning)
                alert_msg.setWindowTitle("⚠️ ALERTES DE MAINTENANCE AUTOMATIQUES")
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
                    msg.setWindowTitle("ℹ️ Statut Maintenance")
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
            return False
    
    def save_heures(self):
        """Sauvegarde les heures de vol dans la base de données"""
        immat = self.immatriculation_input.currentText().strip()
        date_vol = self.date_vol.date().toString("yyyy-MM-dd")
        temps_vol = self.temps_vol.text().strip()
        cycles_str = self.cycles_input.text().strip()
        
        if not immat or not temps_vol:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir au moins l'immatriculation et le temps de vol.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        # convertir cycles en entier, défaut 0
        try:
            cycles = int(cycles_str) if cycles_str else 0
        except ValueError:
            cycles = 0
        
        try:
            self.cursor.execute(
                'INSERT INTO heures_vol (immatriculation, date_vol, temps_vol, cycles) VALUES (?, ?, ?, ?)',
                (immat, date_vol, temps_vol, cycles)
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
        
        # Vérifier si les heures de révision sont atteintes
        # On n'utilise plus le temps cumul
        heures_check = temps_vol
        self.check_maintenance_alert(immat, heures_check)
        
        # Persister les alertes créées
        if hasattr(self, 'db_manager'):
            self.db_manager.commit()
        
        # Nettoyer les champs
        self.temps_vol.clear()
        # l'ancien champ "temps_cumul" a été supprimé, il n'existe plus dans l'interface
        # mais nous conservons la base de données pour compatibilité.
        # Si pour une raison quelconque l'attribut existe encore, on le vide :
        if hasattr(self, 'temps_cumul'):
            try:
                self.temps_cumul.clear()
            except Exception:
                pass
        self.date_vol.setDate(QDate.currentDate())
        
        # Recharger le tableau
        self.load_heures()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_ajout_heure.hide()
    
    def on_row_selected(self):
        self.selected_rows = self.tableau_affichage.selectedIndexes()
        
        # Colorer les lignes sélectionnées en bleu
        for i in range(self.tableau_affichage.rowCount()):
            is_selected = False
            for idx in self.selected_rows:
                if idx.row() == i:
                    is_selected = True
                    break
            
            for j in range(self.tableau_affichage.columnCount()):
                item = self.tableau_affichage.item(i, j)
                if item:
                    if is_selected:
                        item.setBackground(QColor(0, 127, 255))
                        item.setForeground(QColor("white"))
                    else:
                        item.setBackground(QColor("white"))
                        item.setForeground(QColor("black"))
        
        # Afficher le bouton Action si au moins une ligne est sélectionnée
        if len(set(idx.row() for idx in self.selected_rows)) > 0:
            self.btn_action.show()
        else:
            self.btn_action.hide()
    
    def show_action_menu(self):
        selected_rows = list(set(idx.row() for idx in self.tableau_affichage.selectedIndexes()))
        
        if len(selected_rows) == 1:
            row = selected_rows[0]
            item = self.tableau_affichage.item(row, 0)
            
            # Vérifier que la cellule n'est pas vide
            if item is None or item.text().strip() == "":
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Attention")
                msg.setText("Veuillez sélectionner une ligne avec des données.")
                msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
                msg.exec()
                return
            
            immat = item.text()
            
            menu = QMenu(self)
            
            action_modifier = menu.addAction("Modifier")
            
            # Ajouter un séparateur avec espacement
            menu.addSeparator()
            
            action_supprimer = menu.addAction("Supprimer")
            
            
            # Style du menu
            menu.setStyleSheet("""
                QMenu { 
                    background-color: gray; 
                    color: white; 
                    padding: 10px 0px;
                    border-radius: 5px;
                } 
                QMenu::item { 
                    padding: 8px 20px;
                    margin: 5px 0px;
                }
                QMenu::item:selected { 
                    background-color: #007FFF; 
                    border-radius: 3px;
                }
            """)
            
            menu.setFixedWidth(self.btn_action.width())
            
            action = menu.exec(self.btn_action.mapToGlobal(self.btn_action.rect().bottomLeft()))
            
            if action == action_modifier:
                self.modifier_heures(row, immat)
            elif action == action_supprimer:
                self.supprimer_heures(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez sélectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_heures(self, row, immat):
        # Récupérer les données de la ligne avec vérification
        date_vol = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        temps_vol = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        cycles = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.date_vol.setDate(QDate.fromString(date_vol, "yyyy-MM-dd"))
        self.temps_vol.setText(temps_vol)
        self.cycles_input.setText(cycles)
        
        # Changer le titre et le comportement du formulaire
        self.titre.setText("Modifier les heures de vol")
        self.enregistrer.setText("Mettre à jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_heures(immat, date_vol))
        
        self.tableau_affichage.setVisible(False)
        self.frame_ajout_heure.show()
    
    def update_heures(self, immat, date_vol_original):
        date_vol = self.date_vol.date().toString("yyyy-MM-dd")
        temps_vol = self.temps_vol.text().strip()
        cycles_str = self.cycles_input.text().strip()
        
        if not temps_vol:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir le temps de vol.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        try:
            cycles = int(cycles_str) if cycles_str else 0
        except ValueError:
            cycles = 0
        
        try:
            self.cursor.execute(
                'UPDATE heures_vol SET date_vol=?, temps_vol=?, cycles=? WHERE immatriculation=? AND date_vol=?',
                (date_vol, temps_vol, cycles, immat, date_vol_original)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise à jour DB:', e)
            return
        
        # Réinitialiser le formulaire
        self.reset_form()
        self.load_heures()
        self.tableau_affichage.setVisible(True)
        self.frame_ajout_heure.hide()
    
    def supprimer_heures(self, row, immat):
        date_vol = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        
        # Récupérer l'ID stocké dans les données de l'item
        row_id = self.tableau_affichage.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Créer une boîte de dialogue personnalisée
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setGeometry(400, 300, 400, 150)
        dialog.setStyleSheet("QDialog { background-color: #2d2d69; }")
        
        # Label du message
        label = QLabel(f"Êtes-vous sûr de vouloir supprimer cette ligne ?\nImmatriculation: {immat}\nDate: {date_vol}")
        label.setStyleSheet("color: white; font-size: 14px; background-color: #2d2d69;")
        
        # Boutons
        btn_yes = QPushButton("Oui")
        btn_yes.setStyleSheet("background-color: white; color: black; border: 1px solid black; padding: 5px; font-size: 14px; border-radius: 5px;")
        btn_yes.setCursor(Qt.CursorShape.PointingHandCursor)
        
        btn_no = QPushButton("Non")
        btn_no.setStyleSheet("background-color: #007FFF; color: white; border: 1px solid #007FFF; padding: 5px; font-size: 14px; border-radius: 5px;")
        btn_no.setCursor(Qt.CursorShape.PointingHandCursor)
        
        # Layout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(btn_yes)
        buttons_layout.addWidget(btn_no)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(label)
        main_layout.addLayout(buttons_layout)
        dialog.setLayout(main_layout)
        
        # Connecter les boutons
        btn_yes.clicked.connect(lambda: self.confirm_delete(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM heures_vol WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_heures()
        dialog.accept()
    
    def reset_form(self):
        self.temps_vol.clear()
        self.cycles_input.clear()
        self.date_vol.setDate(QDate.currentDate())
        self.titre.setText("Saisir Heures de vol")
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_heures)
        
    def ajouter_heures(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_ajout_heure.show()
        
    def voir_heures(self):
        self.load_heures()
        self.tableau_affichage.setVisible(True)
        self.frame_ajout_heure.hide()
        self.btn_action.hide()