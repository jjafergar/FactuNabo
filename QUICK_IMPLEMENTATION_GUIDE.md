# Guía Rápida de Implementación - Bibliotecas Modernas

## 🚀 Implementación en 3 Pasos

### Paso 1: Instalar Bibliotecas (5 minutos)

```bash
# Opción A (Recomendada): Solo QtAwesome + Charts
pip install qtawesome
pip install PySide6-Charts

# O usar archivo de requirements
pip install -r requirements_modern.txt
```

---

### Paso 2: Actualizar main.py (15 minutos)

#### 2.1 Añadir Imports

```python
# Al inicio de main.py, después de los imports existentes
import qtawesome as qta
from PySide6.QtCharts import (QChart, QChartView, QLineSeries, QPieSeries, 
                               QPieSlice, QValueAxis)
```

#### 2.2 Modificar setup_navigation() - Añadir Íconos

```python
# Buscar la función donde se crea la navegación
# Añadir íconos a cada item

def create_navigation_item(self, text, icon_name):
    """Helper para crear items de navegación con íconos"""
    item = QListWidgetItem(text)
    item.setIcon(qta.icon(icon_name, color='#1D1D1F'))
    return item

# Usar en la navegación:
self.nav_list.addItem(self.create_navigation_item("Dashboard", "fa5s.chart-line"))
self.nav_list.addItem(self.create_navigation_item("Facturas", "fa5s.file-invoice"))
self.nav_list.addItem(self.create_navigation_item("Histórico", "fa5s.history"))
self.nav_list.addItem(self.create_navigation_item("Configuración", "fa5s.cog"))
```

#### 2.3 Modificar Botones - Añadir Íconos

```python
# Buscar donde se crean los botones AnimatedButton o RippleButton
# Añadir íconos:

# Botón enviar
self.send_btn = RippleButton("Enviar Factura")
self.send_btn.setIcon(qta.icon('fa5s.paper-plane', color='white'))
self.send_btn.setIconSize(QSize(20, 20))

# Botón guardar
self.save_btn = RippleButton("Guardar")
self.save_btn.setIcon(qta.icon('fa5s.save', color='white'))
self.save_btn.setIconSize(QSize(20, 20))

# Botón eliminar
self.delete_btn = RippleButton("Eliminar")
self.delete_btn.setIcon(qta.icon('fa5s.trash', color='white'))
self.delete_btn.setIconSize(QSize(20, 20))

# Botón imprimir
self.print_btn = RippleButton("Imprimir")
self.print_btn.setIcon(qta.icon('fa5s.print', color='white'))
self.print_btn.setIconSize(QSize(20, 20))
```

#### 2.4 Añadir Gráfico al Dashboard

```python
def create_revenue_chart(self):
    """Crear gráfico de facturación mensual"""
    # Serie de datos
    series = QLineSeries()
    series.setName("Facturación")
    
    # Datos de ejemplo - REEMPLAZAR con datos reales de BD
    monthly_revenue = [
        (1, 1500), (2, 2300), (3, 1800), (4, 2100),
        (5, 2800), (6, 2400), (7, 3100), (8, 2900),
        (9, 3300), (10, 2700), (11, 3500), (12, 3200)
    ]
    
    for month, revenue in monthly_revenue:
        series.append(month, revenue)
    
    # Estilo de línea (verde corporativo)
    pen = series.pen()
    pen.setWidth(3)
    pen.setColor(QColor("#A0BF6E"))
    series.setPen(pen)
    
    # Crear gráfico
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Facturación Mensual 2024")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().hide()
    
    # Eje X (Meses)
    axis_x = QValueAxis()
    axis_x.setRange(1, 12)
    axis_x.setLabelFormat("%d")
    axis_x.setTitleText("Mes")
    chart.addAxis(axis_x, Qt.AlignBottom)
    series.attachAxis(axis_x)
    
    # Eje Y (Euros)
    axis_y = QValueAxis()
    axis_y.setRange(0, 4000)
    axis_y.setLabelFormat("%.0f€")
    axis_y.setTitleText("Importe")
    chart.addAxis(axis_y, Qt.AlignLeft)
    series.attachAxis(axis_y)
    
    # Vista del gráfico
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.setMinimumHeight(300)
    
    return chart_view

# Añadir al dashboard (buscar donde se crea el dashboard)
def create_dashboard_page(self):
    # ... código existente ...
    
    # Añadir gráfico después de las cards
    chart_container = QFrame()
    chart_container.setProperty("class", "StatCard")
    chart_layout = QVBoxLayout(chart_container)
    
    chart_title = QLabel("Facturación Mensual")
    chart_title.setStyleSheet("font-size: 18px; font-weight: 600; margin-bottom: 10px;")
    chart_layout.addWidget(chart_title)
    
    chart_layout.addWidget(self.create_revenue_chart())
    
    # Añadir al layout principal
    main_layout.addWidget(chart_container)
```

#### 2.5 Añadir Gráfico Circular de Estado

```python
def create_status_pie_chart(self):
    """Crear gráfico circular de estado de facturas"""
    # Obtener datos reales de BD
    # EJEMPLO - reemplazar con query real
    status_data = {
        'Pagadas': 45,
        'Pendientes': 25,
        'Vencidas': 10,
        'Borradores': 20
    }
    
    # Serie
    series = QPieSeries()
    
    # Añadir slices con colores corporativos
    paid = series.append("Pagadas", status_data['Pagadas'])
    paid.setBrush(QColor("#34C759"))  # Verde success
    
    pending = series.append("Pendientes", status_data['Pendientes'])
    pending.setBrush(QColor("#FF9F0A"))  # Naranja warning
    
    overdue = series.append("Vencidas", status_data['Vencidas'])
    overdue.setBrush(QColor("#FF3B30"))  # Rojo error
    
    draft = series.append("Borradores", status_data['Borradores'])
    draft.setBrush(QColor("#86868B"))  # Gris
    
    # Destacar slice más grande
    paid.setLabelVisible(True)
    paid.setExploded(True)
    paid.setExplodeDistanceFactor(0.05)
    
    # Gráfico
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle("Estado de Facturas")
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().setAlignment(Qt.AlignRight)
    
    # Vista
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.setMinimumHeight(250)
    
    return chart_view
```

---

### Paso 3: Probar la Aplicación (5 minutos)

```bash
# Ejecutar la aplicación
python main.py
```

**Verificar:**
- ✅ Íconos en navegación
- ✅ Íconos en botones
- ✅ Gráfico de línea en dashboard
- ✅ Gráfico circular de estados
- ✅ Todo en verde corporativo #A0BF6E

---

## 📋 Checklist de Implementación

### Fase 1: Instalación
- [ ] Instalar qtawesome
- [ ] Instalar PySide6-Charts
- [ ] Verificar imports funcionan

### Fase 2: Íconos
- [ ] Añadir íconos a navegación (4 items)
- [ ] Añadir íconos a botones principales (4-6 botones)
- [ ] Verificar color #1D1D1F en navegación
- [ ] Verificar color white en botones

### Fase 3: Gráficos
- [ ] Implementar create_revenue_chart()
- [ ] Implementar create_status_pie_chart()
- [ ] Añadir gráficos al dashboard
- [ ] Verificar animaciones funcionan
- [ ] Verificar color verde #A0BF6E en gráficos

### Fase 4: Integración de Datos Reales
- [ ] Conectar gráfico de línea con BD (facturación mensual)
- [ ] Conectar gráfico circular con BD (estado facturas)
- [ ] Añadir refresh automático

### Fase 5: Testing
- [ ] Probar en modo claro
- [ ] Probar en modo oscuro
- [ ] Verificar performance (60 FPS)
- [ ] Probar en diferentes resoluciones

---

## 🔧 Troubleshooting

### Error: "No module named 'qtawesome'"
```bash
pip install qtawesome
```

### Error: "No module named 'PySide6.QtCharts'"
```bash
pip install PySide6-Charts
```

### Íconos no se ven
```python
# Verificar el tamaño del ícono
btn.setIconSize(QSize(20, 20))

# Verificar el color (debe contrastar con fondo)
icon = qta.icon('fa5s.home', color='white')  # Para fondo oscuro
icon = qta.icon('fa5s.home', color='#1D1D1F')  # Para fondo claro
```

### Gráficos no se animan
```python
# Asegurarse de que las animaciones están habilitadas
chart.setAnimationOptions(QChart.SeriesAnimations)
# O para todas las animaciones:
chart.setAnimationOptions(QChart.AllAnimations)
```

---

## 💡 Consejos

### 1. Mantener Consistencia de Íconos
```python
# Crear diccionario de íconos al inicio de la clase
ICONS = {
    'send': 'fa5s.paper-plane',
    'save': 'fa5s.save',
    'delete': 'fa5s.trash',
    'print': 'fa5s.print',
    'edit': 'fa5s.edit',
}

# Usar en todo el código
btn.setIcon(qta.icon(ICONS['send'], color='white'))
```

### 2. Reutilizar Creación de Gráficos
```python
def create_line_chart(self, title, data, color='#A0BF6E'):
    """Helper genérico para gráficos de línea"""
    series = QLineSeries()
    for x, y in data:
        series.append(x, y)
    
    pen = series.pen()
    pen.setWidth(3)
    pen.setColor(QColor(color))
    series.setPen(pen)
    
    chart = QChart()
    chart.addSeries(series)
    chart.setTitle(title)
    chart.setAnimationOptions(QChart.SeriesAnimations)
    
    return chart
```

### 3. Conectar con Datos Reales
```python
def load_monthly_revenue_from_db(self):
    """Cargar datos reales de facturación"""
    # Query a la base de datos
    query = """
        SELECT MONTH(fecha) as mes, SUM(total) as total
        FROM facturas
        WHERE YEAR(fecha) = 2024
        GROUP BY MONTH(fecha)
        ORDER BY mes
    """
    
    # Ejecutar query y retornar datos
    conn = sqlite3.connect(self.db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return [(row['mes'], row['total']) for _, row in df.iterrows()]

# Usar en create_revenue_chart:
data = self.load_monthly_revenue_from_db()
for month, revenue in data:
    series.append(month, revenue)
```

---

## 📊 Resultado Esperado

Después de la implementación tendrás:

1. **Navegación moderna**
   - Íconos vectoriales HD
   - Color corporativo #1D1D1F
   - Mejor UX visual

2. **Botones profesionales**
   - Íconos blancos sobre verde #A0BF6E
   - Tamaño 20x20px
   - Ripple effect mantenido

3. **Dashboard con datos**
   - Gráfico de línea (facturación mensual)
   - Gráfico circular (estado facturas)
   - Animaciones suaves
   - Verde corporativo en visualizaciones

4. **Sin cambios estructurales**
   - Código existente intacto
   - Animaciones actuales funcionando
   - Modo oscuro compatible

---

## ⏱️ Tiempo Estimado Total

- **Instalación**: 5 minutos
- **Íconos navegación**: 5 minutos
- **Íconos botones**: 5 minutos
- **Gráfico de línea**: 15 minutos
- **Gráfico circular**: 10 minutos
- **Integración datos reales**: 15 minutos
- **Testing**: 5 minutos

**TOTAL: ~1 hora** para implementación básica

---

¿Listo para comenzar la implementación?
