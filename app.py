# github/twiez

import sys
import random
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel)
from PyQt5.QtGui import QPainter, QColor, QLinearGradient, QIcon
from PyQt5.QtCore import Qt, QTimer, QPoint

# KeyAuth API bilgilerinizi buraya girin
OWNER_ID = "your_ownerid"
APP_NAME = "your_appname"
APP_VERSION = "your_version"
APP_SECRET = "your_secret"

def verify_keyauth(username, license_key):
    payload = {
        "type": "login",  # KeyAuth API'sine göre uyarlayın.
        "username": username,
        "key": license_key,
        "hwid": "example_hwid",  # HWID veya ek parametreler eklenebilir.
        "ownerid": OWNER_ID,
        "appname": APP_NAME,
        "version": APP_VERSION,
        "secret": APP_SECRET
    }
    try:
        response = requests.post("https://keyauth.cc/api/1.0/", json=payload)
        if response.status_code == 200:
            data = response.json()
            if data.get("success", False):
                return True, data.get("message", ":)")
            else:
                return False, data.get("message", "Geçersiz lisans anahtarı!")
        else:
            return False, f"HTTP Hatası: {response.status_code}"
    except Exception as e:
        return False, str(e)

# Anim
class Snowflake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.uniform(0.5, 2)
        self.size = random.uniform(1, 4)
        self.opacity = random.uniform(0.3, 0.8)
        
    def update(self, window_height):
        self.y += self.speed
        if self.y > window_height:
            self.y = 0
            self.x = random.randint(0, window_height)
            
    def get_point(self):
        return QPoint(int(self.x), int(self.y))

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KeyAuth Login")
        self.setFixedSize(800, 600)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon('icon.png'))
        self.snowflakes = []
        self.init_ui()
        self.init_animations()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Tit
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 0, 15, 0)

        icon_label = QLabel()
        icon_label.setPixmap(QIcon('icon.png').pixmap(20, 20))
        title_text = QLabel("twiez")
        title_text.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")

        title_bar_layout.addWidget(icon_label)
        title_bar_layout.addWidget(title_text)
        title_bar_layout.addStretch()

        minimize_btn = QPushButton("−")
        close_btn = QPushButton("×")
        for btn, hover_color in [(minimize_btn, "rgba(255, 255, 255, 0.1)"),
                                 (close_btn, "rgba(255, 0, 0, 0.7)")]:
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    color: white;
                    font-family: Arial;
                    font-size: 16px;
                }}
                QPushButton:hover {{
                    background: {hover_color};
                    border-radius: 15px;
                }}
            """)
        minimize_btn.clicked.connect(self.showMinimized)
        close_btn.clicked.connect(self.close)
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.addWidget(minimize_btn)
        controls_layout.addWidget(close_btn)
        title_bar_layout.addLayout(controls_layout)

        # content 
        self.content_widget = QWidget()
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(16)
        content_layout.setContentsMargins(40, 20, 40, 40)

        title_label = QLabel("Twiez Login")
        title_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 42px;
            font-weight: bold;
            color: white;
        """)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setFixedWidth(400)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(138, 43, 226, 0.7);
                background: rgba(255, 255, 255, 0.15);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
        """)

        self.license_key_input = QLineEdit()
        self.license_key_input.setPlaceholderText("Enter your License Key")
        self.license_key_input.setFixedWidth(400)
        self.license_key_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(138, 43, 226, 0.7);
                background: rgba(255, 255, 255, 0.15);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.6);
            }
        """)

        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(400)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #8A2BE2;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #9B30FF;
            }
        """)
        login_btn.clicked.connect(self.login)

        content_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.license_key_input, alignment=Qt.AlignCenter)
        content_layout.addSpacing(20)
        content_layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(title_bar)
        self.main_layout.addWidget(self.content_widget)

    def login(self):
        username = self.username_input.text().strip()
        license_key = self.license_key_input.text().strip()
        if not username or not license_key:
            print("Lütfen tüm alanları doldurun!")
            return
        
        valid, message = verify_keyauth(username, license_key)
        if valid:
            print("Giriş başarılı:", message)
            self.show_success_screen(message)
        else:
            print("Giriş başarısız:", message)

    def show_success_screen(self, message):
        success_widget = QWidget()
        success_layout = QVBoxLayout(success_widget)
        success_layout.setAlignment(Qt.AlignCenter)
        success_layout.setContentsMargins(40, 20, 40, 40)
        
        success_label = QLabel("Giriş başarılı!")
        success_label.setStyleSheet(""")
            font-family: 'Segoe UI', sans-serif;
            font-size: 42px;
            font-weight: bold;
            color: white;
        """)
        
        subtitle_label = QLabel(message)
        subtitle_label.setStyleSheet("""
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            color: white;
        """)
        
        success_layout.addWidget(success_label, alignment=Qt.AlignCenter)
        success_layout.addSpacing(10)
        success_layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)
        
        self.main_layout.replaceWidget(self.content_widget, success_widget)
        self.content_widget.deleteLater()
        self.content_widget = success_widget

    def init_animations(self):
        for _ in range(30):
            x = random.randint(0, self.width())
            y = random.randint(0, self.height())
            self.snowflakes.append(Snowflake(x, y))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_snowflakes)
        self.timer.start(50)

    def update_snowflakes(self):
        for snowflake in self.snowflakes:
            snowflake.update(self.height())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(138, 43, 226))
        gradient.setColorAt(1, QColor(25, 25, 112))
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)
        for snowflake in self.snowflakes:
            painter.setPen(QColor(255, 255, 255, int(255 * snowflake.opacity)))
            painter.setBrush(QColor(255, 255, 255, int(255 * snowflake.opacity)))
            point = snowflake.get_point()
            painter.drawEllipse(point, int(snowflake.size), int(snowflake.size))

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())