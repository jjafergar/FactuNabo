# Guía de Uso - iOS 26 Design System

## Para Desarrolladores

Esta guía muestra cómo aplicar los estilos iOS 26 en FactuNabo.

## 🚀 Inicio Rápido

### 1. Cargar los Estilos

```python
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)

# Cargar el archivo de estilos
with open("styles.qss", "r", encoding="utf-8") as f:
    app.setStyleSheet(f.read())
```

### 2. Aplicar Clase a un Widget

```python
from PySide6.QtWidgets import QPushButton

# Botón con estilo iOS 26
button = QPushButton("Enviar")
button.setProperty("class", "AnimatedButton")
button.setMinimumHeight(48)  # Altura accesible iOS
```

## 🎨 Componentes Disponibles

### Botones Primarios

```python
button = QPushButton("Aceptar")
button.setProperty("class", "AnimatedButton")
button.setMinimumHeight(48)

# El botón automáticamente tendrá:
# - Color azul iOS 26 (#007AFF)
# - Bordes redondeados (14px)
# - Animación de sombra en hover
# - Padding adecuado (14px 28px)
```

**Resultado**:
- Color de fondo: `#007AFF`
- Texto: blanco, bold, 16px
- Sombra animada con efecto hover
- Altura mínima: 48px (accesibilidad)

### Cards/Tarjetas

```python
from PySide6.QtWidgets import QFrame

card = QFrame()
card.setProperty("class", "StatCard")

# Aplicar sombra iOS 26
from main import apply_shadow
apply_shadow(card)

# El card automáticamente tendrá:
# - Fondo vidriado (rgba(255,255,255,0.92))
# - Bordes redondeados (20px)
# - Padding generoso (24px)
# - Sombra sutil
```

### Inputs de Texto

```python
from PySide6.QtWidgets import QLineEdit

input_field = QLineEdit()
input_field.setPlaceholderText("Escribe aquí...")
input_field.setMinimumHeight(44)

# Automáticamente tendrá:
# - Bordes redondeados (12px)
# - Padding iOS (12px 16px)
# - Focus azul iOS (#007AFF)
```

### Status Chips/Badges

```python
from PySide6.QtWidgets import QLabel

# Badge de éxito
badge = QLabel("Completado")
badge.setProperty("class", "StatusChip")
badge.setProperty("status", "success")

# Badge de advertencia
badge_warning = QLabel("Pendiente")
badge_warning.setProperty("class", "StatusChip")
badge_warning.setProperty("status", "warning")

# Badge de error
badge_error = QLabel("Error")
badge_error.setProperty("class", "StatusChip")
badge_error.setProperty("status", "NABO!")
```

**Colores automáticos**:
- `success`: Verde `#34C759`
- `warning`: Naranja `#FF9F0A`
- `NABO!`: Rojo `#FF3B30`

### Navegación Sidebar

```python
from PySide6.QtWidgets import QListWidget, QListWidgetItem

nav_list = QListWidget()
nav_list.setProperty("class", "NavList")

# Añadir items
items = ["📊 Dashboard", "📜 Histórico", "⚙️ Configuración"]
for item_text in items:
    item = QListWidgetItem(item_text)
    nav_list.addItem(item)

# Automáticamente tendrá:
# - Pills redondeadas (14px)
# - Hover sutil
# - Selección azul iOS (#007AFF)
# - Espaciado optimizado
```

### Tablas Modernas

```python
from PySide6.QtWidgets import QTableWidget

table = QTableWidget()
table.setProperty("class", "ModernTable")

# Automáticamente tendrá:
# - Bordes redondeados (16px)
# - Selección azul translúcida
# - Hover sutil
# - Headers con tipografía clara
```

### Áreas de Texto

```python
from PySide6.QtWidgets import QTextEdit

log_area = QTextEdit()
log_area.setReadOnly(True)

# Automáticamente tendrá:
# - Fuente monoespaciada (SF Mono/Consolas)
# - Bordes redondeados (12px)
# - Scroll suave
```

### Progress Bars

```python
from PySide6.QtWidgets import QProgressBar

progress = QProgressBar()
progress.setValue(75)

# Automáticamente tendrá:
# - Altura delgada (8px)
# - Color azul iOS (#007AFF)
# - Bordes redondeados (4px)
# - Fondo suave
```

### Checkboxes

```python
from PySide6.QtWidgets import QCheckBox

checkbox = QCheckBox("Modo Oscuro")

# Automáticamente tendrá:
# - Indicador redondeado (6px)
# - Color azul iOS cuando checked
# - Icono de check (✓) SVG
```

## 🌓 Modo Oscuro

### Activar Tema Oscuro

```python
from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.setProperty("theme", "dark")
        else:
            self.setProperty("theme", "light")
        
        # Refrescar estilos
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
```

**Colores automáticos en modo oscuro**:
- Fondo: `#000000` (negro puro OLED)
- Cards: `rgba(28, 28, 30, 0.72)` (vidrio oscuro)
- Texto: `#F5F5F7` (blanco suave)
- Primary: `#0A84FF` (azul brillante)

## 🎯 Funciones Helper

### Aplicar Sombra iOS 26

```python
from main import apply_shadow

# Sombra por defecto (blur=24, offset=6, alpha=25)
apply_shadow(my_widget)

# Sombra personalizada
apply_shadow(my_widget, blur=32, offset_y=8, color_str="#000000")
```

### Usar Colores Constantes

```python
from main import (
    COLOR_PRIMARY,    # #007AFF - Azul iOS 26
    COLOR_SUCCESS,    # #34C759 - Verde
    COLOR_WARNING,    # #FF9F0A - Naranja
    COLOR_ERROR,      # #FF3B30 - Rojo
    COLOR_BACKGROUND, # #F5F5F7 - Fondo claro
    COLOR_TEXT,       # #1D1D1F - Texto principal
)

# Usar en código
button.setStyleSheet(f"background-color: {COLOR_PRIMARY};")
```

## 📐 Layouts Recomendados

### Card con Contenido

```python
from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel

card = QFrame()
card.setProperty("class", "StatCard")
apply_shadow(card)

layout = QVBoxLayout(card)
layout.setContentsMargins(24, 24, 24, 24)  # Padding iOS 26
layout.setSpacing(16)  # Espaciado cómodo

title = QLabel("Facturas Enviadas")
title.setStyleSheet("font-size: 20px; font-weight: 600;")

value = QLabel("1,234")
value.setStyleSheet(f"font-size: 34px; font-weight: 700; color: {COLOR_PRIMARY};")

layout.addWidget(title)
layout.addWidget(value)
```

### Formulario iOS Style

```python
from PySide6.QtWidgets import QFormLayout, QLineEdit, QPushButton

form_layout = QFormLayout()
form_layout.setSpacing(16)  # Espaciado iOS
form_layout.setContentsMargins(24, 24, 24, 24)

# Labels
form_layout.addRow("Nombre:", QLineEdit())
form_layout.addRow("Email:", QLineEdit())
form_layout.addRow("Teléfono:", QLineEdit())

# Botón submit
submit_btn = QPushButton("Guardar")
submit_btn.setProperty("class", "AnimatedButton")
submit_btn.setMinimumHeight(48)
form_layout.addRow("", submit_btn)
```

### Sidebar con Navegación

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel

sidebar = QWidget()
sidebar.setProperty("class", "Sidebar")
sidebar.setFixedWidth(260)  # Ancho iOS típico

layout = QVBoxLayout(sidebar)
layout.setContentsMargins(16, 24, 16, 24)
layout.setSpacing(8)

# Logo/Título
title = QLabel("FactuNabo")
title.setStyleSheet("font-size: 24px; font-weight: 700;")
layout.addWidget(title)

layout.addSpacing(20)

# Navegación
nav_list = QListWidget()
nav_list.setProperty("class", "NavList")
layout.addWidget(nav_list)
```

## ✨ Animaciones Personalizadas

### Animar Propiedad

```python
from PySide6.QtCore import QPropertyAnimation, QEasingCurve

animation = QPropertyAnimation(widget, b"geometry")
animation.setDuration(200)  # iOS 26 timing
animation.setEasingCurve(QEasingCurve.OutCubic)
animation.setStartValue(start_rect)
animation.setEndValue(end_rect)
animation.start()
```

### Fade In/Out

```python
from PySide6.QtCore import QPropertyAnimation
from PySide6.QtWidgets import QGraphicsOpacityEffect

# Crear efecto de opacidad
opacity_effect = QGraphicsOpacityEffect(widget)
widget.setGraphicsEffect(opacity_effect)

# Animar
fade = QPropertyAnimation(opacity_effect, b"opacity")
fade.setDuration(200)
fade.setStartValue(0.0)
fade.setEndValue(1.0)
fade.setEasingCurve(QEasingCurve.OutCubic)
fade.start()
```

## 🔍 Debugging de Estilos

### Ver Propiedades Aplicadas

```python
# Verificar clase asignada
print(widget.property("class"))  # Debe mostrar "AnimatedButton", etc.

# Verificar tema
print(window.property("theme"))  # "dark" o "light"
```

### Refrescar Estilos Dinámicamente

```python
# Después de cambiar una propiedad
widget.style().unpolish(widget)
widget.style().polish(widget)
widget.update()
```

## 📱 Consejos de Diseño

### ✅ Hacer

- Usar `COLOR_PRIMARY` para acciones principales
- Mantener altura mínima de botones en 48px
- Aplicar `apply_shadow()` a cards elevadas
- Usar spacing de 8, 16, 24px (múltiplos de 8)
- Mantener texto legible (mínimo 13px)
- Usar border-radius generoso (12-20px)

### ❌ Evitar

- No usar colores fuera de la paleta iOS 26
- No crear botones menores a 44x44px
- No usar sombras muy oscuras (alpha > 40)
- No mezclar estilos de diferentes versiones
- No usar padding impares (preferir 12, 16, 20, 24)
- No sobrecargar con animaciones

## 🎨 Paleta Rápida

```python
# Copiar y pegar en tu código
COLORS = {
    "primary": "#007AFF",
    "success": "#34C759",
    "warning": "#FF9F0A",
    "error": "#FF3B30",
    "background": "#F5F5F7",
    "text": "#1D1D1F",
    "text_secondary": "#86868B",
    "border": "#D1D1D6",
}
```

## 📚 Ejemplos Completos

### Diálogo Modal iOS Style

```python
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton

class IOSDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        # Título
        title = QLabel("Confirmar Acción")
        title.setStyleSheet("font-size: 20px; font-weight: 600;")
        layout.addWidget(title)
        
        # Mensaje
        message = QLabel("¿Estás seguro de que deseas continuar?")
        message.setStyleSheet("color: #86868B;")
        layout.addWidget(message)
        
        layout.addStretch()
        
        # Botones
        btn_confirm = QPushButton("Confirmar")
        btn_confirm.setProperty("class", "AnimatedButton")
        btn_confirm.setMinimumHeight(48)
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet("""
            background-color: #E5E5EA;
            border-radius: 14px;
            padding: 14px 28px;
            min-height: 48px;
        """)
        
        layout.addWidget(btn_confirm)
        layout.addWidget(btn_cancel)
```

### Dashboard Card

```python
def create_stat_card(title, value, color=COLOR_PRIMARY):
    card = QFrame()
    card.setProperty("class", "StatCard")
    apply_shadow(card)
    
    layout = QVBoxLayout(card)
    layout.setContentsMargins(24, 24, 24, 24)
    
    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 16px; color: #86868B;")
    
    value_label = QLabel(str(value))
    value_label.setStyleSheet(f"""
        font-size: 34px;
        font-weight: 700;
        color: {color};
    """)
    
    layout.addWidget(title_label)
    layout.addWidget(value_label)
    layout.addStretch()
    
    return card

# Uso
card = create_stat_card("Total Facturas", "1,234", COLOR_PRIMARY)
```

---

## 🎓 Recursos Adicionales

- **DESIGN_SYSTEM.md**: Especificaciones completas del sistema de diseño
- **BEFORE_AFTER.md**: Comparativa de cambios aplicados
- **styles.qss**: Archivo de estilos completo
- **main.py**: Implementación de referencia

## 🆘 Soporte

Si tienes dudas sobre cómo aplicar los estilos, consulta los archivos de ejemplo en el repositorio o revisa la implementación en `main.py`.

---

**Versión**: iOS 26 Design System v1.0
**Última actualización**: Noviembre 2025
