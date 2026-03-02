from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QTableWidgetItem, QDateEdit, QMessageBox, QMenu, QAbstractItemView, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class AjoutInfo(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 450)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
    
        self.label_info = QLabel("Informations Génerales de l'aéronef",self)
        self.label_info.setGeometry(20,50,400,50)
        self.label_info.setStyleSheet("color:white;font-size:20px;background-color:None")
        self.lower()
        
        # Faire une tableau
        self.tableau_affichage = QTableWidget(20,6,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels(["Immatriculation","Marque/modele","Numero Serie","Date de Fabrication","Propriétaire/Exploitant","heures total"])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,200)
        self.tableau_affichage.setColumnWidth(4,200)
        self.tableau_affichage.setColumnWidth(5,200)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black;border:none")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        
        
        self.btn_voir_info = QPushButton("Voir informations",self)
        self.btn_voir_info.setGeometry(220,10,190,40)
        self.btn_voir_info.setStyleSheet("background-color:blue;font-size:13px;color:white;;border-radius:10px")
        self.btn_voir_info.clicked.connect(self.voir_informations)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(420,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:13px;color:white;;border-radius:10px")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        self.btn_ajout = QPushButton("Nouveaux",self)
        self.btn_ajout.setGeometry(10,10,190,40)
        self.btn_ajout.setStyleSheet("background-color:blue;font-size:13px;color:white;;border-radius:10px")
        self.btn_ajout.clicked.connect(self.ajouter_information)
        
        
        # Frame Ajout
        self.frame_ajout = QFrame(self)
        self.frame_ajout.setGeometry(10,110,1000,450)
        self.frame_ajout.setStyleSheet("background-color:white")

        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        self.titre = QLabel("Ajouter l'information de l'aeronef", self.frame_ajout)
        self.titre.setGeometry(20, 10, 750, 50)
        self.titre.setStyleSheet("font-size: 20px;color:black;background-color:none")
        
        self.hr = QLabel(self.frame_ajout)
        self.hr.setGeometry(0,63,1200,3)
        self.hr.setStyleSheet("background-color:black")
        
    
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_ajout)
        self.immatriculation_label.setGeometry(20, 100, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        
        self.immatriculation_input = QLineEdit(self.frame_ajout)
        self.immatriculation_input.setGeometry(200, 99, 300, 35)
        self.immatriculation_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.marque = QLabel("Marque/Modèle:", self.frame_ajout)
        self.marque.setGeometry(20, 150, 150, 30)
        self.marque.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        
        self.marque = QLineEdit(self.frame_ajout)
        self.marque.setGeometry(200, 149, 300, 35)
        self.marque.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black;")
        
        self.serie = QLabel("Numéro de Série:", self.frame_ajout)
        self.serie.setGeometry(20, 200, 150, 30)
        self.serie.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        
        self.serie = QLineEdit(self.frame_ajout)
        self.serie.setGeometry(200, 199, 300, 35)
        self.serie.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px;")
        
        self.date_fabrication = QLabel("Date fabrication:", self.frame_ajout)
        self.date_fabrication.setGeometry(20, 250, 150, 30)
        self.date_fabrication.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        
        self.date_fabrication = QDateEdit(self.frame_ajout)
        self.date_fabrication.setGeometry(200, 249, 300, 35)
        self.date_fabrication.setDate(QDate.currentDate())
        self.date_fabrication.setCalendarPopup(True)
        self.date_fabrication.setDisplayFormat("yyyy-MM-dd")
        self.date_fabrication.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px;")
        
        self.ppte_exploi = QLabel("Propriétaire:", self.frame_ajout)
        self.ppte_exploi.setGeometry(550, 100, 150, 30)
        self.ppte_exploi.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        
        self.ppte_exploi = QLineEdit(self.frame_ajout)
        self.ppte_exploi.setGeometry(650, 99, 300, 35)
        self.ppte_exploi.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px;")
        
         
        self.heures_total = QLabel("Heures Total \n (hh:mm) :", self.frame_ajout)
        self.heures_total.setGeometry(550, 150, 150, 50)
        self.heures_total.setStyleSheet("color: black; font-size: 16px;background-color:none;;")
        
        self.heures_total = QLineEdit(self.frame_ajout)
        self.heures_total.setGeometry(650, 160, 300, 35)
        self.heures_total.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.hr_2 = QLabel(self.frame_ajout)
        self.hr_2.setGeometry(0,320,1200,3)
        self.hr_2.setStyleSheet("background-color:black")
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_ajout)
        self.enregistrer.setGeometry(700,350,200,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px;")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_information)

        self.frame_ajout.hide()

        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS aircrafts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT UNIQUE NOT NULL,
                    marque TEXT,
                    serie TEXT,
                    date_fabrication TEXT,
                    proprietaire TEXT,
                    heures_total TEXT
                )
            ''')
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)

        # Charger les informations existantes
        self.load_informations()
        self.selected_rows = []
        
        
        
        
    def showEvent(self, event):
        parent = self.parent()
        if parent is not None and hasattr(parent, 'tableau_affichage'):
            try:
                parent.tableau_affichage.hide()
            except Exception:
                pass
        super().showEvent(event)

    def hideEvent(self, event):
        parent = self.parent()
        if parent is not None and hasattr(parent, 'tableau_affichage'):
            try:
                parent.tableau_affichage.show()
            except Exception:
                pass
        super().hideEvent(event)
        
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
            
            
            # Augmenter la hauteur du menu et le style
            menu.setStyleSheet("""
                QMenu { 
                    background-color: gray; 
                    color: white; 
                    padding: 5px 0px;
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
        
            # mettre menu comme taille du bouton action
            menu.setFixedWidth(self.btn_action.width());
            
            action = menu.exec(self.btn_action.mapToGlobal(self.btn_action.rect().bottomLeft()))
            
            if action == action_modifier:
                self.modifier_information(row, immat)
            elif action == action_supprimer:
                self.supprimer_information(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez sélectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_information(self, row, immat):
        # Récupérer les données de la ligne avec vérification
        marque = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        serie = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        date_fab = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        proprietaire = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        heures = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setText(immat)
        self.immatriculation_input.setReadOnly(True)
        self.marque.setText(marque)
        self.serie.setText(serie)
        self.date_fabrication.setDate(QDate.fromString(date_fab, "yyyy-MM-dd"))
        self.ppte_exploi.setText(proprietaire)
        self.heures_total.setText(heures)
        
        # Changer le titre et le comportement du formulaire
        self.titre.setText("Modifier l'information de l'aeronef")
        self.enregistrer.setText("Mettre à jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_information(immat))
        
        self.tableau_affichage.setVisible(False)
        self.frame_ajout.show()
    
    def update_information(self, immat):
        marque = self.marque.text().strip()
        serie = self.serie.text().strip()
        datefab = self.date_fabrication.date().toString("yyyy-MM-dd")
        proprietaire = self.ppte_exploi.text().strip()
        heures = self.heures_total.text().strip()
        
        try:
            self.cursor.execute(
                'UPDATE aircrafts SET marque=?, serie=?, date_fabrication=?, proprietaire=?, heures_total=? WHERE immatriculation=?',
                (marque, serie, datefab, proprietaire, heures, immat)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise à jour DB:', e)
            return
        
        # Réinitialiser le formulaire
        self.reset_form()
        self.load_informations()
        self.tableau_affichage.setVisible(True)
        self.frame_ajout.hide()
    
    def supprimer_information(self, row, immat):
        # Créer une boîte de dialogue personnalisée
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirmation")
        dialog.setGeometry(400, 300, 450, 150)
        dialog.setStyleSheet("QDialog { background-color: #2d2d69; }")
        
        # Label du message
        label = QLabel(f"Êtes-vous sûr de vouloir supprimer l'aéronef avec l'immatriculation '{immat}' ?")
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_aircraft(immat, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_aircraft(self, immat, dialog):
        """Confirme la suppression de l'aéronef"""
        try:
            self.cursor.execute('DELETE FROM aircrafts WHERE immatriculation=?', (immat,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_informations()
        dialog.accept()
    
    def reset_form(self):
        self.immatriculation_input.clear()
        self.immatriculation_input.setReadOnly(False)
        self.marque.clear()
        self.serie.clear()
        self.date_fabrication.setDate(QDate.currentDate())
        self.ppte_exploi.clear()
        self.heures_total.clear()
        self.titre.setText("Ajouter l'information de l'aeronef")
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_information)
        
    def ajouter_information(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_ajout.show()
        
    def voir_informations(self):
        # Recharger avant d'afficher
        self.load_informations()
        self.tableau_affichage.setVisible(True)
        self.frame_ajout.hide()
        self.btn_action.hide()

    def save_information(self):
        immat = self.immatriculation_input.text().strip()
        marque = self.marque.text().strip()
        serie = self.serie.text().strip()
        datefab = self.date_fabrication.date().toString("yyyy-MM-dd")
        proprietaire = self.ppte_exploi.text().strip()
        heures = self.heures_total.text().strip()

        if immat or marque or serie or datefab or proprietaire or heures:
            if not immat:
                return

            try:
                self.cursor.execute(
                    'INSERT INTO aircrafts (immatriculation, marque, serie, date_fabrication, proprietaire, heures_total) VALUES (?, ?, ?, ?, ?, ?)',
                    (immat, marque, serie, datefab, proprietaire, heures)
                )
                self.conn.commit()
            except sqlite3.IntegrityError:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Critical)
                msg.setWindowTitle("Erreur")
                msg.setText(f"L'immatriculation '{immat}' existe déjà, veuillez en choisir une autre.")
                msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
                msg.exec()
                return
            except Exception as e:
                print('Erreur insertion DB:', e)
                return
        else:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Champs vides")
            msg.setText("Veuillez remplir au moins un champ avant d'enregistrer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return

        # nettoyer les champs
        self.immatriculation_input.clear()
        self.marque.clear()
        self.serie.clear()
        self.date_fabrication.setDate(QDate.currentDate())
        self.ppte_exploi.clear()
        self.heures_total.clear()

        # recharger le tableau
        self.load_informations()

    def load_informations(self):
        try:
            self.cursor.execute('SELECT immatriculation, marque, serie, date_fabrication, proprietaire, heures_total FROM aircrafts ORDER BY id DESC')
            rows = self.cursor.fetchall()
        except Exception as e:
            print('Erreur lecture DB:', e)
            rows = []

        # ajuster le nombre de lignes du tableau
        row_count = max(20, len(rows))
        self.tableau_affichage.setRowCount(row_count)

        # vider le contenu existant
        self.tableau_affichage.clearContents()

        # remplir avec les données
        for idx, row in enumerate(rows):
            for col, value in enumerate(row):
                self.tableau_affichage.setItem(idx, col, QTableWidgetItem(str(value)))
        
        
        
        
    
        