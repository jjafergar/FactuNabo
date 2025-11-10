# Checklist de Verificación Visual - iOS 26

## 📋 Guía para validar la modernización

Esta guía te ayudará a verificar visualmente que todos los cambios iOS 26 se han aplicado correctamente cuando ejecutes la aplicación.

---

## 🚀 Antes de Empezar

### Requisitos
- [ ] Python 3.8+ instalado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Pantalla de al menos 1280x720px para ver bien la interfaz

### Ejecutar la aplicación
```bash
python main.py
```

---

## 🎨 Verificación de Colores

### Elementos Azul iOS (#007AFF)
- [ ] Botones primarios son azul iOS (no verde)
- [ ] Items seleccionados en sidebar son azul
- [ ] Progress bars son azul
- [ ] Focus de inputs es azul
- [ ] Checkboxes marcados son azul
- [ ] Links y elementos activos son azul

### Elementos de Estado
- [ ] Success badges son verde (#34C759)
- [ ] Warning badges son naranja (#FF9F0A) - **no** #FF9500
- [ ] Error badges son rojo (#FF3B30)

### Fondos
- [ ] Fondo general es gris muy claro (#F5F5F7) - no debe ser gris oscuro
- [ ] Cards tienen fondo blanco translúcido (vidriado)
- [ ] Sidebar tiene efecto vidrio (se ve ligeramente translúcido)

### Textos
- [ ] Texto principal es negro suave (#1D1D1F) - no negro puro
- [ ] Texto secundario es gris (#86868B)
- [ ] Placeholders son grises claros

---

## 📐 Verificación de Geometría

### Bordes Redondeados
- [ ] Botones tienen esquinas muy redondeadas (~14px)
- [ ] Inputs tienen esquinas redondeadas (~12px)
- [ ] Cards tienen esquinas muy redondeadas (~20px)
- [ ] Pills de navegación están muy redondeadas (~14px)
- [ ] Status chips están redondeadas (~14px)
- [ ] NADA debe tener esquinas cuadradas o poco redondeadas

### Tamaños y Proporciones
- [ ] Botones principales tienen altura de ~48-50px (son táctiles y grandes)
- [ ] Inputs tienen altura cómoda (~44px)
- [ ] Espaciado entre elementos es generoso (no apretado)
- [ ] Cards tienen padding visible (~24px)
- [ ] Status chips tienen buen tamaño (no muy pequeños)

---

## ✨ Verificación de Efectos

### Sombras
- [ ] Cards tienen sombra sutil visible pero no invasiva
- [ ] Botones tienen sombra que aumenta al hacer hover
- [ ] Sombras son SUAVES y difuminadas (no duras)
- [ ] Sidebar NO debe tener sombra dura visible

### Glassmorphism (Efecto Vidrio)
- [ ] Sidebar parece de vidrio translúcido
- [ ] Cards tienen fondo ligeramente translúcido
- [ ] En Windows 11, puede verse efecto Acrylic/Mica (opcional)

### Hover Effects
- [ ] Al pasar mouse sobre botones, la sombra crece suavemente
- [ ] Al pasar mouse sobre items de navegación, se ve fondo sutil
- [ ] Al pasar mouse sobre filas de tabla, se ve highlight azul muy suave
- [ ] Todos los hovers son SUTILES, no bruscos

---

## 🎭 Verificación de Animaciones

### Transiciones
- [ ] Hover en botones es fluido (~200ms)
- [ ] Cambios de sombra son suaves
- [ ] No hay saltos o cambios bruscos
- [ ] Focus en inputs es suave

### Movimientos
- [ ] Navegación entre secciones es fluida
- [ ] Apertura de diálogos es suave
- [ ] Ninguna animación parece "rápida" o "lenta" de forma anormal

---

## 🧭 Verificación de Navegación

### Sidebar
- [ ] Items tienen forma de "píldora" (muy redondeada)
- [ ] Item seleccionado es azul iOS con texto blanco
- [ ] Hover es muy sutil (casi transparente)
- [ ] Espaciado entre items es cómodo
- [ ] Font weight del seleccionado es más bold

### Estructura
- [ ] Sidebar está a la izquierda
- [ ] Ancho de sidebar es cómodo (~250-260px)
- [ ] No hay borde duro entre sidebar y contenido

---

## 📊 Verificación de Componentes

### Botones
- [ ] Botón primario: Azul, texto blanco, muy redondeado, altura buena
- [ ] Hover: Sombra aumenta, color puede oscurecerse ligeramente
- [ ] Pressed: Color se oscurece
- [ ] Disabled: Gris claro, texto gris

### Inputs
- [ ] Borde gris suave (#D1D1D6)
- [ ] Al hacer focus: borde azul iOS (#007AFF)
- [ ] Placeholder es gris claro
- [ ] Padding interno es visible y cómodo
- [ ] Altura es cómoda (~44px)

### Cards/Tarjetas
- [ ] Fondo blanco/translúcido
- [ ] Bordes MUY redondeados (~20px)
- [ ] Sombra sutil pero visible
- [ ] Padding interno generoso
- [ ] Parecen "flotar" sobre el fondo

### Tablas
- [ ] Headers con texto bold
- [ ] Gridlines muy sutiles
- [ ] Selección de fila: fondo azul muy translúcido
- [ ] Hover de fila: fondo azul ultra-sutil
- [ ] Bordes superiores redondeados

### Status Chips
- [ ] Forma de píldora (muy redondeada)
- [ ] Tamaño cómodo (no muy pequeñas)
- [ ] Verde para éxito
- [ ] Naranja (#FF9F0A) para warning
- [ ] Rojo para error
- [ ] Texto blanco y bold

### Progress Bars
- [ ] Barra delgada (~8px altura)
- [ ] Color azul iOS
- [ ] Fondo gris muy claro
- [ ] Bordes redondeados

### Checkboxes
- [ ] Cuadrado con esquinas redondeadas
- [ ] Al marcar: fondo azul iOS
- [ ] Icono de check (✓) visible en blanco
- [ ] Tamaño adecuado (~20x20px)

---

## 🌓 Verificación Modo Oscuro

### Activar Modo Oscuro
(Busca toggle/checkbox de "Modo Oscuro" o similar)

### Colores Oscuros
- [ ] Fondo es negro puro (#000000) - OLED friendly
- [ ] Cards son gris muy oscuro translúcido
- [ ] Texto es blanco suave (#F5F5F7)
- [ ] Primario es azul brillante (#0A84FF) - más brillante que en claro
- [ ] Bordes son grises oscuros pero visibles

### Contraste
- [ ] Todo el texto es legible
- [ ] No hay texto que se pierda en el fondo
- [ ] Botones destacan bien
- [ ] Status chips mantienen buenos colores

---

## ♿ Verificación de Accesibilidad

### Tamaños Táctiles
- [ ] Todos los botones son fácilmente clickeables (≥48x48px)
- [ ] Checkboxes son suficientemente grandes
- [ ] Items de navegación tienen buena área de click

### Contraste
- [ ] Texto principal se lee fácilmente
- [ ] Texto secundario se lee bien (aunque más claro)
- [ ] No hay texto gris sobre gris que sea difícil de leer

### Legibilidad
- [ ] Font size no es demasiado pequeño (≥13px mínimo)
- [ ] Títulos destacan claramente
- [ ] Jerarquía visual es clara

---

## 📱 Verificación General iOS-like

### Look & Feel
- [ ] La interfaz se siente "Apple" / "iOS"
- [ ] Colores son suaves, no estridentes
- [ ] Espaciado es generoso, no apretado
- [ ] Todo es redondeado, nada es cuadrado
- [ ] Sombras son sutiles, no duras
- [ ] Animaciones son fluidas, no bruscas

### Minimalismo
- [ ] La interfaz se siente limpia y ordenada
- [ ] No hay elementos innecesarios
- [ ] Foco en el contenido
- [ ] Espacio en blanco bien usado

### Consistencia
- [ ] Todos los botones primarios usan el mismo azul
- [ ] Todos los bordes redondeados son similares
- [ ] Todas las sombras son sutiles
- [ ] Todo el espaciado es uniforme
- [ ] Todos los efectos hover son sutiles

---

## ⚠️ Problemas Comunes a Buscar

### ❌ Indicadores de que algo NO está bien

#### Colores
- [ ] Si ves verde en botones primarios → MALO (debe ser azul)
- [ ] Si ves naranja #FF9500 → MALO (debe ser #FF9F0A)
- [ ] Si ves negro puro en texto → MALO (debe ser #1D1D1F)
- [ ] Si ves fondo gris oscuro en modo claro → MALO

#### Geometría
- [ ] Si ves esquinas poco redondeadas → MALO
- [ ] Si ves botones pequeños (<44px) → MALO
- [ ] Si ves spacing apretado → MALO

#### Efectos
- [ ] Si ves sombras muy oscuras/duras → MALO
- [ ] Si NO ves sombras en cards → MALO
- [ ] Si no hay efecto vidrio en sidebar → Revisar

#### Animaciones
- [ ] Si las animaciones son muy rápidas → MALO
- [ ] Si hay saltos/brusquedades → MALO
- [ ] Si no hay animación de hover → MALO

---

## ✅ Checklist Rápido (5 minutos)

Para una verificación rápida, confirma estos 10 puntos clave:

1. [ ] **Color primario es azul iOS** (#007AFF, no verde)
2. [ ] **Botones tienen bordes muy redondeados** y altura ≥48px
3. [ ] **Cards tienen sombra sutil** y parecen flotar
4. [ ] **Sidebar tiene efecto vidrio** (translúcido)
5. [ ] **Hover en botones anima la sombra** suavemente
6. [ ] **Navegación usa píldoras azules** al seleccionar
7. [ ] **Status chips usan colores iOS** (verde, naranja #FF9F0A, rojo)
8. [ ] **Inputs tienen focus azul** iOS
9. [ ] **Modo oscuro usa negro puro** (#000000)
10. [ ] **Todo se siente suave y fluido**, estilo Apple

Si los 10 puntos están ✅, ¡la modernización iOS 26 está correcta!

---

## 📸 Capturas Sugeridas

Para documentar los cambios, toma screenshots de:

1. **Dashboard principal** - Vista general
2. **Botón primario en normal** - Color azul
3. **Botón primario en hover** - Sombra aumentada
4. **Sidebar con item seleccionado** - Píldora azul
5. **Formulario con inputs** - Border-radius y padding
6. **Cards de estadísticas** - Sombras y glassmorphism
7. **Tabla con selección** - Highlight azul
8. **Status chips** - Colores iOS
9. **Modo oscuro activado** - Negro puro de fondo
10. **Comparativa lado a lado** - Antes vs Después (si tienes versión anterior)

---

## 🎯 Resultado Esperado

Si todo está correcto, deberías sentir que:
- ✨ La interfaz parece una app de Apple
- 🎨 Los colores son vibrantes pero suaves
- 📐 Todo es redondeado y espacioso
- ☁️ Las sombras son sutiles y elegantes
- 🎭 Las animaciones son fluidas y naturales
- 📱 La app se siente premium y moderna

---

## 🆘 Si algo no se ve bien

1. **Verifica que cargó styles.qss**
   - Revisa que `app.setStyleSheet()` se llamó correctamente

2. **Refresca la aplicación**
   - Cierra y vuelve a abrir
   - A veces Qt cachea estilos

3. **Verifica propiedades**
   - Usa `widget.property("class")` para confirmar
   - Debe retornar "AnimatedButton", "StatCard", etc.

4. **Revisa archivos**
   - `main.py` debe tener `COLOR_PRIMARY = "#007AFF"`
   - `styles.qss` debe tener azul #007AFF en varios lugares

5. **Consulta documentación**
   - `DESIGN_SYSTEM.md` - Specs completas
   - `USAGE_GUIDE.md` - Cómo usar componentes

---

**¡Disfruta la nueva interfaz iOS 26!** 🎉

Si todo se ve bien según este checklist, la modernización fue exitosa.
