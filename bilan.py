from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout, QDateTimeEdit, QCompleter
from PyQt6.QtCore import Qt, QDate, QDateTime, QTime, QStringListModel
from PyQt6.QtGui import QColor
import sqlite3
import os

class Bilan(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(50, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Bilan des visites", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        # filtre immatriculation
        self.filter_label = QLabel("Filtrer immatriculation :", self)
        self.filter_label.setGeometry(440, 70, 160, 30)
        self.filter_label.setStyleSheet("color:white; font-size:14px; background-color:None")
        self.filter_input = QLineEdit(self)
        self.filter_input.setGeometry(610, 70, 200, 30)
        self.filter_input.setStyleSheet("background-color: white; border:1px solid black; padding:5px; font-size:14px")
        self.filter_input.textChanged.connect(self.apply_filter)
        self.filter_completer = QCompleter()
        self.filter_input.setCompleter(self.filter_completer)
         # Faire une tableau
        self.tableau_affichage = QTableWidget(20,6,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        # six columns correspond aux champs que l'on stockera
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Types d'inspection",
            "Dates dernière inspection",
            "heures dernière inspection",
            "heures prochaines inspection",
            "Date de réalisation"
        ])
        self.tableau_affichage.setColumnWidth(0,200)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,150)
        self.tableau_affichage.setColumnWidth(4,150)
        self.tableau_affichage.setColumnWidth(5,150)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_bilan = QPushButton("Nouveaux",self)
        self.btn_ajout_bilan.setGeometry(10,10,190,40)
        self.btn_ajout_bilan.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_bilan.clicked.connect(self.ajouter_bilan)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_bilan)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        
         # Frame Ajout
        self.frame_bilan = QFrame(self)
        self.frame_bilan.setGeometry(10,110,1000,450)
        self.frame_bilan.setStyleSheet("background-color:white")
        

        
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_bilan)
        self.immatriculation_label.setGeometry(20, 20, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_bilan)
        self.immatriculation_input.setGeometry(300, 19, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.types_inspection = QLabel("Types d'inspection :", self.frame_bilan)
        self.types_inspection.setGeometry(20, 50, 300, 80)
        self.types_inspection.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.types_inspection = QComboBox(self.frame_bilan)
        self.types_inspection.setGeometry(300, 70, 300, 35)
        self.types_inspection.setStyleSheet("background-color: white;border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.types_inspection.addItems(["25h","50h","100h","200h","600h","OP1","OP2","OP3","OP4","OP5","OP6","OP7","OP8","OP9","OP10"])
        # self.types_inspection.
        
        self.dernier_inspection = QLabel("Dates dernière inspection :", self.frame_bilan)
        self.dernier_inspection.setGeometry(20, 100, 300, 80)
        self.dernier_inspection.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        
        self.date_dernier_inspection = QDateEdit(self.frame_bilan)
        self.date_dernier_inspection.setGeometry(300, 120, 300, 35)
        self.date_dernier_inspection.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.date_dernier_inspection.setDate(QDate.currentDate())
        self.date_dernier_inspection.setCalendarPopup(True)
        self.date_dernier_inspection.setDisplayFormat("yyyy-MM-dd")
        
        self.heures_dernier_inspection = QLabel("heures dernière inspection :", self.frame_bilan)
        self.heures_dernier_inspection.setGeometry(20, 150, 300, 80)
        self.heures_dernier_inspection.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.heures_dernier_input = QLineEdit(self.frame_bilan)
        self.heures_dernier_input.setGeometry(300, 170, 300, 35)
        self.heures_dernier_input.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        
        
        self.heures_prochains = QLabel("heures prochaines \n inspection :", self.frame_bilan)
        self.heures_prochains.setGeometry(20, 200, 300, 80)
        self.heures_prochains.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.heures_prochains = QLineEdit(self.frame_bilan)
        self.heures_prochains.setGeometry(300, 220, 300, 35)
        self.heures_prochains.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        self.date_prochain_inspection = QLabel("Date de réalisation :", self.frame_bilan)
        self.date_prochain_inspection.setGeometry(20, 250, 300, 80)
        self.date_prochain_inspection.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.date_prochain_inspection = QDateEdit(self.frame_bilan)
        self.date_prochain_inspection.setGeometry(300, 270, 300, 35)
        self.date_prochain_inspection.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.date_prochain_inspection.setDate(QDate.currentDate())
        self.date_prochain_inspection.setCalendarPopup(True)
        self.date_prochain_inspection.setDisplayFormat("yyyy-MM-dd")
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_bilan)
        self.enregistrer.setGeometry(600,370,200,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_bilan)
        
        self.frame_bilan.hide()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON')
            # create table with all expected columns
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS bilan (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    types_inspection TEXT,
                    date_dernier_inspection TEXT,
                    heures_dernier_inspection TEXT,
                    heures_prochains TEXT,
                    date_prochain_inspection TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation) ON DELETE CASCADE
                )
            ''' )
            # ensure older schemas are upgraded with missing columns
            for col in ('heures_dernier_inspection', 'heures_prochains', 'date_prochain_inspection'):
                try:
                    self.cursor.execute(f'ALTER TABLE bilan ADD COLUMN {col} TEXT')
                except Exception:
                    # column already exists or cannot be added; ignore
                    pass
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les bilans
        self.load_immatriculations()
        self.load_bilans()
        self.selected_rows = []
        
    def load_immatriculations(self):
        """Charge tous les matricules depuis la table aircrafts"""
        try:
            self.cursor.execute('SELECT immatriculation FROM aircrafts ORDER BY immatriculation')
            immatriculations = self.cursor.fetchall()
            self.immatriculation_input.clear()
            for immat in immatriculations:
                self.immatriculation_input.addItem(immat[0])
            # update autocomplete list and reset filter
            if hasattr(self, 'filter_completer'):
                self.filter_completer.setModel(QStringListModel([immat[0] for immat in immatriculations]))
            if hasattr(self, 'filter_input'):
                self.filter_input.setText("")
        except Exception as e:
            print('Erreur chargement immatriculations:', e)
    
    def load_bilans(self):
        """Charge les bilans depuis la base de donnees"""
        try:
            self.cursor.execute(
                'SELECT id, immatriculation, types_inspection, date_dernier_inspection, heures_dernier_inspection, heures_prochains, date_prochain_inspection '
                'FROM bilan ORDER BY immatriculation DESC'
            )
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
    
    def apply_filter(self, text: str):
        """Masque les lignes dont l'immatriculation ne contient pas le texte donné."""
        term = text.strip().lower()
        for row in range(self.tableau_affichage.rowCount()):
            item = self.tableau_affichage.item(row, 0)
            if not term:
                self.tableau_affichage.setRowHidden(row, False)
            else:
                show = bool(item and term in item.text().lower())
                self.tableau_affichage.setRowHidden(row, not show)

    def save_bilan(self):
        """Sauvegarde les donnees du bilan dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        types_inspection = self.types_inspection.currentText().strip()
        date_dernier_inspection = self.date_dernier_inspection.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        heures_dernier = self.heures_dernier_input.text().strip()
        heures_prochains = self.heures_prochains.text().strip()
        date_prochain = self.date_prochain_inspection.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
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
                'INSERT INTO bilan (immatriculation, types_inspection, date_dernier_inspection, heures_dernier_inspection, heures_prochains, date_prochain_inspection) VALUES (?, ?, ?, ?, ?, ?)',
                (immat, types_inspection, date_dernier_inspection, heures_dernier, heures_prochains, date_prochain)
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
        self.load_bilans()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_bilan.hide()
    
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
                self.modifier_bilan(row, immat)
            elif action == action_supprimer:
                self.supprimer_bilan(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_bilan(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        types_inspection = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        date_dernier_inspection = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        heures_dernier = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        heures_prochains = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        date_prochain = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.types_inspection.setCurrentText(types_inspection)
        self.date_dernier_inspection.setDateTime(
            QDateTime(QDate.fromString(date_dernier_inspection.split()[0], "yyyy-MM-dd"), QTime())
            if " " in date_dernier_inspection else QDateTime(QDate.currentDate(), QTime())
        )
        self.heures_dernier_input.setText(heures_dernier)
        self.heures_prochains.setText(heures_prochains)
        self.date_prochain_inspection.setDateTime(
            QDateTime(QDate.fromString(date_prochain.split()[0], "yyyy-MM-dd"), QTime())
            if " " in date_prochain else QDateTime(QDate.currentDate(), QTime())
        )
        
        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_bilan(immat))
        
        self.tableau_affichage.setVisible(False)
        self.frame_bilan.show()
    
    def update_bilan(self, immat):
        types_inspection = self.types_inspection.currentText().strip()
        date_dernier_inspection = self.date_dernier_inspection.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        heures_dernier = self.heures_dernier_input.text().strip()
        heures_prochains = self.heures_prochains.text().strip()
        date_prochain = self.date_prochain_inspection.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        try:
            self.cursor.execute(
                'UPDATE bilan SET types_inspection=?, date_dernier_inspection=?, heures_dernier_inspection=?, heures_prochains=?, date_prochain_inspection=? WHERE immatriculation=?',
                (types_inspection, date_dernier_inspection, heures_dernier, heures_prochains, date_prochain, immat)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return
        
        # Reinitialiser le formulaire
        self.reset_form()
        self.load_bilans()
        self.tableau_affichage.setVisible(True)
        self.frame_bilan.hide()
    
    def supprimer_bilan(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_bilan(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_bilan(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM bilan WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_bilans()
        dialog.accept()
    
    def reset_form(self):
        self.types_inspection.setCurrentIndex(0)
        self.heures_dernier_input.clear()
        self.heures_prochains.clear()
        self.date_dernier_inspection.setDate(QDate.currentDate())
        self.date_prochain_inspection.setDate(QDate.currentDate())
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_bilan)
        
    def ajouter_bilan(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_bilan.show()
        
    def voir_listes_bilan(self):
        self.load_bilans()
        self.tableau_affichage.setVisible(True)
        self.frame_bilan.hide()
        self.btn_action.hide()