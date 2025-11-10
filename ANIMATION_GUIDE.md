# Guía de Uso - Nuevas Animaciones y Efectos

## 🎨 Mejoras Implementadas

### 1. **RippleButton** - Botón con Efecto Ripple ⭐⭐⭐

Reemplaza `AnimatedButton` con `RippleButton` para obtener efecto ripple Material Design.

#### Uso Básico:
```python
from ripple_button import RippleButton

# Crear botón con ripple effect
btn = RippleButton("Enviar Factura")
btn.setProperty("class", "AnimatedButton")  # Aplica estilos CSS
```

#### Características:
- ✅ Efecto ripple circular al hacer click
- ✅ Animación de sombra en hover (heredado de AnimatedButton)
- ✅ Contracción de sombra al presionar
- ✅ Color ripple blanco semi-transparente sobre verde

---

### 2. **Animations Module** - Helpers de Animación

Módulo con utilidades reutilizables para animaciones.

#### 2.1 Fade In/Out
```python
from animations import FadeAnimation

# Fade in un widget
FadeAnimation.fade_in(my_widget, duration=300)

# Fade out con callback
def on_hidden():
    my_widget.hide()

FadeAnimation.fade_out(my_widget, duration=300, on_finished=on_hidden)
```

#### 2.2 Slide Animations
```python
from animations import SlideAnimation

# Slide in desde arriba
SlideAnimation.slide_in(widget, direction='down', distance=50, duration=300)

# Slide out hacia la derecha
SlideAnimation.slide_out(widget, direction='right', distance=100, duration=250)
```

Direcciones disponibles: `'up'`, `'down'`, `'left'`, `'right'`

#### 2.3 Stagger Animations (Lista con efecto cascada)
```python
from animations import StaggerAnimation

# Animar lista de widgets con delay escalonado
widgets = [card1, card2, card3, card4]
StaggerAnimation.animate_items(widgets, delay=50, duration=250)

# Resultado: card1 aparece, luego card2 (+50ms), luego card3 (+50ms), etc.
```

#### 2.4 Hover Scale Effect (Cards interactivas)
```python
from animations import HoverScaleEffect

# Aplicar efecto scale en hover
card = QFrame()
card.setProperty("class", "StatCard")

effect = HoverScaleEffect(card, scale_factor=1.02, duration=200)
# Ahora el card se agranda ligeramente al pasar el mouse
```

#### 2.5 Progress Bar Animado
```python
from animations import ProgressAnimation

# Animar progress bar suavemente
progress_bar = QProgressBar()
progress_bar.setValue(0)

# Animar de 0 a 75 en 500ms
ProgressAnimation.animate_to(progress_bar, 75, duration=500)
```

---

### 3. **Input Focus Mejorado**

Los inputs ahora tienen border más grueso (2px) al hacer focus para mejor feedback visual.

#### Antes:
```css
QLineEdit:focus {
    border: 1px solid #A0BF6E;
}
```

#### Ahora:
```css
QLineEdit:focus {
    border: 2px solid #A0BF6E;  /* Más visible */
}
```

**Efecto visual**: El borde se hace más grueso y verde al hacer focus, indicando claramente el input activo.

---

## 📖 Ejemplos Completos

### Ejemplo 1: Dashboard con Cards Animados

```python
from PySide6.QtWidgets import QFrame, QVBoxLayout
from animations import StaggerAnimation, HoverScaleEffect

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Crear cards
        cards = []
        for i in range(4):
            card = QFrame()
            card.setProperty("class", "StatCard")
            # ... configurar card ...
            
            # Aplicar hover effect
            HoverScaleEffect(card, scale_factor=1.02)
            
            layout.addWidget(card)
            cards.append(card)
        
        # Animar entrada con stagger
        StaggerAnimation.animate_items(cards, delay=75, duration=300)
```

**Resultado**: 
- Cards aparecen con efecto cascada
- Al pasar mouse, el card se agranda ligeramente
- Efecto profesional y moderno

---

### Ejemplo 2: Formulario con Fade In

```python
from ripple_button import RippleButton
from animations import FadeAnimation, SlideAnimation

class FormDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        # ... configurar formulario ...
        
        # Botón con ripple
        submit_btn = RippleButton("Guardar")
        submit_btn.setProperty("class", "AnimatedButton")
        submit_btn.clicked.connect(self._on_submit)
        
        # Animar entrada del diálogo
        FadeAnimation.fade_in(self, duration=200)
        SlideAnimation.slide_in(self, direction='down', distance=30)
    
    def _on_submit(self):
        # Animar salida
        FadeAnimation.fade_out(self, duration=200, on_finished=self.accept)
```

**Resultado**:
- Diálogo aparece con fade + slide
- Botón tiene ripple effect
- Cierre animado al guardar

---

### Ejemplo 3: Progress Bar Animado

```python
from animations import ProgressAnimation

class UploadWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = QProgressBar()
        self.progress.setValue(0)
        # ... layout ...
    
    def start_upload(self):
        # Simular upload con animación suave
        self.progress.setValue(0)
        
        # Animar a 100% en 3 segundos
        ProgressAnimation.animate_to(self.progress, 100, duration=3000)
```

**Resultado**: 
- Progress bar se llena suavemente
- Sin saltos bruscos
- Animación fluida

---

### Ejemplo 4: Notificación Toast Mejorada

```python
from animations import FadeAnimation, SlideAnimation

class Toast(QLabel):
    def __init__(self, message, parent):
        super().__init__(message, parent)
        self.setProperty("id", "toast")
        
        # Posicionar arriba
        self.move((parent.width() - self.width()) // 2, -100)
        
        # Animar entrada
        self.show()
        FadeAnimation.fade_in(self, duration=200)
        SlideAnimation.slide_in(self, direction='down', distance=120, duration=300)
        
        # Auto-dismiss después de 3 segundos
        QTimer.singleShot(3000, self._dismiss)
    
    def _dismiss(self):
        def on_finished():
            self.deleteLater()
        
        FadeAnimation.fade_out(self, duration=200, on_finished=on_finished)
        SlideAnimation.slide_out(self, direction='up', distance=50, duration=200)
```

**Resultado**:
- Toast aparece desde arriba con fade
- Se mantiene 3 segundos
- Desaparece con fade + slide

---

## 🎯 Integración con Código Existente

### Reemplazar AnimatedButton con RippleButton

**Antes:**
```python
from main import AnimatedButton

btn = AnimatedButton("Click Me")
```

**Después:**
```python
from ripple_button import RippleButton

btn = RippleButton("Click Me")
# Tiene todas las funciones de AnimatedButton + ripple effect
```

**Compatible**: RippleButton hereda de AnimatedButton, así que es 100% compatible.

---

### Añadir Animaciones a Widgets Existentes

No necesitas reescribir código, solo añade animaciones:

```python
# Widget existente
my_card = QFrame()
# ... código existente ...

# Añadir hover effect (no invasivo)
from animations import HoverScaleEffect
HoverScaleEffect(my_card)

# Andar fade in al mostrarlo
from animations import FadeAnimation
FadeAnimation.fade_in(my_card)
```

---

## ⚡ Performance

### Consideraciones:
- ✅ **RippleButton**: Muy ligero, 60 FPS
- ✅ **FadeAnimation**: Usa GPU acceleration
- ✅ **SlideAnimation**: Smooth, no lag
- ✅ **StaggerAnimation**: Ligero, max 20 items recomendado
- ⚠️ **HoverScaleEffect**: Evitar en +50 cards simultáneos

### Optimizaciones:
- Las animaciones se auto-limpian al terminar
- Timers se detienen automáticamente
- No hay memory leaks

---

## 🎨 Personalización

### Cambiar Color Ripple:
```python
btn = RippleButton("Click")
btn.ripple_color = QColor(0, 122, 255, 100)  # Azul semi-transparente
```

### Ajustar Duración de Animaciones:
```python
# Fade más rápido
FadeAnimation.fade_in(widget, duration=150)

# Slide más lento
SlideAnimation.slide_in(widget, duration=500)

# Progress muy suave
ProgressAnimation.animate_to(progress, 100, duration=2000)
```

### Cambiar Easing Curves:
Las animaciones usan `OutCubic` por defecto, pero puedes modificar el código:

```python
# En animations.py
anim.setEasingCurve(QEasingCurve.OutBack)  # Bounce effect
anim.setEasingCurve(QEasingCurve.InOutQuad)  # Más suave
anim.setEasingCurve(QEasingCurve.OutElastic)  # Elástico
```

---

## 📦 Archivos Nuevos

```
FactuNabo/
├── animations.py          # ✨ NUEVO - Utilidades de animación
├── ripple_button.py       # ✨ NUEVO - Botón con ripple effect
├── ANIMATION_PROPOSAL.md  # ✨ NUEVO - Propuesta completa
└── ANIMATION_GUIDE.md     # ✨ NUEVO - Esta guía
```

---

## 🚀 Próximos Pasos

1. **Probar RippleButton** en main.py
2. **Añadir HoverScaleEffect** a StatCards
3. **Usar StaggerAnimation** al cargar listas
4. **Implementar ProgressAnimation** en uploads

**Documentación completa en**: `ANIMATION_PROPOSAL.md`

---

¿Necesitas ayuda implementando alguna animación específica?
