from PyQt6.QtWidgets import QCompleter, QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import QStringListModel, Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class Temps_vie(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Temps de vie des composants (TSN/TBO)", self)
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
        # adjust columns to match new data structure
        # columns: immat, total heures cellule, nbr tot cycles cellule,
        # num ref ATA, description, action, ref docs,
        # date installation, potentiel date, potentiel heures, potentiel cycles,
        # dates proc rev, pot restant, pot restant cycles,
        # nom equipements, date inst equipements, date calibration
        self.tableau_affichage = QTableWidget(20,18,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Total heures Cellule",
            "Nbr tot cycle Cellule",
            "Num ref ATA",
            "Description",
            "Action",
            "Ref Docs",
            "Date installation",
            "heure installation",
            "Nbr Cycles",
            "Pot en mois",
            "Potentiel heures",
            "Potentiel cycles",
            "Dates Prochains revisions",
            "Pot restant (heures)",
            "Pot restant cycles",
            "Nom equipements",
            "Date calibration"
        ])
        self.tableau_affichage.setColumnWidth(0,150)
        # keep some wide columns for text
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        self.tableau_affichage.setColumnWidth(3,150)
        self.tableau_affichage.setColumnWidth(4,200)
        # other numeric/text columns can be smaller
        for i in range(5,18):
            self.tableau_affichage.setColumnWidth(i,120)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_travaux = QPushButton("Nouveaux",self)
        self.btn_ajout_travaux.setGeometry(10,10,190,40)
        self.btn_ajout_travaux.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_travaux.clicked.connect(self.ajouter_temps)
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_temps)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        
        
         # Frame Ajout
        self.frame_temps = QFrame(self)
        self.frame_temps.setGeometry(10,110,1000,490)  # increased height for extra fields
        self.frame_temps.setStyleSheet("background-color:white")
        
        # immatriculation
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_temps)
        self.immatriculation_label.setGeometry(20, 20, 150, 30)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.immatriculation_input = QComboBox(self.frame_temps)
        self.immatriculation_input.setGeometry(250, 19, 250, 35)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.immatriculation_input.currentTextChanged.connect(self.update_totals_from_immat)
        
        # cellule totals
        self.heures_total_label = QLabel("Total heures Cellule:", self.frame_temps)
        self.heures_total_label.setGeometry(20, 60, 250, 30)
        self.heures_total_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.heures_total = QLineEdit(self.frame_temps)
        self.heures_total.setGeometry(250, 60, 250, 30)
        self.heures_total.setStyleSheet("background-color: white;border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.cycles_label = QLabel("Nbr tot cycle Cellule:", self.frame_temps)
        self.cycles_label.setGeometry(20, 100, 250, 30)
        self.cycles_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        
        self.cycles = QLineEdit(self.frame_temps)
        self.cycles.setGeometry(250, 100, 250, 30)
        self.cycles.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        # --- new left-side fields ---
        self.num_ref_ata_label = QLabel("Num ref ATA:", self.frame_temps)
        self.num_ref_ata_label.setGeometry(20, 140, 250, 30)
        self.num_ref_ata_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.num_ref_ata = QLineEdit(self.frame_temps)
        self.num_ref_ata.setGeometry(250, 140, 250, 30)
        self.num_ref_ata.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.description_label = QLabel("Description:", self.frame_temps)
        self.description_label.setGeometry(20, 180, 250, 30)
        self.description_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.description = QLineEdit(self.frame_temps)
        self.description.setGeometry(250, 180, 250, 30)
        self.description.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.action_label = QLabel("Action:", self.frame_temps)
        self.action_label.setGeometry(20, 220, 250, 30)
        self.action_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.action = QLineEdit(self.frame_temps)
        self.action.setGeometry(250, 220, 250, 30)
        self.action.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.ref_docs_label = QLabel("Ref Docs:", self.frame_temps)
        self.ref_docs_label.setGeometry(20, 260, 250, 30)
        self.ref_docs_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.ref_docs = QLineEdit(self.frame_temps)
        self.ref_docs.setGeometry(250, 260, 250, 30)
        self.ref_docs.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.date_install_label = QLabel("Date installation:", self.frame_temps)
        self.date_install_label.setGeometry(20, 300, 250, 30)
        self.date_install_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.date_installation = QDateEdit(self.frame_temps)
        self.date_installation.setGeometry(250, 300, 250, 30)
        self.date_installation.setDate(QDate.currentDate())
        self.date_installation.setCalendarPopup(True)
        self.date_installation.setDisplayFormat("yyyy-MM-dd")
        self.date_installation.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.heure_inst_label = QLabel("Heure installation:", self.frame_temps)
        self.heure_inst_label.setGeometry(20, 340, 250, 30)
        self.heure_inst_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.heure_inst = QLineEdit(self.frame_temps)
        self.heure_inst.setGeometry(250, 340, 250, 30)
        self.heure_inst.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        
        self.nombre_cycles = QLabel("Cycles :", self.frame_temps)
        self.nombre_cycles.setGeometry(20, 380, 250, 30)
        self.nombre_cycles.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.nombre_cycles_input = QLineEdit(self.frame_temps)
        self.nombre_cycles_input.setGeometry(250, 380, 250, 30)
        self.nombre_cycles_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.potentiel_heures_label = QLabel("Potentiel heures:", self.frame_temps)
        self.potentiel_heures_label.setGeometry(20, 420, 250, 30)
        self.potentiel_heures_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.potentiel_heures = QLineEdit(self.frame_temps)
        self.potentiel_heures.setGeometry(250, 420, 250, 30)
        self.potentiel_heures.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.potentiel_cycles_label = QLabel("Potentiel cycles:", self.frame_temps)
        self.potentiel_cycles_label.setGeometry(550, 20, 250, 30)
        self.potentiel_cycles_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.potentiel_cycles = QLineEdit(self.frame_temps)
        self.potentiel_cycles.setGeometry(750, 20, 200, 30)
        self.potentiel_cycles.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        # Pot en mois (utilisé pour calcul date prochaine revision)
        self.pot_months_label = QLabel("Pot en mois:", self.frame_temps)
        self.pot_months_label.setGeometry(550, 70, 250, 30)
        self.pot_months_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.pot_months = QLineEdit(self.frame_temps)
        self.pot_months.setGeometry(750, 70, 200, 30)
        self.pot_months.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")

        self.dates_proc_rev_label = QLabel("Dates Proc rev:", self.frame_temps)
        self.dates_proc_rev_label.setGeometry(550, 120, 250, 30)
        self.dates_proc_rev_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.dates_proc_rev = QDateEdit(self.frame_temps)
        self.dates_proc_rev.setGeometry(750, 120, 200, 30)
        self.dates_proc_rev.setDate(QDate.currentDate())
        self.dates_proc_rev.setCalendarPopup(True)
        self.dates_proc_rev.setDisplayFormat("yyyy-MM-dd")
        self.dates_proc_rev.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.pot_restant_label = QLabel("Pot restant (heures):", self.frame_temps)
        self.pot_restant_label.setGeometry(550, 170, 250, 30)
        self.pot_restant_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.pot_restant = QLineEdit(self.frame_temps)
        self.pot_restant.setGeometry(750, 170, 200, 30)
        self.pot_restant.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.pot_restant.setReadOnly(True)
        
        self.pot_restant_cycles_label = QLabel("Pot restant cycles:", self.frame_temps)
        self.pot_restant_cycles_label.setGeometry(550, 220, 250, 30)
        self.pot_restant_cycles_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.pot_restant_cycles = QLineEdit(self.frame_temps)
        self.pot_restant_cycles.setGeometry(750, 220, 200, 30)
        self.pot_restant_cycles.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.pot_restant_cycles.setReadOnly(True)
        
        # right side equipment fields similar to moteurs
        self.nom_equipements_label = QLabel("Nom equipements:", self.frame_temps)
        self.nom_equipements_label.setGeometry(550, 270, 250, 30)
        self.nom_equipements_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.nom_equipements = QLineEdit(self.frame_temps)
        self.nom_equipements.setGeometry(750, 270, 200, 30)
        self.nom_equipements.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        # self.nombre_cycles = QLabel("Cycles :", self.frame_temps)
        # self.nombre_cycles.setGeometry(550, 140, 250, 30)
        # self.nombre_cycles.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        # self.nombre_cycles_input = QLineEdit(self.frame_temps)
        # self.nombre_cycles_input.setGeometry(750, 140, 200, 30)
        # self.nombre_cycles_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.date_calibration_label = QLabel("Date de calibration:", self.frame_temps)
        self.date_calibration_label.setGeometry(550, 320, 250, 30)
        self.date_calibration_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")
        self.date_calibration = QDateEdit(self.frame_temps)
        self.date_calibration.setGeometry(750, 320, 200, 30)
        self.date_calibration.setDate(QDate.currentDate())
        self.date_calibration.setCalendarPopup(True)
        self.date_calibration.setDisplayFormat("yyyy-MM-dd")
        self.date_calibration.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        
        self.enregistrer = QPushButton("Enregistrer",self.frame_temps)
        self.enregistrer.setGeometry(750,400,150,40)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_temps)

        self.frame_temps.hide()
        
        # Connect signals for automatic calculations
        self.date_installation.dateChanged.connect(self.compute_date_revision)
        self.pot_months.textChanged.connect(self.compute_date_revision)
        self.heure_inst.textChanged.connect(self.compute_pot_restants)
        self.potentiel_heures.textChanged.connect(self.compute_pot_restants)
        self.nombre_cycles_input.textChanged.connect(self.compute_pot_restants_cycles)
        self.potentiel_cycles.textChanged.connect(self.compute_pot_restants_cycles)
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS temps_vie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    total_heures_cellule TEXT,
                    nbr_tot_cycles_cellule TEXT,
                    num_ref_ata TEXT,
                    description TEXT,
                    action TEXT,
                    ref_docs TEXT,
                    date_installation TEXT,
                    heure_inst TEXT,
                    pot_months TEXT,
                    potentiel_heures TEXT,
                    potentiel_cycles TEXT,
                    dates_proc_rev TEXT,
                    pot_restant TEXT,
                    pot_restant_cycles TEXT,
                    nom_equipements TEXT,
                    nombre_cycles_input TEXT,
                    date_calibration TEXT,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation) ON DELETE CASCADE
                )
            ''' )
            self.conn.commit()
            # Vérifier et ajouter les colonnes manquantes
            self._add_missing_columns()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les temps_vie
        self.load_immatriculations()
        self.load_temps()
        self.selected_rows = []
    
    def _parse_hours_str_to_float(self, s):
        """Parse un champ heures qui peut être 'hh:mm' ou un nombre décimal/entier.
        Retourne les heures en float."""
        try:
            if not s:
                return 0.0
            s = str(s).strip()
            if ':' in s:
                parts = s.split(':')
                h = float(parts[0])
                m = float(parts[1]) if len(parts) > 1 else 0.0
                return h + m / 60.0
            # otherwise try to parse float
            return float(s)
        except Exception:
            return 0.0
    
    def _format_hours_to_str(self, hours_float: float) -> str:
        """Retourne une chaîne "hh:mm" à partir d'un nombre d'heures en float.
        Arrondit les minutes au plus proche entier.
        """
        try:
            h = int(hours_float)
            m = int(round((hours_float - h) * 60))
            if m == 60:
                h += 1
                m = 0
            return f"{h}:{m:02d}"
        except Exception:
            return "0:00"
    
    def _get_heures_cycles_from_heures_vol(self, immat):
        """Récupère la somme des heures (en heures float) et des cycles pour une immatriculation depuis heures_vol."""
        try:
            self.cursor.execute('SELECT temps_vol, cycles FROM heures_vol WHERE immatriculation=?', (immat,))
            rows = self.cursor.fetchall()
        except Exception:
            return 0.0, 0

        total_hours = 0.0
        total_cycles = 0
        for temps, cycles in rows:
            # temps peut être 'hh:mm' ou une valeur numérique
            total_hours += self._parse_hours_str_to_float(temps)
            try:
                total_cycles += int(cycles) if cycles is not None and str(cycles).strip() != '' else 0
            except Exception:
                pass

        return total_hours, total_cycles
    
    def update_totals_from_immat(self, immat):
        """Met à jour les champs total heures et cycles en fonction de l'immatriculation sélectionnée.
        Calcule : base = heures_total/cycles_total dans la table aircrafts
        + totaux provenant de heures_vol pour la même immatriculation.
        """
        if not immat:
            self.heures_total.setText("")
            self.cycles.setText("")
            return
        
        # récupérer heures/cycles de la fiche aéronef
        try:
            self.cursor.execute(
                "SELECT heures_total, cycles_total FROM aircrafts WHERE immatriculation=?",
                (immat,)
            )
            row = self.cursor.fetchone()
        except Exception:
            row = None

        base_hours = 0.0
        base_cycles = 0
        if row:
            if row[0]:
                base_hours = self._parse_hours_str_to_float(row[0])
            try:
                base_cycles = int(row[1]) if row[1] is not None and str(row[1]).strip() != "" else 0
            except Exception:
                base_cycles = 0

        # totaux depuis heures_vol
        total_hv, total_cy = self._get_heures_cycles_from_heures_vol(immat)

        total_h = base_hours + total_hv
        total_c = base_cycles + total_cy

        # mettre à jour les champs
        try:
            self.heures_total.setText(self._format_hours_to_str(total_h))
        except Exception:
            self.heures_total.setText("")
        try:
            self.cycles.setText(str(total_c))
        except Exception:
            self.cycles.setText("")
    
    def _add_missing_columns(self):
        """Ajoute les colonnes manquantes à la table temps_vie si elles n'existent pas"""
        required_columns = [
            'total_heures_cellule',
            'nbr_tot_cycles_cellule',
            'num_ref_ata',
            'description',
            'action',
            'ref_docs',
            'date_installation',
            'heure_inst',
            'pot_months',
            'potentiel_heures',
            'potentiel_cycles',
            'dates_proc_rev',
            'pot_restant',
            'pot_restant_cycles',
            'nom_equipements',
            'nombre_cycles_input',
            'date_calibration'
        ]
        
        try:
            # Récupérer les colonnes existantes
            self.cursor.execute("PRAGMA table_info(temps_vie)")
            existing_columns = {row[1] for row in self.cursor.fetchall()}
            
            # Ajouter les colonnes manquantes
            for column in required_columns:
                if column not in existing_columns:
                    self.cursor.execute(f"ALTER TABLE temps_vie ADD COLUMN {column} TEXT")
                    print(f"Colonne {column} ajoutée à temps_vie")
            
            self.conn.commit()
        except Exception as e:
            print(f'Erreur ajout colonnes manquantes: {e}')
    
    def load_immatriculations(self):
        """Charge tous les matricules depuis la table aircrafts"""
        try:
            self.cursor.execute('SELECT immatriculation FROM aircrafts ORDER BY immatriculation')
            immatriculations = self.cursor.fetchall()
            self.immatriculation_input.clear()
            for immat in immatriculations:
                self.immatriculation_input.addItem(immat[0])
            if hasattr(self, 'filter_completer'):
                self.filter_completer.setModel(QStringListModel([immat[0] for immat in immatriculations]))
            if hasattr(self, 'filter_input'):
                self.filter_input.setText("")
        except Exception as e:
            print('Erreur chargement immatriculations:', e)
    
    def load_temps(self):
        """Charge les temps_vie depuis la base de donnees"""
        try:
            self.cursor.execute(
                'SELECT id, immatriculation, total_heures_cellule, nbr_tot_cycles_cellule, '
                'num_ref_ata, description, action, ref_docs, date_installation, heure_inst, nombre_cycles_input, pot_months, '
                'potentiel_heures, potentiel_cycles, dates_proc_rev, pot_restant, pot_restant_cycles, '
                'nom_equipements, date_calibration '
                'FROM temps_vie ORDER BY immatriculation DESC'
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
    
    def compute_date_revision(self):
        """Calcule automatiquement la date de prochaine révision : date_installation + pot_months"""
        try:
            date_install = self.date_installation.date()
            pot_months_text = self.pot_months.text().strip()
            pot_months = int(pot_months_text) if pot_months_text else 0
            new_date = date_install.addMonths(pot_months)
            self.dates_proc_rev.setDate(new_date)
        except Exception as e:
            print('Erreur calcul date revision:', e)
    
    def compute_pot_restants(self):
        """Calcule automatiquement le potentiel restant heures : heure_inst + potentiel_heures"""
        try:
            inst_h = self._parse_hours_str_to_float(self.heure_inst.text().strip())
            pot_h = self._parse_hours_str_to_float(self.potentiel_heures.text().strip())
            restant_h = inst_h + pot_h
            self.pot_restant.setText(self._format_hours_to_str(restant_h))
        except Exception as e:
            self.pot_restant.setText("")
    
    def compute_pot_restants_cycles(self):
        """Calcule automatiquement le potentiel restant cycles : nombre_cycles_input + potentiel_cycles"""
        try:
            inst_c = int(self.nombre_cycles_input.text().strip()) if self.nombre_cycles_input.text().strip() else 0
            pot_c = int(self.potentiel_cycles.text().strip()) if self.potentiel_cycles.text().strip() else 0
            restant_c = inst_c + pot_c
            self.pot_restant_cycles.setText(str(restant_c))
        except Exception as e:
            self.pot_restant_cycles.setText("")
    
    def save_temps(self):
        """Sauvegarde les donnees du temps_vie dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        total_heures = self.heures_total.text().strip()
        nbr_cycles = self.cycles.text().strip()
        num_ref = self.num_ref_ata.text().strip()
        description = self.description.text().strip()
        action = self.action.text().strip()
        ref_docs = self.ref_docs.text().strip()
        date_install = self.date_installation.date().toString("yyyy-MM-dd")
        heure_inst = self.heure_inst.text().strip()
        pot_months = self.pot_months.text().strip()
        potentiel_heures = self.potentiel_heures.text().strip()
        potentiel_cycles = self.potentiel_cycles.text().strip()
        dates_proc_rev = self.dates_proc_rev.date().toString("yyyy-MM-dd")
        pot_restant = self.pot_restant.text().strip()
        pot_restant_cycles = self.pot_restant_cycles.text().strip()
        nom_equipements = self.nom_equipements.text().strip()
        nombre_cycles_input = self.nombre_cycles_input.text().strip()
        date_calib = self.date_calibration.date().toString("yyyy-MM-dd")
        
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
                'INSERT INTO temps_vie (immatriculation, total_heures_cellule, nbr_tot_cycles_cellule, num_ref_ata, description, action, ref_docs, date_installation, heure_inst, pot_months, potentiel_heures, potentiel_cycles, dates_proc_rev, pot_restant, pot_restant_cycles, nom_equipements, nombre_cycles_input, date_calibration) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ',
                (immat, total_heures, nbr_cycles, num_ref, description, action, ref_docs, date_install, heure_inst, pot_months, potentiel_heures, potentiel_cycles, dates_proc_rev, pot_restant, pot_restant_cycles, nom_equipements, nombre_cycles_input, date_calib)
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
        self.heures_total.clear()
        self.cycles.clear()
        self.num_ref_ata.clear()
        self.description.clear()
        self.action.clear()
        self.ref_docs.clear()
        self.date_installation.setDate(QDate.currentDate())
        self.heure_inst.clear()
        self.potentiel_heures.clear()
        self.potentiel_cycles.clear()
        self.pot_months.clear()
        self.dates_proc_rev.setDate(QDate.currentDate())
        self.pot_restant.clear()
        self.pot_restant_cycles.clear()
        self.nom_equipements.clear()
        self.nombre_cycles_input.clear()
        self.date_calibration.setDate(QDate.currentDate())
        
        # Recharger le tableau
        self.load_temps()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_temps.hide()
    
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
                self.modifier_temps(row, immat)
            elif action == action_supprimer:
                self.supprimer_temps(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_temps(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        total_heures = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        nbr_cycles = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        num_ref = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        description = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        action = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        ref_docs = self.tableau_affichage.item(row, 6).text() if self.tableau_affichage.item(row, 6) else ""
        date_install = self.tableau_affichage.item(row, 7).text() if self.tableau_affichage.item(row, 7) else ""
        heure_inst = self.tableau_affichage.item(row, 8).text() if self.tableau_affichage.item(row, 8) else ""
        pot_months = self.tableau_affichage.item(row, 9).text() if self.tableau_affichage.item(row, 9) else ""
        potentiel_heures = self.tableau_affichage.item(row, 10).text() if self.tableau_affichage.item(row, 10) else ""
        potentiel_cycles = self.tableau_affichage.item(row, 11).text() if self.tableau_affichage.item(row, 11) else ""
        dates_proc_rev = self.tableau_affichage.item(row, 12).text() if self.tableau_affichage.item(row, 12) else ""
        pot_restant = self.tableau_affichage.item(row, 13).text() if self.tableau_affichage.item(row, 13) else ""
        pot_restant_cycles = self.tableau_affichage.item(row, 14).text() if self.tableau_affichage.item(row, 14) else ""
        nom_equipements = self.tableau_affichage.item(row, 15).text() if self.tableau_affichage.item(row, 15) else ""
        nombre_cycles_input = self.tableau_affichage.item(row, 16).text() if self.tableau_affichage.item(row, 16) else ""
        date_calib = self.tableau_affichage.item(row, 17).text() if self.tableau_affichage.item(row, 17) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.heures_total.setText(total_heures)
        self.cycles.setText(nbr_cycles)
        self.num_ref_ata.setText(num_ref)
        self.description.setText(description)
        self.action.setText(action)
        self.ref_docs.setText(ref_docs)
        self.date_installation.setDate(QDate.fromString(date_install, "yyyy-MM-dd"))
        self.heure_inst.setText(heure_inst)
        self.pot_months.setText(pot_months)
        self.potentiel_heures.setText(potentiel_heures)
        self.potentiel_cycles.setText(potentiel_cycles)
        self.dates_proc_rev.setDate(QDate.fromString(dates_proc_rev, "yyyy-MM-dd"))
        self.pot_restant.setText(pot_restant)
        self.pot_restant_cycles.setText(pot_restant_cycles)
        self.nom_equipements.setText(nom_equipements)
        self.nombre_cycles_input.setText(nombre_cycles_input)
        self.date_calibration.setDate(QDate.fromString(date_calib, "yyyy-MM-dd"))
        
        # Get the ID for unique update
        row_id = self.tableau_affichage.item(row, 0).data(Qt.ItemDataRole.UserRole)
        
        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_temps(row_id))
        
        self.tableau_affichage.setVisible(False)
        self.frame_temps.show()
    
    def update_temps(self, row_id):
        total_heures = self.heures_total.text().strip()
        nbr_cycles = self.cycles.text().strip()
        num_ref = self.num_ref_ata.text().strip()
        description = self.description.text().strip()
        action = self.action.text().strip()
        ref_docs = self.ref_docs.text().strip()
        date_install = self.date_installation.date().toString("yyyy-MM-dd")
        heure_inst = self.heure_inst.text().strip()
        pot_months = self.pot_months.text().strip()
        potentiel_heures = self.potentiel_heures.text().strip()
        potentiel_cycles = self.potentiel_cycles.text().strip()
        dates_proc_rev = self.dates_proc_rev.date().toString("yyyy-MM-dd")
        pot_restant = self.pot_restant.text().strip()
        pot_restant_cycles = self.pot_restant_cycles.text().strip()
        nom_equipements = self.nom_equipements.text().strip()
        nombre_cycles_input = self.nombre_cycles_input.text().strip()
        dates_calib = self.date_calibration.date().toString("yyyy-MM-dd")
        
        try:
            self.cursor.execute(
                'UPDATE temps_vie SET total_heures_cellule=?, nbr_tot_cycles_cellule=?, num_ref_ata=?, description=?, action=?, ref_docs=?, date_installation=?, heure_inst=?, pot_months=?, potentiel_heures=?, potentiel_cycles=?, dates_proc_rev=?, pot_restant=?, pot_restant_cycles=?, nom_equipements=?, nombre_cycles_input=?, date_calibration=? WHERE id=?',
                (total_heures, nbr_cycles, num_ref, description, action, ref_docs, date_install, heure_inst, pot_months, potentiel_heures, potentiel_cycles, dates_proc_rev, pot_restant, pot_restant_cycles, nom_equipements, nombre_cycles_input, dates_calib, row_id)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return
        
        # Reinitialiser le formulaire
        self.reset_form()
        self.load_temps()
        self.tableau_affichage.setVisible(True)
        self.frame_temps.hide()
    
    def supprimer_temps(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_temps(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_temps(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM temps_vie WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_temps()
        dialog.accept()
    
    def reset_form(self):
        self.heures_total.clear()
        self.cycles.clear()
        self.num_ref_ata.clear()
        self.description.clear()
        self.action.clear()
        self.ref_docs.clear()
        self.date_installation.setDate(QDate.currentDate())
        self.heure_inst.clear()
        self.potentiel_heures.clear()
        self.potentiel_cycles.clear()
        self.dates_proc_rev.setDate(QDate.currentDate())
        self.pot_restant.clear()
        self.pot_restant_cycles.clear()
        self.nom_equipements.clear()
        self.nombre_cycles_input.clear()
        self.date_calibration.setDate(QDate.currentDate())
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_temps)
        
    def ajouter_temps(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_temps.show()
        # Automatically select the first immatriculation to display totals
        if self.immatriculation_input.count() > 0:
            self.immatriculation_input.setCurrentIndex(0)
            self.update_totals_from_immat(self.immatriculation_input.currentText())
        
    def voir_listes_temps(self):
        self.load_temps()
        self.tableau_affichage.setVisible(True)
        self.frame_temps.hide()
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
        