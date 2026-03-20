from PyQt6.QtWidgets import QCompleter, QLineEdit, QWidget, QLabel, QPushButton,QFrame,QTableWidget, QTableWidgetItem, QComboBox, QMessageBox, QAbstractItemView, QMenu, QDialog, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtGui import QColor
import sqlite3
import os
import re

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
        self.tableau_affichage = QTableWidget(20,10,self)
        self.tableau_affichage.setGeometry(10,110,1000,400)
        self.tableau_affichage.setHorizontalHeaderLabels([
            "Immatriculation",
            "Ref ATA Moteurs",
            "Ref ATA Hélices",
            "Infos Avion",
            "Dernier Vol",
            "Moteurs",
            "Hélices",
            "Temps Vie",
            "Documents",
            "Comptes"
        ])
        self.tableau_affichage.setColumnWidth(0,120)
        self.tableau_affichage.setColumnWidth(1,130)
        self.tableau_affichage.setColumnWidth(2,130)
        self.tableau_affichage.setColumnWidth(3,150)
        self.tableau_affichage.setColumnWidth(4,120)
        self.tableau_affichage.setColumnWidth(5,150)
        self.tableau_affichage.setColumnWidth(6,150)
        self.tableau_affichage.setColumnWidth(7,120)
        self.tableau_affichage.setColumnWidth(8,120)
        self.tableau_affichage.setColumnWidth(9,120)
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
        self.tableau_affichage.setWordWrap(True)
        self.tableau_affichage.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableau_affichage.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableau_affichage.itemSelectionChanged.connect(self.on_row_selected)
        self.tableau_affichage.cellDoubleClicked.connect(self.on_cell_double_clicked)
        self.tableau_affichage.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)
        self.tableau_affichage.cellChanged.connect(self.on_cell_changed)
        
        
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
        self.num_ref_ata_label.hide()

        self.num_ref_ata_input = QLineEdit(self.frame_recapitulatifs)
        self.num_ref_ata_input.setGeometry(300, 200, 300, 35)
        self.num_ref_ata_input.setStyleSheet("background-color: white; border:1px solid black;color:black;padding:5px;font-size:15px")
        self.num_ref_ata_input.hide()

        self.comp_description_label = QLabel("Description composant:", self.frame_recapitulatifs)
        self.comp_description_label.setGeometry(20, 200, 250, 30)
        self.comp_description_label.setStyleSheet("color: black; font-size: 16px;background-color:none;font-weight:bold")

        self.comp_description_input = QLineEdit(self.frame_recapitulatifs)
        self.comp_description_input.setGeometry(300, 200, 300, 35)
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
            self._add_num_ref_ata_column()
        except Exception as e:
            print('Erreur initialisation DB:', e)
        
        # Charger les matricules et construire le tableau agrégé
        self.load_immatriculations()
        self.load_recapitulatifs()
        self.selected_rows = []
    
    def _add_num_ref_ata_column(self):
        """Ajoute les colonnes num_ref_ata, ref_ata_moteurs, ref_ata_helices à la table aircrafts si elles n'existent pas"""
        try:
            self.cursor.execute("PRAGMA table_info(aircrafts)")
            columns = [row[1] for row in self.cursor.fetchall()]
            for col in ['num_ref_ata', 'ref_ata_moteurs', 'ref_ata_helices']:
                if col not in columns:
                    self.cursor.execute(f"ALTER TABLE aircrafts ADD COLUMN {col} TEXT")
                    print(f"Colonne {col} ajoutée à aircrafts")
            self.conn.commit()
        except Exception as e:
            print('Erreur ajout colonnes:', e)
    
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
        """Remplit date_proc_rev / pot_restant / pot_restant_cycles depuis temps_vie."""
        immat = self.immatriculation_input.currentText().strip()
        if not immat:
            self.date_proc_rev_input.clear()
            self.pot_restant_input.clear()
            self.pot_restant_cycles_input.clear()
            return

        try:
            self.cursor.execute(
                'SELECT dates_proc_rev, pot_restant, pot_restant_cycles FROM temps_vie WHERE immatriculation=? ORDER BY rowid DESC LIMIT 1',
                (immat,)
            )
            row = self.cursor.fetchone()
            if row:
                dates_proc_rev, pot_restant, pot_restant_cycles = row
                self.date_proc_rev_input.setText(dates_proc_rev or "")
                self.pot_restant_input.setText(pot_restant or "")
                self.pot_restant_cycles_input.setText(str(pot_restant_cycles) if pot_restant_cycles is not None else "")
            else:
                self.date_proc_rev_input.clear()
                self.pot_restant_input.clear()
                self.pot_restant_cycles_input.clear()
        except Exception as e:
            print('Erreur récupération données temps_vie:', e)
            self.date_proc_rev_input.clear()
            self.pot_restant_input.clear()
            self.pot_restant_cycles_input.clear()

    def _parse_hours_value(self, value):
        """Convertit une chaîne de type 'hh:mm' ou 'hh' en heures décimales.

        Accepte aussi les formats contenant des caractères non numériques (ex: "16h", "16,5").
        Retourne None si la conversion échoue.
        """
        if value is None:
            return None
        s = str(value).strip()
        if not s:
            return None

        # Format hh:mm
        if ':' in s:
            parts = s.split(':')
            if len(parts) == 2:
                try:
                    h = float(parts[0])
                    m = float(parts[1])
                    return h + m / 60.0
                except Exception:
                    return None

        # Supprimer tout sauf chiffres, point, virgule, signe
        import re
        cleaned = re.sub(r"[^0-9.,-]", "", s)
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except Exception:
            return None
    
    def check_alert_criteria(self, immat: str) -> dict:
        """Vérifie les critères d'alerte pour moteurs et hélices
        
        Alerte si AU MOINS UN critère est vrai:
        - Heures restantes (pot_restant) <= 20h
        - Cycles restants (pot_restant_cycles) <= 50
        - Date de révision dans les 30 jours (1 mois)
        
        Retourne: {'moteurs': True/False, 'helices': True/False}
        """
        from datetime import datetime, timedelta
        
        alert_status = {'moteurs': False, 'helices': False}
        
        # Vérifier MOTEURS (boucle sur TOUTES les hélices)
        try:
            self.cursor.execute(
                'SELECT pot_restant, pot_restant_cycles, date_revision FROM moteurs WHERE immatriculation=?',
                (immat,)
            )
            motors = self.cursor.fetchall()
            for pot_h, pot_c, date_rev in motors:
                
                # Convertir les valeurs (prise en charge des formats hh:mm ou '16h')
                try:
                    pot_h_float = self._parse_hours_value(pot_h)
                    pot_c_int = int(str(pot_c).strip()) if pot_c else None
                except:
                    pot_h_float = None
                    pot_c_int = None
                
                # Vérifier la date
                date_in_30d = False
                if date_rev:
                    try:
                        date_obj = datetime.strptime(str(date_rev), "%Y-%m-%d").date()
                        days_until = (date_obj - datetime.now().date()).days
                        date_in_30d = 0 <= days_until <= 30
                    except:
                        pass
                
                # Alerte si AU MOINS UN critère est vrai
                if (pot_h_float is not None and pot_h_float <= 20) or \
                   (pot_c_int is not None and pot_c_int <= 50) or \
                   date_in_30d:
                    alert_status['moteurs'] = True
                    break  # Une seule alerte moteur suffit
        except Exception as e:
            pass
        
        # Vérifier HÉLICES (boucle sur TOUTES les hélices)
        try:
            self.cursor.execute(
                'SELECT pot_restant, pot_restant_cycles, date_revision FROM helices WHERE immatriculation=?',
                (immat,)
            )
            helices = self.cursor.fetchall()
            for pot_h, pot_c, date_rev in helices:
                
                # Convertir les valeurs (prise en charge des formats hh:mm ou '16h')
                try:
                    pot_h_float = self._parse_hours_value(pot_h)
                    pot_c_int = int(str(pot_c).strip()) if pot_c else None
                except:
                    pot_h_float = None
                    pot_c_int = None
                
                # Vérifier la date
                date_in_30d = False
                if date_rev:
                    try:
                        date_obj = datetime.strptime(str(date_rev), "%Y-%m-%d").date()
                        days_until = (date_obj - datetime.now().date()).days
                        date_in_30d = 0 <= days_until <= 30
                    except:
                        pass
                
                # Alerte si AU MOINS UN critère est vrai
                if (pot_h_float is not None and pot_h_float <= 20) or \
                   (pot_c_int is not None and pot_c_int <= 50) or \
                   date_in_30d:
                    alert_status['helices'] = True
                    break  # Une seule alerte hélice suffit
        except Exception as e:
            pass
        
        return alert_status

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

        print("\n🔍 Vérification des alertes moteurs/hélices...")
        for idx, immat in enumerate(immats):
            self.full_data[idx] = immat
            # Définir automatiquement les références ATA
            ref_moteurs = "72"  # Valeur fixe pour moteurs
            ref_helices = "61"   # Valeur fixe pour hélices
            
            # Vérifier les critères d'alerte
            alert_status = self.check_alert_criteria(immat)
            
            data = self.build_detailed_data(immat, multi_line=False)
            # Format des données pour l'affichage en tableau (une seule ligne par cellule)
            table_data = [re.sub(r"\s*\n\s*", " | ", d.strip()) if d else "" for d in data]

            self.tableau_affichage.setItem(idx, 0, QTableWidgetItem(immat))
            item_mot = QTableWidgetItem(ref_moteurs)
            item_mot.setFlags(item_mot.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Rendre non éditable
            self.tableau_affichage.setItem(idx, 1, item_mot)
            item_hel = QTableWidgetItem(ref_helices)
            item_hel.setFlags(item_hel.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Rendre non éditable
            self.tableau_affichage.setItem(idx, 2, item_hel)
            
            for col in range(3, 10):
                item = QTableWidgetItem(table_data[col-3])
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item.setData(Qt.ItemDataRole.UserRole, immat)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

                # NOTE: QTableWidgetItem does not support setTextFormat in PyQt6.
                # Rich text rendering would require a custom delegate (QStyledItemDelegate) for the table.
                
                # Appliquer la coloration rouge du texte pour les alertes
                # Colonne 5 (index 5) = Moteurs, Colonne 6 (index 6) = Hélices
                # Si un critère est atteint, le texte devient rouge (et gras pour visibilité)
                if col == 5 and alert_status['moteurs']:
                    item.setForeground(QColor("#D32F2F"))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                elif col == 6 and alert_status['helices']:
                    item.setForeground(QColor("#D32F2F"))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                
                self.tableau_affichage.setItem(idx, col, item)

        # Ajuster la hauteur des lignes pour afficher les sauts de lignes correctement
        self.tableau_affichage.resizeRowsToContents()

    def format_hours_to_hhmm(self, hours_value):
        """Convertit les heures décimales en format hh:mm"""
        if not hours_value or hours_value == "":
            return ""
        try:
            hours = float(hours_value)
            hours_int = int(hours)
            minutes = int((hours - hours_int) * 60)
            return f"{hours_int:02d}:{minutes:02d}"
        except (ValueError, TypeError):
            return str(hours_value)

    def build_detailed_data(self, immat: str, multi_line: bool = False) -> list:
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
            # Colonne 3: Moteurs (avec ATA prédéfini = 72 et tous les potentiels)
            self.cursor.execute(
                'SELECT marque, numero_serie, pot_months, pot_hours, pot_cycles, pot_restant, pot_restant_cycles, date_revision FROM moteurs '
                'WHERE immatriculation=?',
                (immat,)
            )
            motors = self.cursor.fetchall()
            if motors:
                motors_list = []
                for m in motors:
                    date_rev = m[7] if m[7] else "N/A"
                    pot_restant_formatted = self.format_hours_to_hhmm(m[5])
                    
                    # Vérifier les critères d'alerte pour ce moteur
                    alert_icon = ""
                    try:
                        pot_h = self._parse_hours_value(m[5])
                        pot_c = None
                        try:
                            pot_c = int(str(m[6]).strip()) if m[6] is not None else None
                        except Exception:
                            pot_c = None

                        # Vérifier la date
                        from datetime import datetime
                        date_in_30d = False
                        if m[7]:
                            try:
                                date_obj = datetime.strptime(str(m[7]), "%Y-%m-%d").date()
                                days = (date_obj - datetime.now().date()).days
                                date_in_30d = 0 <= days <= 30
                            except:
                                pass

                        # Si AU MOINS UN critère est true, ajouter l'alerte
                        if (pot_h is not None and pot_h <= 20) or \
                           (pot_c is not None and pot_c <= 50) or \
                           date_in_30d:
                            alert_icon = "⚠️ ALERTE! "
                    except:
                        pass
                    
                    if multi_line:
                        motors_list.append(
                            f"{alert_icon}<b>ATA: 72</b> <br>"
                            f"Marque: {m[0]} <br>"
                            f"N° série: {m[1]} <br>"
                            f"Potentiel: {m[2]} mois / {m[3]} heures / {m[4]} cycles<br>"
                            f"Date Proc rev: {date_rev} <br>"
                            f"Potentiel restant heures: {pot_restant_formatted}h<br>"
                            f"Potentiel restant cycles: {m[6]}c<br>"
                            "*************************************** <br> <br>"
                            
                        )
                    else:
                        motors_list.append(
                            f"{alert_icon}ATA: 72: Marque {m[0]} N° série {m[1]} Potentiel {m[2]}m/{m[3]}h/{m[4]}c Potentiel restant heures {pot_restant_formatted}h Potentiel restant cycles {m[6]}c Date proc rev: {date_rev}"
                        )
                data[2] = ("\n\n" if multi_line else "\n").join(motors_list)
        except Exception as e:
            print(f"Erreur moteurs: {e}")
            pass

        try:
            # Colonne 4: Hélices (avec ATA prédéfini = 61 et tous les potentiels)
            self.cursor.execute(
                'SELECT marque, numero_serie, pot_months, pot_hours, pot_cycles, pot_restant, pot_restant_cycles, date_revision FROM helices '
                'WHERE immatriculation=?',
                (immat,)
            )
            props = self.cursor.fetchall()
            if props:
                props_list = []
                for p in props:
                    date_rev = p[7] if p[7] else "N/A"
                    pot_restant_formatted = self.format_hours_to_hhmm(p[5])
                    
                    # Vérifier les critères d'alerte pour cette hélice
                    alert_icon = ""
                    try:
                        pot_h = self._parse_hours_value(p[5])
                        pot_c = None
                        try:
                            pot_c = int(str(p[6]).strip()) if p[6] is not None else None
                        except Exception:
                            pot_c = None

                        # Vérifier la date
                        from datetime import datetime
                        date_in_30d = False
                        if p[7]:
                            try:
                                date_obj = datetime.strptime(str(p[7]), "%Y-%m-%d").date()
                                days = (date_obj - datetime.now().date()).days
                                date_in_30d = 0 <= days <= 30
                            except:
                                pass

                        # Si AU MOINS UN critère est true, ajouter l'alerte
                        if (pot_h is not None and pot_h <= 20) or \
                           (pot_c is not None and pot_c <= 50) or \
                           date_in_30d:
                            alert_icon = "⚠️ ALERTE! "
                    except:
                        pass
                    
                    if multi_line:
                        props_list.append(
                            f"{alert_icon} <b>ATA: 61</b> <br>"
                            f"Marque: {p[0]} <br>"
                            f"N° série: {p[1]} <br>"
                            f"Potentiel: {p[2]} mois / {p[3]} heures / {p[4]} cycles<br>"
                            f"Date Proc rev: {date_rev} <br>"
                            f"Potentiel restant heures: {pot_restant_formatted}h<br>"
                            f"Potentiel restant cycles: {p[6]}c<br>"
                            "******************************************* <br> <br>"
                            
                        )
                    else:
                        props_list.append(
                            f"{alert_icon} ATA: 61: Marque {p[0]} N° série {p[1]} Potentiel {p[2]}m/{p[3]}h/{p[4]}c Potentiel restant heures {pot_restant_formatted}h Potentiel restant cycles {p[6]}c Date proc rev: {date_rev}"
                        )
                data[3] = ("\n\n" if multi_line else "\n").join(props_list)
        except Exception as e:
            print(f"Erreur hélices: {e}")
            pass

        try:
            # Colonne 5: Temps de Vie avec tous les potentiels
            self.cursor.execute(
                'SELECT num_ref_ata, description, pot_months, potentiel_heures, potentiel_cycles, pot_restant, pot_restant_cycles, dates_proc_rev FROM temps_vie '
                'WHERE immatriculation=? ORDER BY num_ref_ata',
                (immat,)
            )
            rows = self.cursor.fetchall()
            if rows:
                temps_list = []
                for ata, desc, pot_m, pot_h, pot_c, pot_rest_h, pot_rest_c, dates_proc_rev in rows:
                    if multi_line:
                        temps_list.append(
                            f"<b> ATA: {ata}</b> <br>"
                            f"Description: <b>{desc}</b> <br>"
                            f"Potentiel: {pot_m} mois / {pot_h} heures / {pot_c} cycles<br>"
                            f"Date proc rev: {dates_proc_rev}<br>"
                            f"Potentiel restant heures: {pot_rest_h}h<br>"
                            f"Potentiel restant cycles: {pot_rest_c}c<br>"
                            "******************************************** <br> <br>"
                        )
                    else:
                        temps_list.append(
                            f"ATA {ata}: {desc} Potentiel {pot_m}m/{pot_h}h/{pot_c}c Potentiel restant heures {pot_rest_h}h Potentiel restant cycles {pot_rest_c}c Date proc rev: {dates_proc_rev}"
                        )
                data[4] = ("\n\n" if multi_line else "\n").join(temps_list)
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
    
    def on_cell_changed(self, row, col):
        """Gère la modification de cellule - les colonnes ATA sont maintenant fixes"""
        # Les colonnes 1 (Ref ATA Moteurs) et 2 (Ref ATA Hélices) sont maintenant fixes
        # et ne peuvent plus être modifiées
        if col in (1, 2):
            # Restaurer les valeurs fixes
            if col == 1:  # Ref ATA Moteurs
                self.tableau_affichage.item(row, col).setText("72")
            elif col == 2:  # Ref ATA Hélices
                self.tableau_affichage.item(row, col).setText("61")
            return

    def save_recapitulatifs(self):
        """Sauvegarde les donnees du recapitulatif dans la base de donnees"""
        immat = self.immatriculation_input.currentText().strip()
        types = self.types_.currentText().strip()
        certifications = self.certifications.text().strip()
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
                        immatriculation, types, certifications,
                        comp_description, date_proc_rev,
                        pot_restant, pot_restant_cycles
                   ) VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (immat, types, certifications,
                 comp_desc, date_proc, pot_rem, pot_rem_cycles)
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
        """Show a detail dialog when a cell is double-clicked (except for Ref ATA columns)."""
        # Colonnes 1 et 2 sont pour Ref ATA Moteurs et Hélices - permettre l'édition directe
        if column in (1, 2):
            # Laisser PyQt gérer l'édition
            return
        
        # Pour les autres colonnes, afficher le dialogue de détails
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

        # Affichage automatique des numéros ATA moteurs et hélices
        # ref_layout = QHBoxLayout()
        # ref_layout.addWidget(QLabel("<b>Ref ATA Moteurs:</b>"))
        # ref_layout.addWidget(QLabel("<b style='color: #1976d2; font-size: 14px;'>72</b>"))
        # ref_layout.addSpacing(30)
        # ref_layout.addWidget(QLabel("<b>Ref ATA Hélices:</b>"))
        # ref_layout.addWidget(QLabel("<b style='color: #1976d2; font-size: 14px;'>61</b>"))
        # ref_layout.addStretch()
        # layout.addLayout(ref_layout)

        # afficher detailed information in a structured way
        detailed_data = self.build_detailed_data(immat, multi_line=True)
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
        # try:
        #     self.cursor.execute(
        #         'SELECT types, certifications, num_ref_ata, comp_description, date_proc_rev, pot_restant, pot_restant_cycles '
        #         'FROM recapitulatifs WHERE immatriculation=?',
        #         (immat,)
        #     )
        #     rec_rows = self.cursor.fetchall()
        #     if rec_rows:
        #         recap_header = QLabel(f"<b style='color: #1565c0; font-size: 14px;'>Récapitulatif(s) enregistrés :</b>")
        #         recap_header.setStyleSheet("margin-top: 10px; margin-bottom: 2px;")
        #         layout.addWidget(recap_header)
        #         for rec in rec_rows:
        #             rec_text = (
        #                 f"Type: {rec[0]}\n"
        #                 f"Certifications: {rec[1]}\n"
        #                 f"Num ref ATA: {rec[2]}\n"
        #                 f"Description: {rec[3]}\n"
        #                 f"Date Proc Rev: {rec[4]}\n"
        #                 f"Pot restant: {rec[5]} h\n"
        #                 f"Pot cycles: {rec[6]}"
        #             )
        #             rec_label = QLabel(rec_text)
        #             rec_label.setStyleSheet("""
        #                 background-color: white;
        #                 border: 1px solid #ddd;
        #                 border-radius: 4px;
        #                 padding: 8px;
        #                 color: #333333;
        #                 font-family: 'Segoe UI', Arial, sans-serif;
        #             """)
        #             rec_label.setWordWrap(True)
        #             rec_label.setMinimumHeight(60)
        #             layout.addWidget(rec_label)
        # except Exception:
        #     pass

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
        full = self.full_data.get(row, None)
        types = ""
        certifications = ""
        comp_desc = ""
        date_proc = ""
        pot_rem = ""
        pot_rem_cycles = ""
        
        # Remplir les champs du formulaire
        self.immatriculation_input.setCurrentText(immat)
        self.types_.setCurrentText(types if types else "Cellule")
        self.certifications.setText(certifications)
        self.num_ref_ata_input.clear()
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
        certifications = self.certifications.text().strip()
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
                            types=?, certifications=?,
                            comp_description=?, date_proc_rev=?,
                            pot_restant=?, pot_restant_cycles=?
                       WHERE immatriculation=?''',
                    (types, certifications,
                     comp_desc, date_proc,
                     pot_rem, pot_rem_cycles, immat)
                )
            else:
                self.cursor.execute(
                    '''UPDATE recapitulatifs SET 
                            types=?, certifications=?,
                            comp_description=?, date_proc_rev=?,
                            pot_restant=?, pot_restant_cycles=?
                       WHERE id=?''',
                    (types, certifications,
                     comp_desc, date_proc,
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
        