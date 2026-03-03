from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class Directives(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Diréctives de Navigabilité (ADs / Consignes de navigabilité)", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        # Faire une tableau
        # adjust column count for new fields
        self.tableau_affichage = QTableWidget(20,11,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        # new headers: statut, etat, autorite, date_realisation etc
        self.tableau_affichage.setHorizontalHeaderLabels(["Immatriculation","références CN/AD","Titre/Description","Statut","Etat","Autorité","Date Réalisation","Date Applications","Heures,Cycles (à l'applications)","Prochaine Echeance","Méthode de conformité"])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,120)
        self.tableau_affichage.setColumnWidth(4,120)
        self.tableau_affichage.setColumnWidth(5,100)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_directives = QPushButton("Nouveaux",self)
        self.btn_ajout_directives.setGeometry(10,10,190,40)
        self.btn_ajout_directives.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_directives.clicked.connect(self.fonction_directive)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_directives)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
         # Frame Ajout
        self.frame_directives = QFrame(self)
        self.frame_directives.setGeometry(10,110,1000,480)
        self.frame_directives.setStyleSheet("background-color:white")

        # layout to manage field geometry and avoid overlapping
        form_layout = QGridLayout(self.frame_directives)
        form_layout.setContentsMargins(20,20,20,20)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)

        # first row - immatriculation
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_directives)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.immatriculation_input = QComboBox(self.frame_directives)
        self.immatriculation_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")

        # second row - liste ads
        self.listes_ads = QLabel("Listes des Ads Applicables à l'aéronef moteurs,hélices,équipements:", self.frame_directives)
        self.listes_ads.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.listes_ads.setWordWrap(True)

        # third row - references and titre
        self.references = QLabel("Réference CN/AD :",self.frame_directives)
        self.references.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.references_input = QLineEdit(self.frame_directives)
        self.references_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")

        self.titre = QLabel("Titre / description :",self.frame_directives)
        self.titre.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.titre_input = QLineEdit(self.frame_directives)
        self.titre_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")

        # fourth row - statut and etat
        self.statut_label = QLabel("Statut :", self.frame_directives)
        self.statut_label.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.statut_input = QComboBox(self.frame_directives)
        self.statut_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        for opt in ["nom applicable","applicable immediatement","applicable differee ou repetitive","consignes operationnelles"]:
            self.statut_input.addItem(opt)
       
        self.etat = QLabel("Etat :",self.frame_directives)
        self.etat.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.etat_input = QComboBox(self.frame_directives)
        self.etat_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        for opt in ["cellule","moteur","helices","equipements"]:
            self.etat_input.addItem(opt)


        # fifth row - autorite and date_realisation
        self.autorite = QLabel("Autorité :",self.frame_directives)
        self.autorite.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.autorite_input = QComboBox(self.frame_directives)
        self.autorite_input.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        for opt in ["EASA","FAA","ACM"]:
            self.autorite_input.addItem(opt)

        self.date_realisation = QLabel("Date de réalisation :",self.frame_directives)
        self.date_realisation.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.date_realisation_input = QDateEdit(self.frame_directives)
        self.date_realisation_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")
        self.date_realisation_input.setDate(QDate.currentDate())
        self.date_realisation_input.setCalendarPopup(True)
        self.date_realisation_input.setDisplayFormat("yyyy-MM-dd")

        # sixth row - date_applications and heurs
        self.date_applications = QLabel("Dates d'application :",self.frame_directives)
        self.date_applications.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.date_applications_input = QDateEdit(self.frame_directives)
        self.date_applications_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")
        self.date_applications_input.setDate(QDate.currentDate())
        self.date_applications_input.setCalendarPopup(True)
        self.date_applications_input.setDisplayFormat("yyyy-MM-dd")

        self.heurs = QLabel("Heures / Cycles :",self.frame_directives)
        self.heurs.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.heurs_input = QLineEdit(self.frame_directives)
        self.heurs_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")

        # seventh row - prochain and methodes
        self.prochain = QLabel(" Date Prochain \n échéance :",self.frame_directives)
        self.prochain.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.prochain_input = QDateEdit(self.frame_directives)
        self.prochain_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")
        self.prochain_input.setDate(QDate.currentDate())
        self.prochain_input.setCalendarPopup(True)
        self.prochain_input.setDisplayFormat("yyyy-MM-dd")

        self.methodes = QLabel("Methodes \n Conformités :",self.frame_directives)
        self.methodes.setStyleSheet("color: black; font-size: 16px;background-color:none;")
        self.methodes_input = QDateEdit(self.frame_directives)
        self.methodes_input.setStyleSheet("background-color: white;color:black;padding:5px;font-size:15px;border:1px solid black")
        self.methodes_input.setDate(QDate.currentDate())
        self.methodes_input.setCalendarPopup(True)
        self.methodes_input.setDisplayFormat("yyyy-MM-dd")

        # add widgets to layout
        form_layout.addWidget(self.immatriculation_label, 0, 0)
        form_layout.addWidget(self.immatriculation_input, 0, 1, 1, 3)
        form_layout.addWidget(self.listes_ads, 1, 0, 1, 4)

        form_layout.addWidget(self.references, 2, 0)
        form_layout.addWidget(self.references_input, 2, 1)
        form_layout.addWidget(self.titre, 2, 2)
        form_layout.addWidget(self.titre_input, 2, 3)

        form_layout.addWidget(self.statut_label, 3, 0)
        form_layout.addWidget(self.statut_input, 3, 1)
        form_layout.addWidget(self.etat, 3, 2)
        form_layout.addWidget(self.etat_input, 3, 3)

        form_layout.addWidget(self.autorite, 4, 0)
        form_layout.addWidget(self.autorite_input, 4, 1)
        form_layout.addWidget(self.date_realisation, 4, 2)
        form_layout.addWidget(self.date_realisation_input, 4, 3)

        form_layout.addWidget(self.date_applications, 5, 0)
        form_layout.addWidget(self.date_applications_input, 5, 1)
        form_layout.addWidget(self.heurs, 5, 2)
        form_layout.addWidget(self.heurs_input, 5, 3)

        form_layout.addWidget(self.prochain, 6, 0)
        form_layout.addWidget(self.prochain_input, 6, 1)
        form_layout.addWidget(self.methodes, 6, 2)
        form_layout.addWidget(self.methodes_input, 6, 3)
        

        self.enregistrer = QPushButton("Enregistrer",self.frame_directives)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px;padding:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_directive)
        form_layout.addWidget(self.enregistrer, 7, 3)
        
        self.frame_directives.hide()
        
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS directives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    `references` TEXT,
                    titre TEXT,
                    statut TEXT,
                    etat TEXT,
                    autorite TEXT,
                    date_realisation TEXT,
                    date_applications TEXT,
                    heures_cycles TEXT,
                    prochaine_echeance TEXT,
                    methode_conformite TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation) ON DELETE CASCADE
                )
            ''' )
            self.conn.commit()
            # migrate existing schema by adding new columns if they don't exist
            try:
                self.cursor.execute("ALTER TABLE directives ADD COLUMN statut TEXT")
            except Exception:
                pass
            try:
                self.cursor.execute("ALTER TABLE directives ADD COLUMN autorite TEXT")
            except Exception:
                pass
            try:
                self.cursor.execute("ALTER TABLE directives ADD COLUMN date_realisation TEXT")
            except Exception:
                pass
            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les directives
        self.load_immatriculations()
        self.load_directives()
        self.selected_rows = []
        
        # Flag pour mode édition
        self.edit_mode = False
        self.current_edit_immat = None
        
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
    
    def load_directives(self):
        """Charge les directives depuis la base de donnees"""
        try:
            self.cursor.execute('SELECT id, immatriculation, `references`, titre, statut, etat, autorite, date_realisation, date_applications, heures_cycles, prochaine_echeance, methode_conformite FROM directives ORDER BY immatriculation DESC')
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
    
    def save_directive(self):
        """Sauvegarde ou met à jour les donnees de la directive"""
        immat = self.immatriculation_input.currentText().strip()
        references = self.references_input.text().strip()
        titre = self.titre_input.text().strip()
        statut = self.statut_input.currentText().strip()
        etat = self.etat_input.currentText().strip()
        autorite = self.autorite_input.currentText().strip()
        date_realisation = self.date_realisation_input.date().toString("yyyy-MM-dd")
        date_applications = self.date_applications_input.date().toString("yyyy-MM-dd")
        heures_cycles = self.heurs_input.text().strip()
        prochaine_echeance = self.prochain_input.date().toString("yyyy-MM-dd")
        methode_conformite = self.methodes_input.date().toString("yyyy-MM-dd")
        
        if not immat:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez selectionner une immatriculation")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        try:
            if self.edit_mode:
                # Mode édition: UPDATE
                self.cursor.execute(
                    'UPDATE directives SET `references`=?, titre=?, statut=?, etat=?, autorite=?, date_realisation=?, date_applications=?, heures_cycles=?, prochaine_echeance=?, methode_conformite=? WHERE immatriculation=?',
                    (references, titre, statut, etat, autorite, date_realisation, date_applications, heures_cycles, prochaine_echeance, methode_conformite, self.current_edit_immat)
                )
            else:
                # Mode création: INSERT
                self.cursor.execute(
                    'INSERT INTO directives (immatriculation, `references`, titre, statut, etat, autorite, date_realisation, date_applications, heures_cycles, prochaine_echeance, methode_conformite) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (immat, references, titre, statut, etat, autorite, date_realisation, date_applications, heures_cycles, prochaine_echeance, methode_conformite)
                )
            self.conn.commit()
        except Exception as e:
            print('Erreur sauvegarde DB:', e)
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
        self.load_directives()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_directives.hide()
    
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
                self.modifier_directive(row, immat)
            elif action == action_supprimer:
                self.supprimer_directive(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_directive(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        references = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        titre = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        statut = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        etat = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        autorite = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        date_realisation = self.tableau_affichage.item(row, 6).text() if self.tableau_affichage.item(row, 6) else ""
        date_applications = self.tableau_affichage.item(row, 7).text() if self.tableau_affichage.item(row, 7) else ""
        heures_cycles = self.tableau_affichage.item(row, 8).text() if self.tableau_affichage.item(row, 8) else ""
        prochaine_echeance = self.tableau_affichage.item(row, 9).text() if self.tableau_affichage.item(row, 9) else ""
        methode_conformite = self.tableau_affichage.item(row, 10).text() if self.tableau_affichage.item(row, 10) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.references_input.setText(references)
        self.titre_input.setText(titre)
        # populate new fields
        self.statut_input.setCurrentText(statut)
        self.etat_input.setCurrentText(etat)
        self.autorite_input.setCurrentText(autorite)
        self.date_realisation_input.setDate(QDate.fromString(date_realisation, "yyyy-MM-dd"))
        self.date_applications_input.setDate(QDate.fromString(date_applications, "yyyy-MM-dd"))
        self.heurs_input.setText(heures_cycles)
        self.prochain_input.setDate(QDate.fromString(prochaine_echeance, "yyyy-MM-dd"))
        self.methodes_input.setDate(QDate.fromString(methode_conformite, "yyyy-MM-dd"))
        
        # Activer le mode édition
        self.edit_mode = True
        self.current_edit_immat = immat
        
        # Changer le titre du bouton
        self.enregistrer.setText("Mettre a jour")
        
        self.tableau_affichage.setVisible(False)
        self.frame_directives.show()
    

    
    def supprimer_directive(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_directive(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_directive(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM directives WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_directives()
        dialog.accept()
    
    def reset_form(self):
        self.references_input.clear()
        self.titre_input.clear()
        self.statut_input.setCurrentIndex(0)
        self.etat_input.setCurrentIndex(0)
        self.autorite_input.setCurrentIndex(0)
        self.date_realisation_input.setDate(QDate.currentDate())
        self.date_applications_input.setDate(QDate.currentDate())
        self.heurs_input.clear()
        self.prochain_input.setDate(QDate.currentDate())
        self.methodes_input.setDate(QDate.currentDate())
        self.enregistrer.setText("Enregistrer")
        # Désactiver le mode édition
        self.edit_mode = False
        self.current_edit_immat = None
        
    def fonction_directive(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_directives.show()
        
    def voir_listes_directives(self):
        self.load_directives()
        self.tableau_affichage.setVisible(True)
        self.frame_directives.hide()
        self.btn_action.hide()