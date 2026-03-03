from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
import sqlite3
import os

class Recapitulatifs(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Recapitulatifs des echeances", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        # Faire une tableau
        self.tableau_affichage = QTableWidget(20,4,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels(["Immatriculation","Types","Description","Certifications"])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,400)
        self.tableau_affichage.setColumnWidth(3,250)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        
        self.btn_ajout_travaux = QPushButton("Nouveaux",self)
        self.btn_ajout_travaux.setGeometry(10,10,190,40)
        self.btn_ajout_travaux.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_travaux.clicked.connect(self.ajouter_recapitulatifs)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_recaitulatifs)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        
        # Frame Ajout
        self.frame_recapitulatifs = QFrame(self)
        self.frame_recapitulatifs.setGeometry(10,110,1000,480)
        self.frame_recapitulatifs.setStyleSheet("background-color:white")
        

        
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_recapitulatifs)
        self.immatriculation_label.setGeometry(20, 20, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_recapitulatifs)
        self.immatriculation_input.setGeometry(300, 19, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.immatriculation_input.currentTextChanged.connect(self.fill_date_proc_rev_from_temps_vie)
        
        self.types_ = QLabel("Types:", self.frame_recapitulatifs)
        self.types_.setGeometry(20, 50, 300, 80)
        self.types_.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.types_ = QComboBox(self.frame_recapitulatifs)
        self.types_.setGeometry(300, 70, 300, 35)
        self.types_.setStyleSheet("background-color: white;border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.types_.addItems(["Cellule","Moteurs","Helices","Inspection (25h)","Inspection (50h)","Inspection (100h)"])
        
        # (Removed general Description field — using component description instead)

        # Champ Certifications (nouveau)
        self.certifications_label = QLabel("Certifications:", self.frame_recapitulatifs)
        self.certifications_label.setGeometry(20, 90, 300, 80)
        self.certifications_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.certifications = QLineEdit(self.frame_recapitulatifs)
        self.certifications.setGeometry(300, 120, 300, 35)
        self.certifications.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        # Grand titre: Les composants à vie limité
        self.composants_title = QLabel("Les composants à vie limité", self.frame_recapitulatifs)
        self.composants_title.setGeometry(20, 160, 600, 30)
        self.composants_title.setStyleSheet("color: black; font-size: 18px; font-weight:bold; background-color:none")

        # Nouveaux champs pour composants à vie limité
        self.num_ref_ata_label = QLabel("Num ref ATA:", self.frame_recapitulatifs)
        self.num_ref_ata_label.setGeometry(20, 200, 150, 30)
        self.num_ref_ata_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.num_ref_ata_input = QLineEdit(self.frame_recapitulatifs)
        self.num_ref_ata_input.setGeometry(300, 200, 300, 35)
        self.num_ref_ata_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")

        self.comp_description_label = QLabel("Description composant:", self.frame_recapitulatifs)
        self.comp_description_label.setGeometry(20, 250, 250, 30)
        self.comp_description_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.comp_description_input = QLineEdit(self.frame_recapitulatifs)
        self.comp_description_input.setGeometry(300, 250, 300, 35)
        self.comp_description_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")

        self.date_proc_rev_label = QLabel("Date Proc Rev:", self.frame_recapitulatifs)
        self.date_proc_rev_label.setGeometry(20, 300, 150, 30)
        self.date_proc_rev_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.date_proc_rev_input = QLineEdit(self.frame_recapitulatifs)
        self.date_proc_rev_input.setGeometry(300, 300, 300, 35)
        self.date_proc_rev_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")

        self.pot_restant_label = QLabel("Pot restant:", self.frame_recapitulatifs)
        self.pot_restant_label.setGeometry(20, 350, 150, 30)
        self.pot_restant_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.pot_restant_input = QLineEdit(self.frame_recapitulatifs)
        self.pot_restant_input.setGeometry(300, 350, 300, 35)
        self.pot_restant_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")

        self.pot_restant_cycles_label = QLabel("Pot restant Cycles:", self.frame_recapitulatifs)
        self.pot_restant_cycles_label.setGeometry(20, 400, 200, 30)
        self.pot_restant_cycles_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.pot_restant_cycles_input = QLineEdit(self.frame_recapitulatifs)
        self.pot_restant_cycles_input.setGeometry(300, 400, 300, 35)
        self.pot_restant_cycles_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_recapitulatifs)
        self.enregistrer.setGeometry(750,400,200,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_recapitulatifs)
        
        self.frame_recapitulatifs.hide()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS recapitulatifs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    types TEXT,
                    description TEXT,
                    certifications TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            self.conn.commit()
            # Migration: ensure certifications column exists (for older DBs)
            try:
                self.cursor.execute("PRAGMA table_info(recapitulatifs)")
                cols = [r[1] for r in self.cursor.fetchall()]
                if 'certifications' not in cols:
                    self.cursor.execute('ALTER TABLE recapitulatifs ADD COLUMN certifications TEXT')
                    self.conn.commit()
            except Exception:
                pass
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les recapitulatifs
        self.load_immatriculations()
        self.load_recapitulatifs()
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
    
    def fill_date_proc_rev_from_temps_vie(self):
        """Remplit automatiquement date_proc_rev, pot_restant et pot_restant_cycles avec les valeurs calculées depuis temps_vie"""
        immat = self.immatriculation_input.currentText().strip()
        
        if not immat:
            self.date_proc_rev_input.clear()
            self.pot_restant_input.clear()
            self.pot_restant_cycles_input.clear()
            return
        
        try:
            # Récupérer le dernier composant de temps_vie pour cette immatriculation
            self.cursor.execute(
                'SELECT dates_proc_rev, pot_restant, pot_restant_cycles FROM temps_vie WHERE immatriculation=? ORDER BY rowid DESC LIMIT 1',
                (immat,)
            )
            row = self.cursor.fetchone()
            
            if row:
                dates_proc_rev, pot_restant, pot_restant_cycles = row
                self.date_proc_rev_input.setText(dates_proc_rev or "")
                self.pot_restant_input.setText(pot_restant or "")
                self.pot_restant_cycles_input.setText(pot_restant_cycles or "")
            else:
                self.date_proc_rev_input.clear()
                self.pot_restant_input.clear()
                self.pot_restant_cycles_input.clear()
        except Exception as e:
            print('Erreur récupération données temps_vie:', e)
            self.date_proc_rev_input.clear()
            self.pot_restant_input.clear()
            self.pot_restant_cycles_input.clear()
    
    def load_recapitulatifs(self):
        """Charge les recapitulatifs depuis la base de donnees"""
        try:
            self.cursor.execute('SELECT id, immatriculation, types, description, certifications FROM recapitulatifs ORDER BY immatriculation DESC')
            rows = self.cursor.fetchall()
        except Exception as e:
            print('Erreur lecture DB:', e)
            rows = []
        
        # Ajuster le nombre de lignes du tableau
        row_count = max(20, len(rows))
        self.tableau_affichage.setRowCount(row_count)
        
        # Vider le contenu existant
        self.tableau_affichage.clearContents()
        
        # Remplir avec les donnees (en sautant la colonne ID)
        for idx, row in enumerate(rows):
            for col, value in enumerate(row[1:]):  # Ignorer l'ID (index 0)
                item = QTableWidgetItem(str(value))
                # Stocker l'ID dans les donnees de l'item
                item.setData(Qt.ItemDataRole.UserRole, row[0])
                self.tableau_affichage.setItem(idx, col, item)
    
    def save_recapitulatifs(self):
        """Sauvegarde les donnees du recapitulatif dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        types = self.types_.currentText().strip()
        description = self.comp_description_input.text().strip()
        certifications = self.certifications.text().strip()
        
        if not immat:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez selectionner une immatriculation")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        try:
            self.cursor.execute(
                'INSERT INTO recapitulatifs (immatriculation, types, description, certifications) VALUES (?, ?, ?, ?)',
                (immat, types, description, certifications)
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
        
        # Nettoyer les champs
        self.reset_form()
        
        # Recharger le tableau
        self.load_recapitulatifs()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_recapitulatifs.hide()
    
    def on_row_selected(self):
        self.selected_rows = self.tableau_affichage.selectedIndexes()
        
        # Colorer les lignes selectionnees en bleu
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
        
        # Afficher le bouton Action si au moins une ligne est selectionnee
        if len(set(idx.row() for idx in self.selected_rows)) > 0:
            self.btn_action.show()
        else:
            self.btn_action.hide()
    
    def show_action_menu(self):
        selected_rows = list(set(idx.row() for idx in self.tableau_affichage.selectedIndexes()))
        
        if len(selected_rows) == 1:
            row = selected_rows[0]
            item = self.tableau_affichage.item(row, 0)
            
            # Verifier que la cellule n'est pas vide
            if item is None or item.text().strip() == "":
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.setWindowTitle("Attention")
                msg.setText("Veuillez selectionner une ligne avec des donnees.")
                msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
                msg.exec()
                return
            
            immat = item.text()
            
            menu = QMenu(self)
            action_modifier = menu.addAction("Modifier")
            menu.addSeparator()
            action_supprimer = menu.addAction("Supprimer")
            
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
                self.modifier_recapitulatifs(row, immat)
            elif action == action_supprimer:
                self.supprimer_recapitulatifs(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_recapitulatifs(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        types = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        description = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        certifications = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.types_.setCurrentText(types)
        self.comp_description_input.setText(description)
        self.certifications.setText(certifications)
        
        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_recapitulatifs(immat))
        
        self.tableau_affichage.setVisible(False)
        self.frame_recapitulatifs.show()
    
    def update_recapitulatifs(self, immat):
        types = self.types_.currentText().strip()
        description = self.comp_description_input.text().strip()
        certifications = self.certifications.text().strip()
        
        try:
            self.cursor.execute(
                'UPDATE recapitulatifs SET types=?, description=?, certifications=? WHERE immatriculation=?',
                (types, description, certifications, immat)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return
        
        # Reinitialiser le formulaire
        self.reset_form()
        self.load_recapitulatifs()
        self.tableau_affichage.setVisible(True)
        self.frame_recapitulatifs.hide()
    
    def supprimer_recapitulatifs(self, row, immat):
        # Recuperer l'ID stocke dans les donnees de l'item
        row_id = self.tableau_affichage.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Creer une boite de dialogue personnalisee
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setGeometry(400, 300, 400, 150)
        dialog.setStyleSheet("QDialog { background-color: #2d2d69; }")
        
        # Label du message
        label = QLabel(f"Etes-vous sur de vouloir supprimer cette ligne ?\nImmatriculation: {immat}")
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_recapitulatifs(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_recapitulatifs(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM recapitulatifs WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_recapitulatifs()
        dialog.accept()
    
    def reset_form(self):
        self.types_.setCurrentIndex(0)
        self.certifications.clear()
        # Réinitialiser les nouveaux champs ajoutés pour composants à vie limité
        try:
            self.num_ref_ata_input.clear()
        except Exception:
            pass
        try:
            self.comp_description_input.clear()
        except Exception:
            pass
        try:
            self.date_proc_rev_input.clear()
        except Exception:
            pass
        try:
            self.pot_restant_input.clear()
        except Exception:
            pass
        try:
            self.pot_restant_cycles_input.clear()
        except Exception:
            pass
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_recapitulatifs)
        
    def ajouter_recapitulatifs(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_recapitulatifs.show()
        
    def voir_listes_recaitulatifs(self):
        self.load_recapitulatifs()
        self.tableau_affichage.setVisible(True)
        self.frame_recapitulatifs.hide()
        self.btn_action.hide()
        
        self.frame_recapitulatifs.hide()
        
    def ajouter_recapitulatifs(self):
        
        self.tableau_affichage.setVisible(False)
        self.frame_recapitulatifs.show()
        
    def voir_listes_recaitulatifs(self):
        self.tableau_affichage.setVisible(True)
        self.frame_recapitulatifs.hide()
        