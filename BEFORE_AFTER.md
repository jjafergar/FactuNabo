# Comparativa: Antes y Después - iOS 26 Modernization

## Resumen de Cambios

Este documento muestra los cambios específicos realizados para modernizar FactuNabo con estética iOS 26.

## 🎨 Cambios de Color Principal

### Antes (Verde personalizado)
```python
COLOR_PRIMARY = "#A0BF6E"  # Verde personalizado
COLOR_WARNING = "#FF9500"   # Naranja
```

### Después (Azul iOS 26)
```python
COLOR_PRIMARY = "#007AFF"   # Azul iOS 26 oficial
COLOR_WARNING = "#FF9F0A"   # Naranja iOS 26 actualizado
```

**Impacto**: Mayor consistencia con el ecosistema iOS, colores más vibrantes y reconocibles.

---

## 📐 Bordes Redondeados

### Antes
```css
/* Inputs */
border-radius: 10px;

/* Cards */
border-radius: 16px;

/* Botones */
border-radius: 12px;
```

### Después (iOS 26)
```css
/* Inputs */
border-radius: 12px;  /* +2px más suave */

/* Cards */
border-radius: 20px;  /* +4px más redondeado */

/* Botones */
border-radius: 14px;  /* +2px más suave */

/* Navigation Pills */
border-radius: 14px;  /* +4px más redondeado */
```

**Impacto**: Apariencia más suave y moderna, siguiendo las últimas tendencias de diseño iOS.

---

## 🌟 Sombras

### Antes
```python
def apply_shadow(widget, blur=20, offset_y=4, color_str="#000000"):
    shadow.setBlurRadius(blur)
    color.setAlpha(40)  # Sombra moderada
    shadow.setOffset(0, offset_y)
```

### Después (iOS 26)
```python
def apply_shadow(widget, blur=24, offset_y=6, color_str="#000000"):
    shadow.setBlurRadius(blur)  # +4px más difuminado
    color.setAlpha(25)  # Sombra más sutil (-15)
    shadow.setOffset(0, offset_y)  # +2px más elevado
```

**Impacto**: Sombras más sutiles y naturales, creando profundidad sin ser invasivas.

---

## 🔘 Botones Animados

### Antes
```python
# AnimatedButton
self._shadow.setBlurRadius(18)
color = QColor(0, 0, 0, 60)
self._shadow.setOffset(0, 4)
self._anim_blur.setDuration(180)

# Hover
setEndValue(30)  # blur
setEndValue(6)   # offset
```

### Después (iOS 26)
```python
# AnimatedButton
self._shadow.setBlurRadius(24)  # +6px más difuminado
color = QColor(0, 0, 0, 35)     # -25 más sutil
self._shadow.setOffset(0, 6)    # +2px más elevado
self._anim_blur.setDuration(200) # +20ms más suave

# Hover
setEndValue(32)  # blur (+2px más pronunciado)
setEndValue(8)   # offset (+2px mayor elevación)
```

**Impacto**: Animaciones más fluidas y elegantes, con feedback visual mejorado.

---

## 📝 Inputs y Formularios

### Antes
```css
QLineEdit {
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid #E5E5EA;
    font-size: 15px;
}

QLineEdit:focus {
    border: 1px solid #A0BF6E;  /* Verde */
}
```

### Después (iOS 26)
```css
QLineEdit {
    padding: 12px 16px;         /* +2px más espacioso */
    border-radius: 12px;        /* +2px más redondeado */
    border: 1px solid #D1D1D6;  /* Borde más sutil */
    font-size: 15px;
}

QLineEdit:focus {
    border: 1px solid #007AFF;  /* Azul iOS 26 */
}
```

**Impacto**: Inputs más cómodos y accesibles, con feedback visual iOS.

---

## 🎴 Cards y Contenedores

### Antes
```css
QFrame[class="StatCard"] {
    background-color: rgba(255, 255, 255, 0.88);
    border-radius: 16px;
    padding: 20px;
}
```

### Después (iOS 26)
```css
QFrame[class="StatCard"] {
    background-color: rgba(255, 255, 255, 0.92);  /* +4% más opaco */
    border-radius: 20px;                          /* +4px más redondeado */
    padding: 24px;                                /* +4px más espacioso */
    border: none;                                 /* Sin borde para look flotante */
}
```

**Impacto**: Cards con aspecto más premium y "flotante", mejor separación visual.

---

## 🧭 Navegación Sidebar

### Antes
```css
QListWidget[class="NavList"]::item {
    border-radius: 10px;
    padding: 12px 16px;
    margin: 3px 0px;
}

QListWidget[class="NavList"]::item:hover {
    background-color: rgba(160, 191, 110, 0.15);  /* Verde */
}

QListWidget[class="NavList"]::item:selected {
    background-color: #A0BF6E;  /* Verde */
}
```

### Después (iOS 26)
```css
QListWidget[class="NavList"]::item {
    border-radius: 14px;        /* +4px más redondeado */
    padding: 14px 18px;         /* +2px más espacioso */
    margin: 4px 6px;            /* Márgenes horizontales añadidos */
    font-weight: 500;
}

QListWidget[class="NavList"]::item:hover {
    background-color: rgba(0, 0, 0, 0.05);  /* Hover más sutil */
}

QListWidget[class="NavList"]::item:selected {
    background-color: #007AFF;  /* Azul iOS 26 */
    font-weight: 600;
}
```

**Impacto**: Navegación más moderna y consistente con iOS, mejor jerarquía visual.

---

## 🏷️ Status Chips (Badges)

### Antes
```css
QLabel[class="StatusChip"] {
    border-radius: 13px;
    padding: 4px 14px;
    font-size: 12px;
    min-width: 80px;
    max-height: 26px;
}
```

### Después (iOS 26)
```css
QLabel[class="StatusChip"] {
    border-radius: 14px;  /* +1px más redondeado */
    padding: 6px 16px;    /* +2px más espacioso */
    font-size: 13px;      /* +1px más legible */
    min-width: 90px;      /* +10px más ancho */
    max-height: 28px;     /* +2px más alto */
}
```

**Impacto**: Badges más legibles y cómodas visualmente.

---

## 🌓 Efectos de Vidrio

### Antes
```css
QWidget[class="Sidebar"] {
    background-color: rgba(250, 250, 250, 0.72);
}
```

### Después (iOS 26)
```css
QWidget[class="Sidebar"] {
    background-color: rgba(255, 255, 255, 0.78);  /* Blanco más puro, +6% opacidad */
}
```

**Impacto**: Efecto glassmorphism más pronunciado y premium.

---

## 📊 Tablas

### Antes
```css
QTableWidget[class="ModernTable"] {
    selection-background-color: rgba(160, 191, 110, 0.2);  /* Verde */
}

QTableWidget[class="ModernTable"]::item:hover {
    background-color: rgba(160, 191, 110, 0.15);  /* Verde */
}
```

### Después (iOS 26)
```css
QTableWidget[class="ModernTable"] {
    selection-background-color: rgba(0, 122, 255, 0.15);  /* Azul iOS */
}

QTableWidget[class="ModernTable"]::item:hover {
    background-color: rgba(0, 122, 255, 0.12);  /* Azul iOS */
}
```

**Impacto**: Selección más reconocible y consistente con el sistema.

---

## 📱 Fondo de la Aplicación

### Antes
```css
QMainWindow {
    background-color: #F2F2F7;  /* Gris iOS estándar */
}
```

### Después (iOS 26)
```css
QMainWindow {
    background-color: #F5F5F7;  /* Gris más suave y claro */
}
```

**Impacto**: Fondo más luminoso y limpio, mejor para contenido.

---

## 🎯 Colores de Texto

### Antes
```python
COLOR_TEXT = "#000000"              # Negro puro
COLOR_SECONDARY_TEXT = "#8E8E93"    # Gris estándar
```

### Después (iOS 26)
```python
COLOR_TEXT = "#1D1D1F"              # Negro suave (menos duro)
COLOR_SECONDARY_TEXT = "#86868B"    # Gris iOS 26 actualizado
```

**Impacto**: Texto menos agresivo, más cómodo para lectura prolongada.

---

## 🔄 Animaciones

### Antes
```python
self._anim_blur.setDuration(180)  # ms
self._anim_blur.setEasingCurve(QEasingCurve.OutCubic)
```

### Después (iOS 26)
```python
self._anim_blur.setDuration(200)  # +20ms más suave
self._anim_blur.setEasingCurve(QEasingCurve.OutCubic)  # Mismo easing
```

**Impacto**: Transiciones ligeramente más lentas, más naturales y fluidas.

---

## 📈 Resumen de Mejoras

| Aspecto | Mejora | Beneficio |
|---------|--------|-----------|
| **Colores** | iOS 26 oficial | Mayor reconocimiento y consistencia |
| **Bordes** | +2 a +4px | Aspecto más suave y moderno |
| **Sombras** | Más sutiles (-15 alpha) | Profundidad sin ser invasiva |
| **Espaciado** | +2 a +4px | Mejor legibilidad y comodidad |
| **Animaciones** | +20ms | Mayor fluidez y naturalidad |
| **Tipografía** | SF Pro equivalente | Mejor legibilidad |
| **Accesibilidad** | 48px min height | Cumple guías Apple HIG |
| **Efectos** | Glassmorphism mejorado | Look premium y moderno |

---

## 🎨 Paleta Completa: Antes vs Después

### Colores Primarios

| Propósito | Antes | Después | Cambio |
|-----------|-------|---------|--------|
| Primary | `#A0BF6E` 🟢 | `#007AFF` 🔵 | Verde → Azul iOS |
| Success | `#34C759` 🟢 | `#34C759` 🟢 | Sin cambio |
| Warning | `#FF9500` 🟠 | `#FF9F0A` 🟠 | Actualizado iOS 26 |
| Error | `#FF3B30` 🔴 | `#FF3B30` 🔴 | Sin cambio |

### Colores de Fondo

| Propósito | Antes | Después | Cambio |
|-----------|-------|---------|--------|
| Background | `#F2F2F7` | `#F5F5F7` | Más claro |
| Card | `#FFFFFF` | `#FFFFFF` | Sin cambio |
| Sidebar | `#FAFAFA` | `#FFFFFF` | Blanco puro |

---

## ✅ Checklist de Cambios Aplicados

- [x] Color primario: Verde → Azul iOS 26
- [x] Border radius: +2 a +4px en todos los componentes
- [x] Sombras: Más sutiles (alpha 40→25)
- [x] Padding: +2 a +4px para mejor espaciado
- [x] Animaciones: +20ms más fluidas
- [x] Fondo: Más claro y luminoso
- [x] Texto: Negro duro → Negro suave
- [x] Hover: Efectos más sutiles
- [x] Focus: Verde → Azul iOS
- [x] Glassmorphism: Opacidad optimizada
- [x] Navegación: Pills más redondeadas
- [x] Badges: Más grandes y legibles
- [x] Inputs: Altura y padding iOS
- [x] Botones: Min-height 48px (accesibilidad)
- [x] Tablas: Selección azul iOS

---

**Resultado Final**: Una interfaz completamente modernizada que sigue fielmente las guías de diseño iOS 26, con colores vibrantes, formas suaves, sombras sutiles y animaciones fluidas.
