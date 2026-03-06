from PyQt6.QtWidgets import QCompleter, QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QStringListModel, Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class ServicesBulletins(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Bulletins Services (SB) et Modifications", self)
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
        
        # Faire un tableau
        # columns: immatriculation, ref_sbs, description, statut, date_application, date_realisation, date_prochaine
        self.tableau_affichage = QTableWidget(20,7,self)
        self.tableau_affichage.setGeometry(10,110,1000,450)
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Réf SBs",
            "Description",
            "Statut",
            "Date application",
            "Date réalisation",
            "Date prochaine échéance",
        ])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,120)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,120)
        self.tableau_affichage.setColumnWidth(4,120)
        self.tableau_affichage.setColumnWidth(5,120)
        self.tableau_affichage.setColumnWidth(6,120)
        
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_directives = QPushButton("Nouveaux",self)
        self.btn_ajout_directives.setGeometry(10,10,190,40)
        self.btn_ajout_directives.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_directives.clicked.connect(self.ajouter_nouveaux_bulletin)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_bulletin)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
         # Frame Ajout
        self.frame_bulletin = QFrame(self)
        self.frame_bulletin.setGeometry(10,110,1000,450)
        self.frame_bulletin.setStyleSheet("background-color:white")
        

        
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_bulletin)
        self.immatriculation_label.setGeometry(20, 20, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_bulletin)
        self.immatriculation_input.setGeometry(300, 19, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        # remove listes_sbs field; create new fields as per requirements
        self.ref_sbs_label = QLabel("Réf SBs:", self.frame_bulletin)
        self.ref_sbs_label.setGeometry(20, 70, 300, 30)
        self.ref_sbs_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.ref_sbs_input = QLineEdit(self.frame_bulletin)
        self.ref_sbs_input.setGeometry(300, 70, 300, 35)
        self.ref_sbs_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.description_label = QLabel("Description:", self.frame_bulletin)
        self.description_label.setGeometry(20, 120, 300, 30)
        self.description_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.description_input = QLineEdit(self.frame_bulletin)
        self.description_input.setGeometry(300, 120, 300, 35)
        self.description_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.statut_label = QLabel("Statut:", self.frame_bulletin)
        self.statut_label.setGeometry(20, 170, 300, 30)
        self.statut_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.statut_combo = QComboBox(self.frame_bulletin)
        self.statut_combo.setGeometry(300, 170, 300, 35)
        self.statut_combo.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.statut_combo.addItems(["Obligatoire","Recommandé","Optionnel"])
        
        self.date_app_label = QLabel("Date application:", self.frame_bulletin)
        self.date_app_label.setGeometry(20, 220, 300, 30)
        self.date_app_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.date_app_input = QDateEdit(self.frame_bulletin)
        self.date_app_input.setGeometry(300, 220, 300, 35)
        self.date_app_input.setCalendarPopup(True)
        self.date_app_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.date_app_input.setDate(QDate.currentDate())
        
        self.date_real_label = QLabel("Date réalisation:", self.frame_bulletin)
        self.date_real_label.setGeometry(20, 270, 300, 30)
        self.date_real_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.date_real_input = QDateEdit(self.frame_bulletin)
        self.date_real_input.setGeometry(300, 270, 300, 35)
        self.date_real_input.setCalendarPopup(True)
        self.date_real_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.date_real_input.setDate(QDate.currentDate())
        
        self.date_proch_label = QLabel("Date prochaine échéance:", self.frame_bulletin)
        self.date_proch_label.setGeometry(20, 320, 300, 30)
        self.date_proch_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.date_proch_input = QDateEdit(self.frame_bulletin)
        self.date_proch_input.setGeometry(300, 320, 300, 35)
        self.date_proch_input.setCalendarPopup(True)
        self.date_proch_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.date_proch_input.setDate(QDate.currentDate())
        
        # après date prochaine échéance, on passe directement au bouton
        self.enregistrer = QPushButton("Enregistrer",self.frame_bulletin)
        self.enregistrer.setGeometry(700, 370, 150, 40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_bulletin)
        
        self.frame_bulletin.hide()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON')
            # create table with all needed columns; older databases will get missing ones added below
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS service_bulletins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    listes_sbs TEXT,
                    ref_sbs TEXT,
                    description TEXT,
                    statut TEXT,
                    date_application TEXT,
                    date_realisation TEXT,
                    date_prochaine TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation) ON DELETE CASCADE
                )
            ''' )
            # ensure any missing columns exist (migration)
            cols = [row[1] for row in self.cursor.execute("PRAGMA table_info(service_bulletins)").fetchall()]
            for col_name in ("ref_sbs","description","statut","date_application","date_realisation","date_prochaine"):
                if col_name not in cols:
                    self.cursor.execute(f"ALTER TABLE service_bulletins ADD COLUMN {col_name} TEXT")
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les bulletins
        self.load_immatriculations()
        self.load_bulletins()
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
    
    def load_bulletins(self):
        """Charge les service bulletins depuis la base de donnees"""
        try:
            self.cursor.execute('''
                SELECT id, immatriculation, ref_sbs, description, statut,
                       date_application, date_realisation, date_prochaine
                FROM service_bulletins
                ORDER BY immatriculation DESC
            ''')
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
    
    def save_bulletin(self):
        """Sauvegarde les donnees du bulletin dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        ref_sbs = self.ref_sbs_input.text().strip()
        description = self.description_input.text().strip()
        statut = self.statut_combo.currentText()
        date_application = self.date_app_input.date().toString("yyyy-MM-dd")
        date_realisation = self.date_real_input.date().toString("yyyy-MM-dd")
        date_prochaine = self.date_proch_input.date().toString("yyyy-MM-dd")

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
                'INSERT INTO service_bulletins (immatriculation, ref_sbs, description, statut, date_application, date_realisation, date_prochaine) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (immat, ref_sbs, description, statut, date_application, date_realisation, date_prochaine)
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
        self.load_bulletins()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_bulletin.hide()
    
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
                self.modifier_bulletin(row, immat)
            elif action == action_supprimer:
                self.supprimer_bulletin(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_bulletin(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        ref_sbs = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        description = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        statut = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        date_application = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        date_realisation = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        date_prochaine = self.tableau_affichage.item(row, 6).text() if self.tableau_affichage.item(row, 6) else ""

        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.ref_sbs_input.setText(ref_sbs)
        self.description_input.setText(description)
        self.statut_combo.setCurrentText(statut)
        if date_application:
            self.date_app_input.setDate(QDate.fromString(date_application, "yyyy-MM-dd"))
        if date_realisation:
            self.date_real_input.setDate(QDate.fromString(date_realisation, "yyyy-MM-dd"))
        if date_prochaine:
            self.date_proch_input.setDate(QDate.fromString(date_prochaine, "yyyy-MM-dd"))

        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_bulletin(immat))

        self.tableau_affichage.setVisible(False)
        self.frame_bulletin.show()
    
    def update_bulletin(self, immat):
        ref_sbs = self.ref_sbs_input.text().strip()
        description = self.description_input.text().strip()
        statut = self.statut_combo.currentText()
        date_application = self.date_app_input.date().toString("yyyy-MM-dd")
        date_realisation = self.date_real_input.date().toString("yyyy-MM-dd")
        date_prochaine = self.date_proch_input.date().toString("yyyy-MM-dd")

        try:
            self.cursor.execute(
                'UPDATE service_bulletins SET ref_sbs=?, description=?, statut=?, date_application=?, '
                'date_realisation=?, date_prochaine=? WHERE immatriculation=?',
                (ref_sbs, description, statut, date_application, date_realisation, date_prochaine, immat)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return

        # Reinitialiser le formulaire
        self.reset_form()
        self.load_bulletins()
        self.tableau_affichage.setVisible(True)
        self.frame_bulletin.hide()
    
    def supprimer_bulletin(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_bulletin(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_bulletin(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM service_bulletins WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_bulletins()
        dialog.accept()
    
    def reset_form(self):
        self.ref_sbs_input.clear()
        self.description_input.clear()
        self.statut_combo.setCurrentIndex(0)
        self.date_app_input.setDate(QDate.currentDate())
        self.date_real_input.setDate(QDate.currentDate())
        self.date_proch_input.setDate(QDate.currentDate())
        # no historique/reference to clear
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_bulletin)
        
    def ajouter_nouveaux_bulletin(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_bulletin.show()
        
    def voir_listes_bulletin(self):
        self.load_bulletins()
        self.tableau_affichage.setVisible(True)
        self.frame_bulletin.hide()
        self.btn_action.hide()
    
    
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