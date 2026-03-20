from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,QTableWidget,QTableWidgetItem,QFrame,QScrollArea
from PyQt6.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt6.QtCore import Qt, QSize
import sys
from ajout_info import AjoutInfo
from heures_vol import HeuresVol
from moteurs import Moteurs
from helices import Helices
from directive import Directives
from service_bulletins import ServicesBulletins
from bilan import Bilan
from travaux import Travaux
from documents import Documents
from recapitulatifs import Recapitulatifs
from temps_vie import Temps_vie
from alertes_dashboard import AlertesDashboard


class Bienvenue(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bienvenue")
        self.setGeometry(0, 0, 1290, 680)
        # self.setFixedSize(1350, 700)
        self.setStyleSheet("background-color: white;")
        
        # self.setWindowFlags(Qt.WindowType.CustomizeWindowHint)
        self.setWindowFlags(self.windowFlags() & Qt.WindowType.WindowMinimizeButtonHint)
        
        self.navigateur = QLabel(self)
        self.navigateur.setGeometry(0,0,1350,60)
        self.navigateur.setStyleSheet("background-color:blueviolet")
        self.navigateur.lower()
        
        self.titre = QLabel("Gestion de Vol aéronef", self)
        self.titre.setGeometry(20, 5, 800, 50)
        self.titre.setStyleSheet("font-size: 20px;color:white;background-color:none")
        
        self.profil = QPushButton(self)
        self.profil.setGeometry(1200,10,40,40)
        self.profil.setIcon(QIcon("./images/icon_profile.svg"))
        self.profil.setIconSize(QSize(32, 32))
        self.profil.setStyleSheet('border-radius:5px;background-color:white;border:1px solid #333;')
        self.profil.setCursor(Qt.CursorShape.PointingHandCursor)
        self.profil.clicked.connect(self.aff_profil)
        
        self.dashboard = QFrame(self)
        self.dashboard.setGeometry(5,70,250,600)
        self.dashboard.setStyleSheet("background-color:gray;border-radius:15px")
        
        
        self.info = QPushButton("Informations Aeronef",self.dashboard )
        self.info.setGeometry(25,20,200,40)
        self.info.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.info.clicked.connect(self.show_ajout_info)
        
        self.heures = QPushButton("Saisie heures de vol",self.dashboard )
        self.heures.setGeometry(25,70,200,40)
        self.heures.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.heures.setCursor(Qt.CursorShape.PointingHandCursor)
        self.heures.clicked.connect(self.show_heures_vol)
        
        self.moteurs = QPushButton("Moteurs",self.dashboard)
        self.moteurs.setGeometry(25,120,200,40)
        self.moteurs.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.moteurs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.moteurs.clicked.connect(self.show_moteurs)
        
        self.hélices = QPushButton("Hélices",self.dashboard)
        self.hélices.setGeometry(25,170,200,40)
        self.hélices.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.hélices.setCursor(Qt.CursorShape.PointingHandCursor)
        self.hélices.clicked.connect(self.show_helices)
        
        self.temps_vie = QPushButton("Temps de vie (TSN / TBO)",self.dashboard)
        self.temps_vie.setGeometry(25,220,200,40)
        self.temps_vie.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.temps_vie.setCursor(Qt.CursorShape.PointingHandCursor)
        self.temps_vie.clicked.connect(self.show_temps_vie)
        
        self.directive = QPushButton("ADs/Consignes de Navigabilité",self.dashboard)
        self.directive.setGeometry(25,270,200,40)
        self.directive.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.directive.setCursor(Qt.CursorShape.PointingHandCursor)
        self.directive.clicked.connect(self.show_directive)
        
        self.bulletin = QPushButton("SB - Services Bulletins",self.dashboard)
        self.bulletin.setGeometry(25,320,200,40)
        self.bulletin.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.bulletin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bulletin.clicked.connect(self.show_services)
        
        self.bilan = QPushButton("Bilan des visites",self.dashboard)
        self.bilan.setGeometry(25,370,200,40)
        self.bilan.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.bilan.setCursor(Qt.CursorShape.PointingHandCursor)
        self.bilan.clicked.connect(self.show_bilan)
        
        self.travaux = QPushButton("Modification/reparation/Derogation",self.dashboard)
        self.travaux.setGeometry(25,420,200,40)
        self.travaux.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.travaux.setCursor(Qt.CursorShape.PointingHandCursor)
        self.travaux.clicked.connect(self.show_travaux)
        
        self.documents = QPushButton("Documents et certifications",self.dashboard)
        self.documents.setGeometry(25,470,200,40)
        self.documents.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.documents.setCursor(Qt.CursorShape.PointingHandCursor)
        self.documents.clicked.connect(self.show_documents)
        
        self.recapitulatifs = QPushButton("Recapitulatifs des echeances",self.dashboard)
        self.recapitulatifs.setGeometry(25,520,200,40)
        self.recapitulatifs.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:10px;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.recapitulatifs.setCursor(Qt.CursorShape.PointingHandCursor)
        self.recapitulatifs.clicked.connect(self.show_recapitulatifs)
        
        
        # initiation des frames
        
        self.ajout_info_frame = None
        self.heures_vol_frame = None
        # creation bouton alertes
        self.alertes_btn = QPushButton("Alertes \u0026 Maintenance", self)
        self.alertes_btn.setGeometry(900, 10, 260, 40)
        self.alertes_btn.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:#d32f2f;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover{
                color:white;
                background-color:#ff5722;
            }
        """)
        self.alertes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.alertes_btn.clicked.connect(self.show_alertes)

        self.moteurs_frame = None
        self.helices_frame = None
        self.directives_frame = None
        self.services_frame = None
        self.bilan_frame = None
        self.travaux_frame = None
        self.documents_frame = None
        self.recapitulatifs_frame = None
        self.temps_frame = None
        self.alertes_frame = None
        self.info_logiciel_frame = None
        self.ajout_info = AjoutInfo(self)
        self.ajout_info.setGeometry(260,70,1020,600)
        
        # Fenetre Profil
        self.profil_frame = QFrame(self)
        self.profil_frame.setGeometry(1100,60,150,150)
        self.profil_frame.setStyleSheet("background-color:white;border:1px solid black;border-radius:10px;border:1px solid black")
        
        self.profil_label = QLabel("Profil", self.profil_frame)
        self.profil_label.setGeometry(10,10,130,30)
        self.profil_label.setStyleSheet("font-size: 14px;color:black;background-color:none;border:none;padding-left:50px")
        
        
        self.parametres = QPushButton("Information", self.profil_frame)
        self.parametres.setGeometry(10,50,130,30)
        self.parametres.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:5px;
                border:1px solid black;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.parametres.setCursor(Qt.CursorShape.PointingHandCursor)
        self.parametres.clicked.connect(self.show_info_logiciel)
        
        self.deconnexion = QPushButton("Déconnexion", self.profil_frame)
        self.deconnexion.setGeometry(10,100,130,30)
        self.deconnexion.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:black;
                border-radius:5px;
                border:1px solid black;
            }
            QPushButton:hover{
                color:white;
                background-color:blue;
            }
        """)
        self.deconnexion.setCursor(Qt.CursorShape.PointingHandCursor)
        self.deconnexion.clicked.connect(self.deconnexion_clicked)
        self.profil_frame.hide()

    def reset_buttons(self):
        """Reset all dashboard buttons to default black background"""
        buttons = [
            self.info, self.heures, self.moteurs, self.hélices, self.temps_vie,
            self.directive, self.bulletin, self.bilan, self.travaux, self.documents,
            self.recapitulatifs
        ]
        for btn in buttons:
            btn.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:black;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
        # Special for alertes_btn
        self.alertes_btn.setStyleSheet("""
            QPushButton{
                color: white;
                background-color:#d32f2f;
                border-radius:10px;
                font-weight:bold;
            }
            QPushButton:hover{
                color:white;
                background-color:#ff5722;
            }
        """)

    def show_ajout_info(self):
        if self.ajout_info is None:
            self.ajout_info = AjoutInfo(self)
            self.ajout_info.setGeometry(260,70,1020,600)

        if self.ajout_info.isVisible():
            self.ajout_info.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.ajout_info)
            self.ajout_info.show()
            self.ajout_info.raise_()
            self.info.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)

    def hide_all_frames(self, except_frame=None):
        frames = [
            getattr(self, "ajout_info", None),
            getattr(self, "heures_vol_frame", None),
            getattr(self, "moteurs_frame", None),
            getattr(self, "helices_frame", None),
            getattr(self, "directives_frame", None),
            getattr(self, "services_frame", None),
            getattr(self, "bilan_frame", None),
            getattr(self, "travaux_frame", None),
            getattr(self, "documents_frame", None),
            getattr(self, "recapitulatifs_frame", None),
            getattr(self, "temps_frame", None),
            getattr(self, "alertes_frame", None),
            getattr(self, "info_logiciel_frame", None),
        ]

        for f in frames:
            if f is None:
                continue
            if f is except_frame:
                continue
            try:
                f.hide()
            except Exception:
                pass
        
        # Reset all buttons to black when hiding frames
        self.reset_buttons()
            
            
    def refresh_all_immatriculations(self):
        """Ask every child frame that has a combobox of immatriculations to reload its list.
        This method is safe to call even if the frame has not been created yet.
        """
        for attr in [
            'heures_vol_frame', 'bilan_frame', 'travaux_frame', 'temps_frame',
            'services_frame', 'recapitulatifs_frame',
            'moteurs_frame', 'helices_frame', 'directives_frame', 'documents_frame'
        ]:
            widget = getattr(self, attr, None)
            if widget and hasattr(widget, 'load_immatriculations'):
                try:
                    widget.load_immatriculations()
                except Exception:
                    pass

    def show_heures_vol(self):
        # always refresh the combobox just before showing the page
        if self.heures_vol_frame is None:
            self.heures_vol_frame = HeuresVol(self)
            self.heures_vol_frame.setGeometry(260,70,1020,600)

        # reload immatriculations in case new aircrafts have been added
        try:
            self.heures_vol_frame.load_immatriculations()
        except Exception:
            pass

        if self.heures_vol_frame.isVisible():
            self.heures_vol_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.heures_vol_frame)
            self.heures_vol_frame.show()
            self.heures_vol_frame.raise_()
            self.heures.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_moteurs(self):
        if self.moteurs_frame is None:
            self.moteurs_frame = Moteurs(self)
            self.moteurs_frame.setGeometry(260,70,1020,600)

        if self.moteurs_frame.isVisible():
            self.moteurs_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.moteurs_frame)
            self.moteurs_frame.show()
            self.moteurs_frame.raise_()
            self.moteurs.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_helices(self):
        if self.helices_frame is None:
            self.helices_frame = Helices(self)
            self.helices_frame.setGeometry(260,70,1020,600)

        if self.helices_frame.isVisible():
            self.helices_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.helices_frame)
            self.helices_frame.show()
            self.helices_frame.raise_()
            self.hélices.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_directive(self):
        if self.directives_frame is None:
            self.directives_frame = Directives(self)
            self.directives_frame.setGeometry(260,70,1020,600)

        if self.directives_frame.isVisible():
            self.directives_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.directives_frame)
            self.directives_frame.show()
            self.directives_frame.raise_()
            self.directive.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_services(self):
        if self.services_frame is None:
            self.services_frame = ServicesBulletins(self)
            self.services_frame.setGeometry(260,70,1020,600)

        if self.services_frame.isVisible():
            self.services_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.services_frame)
            self.services_frame.show()
            self.services_frame.raise_()
            self.bulletin.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_bilan(self):
        if self.bilan_frame is None:
            self.bilan_frame = Bilan(self)
            self.bilan_frame.setGeometry(260,70,1020,600)

        if self.bilan_frame.isVisible():
            self.bilan_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.bilan_frame)
            self.bilan_frame.show()
            self.bilan_frame.raise_()
            self.bilan.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_travaux(self):
        if self.travaux_frame is None:
            self.travaux_frame = Travaux(self)
            self.travaux_frame.setGeometry(260,70,1020,600)

        if self.travaux_frame.isVisible():
            self.travaux_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.travaux_frame)
            self.travaux_frame.show()
            self.travaux_frame.raise_()
            self.travaux.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_documents(self):
        if self.documents_frame is None:
            self.documents_frame = Documents(self)
            self.documents_frame.setGeometry(260,70,1020,600)

        if self.documents_frame.isVisible():
            self.documents_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.documents_frame)
            self.documents_frame.show()
            self.documents_frame.raise_()
            self.documents.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
            
    def show_recapitulatifs(self):
        if self.recapitulatifs_frame is None:
            self.recapitulatifs_frame = Recapitulatifs(self)
            self.recapitulatifs_frame.setGeometry(260,70,1020,600)

        if self.recapitulatifs_frame.isVisible():
            self.recapitulatifs_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.recapitulatifs_frame)
            self.recapitulatifs_frame.show()
            self.recapitulatifs_frame.raise_()
            self.recapitulatifs.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
    
    def show_temps_vie(self):
        if self.temps_frame is None:
            self.temps_frame = Temps_vie(self)
            self.temps_frame.setGeometry(260,70,1020,600)

        if self.temps_frame.isVisible():
            self.temps_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.temps_frame)
            self.temps_frame.show()
            self.temps_frame.raise_()
            self.temps_vie.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                }
                QPushButton:hover{
                    color:white;
                    background-color:blue;
                }
            """)
    
    def show_alertes(self):
        if self.alertes_frame is None:
            self.alertes_frame = AlertesDashboard(self)
            self.alertes_frame.setGeometry(270,55,1050,620)

        if self.alertes_frame.isVisible():
            self.alertes_frame.hide()
            self.reset_buttons()
        else:
            self.hide_all_frames(except_frame=self.alertes_frame)
            self.alertes_frame.show()
            self.alertes_frame.raise_()
            self.alertes_btn.setStyleSheet("""
                QPushButton{
                    color: white;
                    background-color:blue;
                    border-radius:10px;
                    font-weight:bold;
                }
                QPushButton:hover{
                    color:white;
                    background-color:#ff5722;
                }
            """)
            
    def show_info_logiciel(self):
        """Affiche la fenêtre d'information du logiciel"""
        if self.info_logiciel_frame is None:
            self.info_logiciel_frame = QFrame(self)
            self.info_logiciel_frame.setGeometry(260, 70, 1020, 600)
            self.info_logiciel_frame.setStyleSheet("background-color: white; border-radius: 15px; border: 2px solid #2c3e50;")
            
            # Titre principal
            titre = QLabel("ℹ️  INFORMATION DU LOGICIEL", self.info_logiciel_frame)
            titre.setGeometry(20, 20, 980, 40)
            titre.setStyleSheet("font-size: 24px; color: #2c3e50; font-weight: bold; background-color: transparent;")
            
            # Bouton de fermeture (croix) en haut à droite
            btn_close = QPushButton("✕", self.info_logiciel_frame)
            btn_close.setGeometry(970, 10, 30, 30)
            btn_close.setStyleSheet("""
                QPushButton{
                    color: #e74c3c;
                    background-color: black;
                    border: none;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover{
                    color: #c0392b;
                    background-color: #ecf0f1;
                    border-radius: 15px;
                }
            """)
            btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_close.clicked.connect(lambda: self.info_logiciel_frame.hide())
            
            # Séparateur
            sep1 = QLabel(self.info_logiciel_frame)
            sep1.setGeometry(20, 65, 980, 2)
            sep1.setStyleSheet("background-color: #3498db;")
            
            # Section: Nom et version
            label_name = QLabel("📌 Nom du Logiciel:", self.info_logiciel_frame)
            label_name.setGeometry(40, 90, 200, 30)
            label_name.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background-color: transparent;")
            
            value_name = QLabel("Système de Gestion de Vol pour Aéronefs", self.info_logiciel_frame)
            value_name.setGeometry(250, 90, 700, 30)
            value_name.setStyleSheet("font-size: 14px; color: #34495e; background-color: #ecf0f1; padding: 5px; border-radius: 5px;")
            
            # Version
            label_version = QLabel("📦 Version:", self.info_logiciel_frame)
            label_version.setGeometry(40, 130, 200, 30)
            label_version.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background-color: transparent;")
            
            value_version = QLabel("v1.0.0 - Build 2026", self.info_logiciel_frame)
            value_version.setGeometry(250, 130, 700, 30)
            value_version.setStyleSheet("font-size: 14px; color: #34495e; background-color: #ecf0f1; padding: 5px; border-radius: 5px;")
            
            # Langue
            label_langue = QLabel("🌐 Langue:", self.info_logiciel_frame)
            label_langue.setGeometry(40, 170, 200, 30)
            label_langue.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background-color: transparent;")
            
            value_langue = QLabel("Français (FR)", self.info_logiciel_frame)
            value_langue.setGeometry(250, 170, 700, 30)
            value_langue.setStyleSheet("font-size: 14px; color: #34495e; background-color: #ecf0f1; padding: 5px; border-radius: 5px;")
            
            # Développé par
            label_dev = QLabel("👨💻 Développé par:", self.info_logiciel_frame)
            label_dev.setGeometry(40, 210, 200, 30)
            label_dev.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; background-color: transparent;")
            
            value_dev = QLabel("Iketrika Py", self.info_logiciel_frame)
            value_dev.setGeometry(250, 210, 700, 30)
            value_dev.setStyleSheet("font-size: 14px; color: #27ae60; background-color: #ecf0f1; padding: 5px; border-radius: 5px; font-weight: bold;")
            
            # Séparateur
            sep2 = QLabel(self.info_logiciel_frame)
            sep2.setGeometry(20, 260, 980, 2)
            sep2.setStyleSheet("background-color: #e74c3c;")
            
            # Section sécurité
            titre_securite = QLabel("🔒 MESURES DE SÉCURISATION", self.info_logiciel_frame)
            titre_securite.setGeometry(40, 280, 900, 30)
            titre_securite.setStyleSheet("font-size: 16px; font-weight: bold; color: #e74c3c; background-color: transparent;")
            
            # Scroll area pour les détails de sécurité
            scroll_area = QScrollArea(self.info_logiciel_frame)
            scroll_area.setGeometry(40, 320, 940, 250)
            scroll_area.setStyleSheet("background-color: #ecf0f1; border-radius: 10px; border: 1px solid #bdc3c7;")
            scroll_area.setWidgetResizable(True)
            
            # Contenu scrollable
            scroll_content = QFrame()
            scroll_content.setStyleSheet("background-color: #ecf0f1;")
            layout = QVBoxLayout(scroll_content)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            
            securite_items = [
                "✅ Authentification sécurisée: Système de login avec validation des identifiants",
                "🔐 Chiffrement des données: Protection des données sensibles en base de données SQLite",
                "📊 Base de données sécurisée: SQLite avec contraintes d'intégrité",
                "🛡️ Validation des entrées: Prévention des injections SQL et erreurs de saisie",
                "📋 Audit et historique: Traçabilité complète de toutes les opérations de maintenance",
                "🔑 Gestion des droits: Contrôle d'accès basé sur le profil utilisateur",
                "🔄 Intégrité référentielle: Contraintes de clés étrangères pour la cohérence des données",
                "⚡ Optimisation: Requêtes SQL optimisées pour la performance et la stabilité",
                "🔔 Alertes automatiques: Système de maintenance préventive avec seuils",
                "💾 Sauvegarde: Données persistantes et sécurisées dans la base locale",
            ]
            
            for item in securite_items:
                label_item = QLabel(item, scroll_content)
                label_item.setStyleSheet("font-size: 12px; color: #2c3e50; background-color: white; padding: 8px; border-radius: 5px; margin: 3px; border-left: 4px solid #3498db;")
                label_item.setWordWrap(True)
                layout.addWidget(label_item)
            
            layout.addStretch()
            scroll_area.setWidget(scroll_content)
            
            # Bouton Fermer
            # btn_fermer = QPushButton("Fermer", self.info_logiciel_frame)
            # btn_fermer.setGeometry(420, 580, 180, 40)
            # btn_fermer.setStyleSheet("""
            #     QPushButton{
            #         color: white;
            #         background-color: #e74c3c;
            #         border-radius: 10px;
            #         font-weight: bold;
            #         font-size: 14px;
            #     }
            #     QPushButton:hover{
            #         background-color: #c0392b;
            #     }
            # """)
            # btn_fermer.setCursor(Qt.CursorShape.PointingHandCursor)
            # btn_fermer.clicked.connect(lambda: self.info_logiciel_frame.hide())
        
        if self.info_logiciel_frame.isVisible():
            self.info_logiciel_frame.hide()
            self.profil_frame.hide()
        else:
            self.hide_all_frames(except_frame=self.info_logiciel_frame)
            self.info_logiciel_frame.show()
            self.info_logiciel_frame.raise_()
            
    def aff_profil(self):
        
        
        if self.profil_frame.isVisible():
            self.profil_frame.hide()
        else:
            self.profil_frame.show()
            self.profil_frame.raise_()
            
    def deconnexion_clicked(self):
        # Logique de déconnexion ici
        print("Déconnexion réussie")
        self.close()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bienvenue = Bienvenue()
    bienvenue.show()
    sys.exit(app.exec())