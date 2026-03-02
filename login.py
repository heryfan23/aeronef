from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

class Login(QWidget):
    login_success = pyqtSignal()  # Signal émis après un login réussi
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - Gestion de Vol Aéronef")
        self.setGeometry(400, 250, 600, 400)
        self.setStyleSheet("background-color: #2d2d69;")
        
        # Titre
        self.titre = QLabel("GESTION DE VOL AÉRONEF", self)
        self.titre.setGeometry(50, 30, 500, 50)
        self.titre.setStyleSheet("font-size: 24px; font-weight: bold; color: white; background-color: none;")
        
        # Sous-titre
        self.sous_titre = QLabel("Panneau d'Administration", self)
        self.sous_titre.setGeometry(50, 80, 500, 30)
        self.sous_titre.setStyleSheet("font-size: 14px; color: #CCCCCC; background-color: none;")
        
        # Separator
        self.hr_1 = QLabel(self)
        self.hr_1.setGeometry(50, 120, 500, 2)
        self.hr_1.setStyleSheet("background-color: white;")
        
        # Label Nom d'utilisateur
        self.username_label = QLabel("Nom d'utilisateur:", self)
        self.username_label.setGeometry(50, 150, 200, 30)
        self.username_label.setStyleSheet("font-size: 14px; color: white; background-color: none;")
        
        # Input Nom d'utilisateur
        self.username_input = QLineEdit(self)
        self.username_input.setGeometry(50, 185, 500, 40)
        self.username_input.setStyleSheet("background-color: white; border: 1px solid #333; border-radius: 5px; padding: 8px; font-size: 14px;")
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        
        # Label Mot de passe
        self.password_label = QLabel("Mot de passe:", self)
        self.password_label.setGeometry(50, 235, 200, 30)
        self.password_label.setStyleSheet("font-size: 14px; color: white; background-color: none;")
        
        # Input Mot de passe
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(50, 270, 500, 40)
        self.password_input.setStyleSheet("background-color: white; border: 1px solid #333; border-radius: 5px; padding: 8px; font-size: 14px;")
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Bouton Connexion
        self.btn_login = QPushButton("Connexion", self)
        self.btn_login.setGeometry(50, 330, 500, 40)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.clicked.connect(self.verify_login)
        
        # Données d'accès administrateur
        self.admin_username = "admin"
        self.admin_password = "admin123"
    
    def verify_login(self):
        """Vérifie les identifiants de login"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        # Validation des champs
        if not username or not password:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle("Erreur")
            msg.setText("Veuillez remplir tous les champs.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            return
        
        # Vérification des identifiants
        if username == self.admin_username and password == self.admin_password:
            # Connexion réussie
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Succès")
            msg.setText(f"Bienvenue {username}! Connexion réussie.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            
            # Émettre le signal de succès
            self.login_success.emit()
            self.close()
        else:
            # Identifiants incorrects
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setWindowTitle("Erreur d'authentification")
            msg.setText("Nom d'utilisateur ou mot de passe incorrect.")
            msg.setStyleSheet("QMessageBox { background-color: #2d2d69; } QMessageBox QLabel { color: white; }")
            msg.exec()
            
            # Réinitialiser les champs
            self.username_input.clear()
            self.password_input.clear()
            self.username_input.setFocus()
    
    def keyPressEvent(self, event):
        """Permet de se connecter en appuyant sur Entrée"""
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            self.verify_login()
        else:
            super().keyPressEvent(event)
