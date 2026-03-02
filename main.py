from PyQt6.QtWidgets import QApplication,QWidget,QLabel,QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from bienvenue import Bienvenue
from login import Login
import sys


class FenetrePrincipale(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fenetre Principale")
        self.setGeometry(0, 0, 1300, 700)
        
        
        # Fond Image (background image)
        image = QLabel(self)
        image.setGeometry(0, 0, 1300, 700)
        pixmap = QPixmap("./images/fond_2.webp") #lien image
        image.setPixmap(pixmap) #mampiditra ny sary amin'ny label
        image.setScaledContents(True) #manampy ny sary ho mifanaraka amin'ny haben'ny label
        image.lower() #mametraka ilay sary ho fond (manampy azy ho background)
        
        
        
        self.titre = QLabel("Aviation", self)
        self.titre.setGeometry(550, 30, 200, 50)
        self.titre.setStyleSheet("font-size: 40px; font-weight: bold;color:white")
        
       
        
        self.sous_titre = QLabel("Bienvenue dans le monde de l'aviation", self)
        self.sous_titre.setGeometry(450, 80, 400, 30)
        self.sous_titre.setStyleSheet("font-size: 20px;color: yellow; font-weight: bold;")
        
        self.description = QLabel("L'aviation est un domaine fascinant qui englobe l'étude, la conception, la fabrication \n et  l'exploitation des aéronefs. Que vous soyez passionné par les avions, \n les hélicoptères ou les drones, il y a toujours quelque chose de nouveau à découvrir \n dans le monde de l'aviation.", self)
        self.description.setGeometry(200, 150, 900, 200)
        self.description.setStyleSheet("font-size: 20px;color:black; font-weight: bold;background-color: #aaa5a58f;padding: 10px;border-radius:10px;text-align:center;padding-left:10px")
        
        
        self.bouton_1 = QPushButton("En savoir plus", self)
        self.bouton_1.setGeometry(550, 400, 200, 40)
        self.bouton_1.setStyleSheet("font-size: 15px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;")
        self.bouton_1.setCursor(Qt.CursorShape.PointingHandCursor) #manampy ny cursor ho pointer rehefa mi-hover amin'ny bouton
        
        # fonction clique du bouton
        self.bouton_1.clicked.connect(self.afficher_page_suivante)
        
        self.deconnecter = QPushButton("Déconnecter", self)
        self.deconnecter.setGeometry(1050, 630, 200, 40)
        self.deconnecter.setStyleSheet("font-size: 15px; background-color: #f44336; color: white; border: none; border-radius: 5px;")
        self.deconnecter.setCursor(Qt.CursorShape.PointingHandCursor) #manampy ny cursor ho pointer rehefa mi-hover amin'ny bouton
        
        self.deconnecter.clicked.connect(self.deconnection_page) #manakatona ny fenetre rehefa tsindriana ny bouton deconnecter
        
        
        

        
        
        
        # fonction clique du bouton
    def afficher_page_suivante(self):
        self.hide() #manakatona la fenetre actuelle
        # ouvrir page bienvenue
        self.page_bienvenue = Bienvenue()
        self.page_bienvenue.show() #manokatra la fenetre bienvenue
    
    def deconnection_page(self):
        self.close() #manakatona la fenetre actuelle
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Variable pour garder les références des fenêtres
    login_window = None
    fenetre_principale = None
    bienvenue_window = None
    
    # Afficher d'abord la page de login
    login_window = Login()
    
    # Connecter le signal de succès du login à l'affichage de FenetrePrincipale
    def on_login_success():
        global fenetre_principale
        # Fermer la fenêtre de login
        login_window.close()
        
        # Créer et afficher la fenêtre principale (page d'accueil)
        fenetre_principale = FenetrePrincipale()
        fenetre_principale.show()
    
    login_window.login_success.connect(on_login_success)
    login_window.show()
    
    sys.exit(app.exec())