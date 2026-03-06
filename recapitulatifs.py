from PyQt6.QtWidgets import QCompleter, QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import QStringListModel, Qt
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
        
        
        self.titre = QLabel("📊 Récapitulatifs des Échéances", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 22px;color:white;background-color:none;font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);")
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        # filtre immatriculation
        self.filter_label = QLabel("🔍 Filtrer immatriculation :", self)
        self.filter_label.setGeometry(440, 70, 180, 30)
        self.filter_label.setStyleSheet("color:white; font-size:14px; background-color:None; font-weight: bold;")
        self.filter_input = QLineEdit(self)
        self.filter_input.setGeometry(620, 70, 200, 30)
        self.filter_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #1976d2;
                border-radius: 6px;
                padding: 5px 10px;
                font-size: 14px;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #1565c0;
                background-color: #f0f8ff;
            }
        """)
        self.filter_input.setPlaceholderText("Tapez pour filtrer...")
        self.filter_input.textChanged.connect(self.apply_filter)
        self.filter_completer = QCompleter()
        self.filter_input.setCompleter(self.filter_completer)
        
        # tableau récapitulatif détaillé (lecture seule) : colonnes structurées
        self.tableau_affichage = QTableWidget(20,8,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Infos Avion",
            "Dernier Vol",
            "Moteurs",
            "Hélices",
            "Temps Vie",
            "Documents",
            "Comptes"
        ])
        self.tableau_affichage.setColumnWidth(0,120)
        self.tableau_affichage.setColumnWidth(1,150)
        self.tableau_affichage.setColumnWidth(2,120)
        self.tableau_affichage.setColumnWidth(3,150)
        self.tableau_affichage.setColumnWidth(4,150)
        self.tableau_affichage.setColumnWidth(5,120)
        self.tableau_affichage.setColumnWidth(6,120)
        self.tableau_affichage.setColumnWidth(7,120)
        # Style amélioré pour le tableau
        self.tableau_affichage.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #ddd;
                selection-background-color: #e3f2fd;
                selection-color: black;
                alternate-background-color: #f9f9f9;
            }
            QHeaderView::section {
                background-color: #1976d2;
                color: white;
                padding: 8px;
                border: 1px solid #1565c0;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QTableWidget::item:selected {
                background-color: #2196f3;
                color: white;
            }
        """)
        self.tableau_affichage.setAlternatingRowColors(True)
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        self.tableau_affichage.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        
        # Recapitulatif est lecture seule: on masque les commandes de saisie
        self.btn_ajout_travaux = QPushButton("Nouveaux",self)
        self.btn_ajout_travaux.hide()
        
        self.btn_voir_listes = QPushButton("🔄 Actualiser",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                font-size: 15px;
                font-weight: bold;
                border-radius: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_voir_listes.clicked.connect(self.voir_listes_recaitulatifs)
        self.btn_voir_listes.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self.btn_action = QPushButton("Action",self)
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
            # enable fk support so that cascading works
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS recapitulatifs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    types TEXT,
                    description TEXT,
                    certifications TEXT,
                    num_ref_ata TEXT,
                    comp_description TEXT,
                    date_proc_rev TEXT,
                    pot_restant TEXT,
                    pot_restant_cycles TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation) ON DELETE CASCADE
                )
            ''' )
            self.conn.commit()
            # Migration: ensure newer columns exist for older DBs
            try:
                self.cursor.execute("PRAGMA table_info(recapitulatifs)")
                cols = [r[1] for r in self.cursor.fetchall()]
                missing = []
                for col in ['certifications','num_ref_ata','comp_description','date_proc_rev','pot_restant','pot_restant_cycles']:
                    if col not in cols:
                        missing.append(col)
                for col in missing:
                    # all added as TEXT
                    self.cursor.execute(f'ALTER TABLE recapitulatifs ADD COLUMN {col} TEXT')
                if missing:
                    self.conn.commit()
            except Exception:
                pass
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et construire le tableau agrégé
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
            # update autocomplete list and reset filter
            if hasattr(self, 'filter_completer'):
                self.filter_completer.setModel(QStringListModel([immat[0] for immat in immatriculations]))
            if hasattr(self, 'filter_input'):
                self.filter_input.setText("")
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
        """Construire un récapitulatif global en agrégeant les autres tables."""
        try:
            self.cursor.execute('SELECT immatriculation FROM aircrafts ORDER BY immatriculation')
            immats = [r[0] for r in self.cursor.fetchall()]
        except Exception as e:
            print('Erreur lecture immatriculations pour récapitulatifs:', e)
            immats = []

        # prepare storage for details
        self.full_data = {}
        row_count = max(20, len(immats))
        self.tableau_affichage.setRowCount(row_count)
        self.tableau_affichage.clearContents()

        for idx, immat in enumerate(immats):
            self.full_data[idx] = immat
            data = self.build_detailed_data(immat)
            self.tableau_affichage.setItem(idx, 0, QTableWidgetItem(immat))
            for col in range(1, 8):
                item = QTableWidgetItem(data[col-1])
                item.setData(Qt.ItemDataRole.UserRole, immat)
                self.tableau_affichage.setItem(idx, col, item)

    def build_detailed_data(self, immat: str) -> list:
        """Rassemble des informations détaillées de différentes tables pour une immatriculation, retourne une liste pour chaque colonne."""
        data = ["", "", "", "", "", "", ""]  # 7 colonnes de données

        try:
            # Colonne 1: Infos Avion
            self.cursor.execute(
                'SELECT marque, serie, heures_total, cycles_total '
                'FROM aircrafts WHERE immatriculation=?',
                (immat,)
            )
            row = self.cursor.fetchone()
            if row:
                data[0] = f"Marque: {row[0]}\nSérie: {row[1]}\nHeures: {row[2]}\nCycles: {row[3]}"
        except Exception:
            pass

        try:
            # Colonne 2: Dernier Vol
            self.cursor.execute(
                'SELECT date_vol, temps_vol, cycles FROM heures_vol '
                'WHERE immatriculation=? ORDER BY date_vol DESC LIMIT 1',
                (immat,)
            )
            row = self.cursor.fetchone()
            if row:
                data[1] = f"Date: {row[0]}\nHeures: {row[1]}\nCycles: {row[2]}"
        except Exception:
            pass

        try:
            # Colonne 3: Moteurs
            self.cursor.execute(
                'SELECT marque, numero_serie, pot_restant, pot_restant_cycles FROM moteurs '
                'WHERE immatriculation=?',
                (immat,)
            )
            motors = self.cursor.fetchall()
            if motors:
                motors_list = []
                for m in motors:
                    motors_list.append(f"{m[0]} N° série:{m[1]}\nPotentiel restant:\n{m[2]} heures\n{m[3]} cycles")
                data[2] = "\n\n".join(motors_list)
        except Exception:
            pass

        try:
            # Colonne 4: Hélices
            self.cursor.execute(
                'SELECT marque, numero_serie, pot_restant, pot_restant_cycles FROM helices '
                'WHERE immatriculation=?',
                (immat,)
            )
            props = self.cursor.fetchall()
            if props:
                props_list = []
                for p in props:
                    props_list.append(f"{p[0]} N° série:{p[1]}\nPotentiel restant:\n{p[2]} heures\n{p[3]} cycles")
                data[3] = "\n\n".join(props_list)
        except Exception:
            pass

        try:
            # Colonne 5: Temps de Vie
            self.cursor.execute(
                'SELECT pot_restant, pot_restant_cycles FROM temps_vie '
                'WHERE immatriculation=? ORDER BY rowid DESC LIMIT 1',
                (immat,)
            )
            row = self.cursor.fetchone()
            if row:
                data[4] = f"Potentiel restant:\n{row[0]} heures\n{row[1]} cycles"
        except Exception:
            pass

        try:
            # Colonne 6: Documents
            self.cursor.execute(
                'SELECT crs_date, crs_num FROM documents '
                'WHERE immatriculation=? ORDER BY crs_date DESC LIMIT 1',
                (immat,)
            )
            row = self.cursor.fetchone()
            if row:
                data[5] = f"CRS:\nDate: {row[0]}\nRef: {row[1]}"
        except Exception:
            pass

        try:
            # Colonne 7: Comptes
            directives_cnt = self.cursor.execute('SELECT COUNT(*) FROM directives WHERE immatriculation=?', (immat,)).fetchone()[0]
            travaux_cnt = self.cursor.execute('SELECT COUNT(*) FROM travaux WHERE immatriculation=?', (immat,)).fetchone()[0]
            sb_cnt = self.cursor.execute('SELECT COUNT(*) FROM service_bulletins WHERE immatriculation=?', (immat,)).fetchone()[0]
            data[6] = f"Directives: {directives_cnt}\nTravaux: {travaux_cnt}\nSBs: {sb_cnt}"
        except Exception:
            pass

        return data

    def save_recapitulatifs(self):
        """Sauvegarde les donnees du recapitulatif dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        types = self.types_.currentText().strip()
        description = self.comp_description_input.text().strip()
        certifications = self.certifications.text().strip()
        num_ref = self.num_ref_ata_input.text().strip()
        comp_desc = self.comp_description_input.text().strip()
        date_proc = self.date_proc_rev_input.text().strip()
        pot_rem = self.pot_restant_input.text().strip()
        pot_rem_cycles = self.pot_restant_cycles_input.text().strip()

        # Validate numeric fields if filled
        for field, name in [(pot_rem,"Pot restant"),(pot_rem_cycles,"Pot restant Cycles")]:
            if field:
                try:
                    float(field)
                except ValueError:
                    msg = QMessageBox(self)
                    msg.setIcon(QMessageBox.Icon.Warning)
                    msg.setWindowTitle("Erreur")
                    msg.setText(f"Le champ '{name}' doit être un nombre.")
                    msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
                    msg.exec()
                    return
        
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
                '''INSERT INTO recapitulatifs (
                        immatriculation, types, description, certifications,
                        num_ref_ata, comp_description, date_proc_rev,
                        pot_restant, pot_restant_cycles
                   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (immat, types, description, certifications,
                 num_ref, comp_desc, date_proc, pot_rem, pot_rem_cycles)
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
        
        # no action button in summary view
        self.btn_action.hide()

    def on_cell_double_clicked(self, row, column):
        """Show a detail dialog when a cell is double-clicked."""
        immat = self.tableau_affichage.item(row,0).text() if self.tableau_affichage.item(row,0) else None
        if immat:
            self.show_details(row)

    def show_details(self, row):
        """Display a dialog with all available information for the given row and draw a graph if numeric data present."""
        immat = self.full_data.get(row)
        if not immat:
            return
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Détails - {immat}")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border: 2px solid #1976d2;
                border-radius: 8px;
            }
            QLabel {
                color: #333333;
                font-size: 13px;
                margin: 3px;
            }
        """)

        # create a scrollable area to handle large amounts of data
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(main_widget)

        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(scroll)
        dialog.setLayout(dialog_layout)

        # Titre principal
        title_label = QLabel(f"<h2 style='color: #1976d2; margin-bottom: 10px;'>Détails de l'aéronef: {immat}</h2>")
        title_label.setStyleSheet("border-bottom: 2px solid #1976d2; padding-bottom: 5px;")
        layout.addWidget(title_label)

        # show detailed information in a structured way
        detailed_data = self.build_detailed_data(immat)
        column_headers = ["Infos Avion", "Dernier Vol", "Moteurs", "Hélices", "Temps Vie", "Documents", "Comptes"]

        for i, header in enumerate(column_headers):
            # Section header
            section_label = QLabel(f"<b style='color: #1565c0; font-size: 14px;'>{header}:</b>")
            section_label.setStyleSheet("margin-top: 10px; margin-bottom: 2px;")
            layout.addWidget(section_label)

            # Content
            content_text = detailed_data[i] if detailed_data[i] else "Aucune donnée disponible"
            content_label = QLabel(content_text)
            content_label.setStyleSheet("""
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
            """)
            content_label.setWordWrap(True)
            content_label.setMinimumHeight(60)
            layout.addWidget(content_label)

        # retrieve any recapitulatifs records for this aircraft and show them
        try:
            self.cursor.execute(
                'SELECT types, certifications, num_ref_ata, comp_description, date_proc_rev, pot_restant, pot_restant_cycles '
                'FROM recapitulatifs WHERE immatriculation=?',
                (immat,)
            )
            rec_rows = self.cursor.fetchall()
            if rec_rows:
                recap_header = QLabel(f"<b style='color: #1565c0; font-size: 14px;'>Récapitulatif(s) enregistrés :</b>")
                recap_header.setStyleSheet("margin-top: 10px; margin-bottom: 2px;")
                layout.addWidget(recap_header)
                for rec in rec_rows:
                    rec_text = (
                        f"Type: {rec[0]}\n"
                        f"Certifications: {rec[1]}\n"
                        f"Num ref ATA: {rec[2]}\n"
                        f"Description: {rec[3]}\n"
                        f"Date Proc Rev: {rec[4]}\n"
                        f"Pot restant: {rec[5]} h\n"
                        f"Pot cycles: {rec[6]}"
                    )
                    rec_label = QLabel(rec_text)
                    rec_label.setStyleSheet("""
                        background-color: white;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                        padding: 8px;
                        color: #333333;
                        font-family: 'Segoe UI', Arial, sans-serif;
                    """)
                    rec_label.setWordWrap(True)
                    rec_label.setMinimumHeight(60)
                    layout.addWidget(rec_label)
        except Exception:
            pass

        # attempt graph with pot restant if available
        try:
            # attempt to fetch numeric values again
            self.cursor.execute('SELECT pot_restant, pot_restant_cycles FROM temps_vie WHERE immatriculation=? ORDER BY rowid DESC LIMIT 1', (immat,))
            rowval = self.cursor.fetchone()
            pr = float(rowval[0]) if rowval and rowval[0] else None
            prc = float(rowval[1]) if rowval and rowval[1] else None
        except Exception:
            pr = prc = None
        if pr is not None and prc is not None:
            try:
                from matplotlib.figure import Figure
                from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

                fig = Figure(figsize=(5,3), facecolor='white')
                ax = fig.add_subplot(111)
                bars = ax.bar(['Pot restant (h)', 'Pot cycles'], [pr, prc], color=['#2196f3', '#ff9800'], alpha=0.8)
                ax.set_ylabel('Valeur', fontsize=12, fontweight='bold')
                ax.set_title('Potentiel restant', fontsize=14, fontweight='bold', color='#1976d2')
                ax.grid(True, alpha=0.3)

                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + max(pr, prc)*0.02,
                           f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

                canvas = FigureCanvas(fig)
                canvas.setStyleSheet("border: 1px solid #ddd; border-radius: 4px;")
                layout.addWidget(canvas)
            except Exception as e:
                print(f"Erreur graphique: {e}")
                pass

        # Bouton fermer stylisé
        btn_close = QPushButton("Fermer")
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close, alignment=Qt.AlignmentFlag.AlignCenter)

        dialog.setLayout(layout)
        dialog.resize(600, 800)
        dialog.exec()
    
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
        # we have full_data stored earlier
        full = self.full_data.get(row, None)
        types = ""
        description = ""
        certifications = ""
        num_ref = ""
        comp_desc = ""
        date_proc = ""
        pot_rem = ""
        pot_rem_cycles = ""
        if full:
            # row format: (id, immat, types, description, cert, num_ref, comp_desc, date_proc, pot_rem, pot_rem_cycles)
            _, _, types, description, certifications, num_ref, comp_desc, date_proc, pot_rem, pot_rem_cycles = full
            # store id for update later
            self._editing_id = full[0]
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.types_.setCurrentText(types)
        # description générale corresponds to "description" variable
        self.comp_description_input.setText(description)
        self.certifications.setText(certifications)
        # nouveaux champs
        self.num_ref_ata_input.setText(num_ref or "")
        # comp_description_input is for component description
        self.comp_description_input.setText(comp_desc or "")
        self.date_proc_rev_input.setText(date_proc or "")
        self.pot_restant_input.setText(pot_rem or "")
        self.pot_restant_cycles_input.setText(pot_rem_cycles or "")
        
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
        num_ref = self.num_ref_ata_input.text().strip()
        comp_desc = self.comp_description_input.text().strip()
        date_proc = self.date_proc_rev_input.text().strip()
        pot_rem = self.pot_restant_input.text().strip()
        pot_rem_cycles = self.pot_restant_cycles_input.text().strip()

        try:
            # use the stored row id so we only update the selected record
            row_id = getattr(self, '_editing_id', None)
            if row_id is None:
                # fallback to immatriculation update (older behaviour)
                self.cursor.execute(
                    '''UPDATE recapitulatifs SET 
                            types=?, description=?, certifications=?,
                            num_ref_ata=?, comp_description=?, date_proc_rev=?,
                            pot_restant=?, pot_restant_cycles=?
                       WHERE immatriculation=?''',
                    (types, description, certifications,
                     num_ref, comp_desc, date_proc,
                     pot_rem, pot_rem_cycles, immat)
                )
            else:
                self.cursor.execute(
                    '''UPDATE recapitulatifs SET 
                            types=?, description=?, certifications=?,
                            num_ref_ata=?, comp_description=?, date_proc_rev=?,
                            pot_restant=?, pot_restant_cycles=?
                       WHERE id=?''',
                    (types, description, certifications,
                     num_ref, comp_desc, date_proc,
                     pot_rem, pot_rem_cycles, row_id)
                )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Erreur")
            msg.setText(f"Erreur lors de la mise à jour: {str(e)}")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        # Reinitialiser le formulaire
        self.reset_form()
        # clear editing id
        self._editing_id = None
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
        """Affiche le formulaire de création en réinitialisant les champs."""
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_recapitulatifs.show()
        self.btn_action.hide()

    def voir_listes_recaitulatifs(self):
        """Retourne à la vue tableau et recharge les données."""
        self.load_recapitulatifs()
        self.tableau_affichage.setVisible(True)
        self.frame_recapitulatifs.hide()
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
        