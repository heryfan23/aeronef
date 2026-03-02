from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class Documents(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Documents et Certifications", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
         # Faire une tableau
        self.tableau_affichage = QTableWidget(20,6,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels(["Immatriculation","CRS(date)","CRS(N° ref)","Date validation certificat de navigabilité","Date validation Licence Aéronef","Date de validation Calibrations(ELT,..)"])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,200)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_documents = QPushButton("Nouveaux",self)
        self.btn_ajout_documents.setGeometry(10,10,190,40)
        self.btn_ajout_documents.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_documents.clicked.connect(self.ajouter_documents)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_documents)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
         # Frame Ajout
        self.frame_documents = QFrame(self)
        self.frame_documents.setGeometry(10,110,1000,450)
        self.frame_documents.setStyleSheet("background-color:white")
        

        
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_documents)
        self.immatriculation_label.setGeometry(20, 20, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_documents)
        self.immatriculation_input.setGeometry(300, 19, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.crs_date = QLabel("CRS (Date):", self.frame_documents)
        self.crs_date.setGeometry(20, 50, 300, 80)
        self.crs_date.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.crs_date = QDateEdit(self.frame_documents)
        self.crs_date.setGeometry(300, 70, 300, 35)
        self.crs_date.setStyleSheet("background-color: white;border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.crs_date.setDate(QDate.currentDate())
        self.crs_date.setCalendarPopup(True)
        self.crs_date.setDisplayFormat("yyyy-MM-dd")
        
        self.crs_num = QLabel("CRS (N° ref):", self.frame_documents)
        self.crs_num.setGeometry(20, 120, 300, 80)
        self.crs_num.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.crs_num = QLineEdit(self.frame_documents)
        self.crs_num.setGeometry(300, 140, 300, 35)
        self.crs_num.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        self.date_certificat = QLabel("Date de validité du  \n Cartificat de Navigabilité (CdN):", self.frame_documents)
        self.date_certificat.setGeometry(20, 170, 300, 80)
        self.date_certificat.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.date_certificat = QDateEdit(self.frame_documents)
        self.date_certificat.setGeometry(300, 190, 300, 35)
        self.date_certificat.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.date_certificat.setDate(QDate.currentDate())
        self.date_certificat.setCalendarPopup(True)
        self.date_certificat.setDisplayFormat("yyyy-MM-dd")
        
        self.date_licence = QLabel("Date de Validité dela \n Licence de Station Aéronef:", self.frame_documents)
        self.date_licence.setGeometry(20, 230, 300, 80)
        self.date_licence.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.date_licence = QDateEdit(self.frame_documents)
        self.date_licence.setGeometry(300, 250, 300, 35)
        self.date_licence.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        self.date_licence.setDate(QDate.currentDate())
        self.date_licence.setCalendarPopup(True)
        self.date_licence.setDisplayFormat("yyyy-MM-dd")
        
        self.dates_calibrations = QLabel("Date de validité des calibrations \n (ELT,Transpondeur,altimètre):", self.frame_documents)
        self.dates_calibrations.setGeometry(20, 280, 300, 80)
        self.dates_calibrations.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.dates_calibrations = QDateEdit(self.frame_documents)
        self.dates_calibrations.setGeometry(300, 310, 300, 35)
        self.dates_calibrations.setDate(QDate.currentDate())
        self.dates_calibrations.setCalendarPopup(True)
        self.dates_calibrations.setDisplayFormat("yyyy-MM-dd")
        self.dates_calibrations.setStyleSheet("background-color: white; border:1px solid black;color:black;color:black;padding:5px;font-size:15px")
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_documents)
        self.enregistrer.setGeometry(600,370,200,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_documents)
        
        self.frame_documents.hide()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    crs_date TEXT,
                    crs_num TEXT,
                    date_certificat TEXT,
                    date_licence TEXT,
                    dates_calibrations TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les documents
        self.load_immatriculations()
        self.load_documents()
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
    
    def load_documents(self):
        """Charge les documents depuis la base de donnees"""
        try:
            self.cursor.execute('SELECT id, immatriculation, crs_date, crs_num, date_certificat, date_licence, dates_calibrations FROM documents ORDER BY immatriculation DESC')
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
    
    def save_documents(self):
        """Sauvegarde les donnees du document dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        crs_date = self.crs_date.date().toString("yyyy-MM-dd")
        crs_num = self.crs_num.text().strip()
        date_certificat = self.date_certificat.date().toString("yyyy-MM-dd")
        date_licence = self.date_licence.date().toString("yyyy-MM-dd")
        dates_calibrations = self.dates_calibrations.date().toString("yyyy-MM-dd")
        
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
                'INSERT INTO documents (immatriculation, crs_date, crs_num, date_certificat, date_licence, dates_calibrations) VALUES (?, ?, ?, ?, ?, ?)',
                (immat, crs_date, crs_num, date_certificat, date_licence, dates_calibrations)
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
        self.load_documents()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_documents.hide()
    
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
                self.modifier_documents(row, immat)
            elif action == action_supprimer:
                self.supprimer_documents(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_documents(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        crs_date = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        crs_num = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        date_certificat = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        date_licence = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        dates_calibrations = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.crs_date.setDate(QDate.fromString(crs_date, "yyyy-MM-dd"))
        self.crs_num.setText(crs_num)
        self.date_certificat.setDate(QDate.fromString(date_certificat, "yyyy-MM-dd"))
        self.date_licence.setDate(QDate.fromString(date_licence, "yyyy-MM-dd"))
        self.dates_calibrations.setDate(QDate.fromString(dates_calibrations, "yyyy-MM-dd"))
        
        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_documents(immat))
        
        self.tableau_affichage.setVisible(False)
        self.frame_documents.show()
    
    def update_documents(self, immat):
        crs_date = self.crs_date.date().toString("yyyy-MM-dd")
        crs_num = self.crs_num.text().strip()
        date_certificat = self.date_certificat.date().toString("yyyy-MM-dd")
        date_licence = self.date_licence.date().toString("yyyy-MM-dd")
        dates_calibrations = self.dates_calibrations.date().toString("yyyy-MM-dd")
        
        try:
            self.cursor.execute(
                'UPDATE documents SET crs_date=?, crs_num=?, date_certificat=?, date_licence=?, dates_calibrations=? WHERE immatriculation=?',
                (crs_date, crs_num, date_certificat, date_licence, dates_calibrations, immat)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return
        
        # Reinitialiser le formulaire
        self.reset_form()
        self.load_documents()
        self.tableau_affichage.setVisible(True)
        self.frame_documents.hide()
    
    def supprimer_documents(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_documents(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_documents(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM documents WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_documents()
        dialog.accept()
    
    def reset_form(self):
        self.crs_date.setDate(QDate.currentDate())
        self.crs_num.clear()
        self.date_certificat.setDate(QDate.currentDate())
        self.date_licence.setDate(QDate.currentDate())
        self.dates_calibrations.setDate(QDate.currentDate())
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_documents)
        
    def ajouter_documents(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_documents.show()
        
    def voir_listes_documents(self):
        self.load_documents()
        self.tableau_affichage.setVisible(True)
        self.frame_documents.hide()
        self.btn_action.hide()
        
        
        