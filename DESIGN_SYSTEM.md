# iOS 26 Design System - FactuNabo

## Guía Visual de Modernización

Esta documentación describe el sistema de diseño iOS 26 aplicado a FactuNabo.

## 🎨 Paleta de Colores

### Colores Primarios

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| **iOS Blue** | `#007AFF` | `rgb(0, 122, 255)` | Botones primarios, enlaces, elementos activos |
| **iOS Green** | `#34C759` | `rgb(52, 199, 89)` | Éxito, confirmaciones, estados completados |
| **iOS Orange** | `#FF9F0A` | `rgb(255, 159, 10)` | Advertencias, estados pendientes |
| **iOS Red** | `#FF3B30` | `rgb(255, 59, 48)` | Errores, acciones destructivas |

### Colores de Fondo (Light Mode)

| Color | Hex | Opacidad | Uso |
|-------|-----|----------|-----|
| **Background** | `#F5F5F7` | 100% | Fondo principal de la aplicación |
| **Card** | `#FFFFFF` | 92% | Tarjetas y contenedores elevados |
| **Sidebar** | `#FFFFFF` | 78% | Barra lateral con efecto vidrio |

### Colores de Texto

| Color | Hex | Uso |
|-------|-----|-----|
| **Primary Text** | `#1D1D1F` | Texto principal y títulos |
| **Secondary Text** | `#86868B` | Texto de apoyo, labels, placeholders |
| **Tertiary Text** | `#AEAEB2` | Texto deshabilitado |

### Colores de Borde

| Color | Hex | Uso |
|-------|-----|-----|
| **Border** | `#D1D1D6` | Bordes de inputs, separadores |
| **Light Border** | `#E5E5EA` | Bordes muy sutiles |

## 📐 Geometría y Espaciado

### Border Radius (Esquinas Redondeadas)

```css
/* Componentes por tamaño */
Small Components (Badges, Chips):     14px
Medium Components (Buttons, Inputs):   12px
Large Components (Cards, Dialogs):     20px
Sidebar Navigation Pills:              14px
```

### Padding y Spacing

```css
/* Espaciado interno */
Buttons:          14px 28px  (vertical horizontal)
Inputs:           12px 16px
Cards:            24px (todos los lados)
Status Chips:     6px 16px

/* Márgenes entre elementos */
Tight:            4px
Normal:           8px
Comfortable:      16px
Spacious:         24px
```

### Alturas de Componentes

```css
/* Siguiendo guías de accesibilidad Apple */
Buttons:          min-height: 48px
Inputs:           height: 44px
Status Chips:     max-height: 28px
Progress Bar:     height: 8px
```

## 🌟 Efectos Visuales

### Sombras (Shadows)

```css
/* Sombras sutiles iOS 26 */
Default Card Shadow:
  - blur-radius: 24px
  - offset-y: 6px
  - color: rgba(0, 0, 0, 0.25)

Button Hover Shadow:
  - blur-radius: 32px
  - offset-y: 8px
  - color: rgba(0, 0, 0, 0.35)
```

### Efectos de Vidrio (Glassmorphism)

```css
Sidebar Light:      rgba(255, 255, 255, 0.78)
Card Light:         rgba(255, 255, 255, 0.92)
Sidebar Dark:       rgba(28, 28, 30, 0.72)
Card Dark:          rgba(28, 28, 30, 0.72)
```

### Estados de Hover

```css
/* Tintes translúcidos */
Light Mode Hover:   rgba(0, 122, 255, 0.12)
Dark Mode Hover:    rgba(10, 132, 255, 0.15)
```

## ✨ Animaciones

### Duración y Easing

```css
/* Todas las transiciones */
Duration:         200ms
Easing:           cubic-bezier(0.25, 0.1, 0.25, 1.0)  /* OutCubic */

/* Animaciones específicas */
Button Shadow:    200ms OutCubic
Hover State:      200ms OutCubic
Focus State:      150ms OutCubic
```

### Propiedades Animadas

- Sombras (blur-radius, offset)
- Opacidad
- Colores de fondo
- Escalas sutiles (opcional)

## 🔤 Tipografía

### Familias de Fuentes

```css
/* Preferencia en cascada */
Primary:    "SF Pro Display", "Segoe UI Variable", -apple-system, sans-serif
Text:       "SF Pro Text", "Segoe UI Variable", sans-serif
Mono:       "SF Mono", "Consolas", monospace
```

### Tamaños y Pesos

| Elemento | Tamaño | Peso | Uso |
|----------|--------|------|-----|
| **Título Grande** | 34px | Bold (700) | Títulos de sección |
| **Título** | 20-24px | Semibold (600) | Subtítulos |
| **Body** | 15-16px | Regular (400) | Texto normal |
| **Caption** | 13px | Medium (500) | Etiquetas, descripciones |
| **Small** | 12px | Regular (400) | Texto pequeño |

## 🧩 Componentes Específicos

### Botones Primarios (AnimatedButton)

```css
Background:       #007AFF
Color:            white
Border-radius:    14px
Padding:          14px 28px
Min-height:       48px
Font-size:        16px
Font-weight:      600

/* Estados */
Hover:            #0051D5
Pressed:          #004FC4
Disabled:         #E5E5EA (text: #AEAEB2)

/* Sombra */
Normal:           blur 24px, offset 6px, alpha 35
Hover:            blur 32px, offset 8px, alpha 35
```

### Inputs (QLineEdit)

```css
Background:       white
Border:           1px solid #D1D1D6
Border-radius:    12px
Padding:          12px 16px
Font-size:        15px

/* Focus */
Border-color:     #007AFF
```

### Cards (StatCard)

```css
Background:       rgba(255, 255, 255, 0.92)
Border-radius:    20px
Padding:          24px
Border:           none (efecto flotante)

/* Sombra aplicada vía código Python */
Shadow:           apply_shadow() con defaults
```

### Status Chips

```css
Border-radius:    14px
Padding:          6px 16px
Font-size:        13px
Font-weight:      600
Min-width:        90px
Max-height:       28px

/* Colores según estado */
Success:          #34C759
Warning:          #FF9F0A
Error:            #FF3B30
```

### Navegación Sidebar

```css
/* Items */
Border-radius:    14px
Padding:          14px 18px
Margin:           4px 6px
Font-size:        15px
Font-weight:      500

/* Estados */
Hover:            rgba(0, 0, 0, 0.05)
Selected:         #007AFF (text: white, weight: 600)
```

### Tablas (ModernTable)

```css
Border-radius:    16px (viewport)
Gridline:         #F2F2F7
Selection:        rgba(0, 122, 255, 0.15)
Hover:            rgba(0, 122, 255, 0.12)

/* Headers */
Border-bottom:    1px solid #D1D1D6
Font-weight:      600
Font-size:        13px
```

## 🌓 Modo Oscuro

### Colores Adaptados

| Elemento | Light | Dark |
|----------|-------|------|
| **Background** | `#F5F5F7` | `#000000` |
| **Card** | `rgba(255,255,255,0.92)` | `rgba(28,28,30,0.72)` |
| **Primary Text** | `#1D1D1F` | `#F5F5F7` |
| **Secondary Text** | `#86868B` | `#636366` |
| **Border** | `#D1D1D6` | `#38383A` |
| **Primary Color** | `#007AFF` | `#0A84FF` |

## 📱 Principios de Diseño iOS 26

### 1. Minimalismo
- Reducir elementos visuales innecesarios
- Enfoque en el contenido
- Espaciado generoso

### 2. Claridad
- Jerarquía visual clara
- Contraste adecuado
- Tipografía legible

### 3. Profundidad
- Capas visuales con sombras sutiles
- Efectos de vidrio para separación
- Elevación en interacciones

### 4. Fluidez
- Animaciones suaves y naturales
- Transiciones coherentes
- Feedback visual inmediato

### 5. Consistencia
- Uso coherente de colores
- Espaciado uniforme
- Comportamiento predecible

## 🔍 Ejemplo de Uso

### Crear un Botón iOS 26

**Python (PySide6):**
```python
button = QPushButton("Enviar Factura")
button.setProperty("class", "AnimatedButton")
button.setMinimumHeight(48)
```

**El estilo se aplica automáticamente desde `styles.qss`**

### Crear una Card

**Python:**
```python
card = QFrame()
card.setProperty("class", "StatCard")
apply_shadow(card, blur=24, offset_y=6)
```

## 📊 Métricas de Accesibilidad

- **Contraste mínimo**: 4.5:1 (WCAG AA)
- **Tamaño táctil mínimo**: 44x44px (Apple HIG)
- **Espaciado entre elementos**: Mínimo 8px
- **Legibilidad**: Fuentes no menores a 13px

## 🎯 Checklist de Implementación

- [x] Paleta de colores iOS 26 aplicada
- [x] Border radius aumentados (12-20px)
- [x] Sombras sutiles configuradas
- [x] Padding y spacing optimizados
- [x] Tipografía actualizada
- [x] Animaciones suavizadas
- [x] Componentes de formulario modernizados
- [x] Modo oscuro completo
- [x] Efectos de vidrio implementados
- [x] Accesibilidad considerada

---

**Versión del Sistema de Diseño**: iOS 26
**Última actualización**: Noviembre 2025
**Framework**: PySide6 (Qt for Python)
