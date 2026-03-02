from PyQt6.QtWidgets import QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget,QDateEdit, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor
import sqlite3
import os

class Helices(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
      
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        if parent is None:
            self.setGeometry(100, 100, 900, 500)

        self.setStyleSheet("background-color: #2d2d69;border-radius:10px")
        
        
        self.titre = QLabel("Gestion helices", self)
        self.titre.setGeometry(20, 50, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(20,60,980,3)
        self.hr_1.setStyleSheet("background-color:white")
        
        # Faire une tableau
        # adjust columns to include separate hours and cycles for TSN and TSO
        # plus installation info, potentiel and remaining life
        self.tableau_affichage = QTableWidget(20,16,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Marque/modele (helices)",
            "Numero serie (helices)",
            "TSN heures",
            "TSN cycles",
            "TSO heures",
            "TSO cycles",
            "Date installation",
            "Heures installation",
            "Cycles installation",
            "Pot en mois",
            "Pot en heures",
            "Pot en cycles",
            "Date prochaines revisions",
            "Pot restant",
            "Pot restant cycles"
        ])
        self.tableau_affichage.setColumnWidth(0,150)
        self.tableau_affichage.setColumnWidth(1,200)
        self.tableau_affichage.setColumnWidth(2,200)
        # put reasonable width for numeric columns
        for i in range(3,16):
            self.tableau_affichage.setColumnWidth(i,100)
        self.tableau_affichage.setStyleSheet("background-color:white;color:black")
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.btn_ajout_helices = QPushButton("Nouveaux",self)
        self.btn_ajout_helices.setGeometry(10,10,190,40)
        self.btn_ajout_helices.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_ajout_helices.clicked.connect(self.ajouter_helices)
        
        
        self.btn_voir_listes = QPushButton("Voir Listes",self)
        self.btn_voir_listes.setGeometry(230,10,190,40)
        self.btn_voir_listes.setStyleSheet("background-color:blue;font-size:15px;color:white;font-weight:bold")
        self.btn_voir_listes.clicked.connect(self.voir_listes_helices)
        
        self.btn_action = QPushButton("Action",self)
        self.btn_action.setGeometry(450,10,190,40)
        self.btn_action.setStyleSheet("background-color:green;font-size:15px;color:white;font-weight:bold")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.hide()
        self.btn_action.clicked.connect(self.show_action_menu)
        
        
        
         # Frame Ajout
        self.frame_helices = QFrame(self)
        self.frame_helices.setGeometry(10,110,1000,485)
        self.frame_helices.setStyleSheet("background-color:white")
        
        # immatriculation
        self.immatriculation_label = QLabel("Immatriculation:", self.frame_helices)
        self.immatriculation_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.immatriculation_label.setGeometry(10, 20, 200, 30)
        
        self.immatriculation_input = QComboBox(self.frame_helices)
        self.immatriculation_input.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.immatriculation_input.setGeometry(250, 20, 200, 30)
        
        # marque et modele
        self.models_label = QLabel("Marque et modèle helices:", self.frame_helices)
        self.models_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.models_label.setGeometry(10, 70, 250, 30)
        self.models = QLineEdit(self.frame_helices)
        self.models.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.models.setGeometry(250, 70, 200, 30)
      

        # numero de serie
        self.numero_serie_label = QLabel("Numero de serie helices:", self.frame_helices)
        self.numero_serie_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.numero_serie_label.setGeometry(10, 120, 250, 30)
        self.numero_serie = QLineEdit(self.frame_helices)
        self.numero_serie.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.numero_serie.setGeometry(250, 120, 200, 30)
      

        # TSN hours/cycles
        self.tsn_hours_label = QLabel("TSN heures:", self.frame_helices)
        self.tsn_hours_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.tsn_hours_label.setGeometry(10, 170, 250, 30)
        self.tsn_hours = QLineEdit(self.frame_helices)
        self.tsn_hours.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.tsn_hours.setGeometry(250, 170, 200, 30)
        self.tsn_cycles_label = QLabel("TSN cycles:", self.frame_helices)
        self.tsn_cycles_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.tsn_cycles_label.setGeometry(10, 220, 250, 30)
        self.tsn_cycles = QLineEdit(self.frame_helices)
        self.tsn_cycles.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.tsn_cycles.setGeometry(250, 220, 200, 30)
      
        # TSO hours/cycles
        self.tso_hours_label = QLabel("TSO heures:", self.frame_helices)
        self.tso_hours_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.tso_hours_label.setGeometry(10, 270, 250, 30)
        self.tso_hours = QLineEdit(self.frame_helices)
        
        self.tso_hours.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.tso_hours.setGeometry(250, 270, 200, 30)
        self.tso_cycles_label = QLabel("TSO cycles:", self.frame_helices)
        self.tso_cycles_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.tso_cycles_label.setGeometry(10, 320, 250, 30)
        self.tso_cycles = QLineEdit(self.frame_helices)
        self.tso_cycles.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.tso_cycles.setGeometry(250, 320, 200, 30)
       
        self.date_install_label = QLabel("Date installation:", self.frame_helices)
        self.date_install_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.date_install_label.setGeometry(10, 370, 250, 30)
        
        self.date_installation = QDateEdit(self.frame_helices)
        self.date_installation.setDate(QDate.currentDate())
        self.date_installation.setCalendarPopup(True)
        self.date_installation.setDisplayFormat("yyyy-MM-dd")
        self.date_installation.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.date_installation.setGeometry(250, 370, 200, 30)
        
        self.install_hours_label = QLabel("Heures installation:", self.frame_helices)
        self.install_hours_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.install_hours_label.setGeometry(10, 410, 250, 30)
        
        self.install_hours = QLineEdit(self.frame_helices)
        self.install_hours.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.install_hours.setGeometry(250, 410, 200, 30)
        self.install_cycles_label = QLabel("Cycles installation:", self.frame_helices)
        self.install_cycles_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.install_cycles_label.setGeometry(10, 450, 250, 30)
        self.install_cycles = QLineEdit(self.frame_helices)
        self.install_cycles.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.install_cycles.setGeometry(250, 450, 200, 30)
       
        # section potentiel title
        self.pot_section = QLabel("Potentiel :", self.frame_helices)
        self.pot_section.setStyleSheet("color: black; font-size: 18px; font-weight:bold; background-color:none;border-bottom:2px solid black;")    
        self.pot_section.setGeometry(500, 20, 200, 30)
    

        self.pot_months_label = QLabel("Pot en mois:", self.frame_helices)
        self.pot_months_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.pot_months_label.setGeometry(500, 70, 200, 30)
        
        self.pot_months = QLineEdit(self.frame_helices)
        self.pot_months.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.pot_months.setGeometry(700, 70, 200, 30)
        
        self.pot_hours_label = QLabel("Pot en heures:", self.frame_helices)
        self.pot_hours_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.pot_hours_label.setGeometry(500, 120, 200, 30)
        
        self.pot_hours = QLineEdit(self.frame_helices)
        self.pot_hours.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.pot_hours.setGeometry(700, 120, 200, 30)
        
        self.pot_cycles_label = QLabel("Pot en cycles:", self.frame_helices)
        self.pot_cycles_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.pot_cycles_label.setGeometry(500, 170, 200, 30)
        
        self.pot_cycles = QLineEdit(self.frame_helices)
        self.pot_cycles.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.pot_cycles.setGeometry(700, 170, 200, 30)
      

        # section prochaine revision title
        self.rev_section = QLabel("Prochaine révision :", self.frame_helices)
        self.rev_section.setStyleSheet("color: black; font-size: 18px; font-weight:bold; background-color:none;border-bottom:2px solid black;")
        self.rev_section.setGeometry(500, 220, 250, 30)

        self.dates_revision_label = QLabel("Date prochaines \n revision:", self.frame_helices)
        self.dates_revision_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.dates_revision_label.setGeometry(500, 270, 250, 50)
        
        self.dates_revision = QDateEdit(self.frame_helices)
        self.dates_revision.setDate(QDate.currentDate())
        self.dates_revision.setCalendarPopup(True)
        self.dates_revision.setDisplayFormat("yyyy-MM-dd")
        self.dates_revision.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.dates_revision.setGeometry(700, 280, 200, 30)
        
        self.pot_restant_label = QLabel("Pot restant:", self.frame_helices)
        self.pot_restant_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.pot_restant_label.setGeometry(500, 330, 200, 30)
        
        self.pot_restant = QLineEdit(self.frame_helices)
        self.pot_restant.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.pot_restant.setGeometry(700, 330, 200, 30)
      
        self.pot_restant_cycles_label = QLabel("Pot restant cycles:", self.frame_helices)
        self.pot_restant_cycles_label.setStyleSheet("color: black; font-size: 16px; background-color:none; font-weight:bold")
        self.pot_restant_cycles_label.setGeometry(500, 370, 200, 30)
        
        self.pot_restant_cycles = QLineEdit(self.frame_helices)
        self.pot_restant_cycles.setStyleSheet("background-color: white; border:1px solid black; color:black; padding:5px; font-size:15px")
        self.pot_restant_cycles.setGeometry(700, 370, 200, 30)
     
        # save button
        self.enregistrer = QPushButton("Enregistrer",self.frame_helices)
        self.enregistrer.setStyleSheet("background-color:blue;color:white;font-size:15px;border-radius:10px")
        self.enregistrer.setCursor(Qt.CursorShape.PointingHandCursor)
        self.enregistrer.clicked.connect(self.save_helice)
        
        self.enregistrer.setGeometry(700, 420, 200, 40)
        
        # Connect signals for automatic calculations (date revision and pot restant)
        self.date_installation.dateChanged.connect(self.compute_date_revision)
        self.pot_months.textChanged.connect(self.compute_date_revision)
        self.immatriculation_input.currentIndexChanged.connect(lambda _: self.compute_pot_restants())
        self.pot_hours.textChanged.connect(self.compute_pot_restants)
        self.install_hours.textChanged.connect(self.compute_pot_restants)
        self.pot_cycles.textChanged.connect(self.compute_pot_restants_cycles)
        self.install_cycles.textChanged.connect(self.compute_pot_restants_cycles)

        self.frame_helices.hide()
        # calc details label
        self.calc_details = QLabel("", self.frame_helices)
        self.calc_details.setGeometry(500, 410, 400, 60)
        self.calc_details.setStyleSheet("color: black; font-size:12px; background-color: none;")
        self.calc_details.setWordWrap(True)
        self.compute_all()
        
        # Initialise la base SQLite
        try:
            self.db_path = os.path.join(os.path.dirname(__file__), 'aviation.db')
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS helices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    immatriculation TEXT NOT NULL,
                    marque TEXT,
                    numero_serie TEXT,
                    tsn_hours TEXT,
                    tsn_cycles INTEGER,
                    tso_hours TEXT,
                    tso_cycles INTEGER,
                    date_installation TEXT,
                    install_hours TEXT,
                    install_cycles INTEGER,
                    pot_months INTEGER,
                    pot_hours TEXT,
                    pot_cycles INTEGER,
                    date_revision TEXT,
                    pot_restant TEXT,
                    pot_restant_cycles INTEGER,
                    FOREIGN KEY (immatriculation) REFERENCES aircrafts(immatriculation)
                )
            ''')
            self.conn.commit()
            # add missing columns if upgrading existing database
            self.cursor.execute("PRAGMA table_info(helices)")
            existing = [c[1] for c in self.cursor.fetchall()]
            if 'tsn_hours' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN tsn_hours TEXT')
            if 'tsn_cycles' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN tsn_cycles INTEGER')
            if 'tso_hours' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN tso_hours TEXT')
            if 'tso_cycles' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN tso_cycles INTEGER')
            if 'date_installation' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN date_installation TEXT')
            if 'install_hours' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN install_hours TEXT')
            if 'install_cycles' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN install_cycles INTEGER')
            if 'pot_months' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN pot_months INTEGER')
            if 'pot_hours' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN pot_hours TEXT')
            if 'pot_cycles' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN pot_cycles INTEGER')
            if 'pot_restant' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN pot_restant TEXT')
            if 'pot_restant_cycles' not in existing:
                self.cursor.execute('ALTER TABLE helices ADD COLUMN pot_restant_cycles INTEGER')

            self.conn.commit()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et les helices
        self.load_immatriculations()
        self.load_helices()
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
    
    def load_helices(self):
        """Charge les helices depuis la base de donnees"""
        try:
            self.cursor.execute('''SELECT id, immatriculation, marque, numero_serie, tsn_hours, tsn_cycles, tso_hours, tso_cycles,
                                          date_installation, install_hours, install_cycles,
                                          pot_months, pot_hours, pot_cycles,
                                          date_revision, pot_restant, pot_restant_cycles
                                   FROM helices ORDER BY immatriculation DESC''')
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
            return float(s)
        except Exception:
            return 0.0

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
            total_hours += self._parse_hours_str_to_float(temps)
            try:
                total_cycles += int(cycles) if cycles is not None and str(cycles).strip() != '' else 0
            except Exception:
                pass

        return total_hours, total_cycles

    def compute_date_revision(self):
        """Calcule `dates_revision` = `date_installation` + `pot_months` mois."""
        try:
            months_text = self.pot_months.text().strip()
            months = int(months_text) if months_text else 0
        except Exception:
            months = 0
        try:
            base_date = self.date_installation.date()
            if months > 0:
                new_date = base_date.addMonths(months)
            else:
                new_date = base_date
            self.dates_revision.setDate(new_date)
        except Exception:
            pass

    def compute_pot_restants(self):
        """Calcule pot_restant = pot_hours - (install_hours + total_hours_from_heures_vol) et met à jour le champ."""
        try:
            immat = self.immatriculation_input.currentText().strip()
            pot_hours_val = self._parse_hours_str_to_float(self.pot_hours.text().strip())
            install_hours_val = self._parse_hours_str_to_float(self.install_hours.text().strip())

            total_hours_db, _ = (0.0, 0)
            if immat:
                total_hours_db, _ = self._get_heures_cycles_from_heures_vol(immat)

            remaining = pot_hours_val - (install_hours_val + total_hours_db)
            if abs(remaining - round(remaining)) < 1e-6:
                text = str(int(round(remaining)))
            else:
                text = f"{remaining:.1f}"
            self.pot_restant.setText(text)
        except Exception:
            pass

    def compute_pot_restants_cycles(self):
        """Calcule pot_restant_cycles = pot_cycles - (install_cycles + total_cycles_from_heures_vol)"""
        try:
            immat = self.immatriculation_input.currentText().strip()
            try:
                pot_cycles_val = int(self.pot_cycles.text().strip()) if self.pot_cycles.text().strip() else 0
            except Exception:
                pot_cycles_val = 0
            try:
                install_cycles_val = int(self.install_cycles.text().strip()) if self.install_cycles.text().strip() else 0
            except Exception:
                install_cycles_val = 0

            total_hours_db, total_cycles_db = (0.0, 0)
            if immat:
                total_hours_db, total_cycles_db = self._get_heures_cycles_from_heures_vol(immat)

            remaining_cycles = pot_cycles_val - (install_cycles_val + total_cycles_db)
            self.pot_restant_cycles.setText(str(remaining_cycles))
        except Exception:
            pass

    def compute_all(self):
        # perform calculations
        self.compute_date_revision()
        self.compute_pot_restants()
        self.compute_pot_restants_cycles()

        # Build display summary
        try:
            base_date = self.date_installation.date()
            months_text = self.pot_months.text().strip()
            months = int(months_text) if months_text else 0
            new_date = base_date.addMonths(months) if months > 0 else base_date
            days = base_date.daysTo(new_date)
            # date_line = f"Révision: {base_date.toString('yyyy-MM-dd')} + {months} mois = {new_date.toString('yyyy-MM-dd')} ({days} jours)"

            immat = self.immatriculation_input.currentText().strip()
            pot_h = self._parse_hours_str_to_float(self.pot_hours.text().strip())
            inst_h = self._parse_hours_str_to_float(self.install_hours.text().strip())
            total_h, _ = (0.0, 0)
            if immat:
                total_h, _ = self._get_heures_cycles_from_heures_vol(immat)
            remaining_h = pot_h - (inst_h + total_h)
            hours_line = f"Heures: {pot_h} - ({inst_h} + {total_h:.1f}) = {remaining_h:.1f}" if abs(remaining_h - round(remaining_h)) >= 1e-6 else str(int(round(remaining_h)))

            try:
                pot_c = int(self.pot_cycles.text().strip()) if self.pot_cycles.text().strip() else 0
            except Exception:
                pot_c = 0
            try:
                inst_c = int(self.install_cycles.text().strip()) if self.install_cycles.text().strip() else 0
            except Exception:
                inst_c = 0
            _, total_c = (0.0, 0)
            if immat:
                _, total_c = self._get_heures_cycles_from_heures_vol(immat)
            remaining_c = pot_c - (inst_c + total_c)
            cycles_line = f"Cycles: {pot_c} - ({inst_c} + {total_c}) = {remaining_c}" if remaining_c >= 0 else str(remaining_c)

            # if hasattr(self, 'calc_details'):
            #     self.calc_details.setText(date_line + "\n" + hours_line + "\n" + cycles_line)
        except Exception:
            pass
    
    def save_helice(self):
        """Sauvegarde les donnees de la helice dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        marque = self.models.text().strip()
        numero_serie = self.numero_serie.text().strip()
        tsn_hours = self.tsn_hours.text().strip()
        tsn_cycles_text = self.tsn_cycles.text().strip()
        try:
            tsn_cycles = int(tsn_cycles_text) if tsn_cycles_text else None
        except ValueError:
            tsn_cycles = None
        tso_hours = self.tso_hours.text().strip()
        tso_cycles_text = self.tso_cycles.text().strip()
        try:
            tso_cycles = int(tso_cycles_text) if tso_cycles_text else None
        except ValueError:
            tso_cycles = None
        # installation
        date_inst = self.date_installation.date().toString("yyyy-MM-dd")
        inst_hours = self.install_hours.text().strip()
        inst_cycles_text = self.install_cycles.text().strip()
        try:
            inst_cycles = int(inst_cycles_text) if inst_cycles_text else None
        except ValueError:
            inst_cycles = None
        # potentiel
        pot_months_text = self.pot_months.text().strip()
        try:
            pot_months = int(pot_months_text) if pot_months_text else None
        except ValueError:
            pot_months = None
        pot_hours = self.pot_hours.text().strip()
        pot_cycles_text = self.pot_cycles.text().strip()
        try:
            pot_cycles = int(pot_cycles_text) if pot_cycles_text else None
        except ValueError:
            pot_cycles = None
        # prochaines revision
        date_rev = self.dates_revision.date().toString("yyyy-MM-dd")
        pot_restant = self.pot_restant.text().strip()
        pot_restant_cycles_text = self.pot_restant_cycles.text().strip()
        try:
            pot_restant_cycles = int(pot_restant_cycles_text) if pot_restant_cycles_text else None
        except ValueError:
            pot_restant_cycles = None
        
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
                'INSERT INTO helices (immatriculation, marque, numero_serie, tsn_hours, tsn_cycles, tso_hours, tso_cycles, '
                'date_installation, install_hours, install_cycles, pot_months, pot_hours, pot_cycles, '
                'date_revision, pot_restant, pot_restant_cycles) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (immat, marque, numero_serie, tsn_hours, tsn_cycles, tso_hours, tso_cycles,
                 date_inst, inst_hours, inst_cycles, pot_months, pot_hours, pot_cycles,
                 date_rev, pot_restant, pot_restant_cycles)
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
        self.models.clear()
        self.numero_serie.clear()
        self.tsn_hours.clear()
        self.tsn_cycles.clear()
        self.tso_hours.clear()
        self.tso_cycles.clear()
        self.date_installation.setDate(QDate.currentDate())
        self.install_hours.clear()
        self.install_cycles.clear()
        self.pot_months.clear()
        self.pot_hours.clear()
        self.pot_cycles.clear()
        self.dates_revision.setDate(QDate.currentDate())
        self.pot_restant.clear()
        self.pot_restant_cycles.clear()
        
        # Recharger le tableau
        self.load_helices()
        
        # Afficher le tableau
        self.tableau_affichage.setVisible(True)
        self.frame_helices.hide()
    
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
                self.modifier_helice(row, immat)
            elif action == action_supprimer:
                self.supprimer_helice(row, immat)
        elif len(selected_rows) > 1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Attention")
            msg.setText("Veuillez selectionner une seule ligne pour modifier ou supprimer.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
    
    def modifier_helice(self, row, immat):
        # Recuperer les donnees de la ligne avec verification
        marque = self.tableau_affichage.item(row, 1).text() if self.tableau_affichage.item(row, 1) else ""
        numero_serie = self.tableau_affichage.item(row, 2).text() if self.tableau_affichage.item(row, 2) else ""
        tsn_hours = self.tableau_affichage.item(row, 3).text() if self.tableau_affichage.item(row, 3) else ""
        tsn_cycles = self.tableau_affichage.item(row, 4).text() if self.tableau_affichage.item(row, 4) else ""
        tso_hours = self.tableau_affichage.item(row, 5).text() if self.tableau_affichage.item(row, 5) else ""
        tso_cycles = self.tableau_affichage.item(row, 6).text() if self.tableau_affichage.item(row, 6) else ""
        date_install = self.tableau_affichage.item(row, 7).text() if self.tableau_affichage.item(row, 7) else ""
        install_hours = self.tableau_affichage.item(row, 8).text() if self.tableau_affichage.item(row, 8) else ""
        install_cycles = self.tableau_affichage.item(row, 9).text() if self.tableau_affichage.item(row, 9) else ""
        pot_months = self.tableau_affichage.item(row, 10).text() if self.tableau_affichage.item(row, 10) else ""
        pot_hours = self.tableau_affichage.item(row, 11).text() if self.tableau_affichage.item(row, 11) else ""
        pot_cycles = self.tableau_affichage.item(row, 12).text() if self.tableau_affichage.item(row, 12) else ""
        date_rev = self.tableau_affichage.item(row, 13).text() if self.tableau_affichage.item(row, 13) else ""
        pot_restant = self.tableau_affichage.item(row, 14).text() if self.tableau_affichage.item(row, 14) else ""
        pot_restant_cycles = self.tableau_affichage.item(row, 15).text() if self.tableau_affichage.item(row, 15) else ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.models.setText(marque)
        self.numero_serie.setText(numero_serie)
        self.tsn_hours.setText(tsn_hours)
        self.tsn_cycles.setText(tsn_cycles)
        self.tso_hours.setText(tso_hours)
        self.tso_cycles.setText(tso_cycles)
        self.date_installation.setDate(QDate.fromString(date_install, "yyyy-MM-dd"))
        self.install_hours.setText(install_hours)
        self.install_cycles.setText(install_cycles)
        self.pot_months.setText(pot_months)
        self.pot_hours.setText(pot_hours)
        self.pot_cycles.setText(pot_cycles)
        self.dates_revision.setDate(QDate.fromString(date_rev, "yyyy-MM-dd"))
        self.pot_restant.setText(pot_restant)
        self.pot_restant_cycles.setText(pot_restant_cycles)
        
        # Changer le titre et le comportement du formulaire
        self.enregistrer.setText("Mettre a jour")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(lambda: self.update_helice(immat, date_rev))
        # Recompute derived fields based on loaded values
        self.compute_all()

        self.tableau_affichage.setVisible(False)
        self.frame_helices.show()
    
    def update_helice(self, immat, date_rev_original):
        marque = self.models.text().strip()
        numero_serie = self.numero_serie.text().strip()
        tsn_hours = self.tsn_hours.text().strip()
        tsn_cycles_text = self.tsn_cycles.text().strip()
        try:
            tsn_cycles = int(tsn_cycles_text) if tsn_cycles_text else None
        except ValueError:
            tsn_cycles = None
        tso_hours = self.tso_hours.text().strip()
        tso_cycles_text = self.tso_cycles.text().strip()
        try:
            tso_cycles = int(tso_cycles_text) if tso_cycles_text else None
        except ValueError:
            tso_cycles = None
        # installation
        date_inst = self.date_installation.date().toString("yyyy-MM-dd")
        inst_hours = self.install_hours.text().strip()
        inst_cycles_text = self.install_cycles.text().strip()
        try:
            inst_cycles = int(inst_cycles_text) if inst_cycles_text else None
        except ValueError:
            inst_cycles = None
        # potentiel
        pot_months_text = self.pot_months.text().strip()
        try:
            pot_months = int(pot_months_text) if pot_months_text else None
        except ValueError:
            pot_months = None
        pot_hours = self.pot_hours.text().strip()
        pot_cycles_text = self.pot_cycles.text().strip()
        try:
            pot_cycles = int(pot_cycles_text) if pot_cycles_text else None
        except ValueError:
            pot_cycles = None
        # prochaines revision
        date_rev = self.dates_revision.date().toString("yyyy-MM-dd")
        pot_restant = self.pot_restant.text().strip()
        pot_restant_cycles_text = self.pot_restant_cycles.text().strip()
        try:
            pot_restant_cycles = int(pot_restant_cycles_text) if pot_restant_cycles_text else None
        except ValueError:
            pot_restant_cycles = None
        
        try:
            self.cursor.execute(
                'UPDATE helices SET marque=?, numero_serie=?, tsn_hours=?, tsn_cycles=?, tso_hours=?, tso_cycles=?, '
                'date_installation=?, install_hours=?, install_cycles=?, pot_months=?, pot_hours=?, pot_cycles=?, '
                'date_revision=?, pot_restant=?, pot_restant_cycles=? '
                'WHERE immatriculation=? AND date_revision=?',
                (marque, numero_serie, tsn_hours, tsn_cycles, tso_hours, tso_cycles,
                 date_inst, inst_hours, inst_cycles, pot_months, pot_hours, pot_cycles,
                 date_rev, pot_restant, pot_restant_cycles,
                 immat, date_rev_original)
            )
            self.conn.commit()
        except Exception as e:
            print('Erreur mise a jour DB:', e)
            return
        
        # Reinitialiser le formulaire
        self.reset_form()
        self.load_helices()
        self.tableau_affichage.setVisible(True)
        self.frame_helices.hide()
    
    def supprimer_helice(self, row, immat):
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
        btn_yes.clicked.connect(lambda: self.confirm_delete_helice(row_id, dialog))
        btn_no.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def confirm_delete_helice(self, row_id, dialog):
        """Confirme la suppression"""
        try:
            self.cursor.execute('DELETE FROM helices WHERE id=?', (row_id,))
            self.conn.commit()
        except Exception as e:
            print('Erreur suppression DB:', e)
            return
        
        self.load_helices()
        dialog.accept()
    
    def reset_form(self):
        self.models.clear()
        self.numero_serie.clear()
        self.tsn_hours.clear()
        self.tsn_cycles.clear()
        self.tso_hours.clear()
        self.tso_cycles.clear()
        self.date_installation.setDate(QDate.currentDate())
        self.install_hours.clear()
        self.install_cycles.clear()
        self.pot_months.clear()
        self.pot_hours.clear()
        self.pot_cycles.clear()
        self.dates_revision.setDate(QDate.currentDate())
        self.pot_restant.clear()
        self.pot_restant_cycles.clear()
        self.enregistrer.setText("Enregistrer")
        self.enregistrer.disconnect()
        self.enregistrer.clicked.connect(self.save_helice)
        
    def ajouter_helices(self):
        self.reset_form()
        self.tableau_affichage.setVisible(False)
        self.frame_helices.show()
        
    def voir_listes_helices(self):
        self.load_helices()
        self.tableau_affichage.setVisible(True)
        self.frame_helices.hide()
        self.btn_action.hide()