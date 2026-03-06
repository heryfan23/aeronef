from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout,QTableWidget,QTableWidgetItem,QFrame
from PyQt6.QtGui import QPixmap, QFont, QIcon
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
        
        self.ajout_info = None
        self.heures_vol = None
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

        self.moteurs = None
        self.g_helices = None
        self.g_directives = None
        self.services = None
        self.bilan_services = None
        self.travaux_ = None
        self.documents_ = None
        self.recapitulatifs_ = None
        self.temps = None
        self.alertes_frame = None
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

    def show_ajout_info(self):
        if self.ajout_info is None:
            self.ajout_info = AjoutInfo(self)
            self.ajout_info.setGeometry(260,70,1020,600)

        if self.ajout_info.isVisible():
            self.ajout_info.hide()
        else:
            self.hide_all_frames(except_frame=self.ajout_info)
            self.ajout_info.show()
            self.ajout_info.raise_()

    def hide_all_frames(self, except_frame=None):
        frames = [
            getattr(self, "ajout_info", None),
            getattr(self, "heures_vol", None),
            getattr(self, "moteurs", None),
            getattr(self, "g_helices", None),
            getattr(self, "g_directives", None),
            getattr(self, "services", None),
            getattr(self, "bilan_services", None),
            getattr(self, "travaux_", None),
            getattr(self, "documents_", None),
            getattr(self, "recapitulatifs_", None),
            getattr(self, "temps", None),
            getattr(self, "alertes_frame", None),
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
            
            
    def refresh_all_immatriculations(self):
        """Ask every child frame that has a combobox of immatriculations to reload its list.
        This method is safe to call even if the frame has not been created yet.
        """
        for attr in [
            'heures_vol', 'bilan', 'travaux_', 'temps',
            'service_bulletins', 'recapitulatifs_',
            'moteurs', 'g_helices', 'g_directives', 'documents_'
        ]:
            widget = getattr(self, attr, None)
            if widget and hasattr(widget, 'load_immatriculations'):
                try:
                    widget.load_immatriculations()
                except Exception:
                    pass

    def show_heures_vol(self):
        # always refresh the combobox just before showing the page
        if self.heures_vol is None:
            self.heures_vol = HeuresVol(self)
            self.heures_vol.setGeometry(260,70,1020,600)

        # reload immatriculations in case new aircrafts have been added
        try:
            self.heures_vol.load_immatriculations()
        except Exception:
            pass

        if self.heures_vol.isVisible():
            self.heures_vol.hide()
        else:
            self.hide_all_frames(except_frame=self.heures_vol)
            self.heures_vol.show()
            self.heures_vol.raise_()
            
    def show_moteurs(self):
        if self.moteurs is None:
            self.moteurs = Moteurs(self)
            self.moteurs.setGeometry(260,70,1020,600)

        if self.moteurs.isVisible():
            self.moteurs.hide()
        else:
            self.hide_all_frames(except_frame=self.moteurs)
            self.moteurs.show()
            self.moteurs.raise_()
            
    def show_helices(self):
        if self.g_helices is None:
            self.g_helices = Helices(self)
            self.g_helices.setGeometry(260,70,1020,600)

        if self.g_helices.isVisible():
            self.g_helices.hide()
        else:
            self.hide_all_frames(except_frame=self.g_helices)
            self.g_helices.show()
            self.g_helices.raise_()
            
    def show_directive(self):
        if self.g_directives is None:
            self.g_directives = Directives(self)
            self.g_directives.setGeometry(260,70,1020,600)

        if self.g_directives.isVisible():
            self.g_directives.hide()
        else:
            self.hide_all_frames(except_frame=self.g_directives)
            self.g_directives.show()
            self.g_directives.raise_()
            
    def show_services(self):
        if self.services is None:
            self.services = ServicesBulletins(self)
            self.services.setGeometry(260,70,1020,600)

        if self.services.isVisible():
            self.services.hide()
        else:
            self.hide_all_frames(except_frame=self.services)
            self.services.show()
            self.services.raise_()
            
    def show_bilan(self):
        if self.bilan_services is None:
            self.bilan_services = Bilan(self)
            self.bilan_services.setGeometry(260,70,1020,600)

        if self.bilan_services.isVisible():
            self.bilan_services.hide()
        else:
            self.hide_all_frames(except_frame=self.bilan_services)
            self.bilan_services.show()
            self.bilan_services.raise_()
            
    def show_travaux(self):
        if self.travaux_ is None:
            self.travaux_ = Travaux(self)
            self.travaux_.setGeometry(260,70,1020,600)

        if self.travaux_.isVisible():
            self.travaux_.hide()
        else:
            self.hide_all_frames(except_frame=self.travaux_)
            self.travaux_.show()
            self.travaux_.raise_()
            
    def show_documents(self):
        if self.documents_ is None:
            self.documents_ = Documents(self)
            self.documents_.setGeometry(260,70,1020,600)

        if self.documents_.isVisible():
            self.documents_.hide()
        else:
            self.hide_all_frames(except_frame=self.documents_)
            self.documents_.show()
            self.documents_.raise_()
            
    def show_recapitulatifs(self):
        if self.recapitulatifs_ is None:
            self.recapitulatifs_ = Recapitulatifs(self)
            self.recapitulatifs_.setGeometry(260,70,1020,600)

        if self.recapitulatifs_.isVisible():
            self.recapitulatifs_.hide()
        else:
            self.hide_all_frames(except_frame=self.recapitulatifs_)
            self.recapitulatifs_.show()
            self.recapitulatifs_.raise_()
    
    def show_temps_vie(self):
        if self.temps is None:
            self.temps = Temps_vie(self)
            self.temps.setGeometry(260,70,1020,600)

        if self.temps.isVisible():
            self.temps.hide()
        else:
            self.hide_all_frames(except_frame=self.temps)
            self.temps.show()
            self.temps.raise_()
    
    def show_alertes(self):
        if self.alertes_frame is None:
            self.alertes_frame = AlertesDashboard(self)
            self.alertes_frame.setGeometry(270,55,1050,620)

        if self.alertes_frame.isVisible():
            self.alertes_frame.hide()
        else:
            self.hide_all_frames(except_frame=self.alertes_frame)
            self.alertes_frame.show()
            self.alertes_frame.raise_()
            
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