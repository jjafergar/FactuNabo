# main.py (dashboard, histórico, config, validaciones, stepper, selector post-envío Macro + login con overlay y estilo unificado + borrar historial + fix login style/center v2 + fix splitter handle v3 + layout Enviar compacto + Font changes + Modern Login UI v2 Frameless + FIX QFont + Logo Tematizado)
# [CORREGIDO] Ahora usa macro_adapter.adapt_from_macro(path) con 1 solo argumento (lee hoja "CLIENTES" interna)
# [MODIFICADO] Dashboard mejorado con consulta dinámica por EMISOR y PERIODO.
import sys
import os
import json
import sqlite3
import webbrowser
import hashlib
import re
import glob
import pandas as pd
from datetime import datetime
import platform
import ctypes

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QTextEdit,
    QProgressBar, QFrame, QToolButton, QLineEdit, QCheckBox, QSplitter,
    QListWidget, QStackedWidget, QDialog, QFormLayout, QMessageBox,
    QListWidgetItem, QHeaderView, QInputDialog, QComboBox, QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect, QStyle # <-- Iconos Sidebar (Aunque ahora no se usa para emojis)
)
from PySide6.QtGui import (
    QPixmap, QFont, QColor, QIcon, QKeySequence, QShortcut, QPalette, QScreen # Necesario para QScreen, QDesktopServices
)

from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import (
QEasingCurve, QPoint, QPropertyAnimation, QRect, QSettings, QSize, QThread, QTimer, QUrl, Qt
)

from worker import Worker
import macro_adapter

# --- Resource path helper for PyInstaller ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, relative_path)


# --- Helpers ---
def _normalize_invoice_id(x):
    s = str(x).strip()
    # Si es numérico (incluye "25042.0"), devolvemos entero sin .0
    if re.fullmatch(r"\d+(?:\.0+)?", s):
        try:
            return str(int(float(s)))
        except Exception:
            return s
    # Si es alfanumérico (p.ej. "Int_25003"), devolvemos tal cual
    return s


# Formato monetario (es-ES): 3.976,42€
def format_eur(value) -> str:
    try:
        v = float(value)
    except Exception:
        return ""
    s = f"{v:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s}€"

# [NUEVO] Helper para aplicar sombras
def apply_shadow(widget, blur=20, offset_y=4, color_str="#000000"):
    """Aplica un efecto de sombra sutil y moderno."""
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    # Sombra muy suave (alfa bajo)
    color = QColor(color_str)
    color.setAlpha(40)
    shadow.setColor(color)
    shadow.setOffset(0, offset_y)
    widget.setGraphicsEffect(shadow)


# [NUEVO] Windows Acrylic/Mica (blur/transparencia real)
def enable_windows_backdrop(win_id, dark_mode: bool = False):
    """
    Intenta activar Mica/Acrylic/Immersive Dark Mode en Windows 10/11.
    Silencioso si falla o no aplica.
    """
    try:
        if platform.system().lower() != "windows":
            return
        hwnd = int(win_id)
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20  # BOOL
        DWMWA_MICA_EFFECT = 1029            # BOOL (Windows 11 antiguas)
        DWMWA_SYSTEMBACKDROP_TYPE = 38      # DWORD (Windows 11 22H2+)
        # 0=Auto, 1=None, 2=Mica, 3=Acrylic (algunas builds), 4=Tabbed
        backdrop_mica = ctypes.c_int(2)
        # backdrop_acrylic = ctypes.c_int(3)
        dark = ctypes.c_int(1 if dark_mode else 0)
        dwmapi = ctypes.windll.dwmapi
        # Dark chrome
        dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(dark), ctypes.sizeof(dark))
        # System backdrop (prefer Mica)
        dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(backdrop_mica), ctypes.sizeof(backdrop_mica))
        # Fallback for older Windows 11
        mica_on = ctypes.c_int(1)
        dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_MICA_EFFECT, ctypes.byref(mica_on), ctypes.sizeof(mica_on))
        # If you prefer Acrylic, uncomment:
        # dwmapi.DwmSetWindowAttribute(hwnd, DWMWA_SYSTEMBACKDROP_TYPE, ctypes.byref(backdrop_acrylic), ctypes.sizeof(backdrop_acrylic))
    except Exception:
        pass

# --- Colores/Recursos ---
COLOR_PRIMARY = "#A0BF6E"
COLOR_SUCCESS = "#34C759"
COLOR_WARNING = "#FF9500"
COLOR_ERROR = "#FF3B30"
COLOR_BACKGROUND = "#F2F2F7"
COLOR_CARD = "#FFFFFF"
COLOR_TEXT = "#000000"
COLOR_SECONDARY_TEXT = "#8E8E93"
COLOR_BORDER = "#C6C6C8"
COLOR_SIDEBAR = "#FAFAFA"
COLOR_SIDEBAR_DARK = "#1C1C1E"
COLOR_DARK_BG = "#000000"
COLOR_DARK_CARD = "#1C1C1E"
COLOR_DARK_TEXT = "#FFFFFF"
COLOR_DARK_BORDER = "#38383A"

RESOURCE_DIR = resource_path("resources")
DB_PATH = resource_path("factunabo_history.db")
USERS_PATH = resource_path("users.json")


# --- DB ---
# [MODIFICADO] init_database para añadir la columna 'importe'
def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_envio TEXT NOT NULL,
            num_factura TEXT,
            empresa TEXT,
            estado TEXT,
            detalles TEXT,
            pdf_url TEXT,
            excel_path TEXT,
            importe REAL DEFAULT 0.0,
            cliente TEXT
        )
        """
    )
    # --- [NUEVO] Añadir columna 'importe' si la tabla ya existe ---
    try:
        cursor.execute("ALTER TABLE envios ADD COLUMN importe REAL DEFAULT 0.0")
    except sqlite3.OperationalError:
        pass
    # --- [FIN NUEVO] ---
    # --- [NUEVO] Añadir columna 'cliente' si la tabla ya existe ---
    try:
        cursor.execute("ALTER TABLE envios ADD COLUMN cliente TEXT")
    except sqlite3.OperationalError:
        pass
    # --- [FIN NUEVO] ---
    conn.commit()
    conn.close()


# --- Componentes UI ---

# [TOTALMENTE CORREGIDO] AnimatedButton refactorizada para evitar conflictos de eventos
class AnimatedButton(QPushButton):
    """Botón con animación de "elevación" (sombra) al estilo macOS."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "AnimatedButton")

        # Sombra base
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(18)
        color = QColor(0, 0, 0, 60) # Usamos un color de sombra fijo y seguro
        self._shadow.setColor(color)
        self._shadow.setOffset(0, 4)
        self.setGraphicsEffect(self._shadow)

        # Animación para el radio de la sombra (blur)
        self._anim_blur = QPropertyAnimation(self._shadow, b"blurRadius")
        self._anim_blur.setDuration(180)
        self._anim_blur.setEasingCurve(QEasingCurve.OutCubic)

        # Animación para el offset (Y)
        self._anim_offset = QPropertyAnimation(self._shadow, b"yOffset")
        self._anim_offset.setDuration(180)
        self._anim_offset.setEasingCurve(QEasingCurve.OutCubic)

    # --- [NUEVAS FUNCIONES HELPER] ---
    def _animate_hover_in(self):
        """Animates the button shadow to the 'hover' state."""
        self._anim_blur.stop()
        self._anim_blur.setStartValue(self._shadow.blurRadius())
        self._anim_blur.setEndValue(30)
        self._anim_blur.start()

        self._anim_offset.stop()
        self._anim_offset.setStartValue(self._shadow.yOffset())
        self._anim_offset.setEndValue(6) # Sube un poco
        self._anim_offset.start()

    def _animate_hover_out(self):
        """Animates the button shadow to the 'normal' state."""
        self._anim_blur.stop()
        self._anim_blur.setStartValue(self._shadow.blurRadius())
        self._anim_blur.setEndValue(18)
        self._anim_blur.start()

        self._anim_offset.stop()
        self._anim_offset.setStartValue(self._shadow.yOffset())
        self._anim_offset.setEndValue(4)
        self._anim_offset.start()
    # --- [FIN DE FUNCIONES HELPER] ---

    def enterEvent(self, e):
        # Al pasar el ratón, la sombra se expande y "sube"
        self._animate_hover_in()
        super().enterEvent(e)

    def leaveEvent(self, e):
        # Vuelve al estado normal
        self._animate_hover_out()
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        # Al presionar, la sombra se contrae (efecto "click")
        self._anim_blur.stop()
        self._anim_blur.setStartValue(self._shadow.blurRadius())
        self._anim_blur.setEndValue(10)
        self._anim_blur.start()

        self._anim_offset.stop()
        self._anim_offset.setStartValue(self._shadow.yOffset())
        self._anim_offset.setEndValue(2)
        self._anim_offset.start()

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        # Al soltar, vuelve al estado hover/normal
        super().mouseReleaseEvent(e) # Llama al padre primero

        # [CORRECCIÓN 1: DeprecationWarning]
        # e.pos() está obsoleto, usamos e.position().toPoint()
        current_pos = e.position().toPoint()

        # [CORRECCIÓN 2: TypeError]
        # No llames a enterEvent/leaveEvent. Llama a las funciones de animación.
        if self.rect().contains(current_pos):
            self._animate_hover_in() # El ratón sigue encima
        else:
            self._animate_hover_out() # El ratón se soltó fuera


class StatusChip(QLabel):
    def __init__(self, status, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "StatusChip")
        up = (status or "").upper()
        if up in ["ÉXITO", "SUCCESS"]:
            self.setProperty("status", "success")
        elif up in ["DUPLICADO", "DUPLICATE", "ATENCION"]:
            self.setProperty("status", "warning")
        else:
            self.setProperty("status", "NABO!") # O "error" si prefieres
        self.setText(up)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(26)


class ModernTable(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "ModernTable")
        self.setAlternatingRowColors(True)
        self.setMouseTracking(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)


# --- Stepper ---
# [MODIFICADO] StepperWidget ahora anima la línea de progreso
class StepperWidget(QWidget):
    def __init__(self, steps, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current_step = 0
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(0)
        self.step_labels = []
        self.step_circles = []
        self.step_lines = []
        self.line_anims = [] # [NUEVO]

        for i, step_name in enumerate(self.steps):
            circle = QLabel()
            circle.setFixedSize(40, 40)
            circle.setAlignment(Qt.AlignCenter)
            circle.setProperty("class", "StepCircle")
            circle.setProperty("state", "pending")
            circle.setText(str(i + 1))
            self.step_circles.append(circle)

            label = QLabel(step_name)
            label.setAlignment(Qt.AlignCenter)
            label.setProperty("class", "StepLabel")
            self.step_labels.append(label)

            step_container = QVBoxLayout()
            step_container.addWidget(circle, alignment=Qt.AlignCenter)
            step_container.addWidget(label)
            layout.addLayout(step_container)

            if i < len(self.steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setProperty("class", "StepLine")
                line.setProperty("state", "pending")
                line.setFixedHeight(2)
                line.setMinimumWidth(60)

                # [NUEVO] Preparar animación
                line.setMaximumWidth(0) # Empieza oculto
                anim = QPropertyAnimation(line, b"maximumWidth")
                anim.setDuration(400)
                anim.setEasingCurve(QEasingCurve.OutCubic)
                self.line_anims.append(anim)

                self.step_lines.append(line)
                layout.addWidget(line, alignment=Qt.AlignVCenter)

        self.set_step(0) # Inicializa el estado visual

    def set_step(self, step_index):
        self.current_step = step_index
        for i, circle in enumerate(self.step_circles):
            if i < step_index:
                circle.setProperty("state", "completed")
                circle.setText("✓")
            elif i == step_index:
                circle.setProperty("state", "active")
                circle.setText(str(i + 1))
            else:
                circle.setProperty("state", "pending")
                circle.setText(str(i + 1))
            circle.style().unpolish(circle)
            circle.style().polish(circle)

        for i, line in enumerate(self.step_lines):
            is_completed = (i < step_index)
            line.setProperty("state", "completed" if is_completed else "pending")
            line.style().unpolish(line)
            line.style().polish(line)

            # [NUEVO] Animar la línea
            anim = self.line_anims[i]
            anim.stop() # Detiene animación anterior si la hay

            target_width = line.minimumWidth() if is_completed else 0
            current_width = line.width()

            if current_width != target_width:
                anim.setStartValue(current_width)
                anim.setEndValue(target_width)
                anim.start()


# --- Login con overlay (estilo integrado) ---
class Overlay(QWidget):
    """Capa que oscurece la ventana y bloquea clicks mientras el login está visible."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_NoSystemBackground, False)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)  # Captura eventos
        self.setStyleSheet("background-color: rgba(0,0,0,0.35);")
        self.hide()

    def resizeEvent(self, e):
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().resizeEvent(e)


class LoginDialog(QDialog):
    """Login con el mismo look (usa styles.qss) y sin cerrar la app en fallo."""

    def __init__(self, parent=None):
        super().__init__(parent)

        # --- [MODIFICACIÓN FRAMELESS] ---
        # Ocultar la barra de título y activar fondo transparente
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # --- [FIN MODIFICACIÓN] ---

        self.setWindowTitle("Acceso a FactuNabo") # Aunque no se vea, es bueno mantenerlo
        self.setModal(True)
        self.setMinimumWidth(400) # <-- Ancho reducido
        self.settings = QSettings("FactuNabo", "Login")
        self._ensure_users_file()
        self._init_ui()

    def _ensure_users_file(self):
        if not os.path.exists(USERS_PATH):
            default = {
                "users": [
                    {
                        "username": "admin",
                        "password_hash": hashlib.sha256("admin".encode("utf-8")).hexdigest(),
                    }
                ]
            }
            with open(USERS_PATH, "w", encoding="utf-8") as f:
                json.dump(default, f, indent=2, ensure_ascii=False)

    def _load_users(self):
        try:
            with open(USERS_PATH, "r", encoding="utf-8") as f:
                return json.load(f).get("users", [])
        except Exception:
            return []

    # [MODIFICADO] _init_ui para un look más moderno
    def _init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("LoginCard") # <-- ID para el QSS
        apply_shadow(card, blur=30, offset_y=5) # Sombra

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28) # Más padding
        card_layout.setSpacing(15) # Un poco más de espacio

        title = QLabel("FactuNabo – Inicio de sesión")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 700;")
        card_layout.addWidget(title)

        subtitle = QLabel("Introduce tus credenciales para continuar")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color:#8E8E93;")
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(10) # Espacio antes de los inputs

        # --- [MODIFICACIÓN] Quitar QFormLayout por un QVBoxLayout ---
        input_layout = QVBoxLayout()
        input_layout.setSpacing(10) # Espacio entre inputs

        self.username = QLineEdit()
        self.username.setPlaceholderText("Usuario")
        self.username.returnPressed.connect(lambda: (self.password.setFocus(), self.password.selectAll()))
        input_layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.do_login)
        input_layout.addWidget(self.password)

        card_layout.addLayout(input_layout)
        # --- [FIN MODIFICACIÓN] ---

        self.remember = QCheckBox("Recordarme")
        card_layout.addWidget(self.remember)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color:#FF3B30; font-weight:600;")
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        last_user = self.settings.value("last_user", "")
        if last_user:
            self.username.setText(last_user)
            self.remember.setChecked(True)
            QTimer.singleShot(0, self.password.setFocus)

        card_layout.addSpacing(10) # Espacio antes de los botones

        # --- [MODIFICACIÓN] Botones apilados, "Entrar" al 100% ---
        btns_layout = QVBoxLayout()
        btns_layout.setSpacing(8)

        btn_login = AnimatedButton("Entrar")
        btn_login.clicked.connect(self.do_login)
        btns_layout.addWidget(btn_login)

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject) # self.reject() cierra el diálogo
        # Hacemos que el botón "Cancelar" parezca un enlace
        btn_cancel.setProperty("class", "LinkButton")
        btns_layout.addWidget(btn_cancel, alignment=Qt.AlignCenter)

        card_layout.addLayout(btns_layout)
        # --- [FIN MODIFICACIÓN] ---

        root.addStretch()
        root.addWidget(card, alignment=Qt.AlignCenter)
        root.addStretch()


    def do_login(self):
        u = (self.username.text() or "").strip()
        p = self.password.text() or ""
        if not u or not p:
            self._show_error("Indica usuario y contraseña.")
            return
        users = self._load_users()
        ok = any(
            (u == item.get("username") and hashlib.sha256(p.encode("utf-8")).hexdigest() == item.get("password_hash"))
            for item in users
        )
        if not ok:
            self._show_error("Usuario o contraseña incorrectos.")
            self.password.clear()
            self.password.setFocus()
            return
        if self.remember.isChecked():
            self.settings.setValue("last_user", u)
        else:
            self.settings.remove("last_user")
        os.environ["FACTUNABO_USER"] = u
        self.accept()

    def _show_error(self, msg: str):
        self.error_label.setText(msg)
        self.error_label.setVisible(True)


# --- Config API Dialog ---
# [MODIFICADO] ConfigDialog ahora es Frameless y centrado
class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # --- 1. Añadir Banderas Frameless ---
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.setMinimumWidth(500)
        self.settings = QSettings("FactuNabo", "APIConfig")
        self.init_ui()
        self.load_settings()

    # --- 2. Reestructurar UI para que sea una "tarjeta" ---
    def init_ui(self):
        # Layout raíz transparente
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        # Tarjeta contenedora (usamos "LoginCard" para reusar el estilo QSS)
        card = QFrame()
        card.setObjectName("LoginCard") 
        apply_shadow(card, blur=25, offset_y=4) 

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(28, 28, 28, 28) # Padding
        card_layout.setSpacing(15) # Espaciado

        # Título
        title = QLabel("Configuración de API")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 700;")
        card_layout.addWidget(title)
        card_layout.addSpacing(10)

        # Formulario
        form = QFormLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://api.example.com")
        form.addRow("URL de API:", self.url_input)
        self.token_input = QLineEdit()
        self.token_input.setEchoMode(QLineEdit.Password)
        self.token_input.setPlaceholderText("Token de autenticación")
        form.addRow("Token:", self.token_input)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        form.addRow("Usuario:", self.user_input)
        self.timeout_input = QLineEdit()
        self.timeout_input.setPlaceholderText("30")
        self.timeout_input.setText("30")
        form.addRow("Timeout (seg):", self.timeout_input)
        card_layout.addLayout(form)
        
        card_layout.addSpacing(10) # Espacio antes de botones

        # Botones
        btn_layout = QHBoxLayout()
        btn_save = AnimatedButton("Guardar") # Botón primario animado
        btn_save.clicked.connect(self.save_settings)
        btn_cancel = QPushButton("Cancelar") # Botón secundario normal
        btn_cancel.clicked.connect(self.reject)
        
        # Hacemos que "Cancelar" se vea como un link (opcional, pero consistente)
        btn_cancel.setProperty("class", "LinkButton")
        
        btn_layout.addStretch()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)
        card_layout.addLayout(btn_layout)

        # Centrar la tarjeta en el layout raíz
        root.addStretch()
        root.addWidget(card, alignment=Qt.AlignCenter)
        root.addStretch()

    def load_settings(self):
        self.url_input.setText(self.settings.value("api_url", ""))
        self.token_input.setText(self.settings.value("api_token", ""))
        self.user_input.setText(self.settings.value("api_user", ""))
        self.timeout_input.setText(self.settings.value("api_timeout", "30"))

    def save_settings(self):
        self.settings.setValue("api_url", self.url_input.text())
        self.settings.setValue("api_token", self.token_input.text())
        self.settings.setValue("api_user", self.user_input.text())
        self.settings.setValue("api_timeout", self.timeout_input.text())
        self.accept()


# --- Ventana Principal ---
class MainWindow(QMainWindow):

    # --- PDF helpers (abrir local o URL) + botón con icono SVG ---
    def _open_invoice_pdf(self, invoice_id: str, fallback_url: str = ""):
        """Intenta abrir el PDF guardado (según nº de factura). Si no lo encuentra, abre la URL."""
        try:
            # Directorio configurado en la UI (si existe ese campo)
            dest = getattr(self, "txt_pdf_dest", None).text() if hasattr(self, "txt_pdf_dest") else ""
            if dest and os.path.isdir(dest):
                # Patrones habituales: "Nº - Cliente - Importe.pdf" u otros
                patterns = [
                    f"{invoice_id} - *.pdf",
                    f"{invoice_id}-*.pdf",
                    f"{invoice_id}*.pdf",
                ]
                matches = []
                for pat in patterns:
                    matches.extend(glob.glob(os.path.join(dest, pat)))
                matches = [p for p in matches if os.path.getsize(p) > 0]
                if matches:
                    best = max(matches, key=os.path.getmtime)
                    QDesktopServices.openUrl(QUrl.fromLocalFile(best))
                    return
            # Fallback a la URL si no hay PDF local
            if fallback_url:
                webbrowser.open(fallback_url)
            else:
                if hasattr(self, "show_toast"):
                    self.show_toast("⚠️ No se encontró el PDF guardado ni hay URL disponible.")
        except Exception as e:
            if hasattr(self, "show_error"):
                self.show_error(f"No se pudo abrir el PDF: {e}")

    def _make_pdf_button(self, invoice_id: str, pdf_url: str, svg_path: str = None):
        btn = QToolButton()
        btn.setToolTip("Abrir PDF")
        btn.setMinimumHeight(28)
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(lambda checked=False, _id=invoice_id, _url=pdf_url: self._open_invoice_pdf(_id, _url))

        # Intentar cargar icono SVG
        icon = None
        try:
            if svg_path and os.path.exists(svg_path):
                icon = QIcon(svg_path)
            else:
                default_svg = os.path.join(RESOURCE_DIR, "ver.pdf.svg")
                if os.path.exists(default_svg):
                    icon = QIcon(default_svg)
        except Exception:
            icon = None

        if icon and not icon.isNull():
            btn.setIcon(icon)
            btn.setIconSize(QSize(20, 20))
            btn.setToolButtonStyle(Qt.ToolButtonIconOnly)
            btn.setText("")
        else:
            btn.setText("Ver")  # fallback textual

        return btn

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground) # Habilitar fondo translúcido
        self.setWindowTitle("FactuNabo")
        self.setMinimumSize(1200, 700)
        self.showMaximized() # <-- ABRIR MAXIMIZADO
        self.theme = "light"
        self.setProperty("theme", self.theme)
        self.loaded_invoice_count = 0  # KPI: facturas cargadas
        # Activar backdrop del sistema (Windows 11): Mica/Acrylic
        try:
            enable_windows_backdrop(self.winId(), dark_mode=(self.theme == "dark"))
        except Exception:
            pass

        icon_path = os.path.join(RESOURCE_DIR, "logo.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        init_database()

        # Carga de estilos
        style_sheet_content = self._get_themed_stylesheet()
        if style_sheet_content:
            # Aplicar a toda la app para herencia consistente (dialogs incluidos)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(style_sheet_content)
            # Asegurar también en la ventana por si el QApplication no existiera aún
            self.setStyleSheet(style_sheet_content)

        # El worker y el thread se crearán bajo demanda en send_facturas
        self.worker = None
        self.thread = None

        self.sending_in_progress = False
        self.current_excel_path = None
        # --- [NUEVO] Atributos para almacenar los dataframes históricos ---
        self.df_factura_historico = None
        self.df_conceptos_historico = None
        # --- [FIN NUEVO] ---
        self.validation_errors = []
        self.post_action_mode = "MARK"
        self._overlay = Overlay(self)

        # --- [MODIFICADO] Referencias del Dashboard ---
        self.total_label = None
        self.success_label = None
        self.month_total_label = None
        self.month_count_label = None
        
        # --- [NUEVO] Referencias a las nuevas tablas y widgets de consulta ---
        self.table_last_errors = None
        self.dash_combo_empresas = None
        self.dash_combo_periodo = None
        self.dash_btn_consultar = None
        self.dash_label_resultado = None
        self.dash_table_resultados = None
        # --- [FIN NUEVO] ---
        
        # --- [NUEVO] Referencia al logo ---
        self.logo_label = None
        # --- [FIN NUEVO] ---

        self.init_ui()

        self.shortcut_open = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut_open.activated.connect(self.select_excel)

        self.toast_timer = QTimer(self)
        self.toast_timer.timeout.connect(self.hide_toast)

        # Hilo temporal para descarga manual de PDFs
        self.dthread = None
        self.dworker = None

    def _get_themed_stylesheet(self):
        """Reads the QSS file and replaces placeholders with resource paths."""
        qss_path = resource_path("styles.qss")
        if not os.path.exists(qss_path):
            return ""

        with open(qss_path, "r", encoding="utf-8") as f:
            qss = f.read()

        # Replace placeholders with actual paths
        logo_light_path = resource_path(os.path.join("resources", "logo_light.png")).replace("\\", "/")
        logo_dark_path = resource_path(os.path.join("resources", "logo_dark.png")).replace("\\", "/")

        qss = qss.replace("%%LOGO_LIGHT%%", logo_light_path)
        qss = qss.replace("%%LOGO_DARK%%", logo_dark_path)

        return qss

    # ----- Login gating -----
    # [REVISADO] require_login con centrado y estilo más robustos
    def require_login(self):
        self._overlay.setGeometry(self.rect())
        self._overlay.show()
        dlg = LoginDialog(self)

        # --- [MODIFICADO: Aplicar estilo directamente] ---
        # Cargar el QSS general y aplicarlo al diálogo
        style_sheet_content = self._get_themed_stylesheet()
        if style_sheet_content:
            dlg.setStyleSheet(style_sheet_content)
            dlg.setProperty("theme", self.theme)

        # Forzar un repintado inicial del diálogo
        dlg.style().unpolish(dlg)
        dlg.style().polish(dlg)
        dlg.adjustSize() # Asegura que el tamaño se calcule con el nuevo estilo
        # --- [FIN MODIFICADO] ---

        # --- [Centrado respecto a la pantalla] ---
        screen = QApplication.primaryScreen()
        if screen: # Asegurarse de que tenemos una pantalla
            screen_geometry = screen.availableGeometry()
            # Usamos geometry() DESPUÉS de adjustSize() para obtener el tamaño correcto
            dlg_geometry = dlg.geometry()
            center_point = screen_geometry.center() - QPoint(dlg_geometry.width() // 2, dlg_geometry.height() // 2)
            dlg.move(center_point)
        # --- [FIN CENTRADO] ---

        res = dlg.exec()
        if res == QDialog.Accepted:
            self._overlay.hide()
            return True
        else:
            QTimer.singleShot(0, self.close)
            return False


    # ----- UI -----
    def init_ui(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(0) # <-- ASEGURADO que sea 0

        # --- [AÑADIDO ESTILO DIRECTO AL SPLITTER] ---
        # Forzar estilo invisible directamente en el splitter para eliminar la línea
        splitter.setStyleSheet("QSplitter::handle { background-color: transparent; border: none; width: 0px; image: none; }")
        # --- [FIN AÑADIDO] ---

        # Sidebar
        sidebar = QWidget()
        sidebar.setProperty("class", "Sidebar")
        sidebar.setFixedWidth(270)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 20, 15, 20)
        sidebar_layout.setSpacing(10)

        logo_container = QHBoxLayout()
        
        # --- [MODIFICADO PARA LOGO TEMATIZADO] ---
        # Ya no cargamos QPixmap aquí, solo creamos el QLabel con un ID
        self.logo_label = QLabel() 
        self.logo_label.setObjectName("SidebarLogo") # ID para el QSS
        self.logo_label.setMinimumSize(100, 100) # Darle un tamaño fijo
        self.logo_label.setScaledContents(False) # Dejamos que QSS controle (con 'image:')
        self.logo_label.setAlignment(Qt.AlignCenter) 
        logo_container.addWidget(self.logo_label)
        # --- [FIN MODIFICACIÓN] ---
        
        title = QLabel("FactuNabo")
        title.setObjectName("sidebarTitle")
        logo_container.addWidget(title)
        logo_container.addStretch()
        sidebar_layout.addLayout(logo_container)

        sidebar_layout.addSpacing(20)

        self.nav_list = QListWidget()
        self.nav_list.setProperty("class", "NavList")

        # --- [Revertido a Emojis] ---
        menu_items = [
            ("📊 Dashboard", 0),
            ("📁 Cargar Excel", 1),
            ("🚀 Enviar Facturas", 2), # <-- El cohete
            ("📜 Histórico", 3),
            ("⚙️ Configuración", 4),
        ]

        for text, index in menu_items:
            item = QListWidgetItem(text) # Item solo con texto (incluye emoji)
            item.setData(Qt.UserRole, index)
            self.nav_list.addItem(item)
        # --- [Fin Revertido a Emojis] ---

        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.change_page)
        sidebar_layout.addWidget(self.nav_list)

        sidebar_layout.addStretch()

        self.dark_toggle = QCheckBox("Modo Oscuro")
        self.dark_toggle.toggled.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.dark_toggle)

        splitter.addWidget(sidebar)

        # Content
        self.content_stack = QStackedWidget()
        self.content_stack.setProperty("class", "ContentStack")

        self.dashboard_page = self.create_dashboard_page()
        self.content_stack.addWidget(self.dashboard_page)

        self.excel_page = self.create_excel_page()
        self.content_stack.addWidget(self.excel_page)

        self.send_page = self.create_send_page()
        self.content_stack.addWidget(self.send_page)

        self.history_page = self.create_history_page()
        self.content_stack.addWidget(self.history_page)

        self.config_page = self.create_config_page()
        self.content_stack.addWidget(self.config_page)

        splitter.addWidget(self.content_stack)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

        # Toast
        self.toast = QLabel(self)
        self.toast.setObjectName("toast")
        self.toast.setAlignment(Qt.AlignCenter)
        self.toast.hide()
        self.toast_anim = QPropertyAnimation(self.toast, b"geometry")
        self.toast_anim.setEasingCurve(QEasingCurve.OutCubic)

    # [MODIFICADO] create_dashboard_page ahora es mucho más completo
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20) # Reducimos el espaciado

        # --- TÍTULO ---
        header = QLabel("DASHBOARD")
        header.setFont(QFont(QApplication.font().family(), 28, QFont.Bold)) 
        header.setStyleSheet("margin-bottom: 5px;")
        layout.addWidget(header)

        # --- Subtítulo de Estadísticas ---
        stats_title = QLabel("Estadísticas Clave")
        stats_title.setFont(QFont(QApplication.font().family(), 18, QFont.Bold))
        layout.addWidget(stats_title)

        stats_layout = QHBoxLayout()
        # Las tarjetas se crean aquí, y guardan la referencia en self.X_label
        total_card = self.create_stat_card("Total Enviados", "0", COLOR_SECONDARY_TEXT)
        stats_layout.addWidget(total_card)
        success_card = self.create_stat_card("Éxitos (Total)", "0", COLOR_SECONDARY_TEXT)
        stats_layout.addWidget(success_card)
        # --- TARJETAS MENSUALES ---
        month_total_card = self.create_stat_card("Facturado (Mes)", "0,00€", COLOR_PRIMARY)
        stats_layout.addWidget(month_total_card)
        month_count_card = self.create_stat_card("Envíos (Mes)", "0", COLOR_SUCCESS)
        stats_layout.addWidget(month_count_card)
        # --- FIN TARJETAS MENSUALES ---
        layout.addLayout(stats_layout)

        layout.addSpacing(15)

        # --- [NUEVO] Sección de Paneles de Consulta ---
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)

        # --- Panel 1: Consulta por Emisor ---
        consulta_card = QFrame()
        consulta_card.setProperty("class", "ConfigGroup") # Reusamos el estilo de "tarjeta"
        apply_shadow(consulta_card, blur=20, offset_y=3)
        consulta_layout = QVBoxLayout(consulta_card)
        
        consulta_title = QLabel("Consulta por Emisor")
        consulta_title.setFont(QFont(QApplication.font().family(), 16, QFont.Bold))
        consulta_layout.addWidget(consulta_title)
        
        # Formulario de consulta
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        self.dash_combo_empresas = QComboBox()
        self.dash_combo_periodo = QComboBox()
        self.dash_combo_periodo.addItems([
            "1º Trimestre",
            "2º Trimestre",
            "3º Trimestre",
            "4º Trimestre",
            "Ejercicio Actual",
            "Total Histórico"
        ])
        form_layout.addRow("Empresa Emisora:", self.dash_combo_empresas)
        form_layout.addRow("Periodo:", self.dash_combo_periodo)
        consulta_layout.addLayout(form_layout)

        # Botón de consulta
        self.dash_btn_consultar = AnimatedButton("🔍 Consultar")
        self.dash_btn_consultar.clicked.connect(self.run_dashboard_query)
        consulta_layout.addWidget(self.dash_btn_consultar)

        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setProperty("class", "SeparatorLine")
        consulta_layout.addWidget(line)

        # --- [NUEVO] Barra de búsqueda ---
        self.dash_search_bar = QLineEdit()
        self.dash_search_bar.setPlaceholderText("Buscar en resultados...")
        self.dash_search_bar.textChanged.connect(self.filter_dashboard_table)
        consulta_layout.addWidget(self.dash_search_bar)

        # Resultados de consulta
        self.dash_label_resultado = QLabel("Selecciona filtros y pulsa 'Consultar'")
        self.dash_label_resultado.setObjectName("excelSummary") # Reusamos estilo
        self.dash_label_resultado.setAlignment(Qt.AlignCenter)
        consulta_layout.addWidget(self.dash_label_resultado)

        self.dash_table_resultados = ModernTable(0, 6)
        self.dash_table_resultados.setHorizontalHeaderLabels(["Fecha", "Factura", "Cliente", "Empresa Emisora", "Importe", "Ver Factura"])
        hdr_res = self.dash_table_resultados.horizontalHeader()
        hdr_res.setSectionResizeMode(0, QHeaderView.ResizeToContents) # Fecha
        hdr_res.setSectionResizeMode(1, QHeaderView.Stretch) # Factura
        hdr_res.setSectionResizeMode(2, QHeaderView.Stretch) # Cliente
        hdr_res.setSectionResizeMode(3, QHeaderView.Stretch) # Empresa Emisora
        hdr_res.setSectionResizeMode(4, QHeaderView.ResizeToContents) # Importe
        hdr_res.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Ver Factura
        consulta_layout.addWidget(self.dash_table_resultados, 1)

        panels_layout.addWidget(consulta_card, 1) # '1' para que ocupe más espacio

        layout.addLayout(panels_layout, 1) # El '1' hace que se expanda verticalmente

        layout.addSpacing(15)
        # --- [FIN NUEVA SECCIÓN] ---

        actions_label = QLabel("Acciones Rápidas")
        actions_label.setFont(QFont(QApplication.font().family(), 18, QFont.Bold)) # Usa fuente global
        layout.addWidget(actions_label)
        actions_layout = QHBoxLayout()
        btn_load = AnimatedButton("📁 Cargar Excel")
        btn_load.clicked.connect(lambda: self.nav_list.setCurrentRow(1))
        actions_layout.addWidget(btn_load)
        btn_send = AnimatedButton("🚀 Enviar Facturas")
        btn_send.clicked.connect(lambda: self.nav_list.setCurrentRow(2))
        actions_layout.addWidget(btn_send)
        btn_history = AnimatedButton("📜 Ver Histórico")
        btn_history.clicked.connect(lambda: self.nav_list.setCurrentRow(3))
        actions_layout.addWidget(btn_history)
        layout.addLayout(actions_layout)
        
        layout.addStretch(0) # Modificado a 0
        
        # Cargar datos iniciales
        QTimer.singleShot(100, self.update_dashboard_stats)
        QTimer.singleShot(150, self.populate_dashboard_filters) # Cargar filtros después
        return page

    # [MODIFICADO] create_stat_card para asignar nuevas referencias
    def create_stat_card(self, title, value, color):
        card = QFrame()
        card.setProperty("class", "StatCard")
        card_layout = QVBoxLayout(card)
        value_label = QLabel(value)
        # Usamos la fuente global pero ajustamos tamaño/peso
        value_label.setFont(QFont(QApplication.font().family(), 36, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLOR_SECONDARY_TEXT};") # Mantiene estilo secundario
        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        # Guardamos la referencia a la etiqueta del valor
        if "Total Enviados" in title:
            self.total_label = value_label
        elif "Éxitos" in title or "Éxitos (Total)" in title:
            self.success_label = value_label
        elif "Facturado (Mes)" in title:  # <-- [NUEVO]
            self.month_total_label = value_label
        elif "Envíos (Mes)" in title: # <-- [NUEVO]
            self.month_count_label = value_label

        apply_shadow(card, blur=25, offset_y=5)

        return card

    def create_excel_page(self):
        page = QWidget()
        page.setAcceptDrops(True)
        page.dragEnterEvent = self.dragEnterEvent
        page.dropEvent = self.dropEvent
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        header = QLabel("CARGAR ARCHIVO EXCEL")
        header.setFont(QFont(QApplication.font().family(), 32, QFont.Bold)) # Usa fuente global
        layout.addWidget(header)
        self.stepper = StepperWidget(["Cargar", "Validar", "Listo"])
        layout.addWidget(self.stepper)
        self.btn_select_excel = AnimatedButton("📁 Seleccionar Excel")
        # self.btn_select_excel.setMinimumHeight(50) # Eliminado
        self.btn_select_excel.clicked.connect(self.select_excel)
        layout.addWidget(self.btn_select_excel)

        # --- Botón de limpieza manual ---
        btn_clear = AnimatedButton("🧹 Limpiar")
        btn_clear.clicked.connect(self.clear_excel_table)
        layout.addWidget(btn_clear)

        hint = QLabel("o arrastra el archivo aquí")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"color: {COLOR_SECONDARY_TEXT};")
        layout.addWidget(hint)
        self.validation_label = QLabel("")
        self.validation_label.setWordWrap(True)
        layout.addWidget(self.validation_label)
        # KPI contador + total base
        self.loaded_summary = QLabel("")
        self.loaded_summary.setObjectName("excelSummary")
        self.loaded_summary.setVisible(False)
        layout.addWidget(self.loaded_summary)

        # Contenedor redondeado para la tabla de carga de Excel
        excel_card = QFrame()
        excel_card.setProperty("class", "TableCard")
        apply_shadow(excel_card, blur=20, offset_y=3)
        excel_layout = QVBoxLayout(excel_card)
        excel_layout.setContentsMargins(0, 0, 0, 0)
        excel_layout.setSpacing(0)

        self.table_excel = ModernTable(0, 8)
        self.table_excel.setHorizontalHeaderLabels([
            "Factura", "Empresa Emisora", "Cliente", "Base Imponible",
            "Cantidad IVA", "Retención", "Importe Total", "Fecha"
        ])

        # --- Ajuste de columnas ---
        hdr = self.table_excel.horizontalHeader()
        hdr.setSectionResizeMode(0, QHeaderView.ResizeToContents)    # Factura
        hdr.setSectionResizeMode(1, QHeaderView.Stretch)            # Empresa Emisora
        hdr.setSectionResizeMode(2, QHeaderView.Stretch)            # Cliente
        hdr.setSectionResizeMode(3, QHeaderView.ResizeToContents)    # Base Imponible
        hdr.setSectionResizeMode(4, QHeaderView.ResizeToContents)    # Cantidad IVA
        hdr.setSectionResizeMode(5, QHeaderView.ResizeToContents)    # Retención
        hdr.setSectionResizeMode(6, QHeaderView.ResizeToContents)    # Importe Total
        hdr.setSectionResizeMode(7, QHeaderView.ResizeToContents)    # Fecha

        excel_layout.addWidget(self.table_excel)
        layout.addWidget(excel_card)
        layout.addStretch()
        return page

    # [MODIFICADO] create_send_page con layout más compacto
    def create_send_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 20, 40, 20) # Reducir aún más margen vertical
        layout.setSpacing(10) # Reducir aún más espaciado

        header = QLabel("ENVIAR FACTURAS")
        header.setFont(QFont(QApplication.font().family(), 32, QFont.Bold)) # Usa fuente global
        layout.addWidget(header)

        self.send_stepper = StepperWidget(["Preparar", "Enviar", "Generar PDF", "Completado"])
        self.send_stepper.layout().setContentsMargins(20, 5, 20, 5) # Menos margen vertical en stepper
        layout.addWidget(self.send_stepper)

        # --- Grupo 1: Opciones de Envío ---
        group1_frame = QFrame()
        group1_frame.setProperty("class", "ConfigGroup")
        apply_shadow(group1_frame, blur=20, offset_y=3)
        group1_layout = QVBoxLayout(group1_frame)
        group1_layout.setSpacing(10) # Reducir espaciado interno del grupo
        g1_title = QLabel("Acción Post-Envío")
        g1_title.setFont(QFont(QApplication.font().family(), 16, QFont.Bold)) # Usa fuente global
        group1_layout.addWidget(g1_title)
        post_row = QHBoxLayout()
        post_row.addWidget(QLabel("Acción sobre la Macro:"))
        self.post_action_combo = QComboBox()
        self.post_action_combo.addItem("Marcar estado en Macro (col. AC)", userData="MARK")
        self.post_action_combo.addItem("Borrar filas enviadas OK/Duplicadas", userData="DELETE_OK")
        self.post_action_combo.currentIndexChanged.connect(self._on_post_action_changed)
        post_row.addWidget(self.post_action_combo)
        post_row.addStretch()
        group1_layout.addLayout(post_row)
        layout.addWidget(group1_frame)


        # --- Grupo 2: Opciones de Descarga PDF ---
        group2_frame = QFrame()
        group2_frame.setProperty("class", "ConfigGroup")
        apply_shadow(group2_frame, blur=20, offset_y=3)
        group2_layout = QVBoxLayout(group2_frame)
        group2_layout.setSpacing(10) # Reducir espaciado interno del grupo
        g2_title = QLabel("Descarga de PDFs")
        g2_title.setFont(QFont(QApplication.font().family(), 16, QFont.Bold)) # Usa fuente global
        group2_layout.addWidget(g2_title)
        self.chk_auto_download = QCheckBox("Descargar PDFs automáticamente al terminar")
        self.chk_auto_download.setChecked(False)
        group2_layout.addWidget(self.chk_auto_download)
        dl_row = QFormLayout()
        dl_row.setSpacing(10)
        self.txt_pdf_dest = QLineEdit(
            r"C:\Users\administracionaba\Desktop\FACTURANTIA\FactuNabo EXE\Facturas PDF" # Considera usar una ruta relativa o configurable
        )
        dl_row.addRow("Carpeta destino:", self.txt_pdf_dest)
        self.cmb_browser = QComboBox()
        self.cmb_browser.addItems(["chrome", "edge"])
        self.cmb_browser.setCurrentText("chrome")
        dl_row.addRow("Navegador:", self.cmb_browser)
        group2_layout.addLayout(dl_row)
        layout.addWidget(group2_frame)


        # --- Botones de Acción Principales ---
        action_layout = QHBoxLayout()
        self.btn_send = AnimatedButton("🚀 Iniciar Envío")
        # self.btn_send.setMinimumHeight(50) # Eliminado para que tome tamaño del padding
        self.btn_send.clicked.connect(self.send_facturas)
        self.btn_send.setEnabled(False)
        action_layout.addWidget(self.btn_send)
        self.btn_download_pdfs = AnimatedButton("📥 Guardar PDFs")
        # self.btn_download_pdfs.setMinimumHeight(50) # Eliminado
        self.btn_download_pdfs.setToolTip("Descargar los PDFs de las facturas del último envío")
        self.btn_download_pdfs.setEnabled(False)
        self.btn_download_pdfs.clicked.connect(self.download_pdfs_clicked)
        action_layout.addWidget(self.btn_download_pdfs)
        layout.addLayout(action_layout)


        # --- Barra de Progreso ---
        self.progress = QProgressBar()
        self.progress.setTextVisible(True)
        self.progress_anim = QPropertyAnimation(self.progress, b"value")
        self.progress_anim.setEasingCurve(QEasingCurve.InOutSine)
        layout.addWidget(self.progress)


        # --- [NUEVO] Tabla de Previsualización ---
        preview_title = QLabel("Previsualización de Facturas a Enviar")
        preview_title.setFont(QFont(QApplication.font().family(), 16, QFont.Bold))
        layout.addWidget(preview_title)

        # Contenedor redondeado para la tabla de previsualización
        preview_card = QFrame()
        preview_card.setProperty("class", "TableCard")
        apply_shadow(preview_card, blur=20, offset_y=3)
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)

        self.table_preview = ModernTable(0, 5)
        self.table_preview.setHorizontalHeaderLabels(["Factura", "Empresa Emisora", "Cliente", "Importe Total", "Fecha"])
        hp = self.table_preview.horizontalHeader()
        hp.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hp.setSectionResizeMode(1, QHeaderView.Stretch)
        hp.setSectionResizeMode(2, QHeaderView.Stretch)
        hp.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hp.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        preview_layout.addWidget(self.table_preview)
        layout.addWidget(preview_card)


        # --- [MODIFICADO] Grupo 3 ahora es un atributo de clase (self.results_group) y está oculto ---
        self.results_group = QFrame()
        self.results_group.setProperty("class", "ConfigGroup")
        apply_shadow(self.results_group, blur=20, offset_y=3)
        group3_layout = QVBoxLayout(self.results_group)
        group3_layout.setSpacing(10) # Reducir espaciado interno
        g3_title = QLabel("Resultados del Envío")
        g3_title.setFont(QFont(QApplication.font().family(), 16, QFont.Bold)) # Usa fuente global
        group3_layout.addWidget(g3_title)
        filter_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar por factura o empresa...")
        
        # ######################################################################
        # INICIO DE LA CORRECCIÓN DE ERROR
        # La línea de abajo era la que fallaba. Ahora 'self.apply_search' existe.
        # ######################################################################
        self.search_bar.textChanged.connect(self.apply_search)
        
        filter_layout.addWidget(self.search_bar)
        self.filters = {}
        for status, _color in [("ÉXITO", COLOR_SUCCESS), ("DUPLICADO", COLOR_WARNING), ("ERROR", COLOR_ERROR)]:
            btn = QPushButton(status)
            btn.setCheckable(True)
            btn.setProperty("filter", "true")
            btn.setProperty("status", status)
            
            # ######################################################################
            # INICIO DE LA CORRECCIÓN DE ERROR
            # La línea de abajo fallaría después. Ahora 'self.apply_filter' existe.
            # ######################################################################
            btn.clicked.connect(self.apply_filter)
            
            self.filters[status] = btn
            filter_layout.addWidget(btn)
        group3_layout.addLayout(filter_layout)
        self.table_envio = ModernTable(0, 7)
        self.table_envio.setHorizontalHeaderLabels(["Factura", "Empresa Emisora", "Cliente", "Importe", "Estado", "Detalles", "Ver Factura"])
        henv = self.table_envio.horizontalHeader()
        self.table_envio.verticalHeader().setDefaultSectionSize(36)
        henv.setStretchLastSection(False)
        henv.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        henv.setSectionResizeMode(1, QHeaderView.Stretch)
        henv.setSectionResizeMode(2, QHeaderView.Stretch)
        henv.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        henv.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        henv.setSectionResizeMode(5, QHeaderView.Stretch)
        henv.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        group3_layout.addWidget(self.table_envio)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(120) # Reducir altura máx log
        group3_layout.addWidget(self.log_area)
        self.btn_export = AnimatedButton("📤 Exportar Resultados")
        self.btn_export.clicked.connect(self.export_results)
        group3_layout.addWidget(self.btn_export)

        # Añadimos el results_group con factor de estiramiento y lo ocultamos
        layout.addWidget(self.results_group, 1) # <-- El '1' hace que se expanda
        self.results_group.setVisible(False)

        return page

    def create_history_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        header_layout = QHBoxLayout()
        header = QLabel("HISTÓRICO DE ENVÍOS")
        header.setFont(QFont(QApplication.font().family(), 32, QFont.Bold)) # Usa fuente global
        header_layout.addWidget(header)
        header_layout.addStretch()
        btn_refresh = AnimatedButton("🔄 Actualizar")
        btn_refresh.clicked.connect(self.load_history)
        header_layout.addWidget(btn_refresh)
        layout.addLayout(header_layout)

        # [MODIFICADO] Contenedor redondeado para el histórico
        history_card = QFrame()
        history_card.setProperty("class", "TableCard")
        apply_shadow(history_card, blur=20, offset_y=3)
        history_layout = QVBoxLayout(history_card)
        history_layout.setContentsMargins(0, 0, 0, 0)
        history_layout.setSpacing(0)

        # Histórico ahora muestra 8 columnas (incluye importe)
        self.table_history = ModernTable(0, 9)
        self.table_history.setHorizontalHeaderLabels(["ID", "Fecha", "Factura", "Empresa Emisora", "Cliente", "Importe", "Estado", "Detalles", "PDF"])
        # Ajuste de columnas histórico
        hh = self.table_history.horizontalHeader()
        hh.setStretchLastSection(False)
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        hh.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Fecha
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Factura
        hh.setSectionResizeMode(3, QHeaderView.Stretch)  # Empresa
        hh.setSectionResizeMode(4, QHeaderView.Stretch)  # Cliente
        hh.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Importe
        hh.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Estado
        hh.setSectionResizeMode(7, QHeaderView.Stretch)  # Detalles
        hh.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # PDF

        history_layout.addWidget(self.table_history)
        layout.addWidget(history_card)
        self.load_history()
        return page

    # [MODIFICADO] create_config_page ahora usa ConfigGroup y tiene botón Borrar Histórico
    def create_config_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        header = QLabel("CONFIGURACIÓN")
        header.setFont(QFont(QApplication.font().family(), 32, QFont.Bold)) # Usa fuente global
        layout.addWidget(header)

        # --- Grupo 1: API ---
        group1_frame = QFrame()
        group1_frame.setProperty("class", "ConfigGroup")
        apply_shadow(group1_frame, blur=20, offset_y=3)
        group1_layout = QVBoxLayout(group1_frame)
        group1_layout.setSpacing(15)

        g1_title = QLabel("Conexión API")
        g1_title.setFont(QFont(QApplication.font().family(), 18, QFont.Bold)) # Usa fuente global
        group1_layout.addWidget(g1_title)

        btn_config = AnimatedButton("⚙️ Configurar Parámetros API")
        # btn_config.setMinimumHeight(50) # Eliminado
        btn_config.clicked.connect(self.open_config_dialog)
        group1_layout.addWidget(btn_config)

        info = QLabel("Configura la URL, Token y Usuario para la conexión con Facturantia.")
        info.setWordWrap(True)
        info.setStyleSheet(f"color: {COLOR_SECONDARY_TEXT};")
        group1_layout.addWidget(info)
        layout.addWidget(group1_frame)

        # --- Grupo 2: Gestión de Datos --- # Modificado título
        group2_frame = QFrame()
        group2_frame.setProperty("class", "ConfigGroup")
        apply_shadow(group2_frame, blur=20, offset_y=3)
        group2_layout = QVBoxLayout(group2_frame)
        group2_layout.setSpacing(15)

        sec_title = QLabel("Usuarios e Historial") # Modificado título
        sec_title.setFont(QFont(QApplication.font().family(), 18, QFont.Bold)) # Usa fuente global
        group2_layout.addWidget(sec_title)

        # Tabla de usuarios
        users_title = QLabel("Gestión de Usuarios")
        users_title.setFont(QFont(QApplication.font().family(), 16, QFont.Medium)) # Usa fuente global
        group2_layout.addWidget(users_title)

        self.users_table = QTableWidget(0, 2)
        self.users_table.setProperty("class", "ModernTable")
        self.users_table.setHorizontalHeaderLabels(["Usuario", "Hash (oculto)"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)

        group2_layout.addWidget(self.users_table)

        # Botonera Usuarios
        user_row = QHBoxLayout()
        btn_add = AnimatedButton("➕ Añadir usuario")
        btn_reset = AnimatedButton("🔑 Cambiar contraseña")
        btn_del = AnimatedButton("🗑️ Eliminar usuario")
        user_row.addWidget(btn_add)
        user_row.addWidget(btn_reset)
        user_row.addWidget(btn_del)
        user_row.addStretch()
        group2_layout.addLayout(user_row)

        group2_layout.addSpacing(20) # Separador visual

        # --- [AÑADIDO BORRAR HISTORIAL] ---
        history_title = QLabel("Gestión de Historial")
        history_title.setFont(QFont(QApplication.font().family(), 16, QFont.Medium)) # Usa fuente global
        group2_layout.addWidget(history_title)

        history_row = QHBoxLayout()
        btn_clear_history = AnimatedButton("🧹 Borrar Histórico")
        # Estilo de advertencia (color warning)
        btn_clear_history.setStyleSheet(f"background-color: {COLOR_WARNING};")
        history_row.addWidget(btn_clear_history)
        history_row.addStretch()
        group2_layout.addLayout(history_row)
        # --- [FIN AÑADIDO BORRAR HISTORIAL] ---

        layout.addWidget(group2_frame) # Añadir el grupo 2 al layout principal

        # Conectar señales
        btn_add.clicked.connect(self.cfg_add_user)
        btn_reset.clicked.connect(self.cfg_reset_password)
        btn_del.clicked.connect(self.cfg_delete_user)
        btn_clear_history.clicked.connect(self.clear_history_confirmation) # <-- Conectar señal nueva

        self.cfg_reload_users()
        layout.addStretch()
        return page

    # --- Gestión de usuarios ---
    def _users_file(self):
        return USERS_PATH

    def _read_users(self):
        path = self._users_file()
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("users", [])
        except Exception:
            return []

    def _write_users(self, users_list):
        data = {"users": users_list}
        with open(self._users_file(), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def cfg_reload_users(self):
        users = self._read_users()
        self.users_table.setRowCount(0)
        for u in users:
            row = self.users_table.rowCount()
            self.users_table.insertRow(row)
            self.users_table.setItem(row, 0, QTableWidgetItem(str(u.get("username", ""))))
            h = str(u.get("password_hash", ""))
            self.users_table.setItem(row, 1, QTableWidgetItem(h[:10] + "…"))

    def cfg_add_user(self):
        username, ok = QInputDialog.getText(self, "Nuevo usuario", "Usuario:")
        if not ok or not username.strip():
            return
        password, ok = QInputDialog.getText(self, "Nuevo usuario", "Contraseña:", QLineEdit.Password)
        if not ok or not password:
            return
        users = self._read_users()
        if any(u.get("username") == username for u in users):
            QMessageBox.warning(self, "Usuarios", f"El usuario '{username}' ya existe.")
            return
        users.append({"username": username, "password_hash": hashlib.sha256(password.encode("utf-8")).hexdigest()})
        self._write_users(users)
        self.show_toast(f"✅ Usuario '{username}' creado")
        self.cfg_reload_users()

    def cfg_selected_username(self):
        row = self.users_table.currentRow()
        if row < 0:
            return None
        item = self.users_table.item(row, 0)
        return item.text().strip() if item else None

    def cfg_reset_password(self):
        username = self.cfg_selected_username()
        if not username:
            QMessageBox.information(self, "Usuarios", "Selecciona un usuario en la tabla.")
            return
        password, ok = QInputDialog.getText(
            self, "Cambiar contraseña", f"Nueva contraseña para '{username}':", QLineEdit.Password
        )
        if not ok or not password:
            return
        users = self._read_users()
        for u in users:
            if u.get("username") == username:
                u["password_hash"] = hashlib.sha256(password.encode("utf-8")).hexdigest()
                break
        self._write_users(users)
        self.show_toast("✅ Contraseña actualizada")
        self.cfg_reload_users()

    def cfg_delete_user(self):
        username = self.cfg_selected_username()
        if not username:
            QMessageBox.information(self, "Usuarios", "Selecciona un usuario en la tabla.")
            return
        if username.lower() == "admin":
            QMessageBox.warning(self, "Usuarios", "No se permite eliminar el usuario 'admin'.")
            return
        ret = QMessageBox.question(self, "Eliminar usuario", f"¿Eliminar el usuario '{username}'?")
        if ret != QMessageBox.Yes:
            return
        users = [u for u in self._read_users() if u.get("username") != username]
        self._write_users(users)
        self.show_toast(f"🗑️ Usuario '{username}' eliminado")
        self.cfg_reload_users()

    # --- [NUEVAS FUNCIONES BORRAR HISTORIAL] ---
    def clear_history_confirmation(self):
        reply = QMessageBox.question(self, 'Confirmar Borrado',
                                     "¿Estás seguro de que quieres borrar TODO el historial de envíos?\n"
                                     "Esta acción NO se puede deshacer y pondrá el Dashboard a cero.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.clear_history_execute()

    def clear_history_execute(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM envios") # Borra todos los registros
            conn.commit()
            # Opcional: Limpiar espacio no usado en la DB
            cursor.execute("VACUUM")
            conn.commit()
            conn.close()

            self.show_toast("✅ Historial de envíos borrado.")
            # Recargar la tabla del histórico (que ahora estará vacía)
            self.load_history()
            # update_dashboard_stats() ya se llama dentro de load_history()

        except Exception as e:
            self.show_error(f"Error al borrar el historial: {e}")
            print(f"Error borrando historial: {e}")
    # --- [FIN NUEVAS FUNCIONES] ---


    # --- Navegación/tema ---
    def change_page(self, index):
        # Animación de transición tipo iOS (fade out/in)
        if index == self.content_stack.currentIndex():
            return
        # Tomar snapshot de la vista actual
        try:
            prev_pix = self.content_stack.grab()
        except Exception:
            prev_pix = None
        # Cambiar inmediatamente al destino para preparar fade-in del nuevo contenido
        self.content_stack.setCurrentIndex(index)
        # Si no hay snapshot, no animamos
        if prev_pix is None:
            return
        # Crear overlay con el snapshot anterior y desvanecerlo
        overlay = QLabel(self.content_stack)
        overlay.setPixmap(prev_pix)
        overlay.setGeometry(self.content_stack.rect())
        overlay.raise_()
        effect = QGraphicsOpacityEffect(overlay)
        overlay.setGraphicsEffect(effect)
        effect.setOpacity(1.0)
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(220)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        # Mantener referencias hasta finalizar
        if not hasattr(self, "_page_overlays"):
            self._page_overlays = []
        self._page_overlays.append((overlay, anim))
        def _cleanup():
            overlay.deleteLater()
            try:
                self._page_overlays.remove((overlay, anim))
            except Exception:
                pass
        anim.finished.connect(_cleanup)
        overlay.show()
        anim.start()
        if index == 0: # Índice del Dashboard
            self.update_dashboard_stats() # Recarga stats de tarjetas y errores
            self.populate_dashboard_filters() # Recarga el combo de empresas
        elif index == 3: # Índice del Histórico
            self.load_history() # Recarga el histórico al cambiar a esa página

    def toggle_theme(self, checked):
        self.theme = "dark" if checked else "light"
        self.setProperty("theme", self.theme)
        app = QApplication.instance()
        style_sheet_content = self._get_themed_stylesheet()
        if style_sheet_content:
            app.setStyleSheet(style_sheet_content)

        # Re-aplicar estilos (necesario para que todo se repinte)
        # Usamos un temporizador para asegurar que se haga después del evento actual
        QTimer.singleShot(0, self._refresh_styles)

    # [CORREGIDO] _refresh_styles ahora es más simple y evita el TypeError
    def _refresh_styles(self):
        app = QApplication.instance()
        for w in app.allWidgets():
            try:
                # Estas dos líneas suelen ser suficientes para refrescar el estilo
                w.style().unpolish(w)
                w.style().polish(w)
                # Eliminamos w.update() ya que causaba TypeErrors en varios widgets
            except RuntimeError:
                # Mantenemos esto por si el widget se elimina mientras iteramos
                pass
            # Eliminamos el bloque 'except TypeError' ya que quitamos la causa


    def _on_post_action_changed(self, idx):
        self.post_action_mode = self.post_action_combo.itemData(idx) or "MARK"
        self.append_log(f"Acción post-envío seleccionada: {self.post_action_mode}")

    # --- Drag & drop Excel ---
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith((".xlsx", ".xlsm", ".xls")):
            self.process_dropped_excel(file_path)
        event.accept()

    def process_dropped_excel(self, path):
        self.select_excel(path)

    # --- Limpieza integral de la página "Cargar Excel" ---
    def clear_excel_table(self):
        if hasattr(self, "table_excel"):
            self.table_excel.setRowCount(0)
        if hasattr(self, "validation_label"):
            self.validation_label.clear()
        if hasattr(self, "stepper"):
            self.stepper.set_step(0)
        if hasattr(self, "btn_send"):
            self.btn_send.setEnabled(False)
        self.current_excel_path = None
        self.loaded_invoice_count = 0
        self._update_send_badge()

        # Limpiar también la página de envío
        self.clear_send_page()

    def select_excel(self, path=None):
        if not path:
            path, _ = QFileDialog.getOpenFileName(
                self,
                "Seleccionar Excel",
                "",
                "Hojas de cálculo (*.xlsx *.XLSX *.xlsm *.XLSM *.xls *.XLS);;Todos los archivos (*.*)",
            )
        if not path:
            return

        self.clear_excel_table()

        self.current_excel_path = path
        self.stepper.set_step(0)
        self.append_log(f"📁 Excel seleccionado: {path}")
        if self.validate_excel(path):
            self.stepper.set_step(2)
            self.btn_send.setEnabled(True)
            self.validation_label.setText("✅ Archivo validado correctamente")
            self.validation_label.setStyleSheet(f"color: {COLOR_SUCCESS}; font-weight: bold;")
        else:
            self.stepper.set_step(1)
            self.btn_send.setEnabled(False)

            def _fmt_err(e):
                if isinstance(e, str):
                    return e
                if isinstance(e, (list, tuple)):
                    # FIX: 'y' → 'and' para Python
                    return " - ".join(str(x) for x in e if x is not None and str(x).strip() != "")
                try:
                    return str(e)
                except Exception:
                    return repr(e)

            errs_str = [_fmt_err(e) for e in self.validation_errors]
            error_msg = "❌ Errores de validación:\n" + "\n".join(errs_str)
            self.validation_label.setText(error_msg)
            self.validation_label.setStyleSheet(f"color: {COLOR_ERROR};")
            return

        # --- [INICIO DE LA CORRECCIÓN] ---
        # Llamar a adapt_from_macro con UN solo argumento, como en tus archivos.
        try:
            # --- [MODIFICADO] Capturar y almacenar los 6 dataframes ---
            (
                df_factura, df_conceptos, df_forma_pago, df_txt,
                self.df_factura_historico, self.df_conceptos_historico
            ) = macro_adapter.adapt_from_macro(path)
        # --- [FIN MODIFICADO] ---
        except Exception as e:
            self.append_log(f"❌ Error leyendo Excel (Macro): {e}")
            self.show_error(f"Error procesando el Excel: {e}")
            return

        # --- Normalizamos NumFactura en ambos DF y usamos el mismo ID para todo ---
        if "NumFactura" in df_factura.columns:
            df_factura["__id_norm__"] = df_factura["NumFactura"].map(_normalize_invoice_id)
        else:
            df_factura["__id_norm__"] = ""

        if "NumFactura" in df_conceptos.columns:
            df_conceptos["__id_norm__"] = df_conceptos["NumFactura"].map(_normalize_invoice_id)
        else:
            df_conceptos["__id_norm__"] = ""

        self.table_excel.setRowCount(0)
        for i, row in df_factura.iterrows():
            self.table_excel.insertRow(i)
            has_error = i in [err[0] for err in self.validation_errors if isinstance(err, tuple)]

            # [MODIFICADO] Color de error más sutil
            err_color = QColor(COLOR_ERROR)
            err_color.setAlpha(40) # 40/255 de opacidad
            bg_color = err_color if has_error else QColor(COLOR_CARD)

            # Color de texto normal
            text_color = QColor(COLOR_TEXT)
            if self.theme == "dark":
                bg_color = err_color if has_error else QColor(COLOR_DARK_CARD)
                text_color = QColor(COLOR_DARK_TEXT)

            inv_id = row.get("__id_norm__", "")
            item_factura = QTableWidgetItem(inv_id)
            item_factura.setBackground(bg_color)
            item_factura.setForeground(text_color)
            self.table_excel.setItem(i, 0, item_factura)

            item_empresa = QTableWidgetItem(str(row.get("empresa_emisora", "")))
            item_empresa.setBackground(bg_color)
            item_empresa.setForeground(text_color)
            self.table_excel.setItem(i, 1, item_empresa)

            # Cliente
            item_cliente = QTableWidgetItem(str(row.get("cliente_nombre", "")))
            item_cliente.setBackground(bg_color)
            item_cliente.setForeground(text_color)
            self.table_excel.setItem(i, 2, item_cliente)

            # Cálculos de importes
            base_sum = 0.0
            iva_sum = 0.0
            ret_sum = 0.0
            if inv_id:
                # Añadir filtro por empresa emisora
                em_act = row.get("empresa_emisora", "")
                conceptos_factura = df_conceptos[
                    (df_conceptos["__id_norm__"] == inv_id) &
                    (df_conceptos["empresa_emisora"] == em_act)
                ]
                if not conceptos_factura.empty:
                    base_sum = float(conceptos_factura["base_unidad"].sum() or 0.0)

                    # Calcular IVA
                    iva_sum = (conceptos_factura["base_unidad"] * (conceptos_factura["porcentaje"] / 100.0)).sum() if not conceptos_factura["base_unidad"].empty else 0.0


                    # Calcular Retención
                    ret_sum = (conceptos_factura["base_unidad"] * (conceptos_factura["porcentaje_retenido"] / 100.0)).sum() if not conceptos_factura["base_unidad"].empty else 0.0

            total_sum = base_sum + iva_sum - ret_sum

            # Base Imponible
            item_base = QTableWidgetItem(format_eur(base_sum))
            item_base.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_base.setBackground(bg_color)
            item_base.setForeground(text_color)
            self.table_excel.setItem(i, 3, item_base)

            # Cantidad IVA
            item_iva = QTableWidgetItem(format_eur(iva_sum))
            item_iva.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_iva.setBackground(bg_color)
            item_iva.setForeground(text_color)
            self.table_excel.setItem(i, 4, item_iva)

            # Retención
            item_ret = QTableWidgetItem(format_eur(ret_sum))
            item_ret.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_ret.setBackground(bg_color)
            item_ret.setForeground(text_color)
            self.table_excel.setItem(i, 5, item_ret)

            # Importe Total
            item_total = QTableWidgetItem(format_eur(total_sum))
            item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            item_total.setBackground(bg_color)
            item_total.setForeground(text_color)
            self.table_excel.setItem(i, 6, item_total)

            fecha = row.get("fecha_emision", "")
            fecha_str = pd.to_datetime(fecha).strftime("%d/%m/%Y") if pd.notna(fecha) else ""
            item_fecha = QTableWidgetItem(fecha_str)
            item_fecha.setBackground(bg_color)
            item_fecha.setForeground(text_color)
            self.table_excel.setItem(i, 7, item_fecha)

        # Reajuste final de columnas después de cargar
        for col in [0, 3, 4, 5, 6, 7]:
            self.table_excel.resizeColumnToContents(col)

        # --- [NUEVO] Poblar la tabla de previsualización en la página de envío ---
        try:
            self.table_preview.setRowCount(0)
            for i in range(self.table_excel.rowCount()):
                row_idx = self.table_preview.rowCount()
                self.table_preview.insertRow(row_idx)
                # Copiamos los datos relevantes de la tabla excel a la de previsualización
                # Factura (col 0), Empresa (col 1), Cliente (col 2), Total (col 6), Fecha (col 7)
                self.table_preview.setItem(row_idx, 0, QTableWidgetItem(self.table_excel.item(i, 0).text()))
                self.table_preview.setItem(row_idx, 1, QTableWidgetItem(self.table_excel.item(i, 1).text()))
                self.table_preview.setItem(row_idx, 2, QTableWidgetItem(self.table_excel.item(i, 2).text()))

                item_total = QTableWidgetItem(self.table_excel.item(i, 6).text())
                item_total.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_preview.setItem(row_idx, 3, item_total)

                self.table_preview.setItem(row_idx, 4, QTableWidgetItem(self.table_excel.item(i, 7).text()))

            # Ajustar columnas de la tabla de previsualización
            for col_prev in [0, 3, 4]:
                self.table_preview.resizeColumnToContents(col_prev)
        except Exception as e:
            print(f"Error al poblar la tabla de previsualización: {e}")
        # --- [FIN NUEVO] ---

        # KPI: contador y total base
        try:
            count = len(df_factura)
            total_base = float(df_conceptos["base_unidad"].sum() or 0.0)
            msg = f"📥 {count} facturas cargadas · Total base: {format_eur(total_base)}"
            self.loaded_summary.setText(msg)
            self.loaded_summary.setVisible(True)
            self.loaded_invoice_count = count
            self._update_send_badge()
            self.show_toast(msg)
        except Exception:
            pass

        if hasattr(self.worker, "set_excel_path"):
            self.worker.set_excel_path(path)

    def validate_excel(self, path):
        self.validation_errors = []
        
        # --- [INICIO DE LA CORRECCIÓN] ---
        # Llamar a adapt_from_macro con UN solo argumento
        try:
            # --- [MODIFICADO] Capturar los 6 dataframes, aunque no se usen todos aquí ---
            (
                df_factura, df_conceptos, df_forma_pago, df_txt,
                _, _ # Ignoramos los históricos en la validación simple
            ) = macro_adapter.adapt_from_macro(path)
        # --- [FIN MODIFICADO] ---
        except Exception as e:
            self.validation_errors.append(f"Error leyendo archivo (Macro): {str(e)}")
            return False

        required_cols = ["NumFactura", "empresa_emisora", "fecha_emision"]
        missing_cols = [col for col in required_cols if col not in df_factura.columns]
        if missing_cols:
            self.validation_errors.append(f"Faltan columnas: {', '.join(missing_cols)}")
            return False

        bases = df_conceptos.groupby("NumFactura")["base_unidad"].sum().to_dict()
        for i, row in df_factura.reset_index(drop=True).iterrows():
            row_errors = []
            if pd.isna(row.get("NumFactura")) or str(row.get("NumFactura")).strip() == "":
                row_errors.append("Número de factura vacío")
            if pd.isna(row.get("empresa_emisora")) or str(row.get("empresa_emisora")).strip() == "":
                row_errors.append("Empresa emisora vacía")
            if pd.isna(row.get("fecha_emision")):
                row_errors.append("Fecha de emisión vacía")
            if bases.get(row.get("NumFactura"), 0) <= 0:
                row_errors.append("Importe inválido (base_unidad <= 0)")
            if row_errors:
                self.validation_errors.append((i, f"Fila {i+2}: {', '.join(row_errors)}"))
        return len(self.validation_errors) == 0

    def send_facturas(self):
        if not self.current_excel_path:
            self.show_toast("❌ No hay archivo Excel cargado")
            return

        # --- [NUEVO] Ocultar previsualización y mostrar resultados ---
        self.table_preview.setVisible(False)
        self.results_group.setVisible(True)
        # --- [FIN NUEVO] ---

        # Limpiar tabla de envío actual y pasos
        self.table_envio.setRowCount(0)
        self.send_stepper.set_step(0)

        # Progreso indeterminado mientras dura el envío (más honesto)
        self.progress.setRange(0, 0)

        self.sending_in_progress = True
        self.btn_send.setEnabled(False)
        self.btn_download_pdfs.setEnabled(False)

        # Evitar reseguir resultados antiguos: respaldar summary.json si existe
        try:
            summary_path = os.path.join("responses", "summary.json")
            if os.path.exists(summary_path):
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup = os.path.join("responses", f"summary_{ts}.json")
                os.replace(summary_path, backup)
        except Exception:
            pass

        # EXISTENTE: acción post-macro
        os.environ["POST_MACRO_ACTION"] = self.post_action_mode

        # EXISTENTE: opciones en entorno para compatibilidad
        os.environ["AUTO_DOWNLOAD_PDFS"] = "1" if getattr(self, "chk_auto_download", None) and self.chk_auto_download.isChecked() else "0"
        os.environ["PDF_DEST_DIR"] = (
            self.txt_pdf_dest.text()
            if hasattr(self, "txt_pdf_dest")
            else r"C:\Users\administracionaba\Desktop\FACTURANTIA\FactuNabo EXE\Facturas PDF"
        )
        os.environ["PDF_BROWSER"] = self.cmb_browser.currentText() if hasattr(self, "cmb_browser") else "chrome"
        os.environ["PDF_HEADLESS"] = "1"

        # --- [FIX] Crear un nuevo worker y thread para cada envío ---
        self.thread = QThread()
        self.worker = Worker()

        # Mover worker al thread
        self.worker.moveToThread(self.thread)

        # Conectar señales
        self.worker.log_signal.connect(self.append_log, Qt.QueuedConnection)
        self.worker.finished.connect(self.on_finished, Qt.QueuedConnection)
        self.thread.started.connect(self.worker.process)

        # Configurar el worker con los datos actuales
        self.worker.set_excel_path(self.current_excel_path)

        # --- [NUEVO] Pasar los dataframes históricos al worker ---
        self.worker.set_historical_data(
            self.df_factura_historico,
            self.df_conceptos_historico
        )
        # --- [FIN NUEVO] ---

        self.worker.set_post_macro_action(self.post_action_mode)
        self.worker.set_download_options(
            auto=(self.chk_auto_download.isChecked() if hasattr(self, "chk_auto_download") else False),
            dest=(self.txt_pdf_dest.text() if hasattr(self, "txt_pdf_dest") else ""),
            browser=(self.cmb_browser.currentText() if hasattr(self, "cmb_browser") else "chrome"),
            headless=True,
        )

        QTimer.singleShot(500, lambda: self.send_stepper.set_step(1))
        self.thread.start()

    # --- FIX: Slot GUI para limpiar hilo de descargas de forma segura ---
    def on_downloads_done_gui(self):
        """Siempre ejecutado en el hilo de la GUI."""
        try:
            self.progress.setRange(0, 100)
            self.progress.setValue(100)
            self.show_toast("✅ Descarga de PDFs terminada")
        finally:
            # Cierre/limpieza del hilo de descargas SOLO desde la GUI
            try:
                if getattr(self, "dthread", None) and self.dthread.isRunning():
                    self.dthread.quit()
                    self.dthread.wait(3000)
            except Exception:
                pass
            try:
                if getattr(self, "dworker", None):
                    self.dworker.deleteLater()
                if getattr(self, "dthread", None):
                    self.dthread.deleteLater()
            except Exception:
                pass
            self.dthread = None
            self.dworker = None
            if hasattr(self, "btn_download_pdfs") and self.btn_download_pdfs:
                self.btn_download_pdfs.setEnabled(True)

    def download_pdfs_clicked(self):
        # protección: necesita summary.json
        summary_path = os.path.join("responses", "summary.json")
        if not os.path.exists(summary_path):
            self.show_toast("⚠️ No hay resumen disponible. Primero ejecuta un envío.")
            return

        # Barra indeterminada mientras descarga
        self.progress.setRange(0, 0)
        self.append_log("📥 Iniciando descarga manual de PDFs...")
        self.btn_download_pdfs.setEnabled(False)

        # Hilo temporal con un Worker “solo descarga”
        self.dthread = QThread(self)
        self.dworker = Worker()
        try:
            self.dworker.set_download_options(
                auto=True,  # habilita opciones internas; se llama download_pdfs() directamente
                dest=(self.txt_pdf_dest.text() if hasattr(self, "txt_pdf_dest") else ""),
                browser=(self.cmb_browser.currentText() if hasattr(self, "cmb_browser") else "chrome"),
                headless=True,
            )
        except Exception:
            pass

        self.dworker.moveToThread(self.dthread)
        # FIX(Queued): logs del worker de descargas también encolados a GUI
        self.dworker.log_signal.connect(self.append_log, Qt.QueuedConnection)
        self.dthread.started.connect(self.dworker.download_pdfs)

        # --- FIX(Queued): conectar señal a GUI con entrega encolada
        if hasattr(self.dworker, "downloads_done"):
            self.dworker.downloads_done.connect(self.on_downloads_done_gui, Qt.QueuedConnection)
        else:
            self.show_error("El Worker no expone la señal 'downloads_done'. Actualiza worker.py.")

        self.dthread.start()

    # ######################################################################
    # INICIO DEL BLOQUE AÑADIDO (FUNCIONES DE FILTRADO QUE FALTABAN)
    # ######################################################################

    def _apply_envio_filters(self):
        """Función central que aplica BÚSQUEDA y FILTROS de estado a la tabla de envío."""
        if not hasattr(self, 'table_envio'):
            return

        # 1. Obtener el texto de búsqueda
        search_text = ""
        if hasattr(self, 'search_bar'):
            search_text = self.search_bar.text().strip().lower()

        # 2. Obtener los filtros de estado activos
        active_statuses = []
        if hasattr(self, 'filters'):
            for status, btn in self.filters.items():
                if btn.isChecked():
                    # Usamos el nombre del botón (ÉXITO, DUPLICADO, ERROR)
                    active_statuses.append(status.lower())

        # 3. Iterar y aplicar
        for row in range(self.table_envio.rowCount()):
            # Obtener datos de la fila
            item_factura = self.table_envio.item(row, 0)
            item_empresa = self.table_envio.item(row, 1)
            widget_estado = self.table_envio.cellWidget(row, 2) # Es un StatusChip

            text_factura = item_factura.text().lower() if item_factura else ""
            text_empresa = item_empresa.text().lower() if item_empresa else ""
            
            # El StatusChip tiene el texto (ÉXITO, DUPLICADO, NABO!/ERROR)
            text_estado = ""
            if isinstance(widget_estado, StatusChip):
                text_estado = widget_estado.text().lower()
            elif isinstance(widget_estado, QLabel): # Fallback
                text_estado = widget_estado.text().lower()
            
            # Mapear "NABO!" a "error" si es necesario
            if "nabo" in text_estado:
                text_estado = "error"

            # --- Aplicar Lógica ---
            
            # 1. Comprobar filtro de texto
            match_text = True # Asumir que coincide si no hay texto
            if search_text:
                match_text = (search_text in text_factura) or (search_text in text_empresa)

            # 2. Comprobar filtro de estado
            match_status = True # Asumir que coincide si no hay filtros activos
            if active_statuses:
                match_status = (text_estado in active_statuses)

            # 3. Decisión final
            self.table_envio.setRowHidden(row, not (match_text and match_status))

    def apply_search(self, text):
        """Slot para la barra de búsqueda. Llama al filtro principal."""
        self._apply_envio_filters()

    def apply_filter(self):
        """Slot para los botones de filtro. Llama al filtro principal."""
        self._apply_envio_filters()
        
    # ######################################################################
    # FIN DEL BLOQUE AÑADIDO
    # ######################################################################

    # --- FIX(GUI-guard): asegurar que append_log corre en el hilo GUI
    def append_log(self, msg):
        # Si esta función entra desde un hilo que no es el de la GUI, reencola de forma segura
        if QThread.currentThread() != QApplication.instance().thread():
            # Usamos Qt.QueuedConnection para encolar el mensaje de forma segura
            self.worker.log_signal.emit(str(msg))
            return

        # Actualización del Stepper si el log lo indica
        msg_str = str(msg)
        if "Generando PDF" in msg_str or "descarga" in msg_str.lower():
            if self.sending_in_progress and self.send_stepper.current_step < 2:
                self.send_stepper.set_step(2)

        # Asegurarse de que log_area existe antes de usarla
        if hasattr(self, 'log_area') and self.log_area:
             self.log_area.append(msg_str)
             self.log_area.verticalScrollBar().setValue(self.log_area.verticalScrollBar().maximum())

        self.show_toast(msg_str)

        # Habilita el botón de PDFs en cuanto exista el summary
        try:
            if os.path.exists(os.path.join("responses", "summary.json")):
                 if hasattr(self, 'btn_download_pdfs') and self.btn_download_pdfs:
                      self.btn_download_pdfs.setEnabled(True)
        except Exception:
            pass

        # Si el proceso principal no está en marcha, no intentes actualizar la tabla de envío
        if not self.sending_in_progress or not hasattr(self, 'table_envio'):
            return

        # --- [INICIO DE LA MODIFICACIÓN] ---
        # La lógica de guardado en BBDD se ha movido a on_finished.
        # Esta función ahora solo actualiza la tabla de la UI.
        summary_path = os.path.join("responses", "summary.json")
        if not os.path.exists(summary_path):
            return
        try:
            with open(summary_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    return
        except Exception:
            return

        if not isinstance(data, list):
             return

        self.table_envio.setRowCount(0)

        for i, item in enumerate(data):
            self.table_envio.insertRow(i)
            if not isinstance(item, dict):
                 continue
            try:
                self.table_envio.setItem(i, 0, QTableWidgetItem(str(item.get("id", ""))))
                self.table_envio.setItem(i, 1, QTableWidgetItem(str(item.get("empresa", ""))))
                self.table_envio.setItem(i, 2, QTableWidgetItem(str(item.get("cliente", ""))))

                item_importe = QTableWidgetItem(format_eur(item.get("importe", 0.0)))
                item_importe.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_envio.setItem(i, 3, item_importe)

                estado = str(item.get("status", "")).upper()
                if estado == "DUPLICATE": estado = "DUPLICADO"
                elif estado == "ATENCION": estado = "DUPLICADO"
                chip = StatusChip(estado)
                self.table_envio.setCellWidget(i, 4, chip)
                self.table_envio.setItem(i, 5, QTableWidgetItem(str(item.get("details", ""))))
                pdf_url = item.get("pdf_url", "")
                invoice_id = str(item.get("id") or item.get("NumFactura") or item.get("num_factura") or "").strip()
                btn_open = self._make_pdf_button(invoice_id, pdf_url)
                self.table_envio.setCellWidget(i, 6, btn_open)
                # LA LLAMADA A self.save_to_history(item) HA SIDO ELIMINADA DE AQUÍ
            except Exception as e:
                 print(f"Error procesando item {i} del summary para la UI: {e} - Item: {item}")
                 error_item = QTableWidgetItem("Error procesando")
                 error_item.setForeground(QColor(COLOR_ERROR))
                 for col_err in range(self.table_envio.columnCount()):
                      if not self.table_envio.item(i, col_err):
                           self.table_envio.setItem(i, col_err, error_item.clone())
        # --- [FIN DE LA MODIFICACIÓN] ---


    # ######################################################################
    # INICIO DEL BLOQUE CORREGIDO (INDENTACIÓN AÑADIDA)
    # Todas las siguientes funciones ahora están DENTRO de MainWindow
    # ######################################################################

    def on_finished(self, *args, **kwargs):
        """
        Slot llamado cuando el worker termina.
        1. Restaura botones y estado de la UI.
        2. Llama a la función que guarda el resumen en la BBDD.
        """
        try:
            self.sending_in_progress = False
            if hasattr(self, 'progress'):
                self.progress.setRange(0, 100)
                self.progress.setValue(100)
            if hasattr(self, 'send_stepper'):
                self.send_stepper.set_step(3)

            # --- [NUEVO] Guardar el resumen en la BBDD ---
            summary_path = os.path.join("responses", "summary.json")
            if os.path.exists(summary_path):
                try:
                    with open(summary_path, "r", encoding="utf-8") as f:
                        summary_data = json.load(f)
                    if isinstance(summary_data, list):
                        self.save_summary_to_history(summary_data)
                except Exception as e:
                    self.show_error(f"Error al procesar el resumen para el historial: {e}")
            # --- [FIN NUEVO] ---

        except Exception as e:
            print(f"Error en on_finished: {e}")
        finally:
            if hasattr(self, "btn_send"):
                self.btn_send.setEnabled(True)
            if hasattr(self, "btn_download_pdfs"):
                self.btn_download_pdfs.setEnabled(True)
            if hasattr(self, "_overlay"):
                self._overlay.hide()

            # --- [FIX] Limpieza del thread y worker ---
            if self.thread and self.thread.isRunning():
                self.thread.quit()
                self.thread.wait() # Esperar a que termine limpiamente

            # Marcar para eliminación segura
            if self.worker:
                self.worker.deleteLater()
            if self.thread:
                self.thread.deleteLater()

            self.worker = None
            self.thread = None


    def show_error(self, message):
        """Muestra un error de forma centralizada (para conexiones del worker)."""
        try:
            if hasattr(self, "statusbar"):
                self.statusbar.showMessage(str(message), 8000)
            QMessageBox.critical(self, "Error", str(message))
        except Exception:
            # Fallback: imprimir en consola
            print(f"[ERROR] {message}")

    # [NUEVA FUNCIÓN]
    def _parse_and_sum_amount(self, raw_amount):
        """
        Parsea y convierte un importe a float, manejando tanto números como strings
        en formato español ('1.234,56').
        """
        if isinstance(raw_amount, (int, float)):
            return float(raw_amount)

        if not raw_amount or not str(raw_amount).strip():
            return 0.0

        try:
            # Si es un string, aplicamos la normalización
            amount_str = str(raw_amount).replace('.', '').replace(',', '.')
            return float(amount_str)
        except (ValueError, TypeError):
            return 0.0

    # [REDISEÑADO] save_summary_to_history para guardar facturas individuales
    def save_summary_to_history(self, summary_data: list):
        """
        Procesa el resultado de un envío (summary.json) y guarda una entrada
        por cada factura individual en la BBDD.
        """
        if not summary_data:
            return

        records_to_insert = []
        for item in summary_data:
            if not isinstance(item, dict):
                continue

            # Extraer datos de cada factura
            num_factura = item.get("id") or item.get("NumFactura") or "N/A"
            empresa = item.get("empresa") or "Desconocida"
            cliente = item.get("cliente") or ""
            raw_amount = (item.get("amount") or item.get("importe") or
                          item.get("importe_total") or item.get("total") or 0.0)
            importe = self._parse_and_sum_amount(raw_amount)

            status = str(item.get("status", "ERROR")).upper()
            if status in ("OK", "SUCCESS"):
                status = "ÉXITO"
            elif status in ("DUPLICATE", "ATENCION"):
                status = "DUPLICADO"

            detalles = item.get("details", "")
            if isinstance(detalles, dict):
                detalles = json.dumps(detalles, ensure_ascii=False)

            pdf_url = item.get("pdf_url", "")
            if isinstance(pdf_url, dict):
                pdf_url = json.dumps(pdf_url, ensure_ascii=False)

            # Preparar la tupla para la inserción
            records_to_insert.append((
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                num_factura,
                empresa,
                status,
                detalles,
                pdf_url,
                self.current_excel_path or "",
                importe,
                cliente
            ))

        # Insertar todos los registros en una única transacción
        if not records_to_insert:
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.executemany(
                """INSERT INTO envios (
                    fecha_envio, num_factura, empresa, estado,
                    detalles, pdf_url, excel_path, importe, cliente
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                records_to_insert
            )
            conn.commit()
            conn.close()
            self.show_toast(f"✅ {len(records_to_insert)} facturas guardadas en el historial.")
        except Exception as e:
            print(f"Error guardando resumen en BBDD: {e}")
            self.show_error(f"Error al guardar en el historial: {e}")

    # ######################################################################
    # INICIO DEL BLOQUE CORREGIDO (AÑADIDA INDENTACIÓN)
    # ######################################################################

    def load_history(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            # Aseguramos seleccionar las 8 columnas (o las que existan, por si acaso)
            # El orden debe coincidir con la tabla (importe es el 8º)
            cursor.execute("SELECT id, fecha_envio, num_factura, empresa, estado, detalles, pdf_url, importe, cliente FROM envios ORDER BY fecha_envio DESC LIMIT 100")
            rows = cursor.fetchall()
            conn.close()
            
            self.table_history.setRowCount(0)
            
            for row in rows:
                (db_id, fecha, num_factura, empresa, estado, detalles, pdf_url, importe, cliente) = row
                row_index = self.table_history.rowCount()
                self.table_history.insertRow(row_index)
                
                self.table_history.setItem(row_index, 0, QTableWidgetItem(str(db_id)))
                self.table_history.setItem(row_index, 1, QTableWidgetItem(fecha))
                self.table_history.setItem(row_index, 2, QTableWidgetItem(num_factura))
                self.table_history.setItem(row_index, 3, QTableWidgetItem(empresa))
                self.table_history.setItem(row_index, 4, QTableWidgetItem(cliente))
                
                item_importe = QTableWidgetItem(format_eur(importe))
                item_importe.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table_history.setItem(row_index, 5, item_importe)
                
                chip = StatusChip(estado)
                self.table_history.setCellWidget(row_index, 6, chip)
                
                self.table_history.setItem(row_index, 7, QTableWidgetItem(detalles))
                
                # Botón PDF (ahora en la columna 7)
                btn_pdf = self._make_pdf_button(num_factura, pdf_url)
                if btn_pdf:
                    self.table_history.setCellWidget(row_index, 8, btn_pdf)

            # Ajustar columnas
            self.table_history.resizeColumnToContents(0)
            self.table_history.resizeColumnToContents(1)
            self.table_history.resizeColumnToContents(2)
            self.table_history.resizeColumnToContents(4)
            self.table_history.resizeColumnToContents(5)
            self.table_history.resizeColumnToContents(7)

            self.update_dashboard_stats() # Llama a la actualización después de cargar
        except Exception as e:
            self.show_toast(f"Error cargando histórico: {str(e)}")
            print(f"Error cargando histórico: {e}") # Debug

    # [MODIFICADO] update_dashboard_stats ahora es más simple (sin Top 5)
    def update_dashboard_stats(self):
        """Actualiza las 4 tarjetas principales del Dashboard desde la DB."""
        if not all([self.total_label, self.success_label, self.month_total_label, self.month_count_label]):
            print("Warning: Faltan referencias a las etiquetas del Dashboard.")
            return
        
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # 1. Totales Históricos
            cursor.execute("SELECT COUNT(*) FROM envios WHERE estado = 'ÉXITO'")
            total_exitos = cursor.fetchone()[0] or 0

            # 2. Totales Mensuales (Mes actual)
            mes_actual = datetime.now().strftime("%Y-%m")
            cursor.execute(
                "SELECT COUNT(*), SUM(importe) FROM envios WHERE (estado LIKE 'ÉXITO%' OR estado = 'OK' OR estado = 'SUCCESS') AND strftime('%Y-%m', fecha_envio) = ?",
                (mes_actual,)
            )
            mes_count, mes_total = cursor.fetchone() or (0, 0.0)
            
            conn.close()

            # 3. Asignar valores
            self.total_label.setText(str(total_exitos))
            self.success_label.setText(str(total_exitos))
            self.month_count_label.setText(str(mes_count))
            self.month_total_label.setText(format_eur(mes_total or 0.0))

        except Exception as e:
            self.show_toast(f"Error actualizando dashboard: {str(e)}")
            print(f"Error actualizando dashboard: {e}") # Debug


    def populate_dashboard_filters(self):
        """Carga el combo de empresas desde la DB (tabla envios)."""
        self.dash_combo_empresas.clear()
        self.dash_combo_empresas.addItem("Todas las Empresas", userData="ALL")
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            rows = cur.execute("SELECT DISTINCT empresa FROM envios WHERE empresa IS NOT NULL AND empresa != '' ORDER BY empresa").fetchall()
            conn.close()
            for (e,) in rows:
                self.dash_combo_empresas.addItem(str(e), userData=str(e))
        except Exception as e:
            print(f"Error cargando empresas: {e}")
    
    def run_dashboard_query(self):
        """Consulta la DB por empresa y periodo y muestra resultados en la tabla del Dashboard."""
        if not self.dash_combo_empresas or not self.dash_table_resultados:
            return

        emisor = self.dash_combo_empresas.currentData()
        periodo = self.dash_combo_periodo.currentText()

        from datetime import date, timedelta
        def _month_bounds(d=None):
            d = d or date.today()
            start = d.replace(day=1).strftime("%Y-%m-%d")
            if d.month == 12:
                end = d.replace(year=d.year+1, month=1, day=1).strftime("%Y-%m-%d")
            else:
                end = d.replace(month=d.month+1, day=1).strftime("%Y-%m-%d")
            return start, end

        def _period_bounds(label: str):
            today = date.today()
            y, m = today.year, today.month
            if label in ("Este Año", "Ejercicio Actual", "Todo el año"):
                return f"{y}-01-01", f"{y+1}-01-01"
            if label == "Año Anterior":
                return f"{y-1}-01-01", f"{y}-01-01"
            if label == "1º Trimestre":
                return f"{y}-01-01", f"{y}-04-01"
            if label == "2º Trimestre":
                return f"{y}-04-01", f"{y}-07-01"
            if label == "3º Trimestre":
                return f"{y}-07-01", f"{y}-10-01"
            if label == "4º Trimestre":
                return f"{y}-10-01", f"{y+1}-01-01"
            if label == "Total Histórico":
                return None, None
            # fallback: mes actual
            return _month_bounds(today)

        dfrom, dto = _period_bounds(periodo)

        where = ["estado = 'ÉXITO'"]
        params = []
        if dfrom:
            where.append("substr(fecha_envio,1,10) >= ?"); params.append(dfrom)
        if dto:
            where.append("substr(fecha_envio,1,10) < ?"); params.append(dto)
        if emisor and emisor != "ALL":
            where.append("empresa = ?"); params.append(emisor)

        sql = "SELECT fecha_envio, num_factura, IFNULL(importe,0.0), cliente, empresa, pdf_url FROM envios"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY fecha_envio DESC, id DESC"

        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            rows = cur.execute(sql, params).fetchall()
            conn.close()
        except Exception as e:
            self.dash_label_resultado.setText(f"Error consultando DB: {e}")
            return

        # volcar en tabla
        self.dash_table_resultados.setRowCount(0)
        total = 0.0
        for i, (fecha, factura, importe, cliente, empresa, pdf_url) in enumerate(rows):
            self.dash_table_resultados.insertRow(i)
            self.dash_table_resultados.setItem(i, 0, QTableWidgetItem(str(fecha)[:10]))
            self.dash_table_resultados.setItem(i, 1, QTableWidgetItem(str(factura or "")))
            self.dash_table_resultados.setItem(i, 2, QTableWidgetItem(str(cliente or "")))
            self.dash_table_resultados.setItem(i, 3, QTableWidgetItem(str(empresa or "")))
            item_imp = QTableWidgetItem(format_eur(importe or 0.0))
            item_imp.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.dash_table_resultados.setItem(i, 4, item_imp)

            # Botón Ver PDF
            btn_pdf = self._make_pdf_button(factura, pdf_url)
            if btn_pdf:
                self.dash_table_resultados.setCellWidget(i, 5, btn_pdf)

            total += float(importe or 0.0)

        self.dash_label_resultado.setText(f"Total: {format_eur(total)} en {len(rows)} facturas")
        header = self.dash_table_resultados.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)

    def filter_dashboard_table(self):
        """Filtra la tabla de resultados del dashboard según el texto de búsqueda."""
        search_text = self.dash_search_bar.text().strip().lower()
        for i in range(self.dash_table_resultados.rowCount()):
            factura_item = self.dash_table_resultados.item(i, 1)
            cliente_item = self.dash_table_resultados.item(i, 2)
            empresa_item = self.dash_table_resultados.item(i, 3)

            factura_text = factura_item.text().lower() if factura_item else ""
            cliente_text = cliente_item.text().lower() if cliente_item else ""
            empresa_text = empresa_item.text().lower() if empresa_item else ""

            # La fila es visible si el texto de búsqueda está en cualquiera de los campos relevantes
            is_match = (search_text in factura_text or
                        search_text in cliente_text or
                        search_text in empresa_text)

            self.dash_table_resultados.setRowHidden(i, not is_match)


    # ######################################################################
    # MÁS FUNCIONES QUE FALTABAN (HELPER UI)
    # ######################################################################

    def _update_send_badge(self):
        """Actualiza el texto del botón 'Enviar Facturas' en el sidebar."""
        try:
            # Buscar el item 2 (Enviar Facturas)
            item = self.nav_list.item(2) # Asumiendo que "Enviar" es el índice 2
            if not item:
                return

            count = self.loaded_invoice_count
            base_text = "🚀 Enviar Facturas"
            
            if count > 0:
                item.setText(f"{base_text} ({count})")
            else:
                item.setText(base_text)
        except Exception as e:
            print(f"Error actualizando badge: {e}")

    def clear_send_page(self):
        """Resetea la UI de la página de envío a su estado inicial."""
        # --- [MODIFICADO] Limpia también la tabla de previsualización y restaura la visibilidad ---
        if hasattr(self, "table_preview"):
            self.table_preview.setRowCount(0)
            self.table_preview.setVisible(True) # Aseguramos que sea visible

        if hasattr(self, "results_group"):
            self.results_group.setVisible(False) # Ocultamos los resultados

        if hasattr(self, "table_envio"):
            self.table_envio.setRowCount(0)
        if hasattr(self, "log_area"):
            self.log_area.clear()
        if hasattr(self, "progress"):
            self.progress.setValue(0)
            self.progress.setRange(0, 100) # Reset range in case it was indeterminate
        if hasattr(self, "send_stepper"):
            self.send_stepper.set_step(0)
        if hasattr(self, "search_bar"):
            self.search_bar.clear()
        if hasattr(self, "filters"):
            for status, btn in self.filters.items():
                btn.setChecked(False)
        if hasattr(self, "btn_download_pdfs"):
            self.btn_download_pdfs.setEnabled(False)
            
    def open_config_dialog(self):
        """Abre el diálogo de configuración de API."""
        dlg = ConfigDialog(self)
        # Aplicar el QSS actual
        style_sheet_content = self._get_themed_stylesheet()
        if style_sheet_content:
            dlg.setStyleSheet(style_sheet_content)
            dlg.setProperty("theme", self.theme)
        
        # Forzar repintado y centrado (similar al login)
        dlg.style().unpolish(dlg)
        dlg.style().polish(dlg)
        dlg.adjustSize()
        
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.availableGeometry()
            dlg_geometry = dlg.geometry()
            center_point = screen_geometry.center() - QPoint(dlg_geometry.width() // 2, dlg_geometry.height() // 2)
            dlg.move(center_point)
            
        dlg.exec()


    def export_results(self):
        """Exporta la tabla de resultados de envío (self.table_envio) a un CSV."""
        if not hasattr(self, 'table_envio') or self.table_envio.rowCount() == 0:
            self.show_toast("⚠️ No hay resultados para exportar.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Guardar resultados", "resultados_envio.csv", "CSV (*.csv)")
        if not path:
            return

        try:
            data = []
            headers = ["Factura", "Empresa Emisora", "Estado", "Detalles", "PDF_URL"]
            data.append(headers)

            for row in range(self.table_envio.rowCount()):
                factura = self.table_envio.item(row, 0).text() if self.table_envio.item(row, 0) else ""
                empresa = self.table_envio.item(row, 1).text() if self.table_envio.item(row, 1) else ""
                
                # Estado desde el Chip
                estado_widget = self.table_envio.cellWidget(row, 2)
                estado = ""
                if isinstance(estado_widget, StatusChip):
                    estado = estado_widget.text()
                
                detalles = self.table_envio.item(row, 3).text() if self.table_envio.item(row, 3) else ""
                
                # PDF URL (esto es más complejo, está en el botón)
                # Por simplicidad, lo dejaremos vacío. Si fuera crucial, necesitaríamos
                # almacenar la URL en el 'data' del item de la tabla.
                pdf_url = "" # Simplificación
                
                data.append([factura, empresa, estado, detalles, pdf_url])

            with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                import csv
                writer = csv.writer(f, delimiter=';') # Usar ; para Excel en español
                writer.writerows(data)
                
            self.show_toast(f"✅ Resultados exportados a {path}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.dirname(path))) # Abrir carpeta

        except Exception as e:
            self.show_error(f"Error al exportar CSV: {e}")

    # --- Toast (Notificaciones) ---
    def show_toast(self, message, duration=3000, color_class="info"):
        """Muestra una notificación toast."""
        if not hasattr(self, 'toast'):
            print(f"TOAST: {message}")
            return
            
        self.toast.setText(message)
        self.toast.setProperty("class", color_class) # info, success, warning, error
        self.toast.style().unpolish(self.toast)
        self.toast.style().polish(self.toast)
        
        self.toast.adjustSize()
        width = self.toast.width() + 40 # Añadir padding horizontal
        self.toast.setFixedWidth(width)
        
        start_y = self.height()
        end_y = self.height() - self.toast.height() - 20
        
        start_x = (self.width() - width) // 2
        
        start_rect = QRect(start_x, start_y, width, self.toast.height())
        end_rect = QRect(start_x, end_y, width, self.toast.height())
        
        self.toast.setGeometry(start_rect)
        self.toast.show()
        
        self.toast_anim.stop()
        self.toast_anim.setDuration(400)
        self.toast_anim.setStartValue(start_rect)
        self.toast_anim.setEndValue(end_rect)
        self.toast_anim.start()
        
        self.toast_timer.stop()
        self.toast_timer.start(duration)

    def hide_toast(self):
        """Oculta el toast con animación."""
        start_rect = self.toast.geometry()
        end_rect = QRect(start_rect.x(), self.height(), start_rect.width(), start_rect.height())
        
        self.toast_anim.stop()
        self.toast_anim.setDuration(300)
        self.toast_anim.setStartValue(start_rect)
        self.toast_anim.setEndValue(end_rect)
        self.toast_anim.start()
        
        # Ocultar realmente después de la animación
        QTimer.singleShot(300, self.toast.hide)
        
    # ######################################################################
    # FIN DEL BLOQUE CORREGIDO
    # ######################################################################


def main():
    # [NUEVO] Habilitar HiDPI
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    
    # Aplicar la fuente global ANTES de crear la ventana
    font = QFont("Segoe UI Variable", 15) # <-- Fuente y tamaño base
    
    # --- [CORRECCIÓN AttributeError] ---
    # El valor correcto es QFont.StyleStrategy.PreferQuality
    font.setStyleStrategy(QFont.StyleStrategy.PreferQuality)
    # --- [FIN CORRECCIÓN] ---
    
    app.setFont(font)
    
    # --- [NUEVO] Importar el shim ANTES de crear la ventana ---
    # Esto reemplaza QMessageBox.critical, .question, etc.
    try:
        import dialog_shim
    except ImportError:
        print("Advertencia: no se encontró 'dialog_shim.py' o 'modern_dialogs.py'. Se usarán diálogos nativos.")
    # --- [FIN NUEVO] ---

    window = MainWindow()

    # [NUEVO] Forzar el repintado inicial después de mostrar la ventana
    window.show()
    # Usar QTimer.singleShot para asegurar que _refresh_styles se ejecute después de que la ventana sea visible
    QTimer.singleShot(100, window._refresh_styles) # Aumentado ligero delay

    # El login se ejecuta después de mostrar la ventana principal
    if window.require_login():
        sys.exit(app.exec())
    else:
        sys.exit(0) # Salir si el login es cancelado


if __name__ == "__main__":
    main()