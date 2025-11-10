# Ejemplos de Implementación - Bibliotecas Modernas

## 🎨 Opción A: QtAwesome + PySide6-Charts (RECOMENDADO)

### Instalación
```bash
pip install qtawesome
pip install PySide6-Charts
```

---

## 📖 Guía Completa de QtAwesome

### 1. Íconos Básicos en Botones

```python
import qtawesome as qta
from ripple_button import RippleButton

class ModernUI:
    def setup_buttons(self):
        # Botón enviar con ícono de avión
        self.send_btn = RippleButton("Enviar")
        self.send_btn.setIcon(qta.icon('fa5s.paper-plane', color='white'))
        self.send_btn.setProperty("class", "AnimatedButton")
        
        # Botón guardar con ícono de disco
        self.save_btn = RippleButton("Guardar")
        self.save_btn.setIcon(qta.icon('fa5s.save', color='white'))
        
        # Botón eliminar con ícono de basura
        self.delete_btn = RippleButton("Eliminar")
        self.delete_btn.setIcon(qta.icon('fa5s.trash', color='white'))
        
        # Botón imprimir
        self.print_btn = RippleButton("Imprimir")
        self.print_btn.setIcon(qta.icon('fa5s.print', color='white'))
```

### 2. Íconos en Navegación Sidebar

```python
def setup_navigation(self):
    # Dashboard
    nav_item = QListWidgetItem("Dashboard")
    nav_item.setIcon(qta.icon('fa5s.home', color='#1D1D1F'))
    self.nav_list.addItem(nav_item)
    
    # Facturas
    nav_item = QListWidgetItem("Facturas")
    nav_item.setIcon(qta.icon('fa5s.file-invoice', color='#1D1D1F'))
    self.nav_list.addItem(nav_item)
    
    # Histórico
    nav_item = QListWidgetItem("Histórico")
    nav_item.setIcon(qta.icon('fa5s.history', color='#1D1D1F'))
    self.nav_list.addItem(nav_item)
    
    # Configuración
    nav_item = QListWidgetItem("Configuración")
    nav_item.setIcon(qta.icon('fa5s.cog', color='#1D1D1F'))
    self.nav_list.addItem(nav_item)
```

### 3. Íconos Animados (Spinner, Pulse)

```python
def show_loading(self):
    # Spinner animado
    self.loading_label = QLabel("Cargando...")
    spin_icon = qta.icon('fa5s.spinner', 
                         color='#A0BF6E',
                         animation=qta.Spin(self.loading_label))
    self.loading_label.setIcon(spin_icon)
    
def show_notification(self):
    # Ícono con pulse
    alert_icon = qta.icon('fa5s.bell',
                         color='#FF9F0A',
                         animation=qta.Pulse(self.alert_btn))
    self.alert_btn.setIcon(alert_icon)
```

### 4. Íconos en Estado (Success, Warning, Error)

```python
def create_status_chip(self, text, status):
    chip = QLabel(text)
    chip.setProperty("class", "StatusChip")
    chip.setProperty("status", status)
    
    # Añadir ícono según estado
    if status == "success":
        icon = qta.icon('fa5s.check-circle', color='white')
    elif status == "warning":
        icon = qta.icon('fa5s.exclamation-triangle', color='white')
    elif status == "error":
        icon = qta.icon('fa5s.times-circle', color='white')
    
    chip.setPixmap(icon.pixmap(16, 16))
    return chip
```

### 5. Íconos de Archivos y Documentos

```python
def show_file_icons(self):
    # PDF
    pdf_icon = qta.icon('fa5s.file-pdf', color='#FF3B30')
    
    # Excel
    excel_icon = qta.icon('fa5s.file-excel', color='#34C759')
    
    # Word
    word_icon = qta.icon('fa5s.file-word', color='#007AFF')
    
    # Factura
    invoice_icon = qta.icon('fa5s.file-invoice-dollar', color='#A0BF6E')
```

### 6. Tamaños de Íconos

```python
# Pequeño (16x16) - Para texto inline
small_icon = qta.icon('fa5s.info', color='#86868B')
label.setPixmap(small_icon.pixmap(16, 16))

# Mediano (24x24) - Para botones
medium_icon = qta.icon('fa5s.save', color='white')
btn.setIcon(medium_icon)
btn.setIconSize(QSize(24, 24))

# Grande (48x48) - Para placeholders
large_icon = qta.icon('fa5s.cloud-upload', color='#A0BF6E')
label.setPixmap(large_icon.pixmap(48, 48))
```

### 7. Íconos Multi-Color

```python
# Combinar múltiples íconos
stacked_icon = qta.icon('fa5s.square', 'fa5s.check',
                       options=[
                           {'color': '#A0BF6E'},
                           {'scale_factor': 0.6, 'color': 'white'}
                       ])
```

### 8. Lista Completa de Íconos Útiles para FactuNabo

```python
FACTU_NABO_ICONS = {
    # Navegación
    'dashboard': 'fa5s.chart-line',
    'invoices': 'fa5s.file-invoice',
    'history': 'fa5s.history',
    'settings': 'fa5s.cog',
    'help': 'fa5s.question-circle',
    
    # Acciones
    'create': 'fa5s.plus-circle',
    'edit': 'fa5s.edit',
    'delete': 'fa5s.trash',
    'save': 'fa5s.save',
    'cancel': 'fa5s.times',
    'send': 'fa5s.paper-plane',
    'print': 'fa5s.print',
    'download': 'fa5s.download',
    'upload': 'fa5s.upload',
    
    # Estados
    'success': 'fa5s.check-circle',
    'warning': 'fa5s.exclamation-triangle',
    'error': 'fa5s.times-circle',
    'info': 'fa5s.info-circle',
    'pending': 'fa5s.clock',
    
    # Datos
    'user': 'fa5s.user',
    'company': 'fa5s.building',
    'email': 'fa5s.envelope',
    'phone': 'fa5s.phone',
    'location': 'fa5s.map-marker-alt',
    'calendar': 'fa5s.calendar',
    'money': 'fa5s.euro-sign',
    
    # Archivos
    'pdf': 'fa5s.file-pdf',
    'excel': 'fa5s.file-excel',
    'csv': 'fa5s.file-csv',
    'folder': 'fa5s.folder',
    
    # UI
    'search': 'fa5s.search',
    'filter': 'fa5s.filter',
    'sort': 'fa5s.sort',
    'refresh': 'fa5s.sync',
    'menu': 'fa5s.bars',
    'expand': 'fa5s.chevron-down',
    'collapse': 'fa5s.chevron-up',
}

# Uso:
icon = qta.icon(FACTU_NABO_ICONS['send'], color='white')
```

---

## 📊 Guía Completa de PySide6-Charts

### 1. Gráfico de Línea (Facturación Mensual)

```python
from PySide6.QtCharts import (QChart, QChartView, QLineSeries, 
                               QValueAxis, QDateTimeAxis)
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QPainter, QColor

class RevenueChart(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Crear serie de datos
        series = QLineSeries()
        series.setName("Facturación")
        
        # Datos de ejemplo (mes, importe)
        data = [
            (1, 1500), (2, 2300), (3, 1800), (4, 2100),
            (5, 2800), (6, 2400), (7, 3100), (8, 2900),
            (9, 3300), (10, 2700), (11, 3500), (12, 3200)
        ]
        
        for month, revenue in data:
            series.append(month, revenue)
        
        # Estilo de línea
        pen = series.pen()
        pen.setWidth(3)
        pen.setColor(QColor("#A0BF6E"))  # Verde corporativo
        series.setPen(pen)
        
        # Crear gráfico
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Facturación Mensual 2024")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
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
        axis_y.setTitleText("Facturación")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Vista del gráfico
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(chart_view)
```

### 2. Gráfico de Barras (Facturas por Cliente)

```python
from PySide6.QtCharts import QBarSeries, QBarSet, QBarCategoryAxis

class ClientBarChart(QWidget):
    def __init__(self):
        super().__init__()
        
        # Crear conjuntos de datos
        bar_set = QBarSet("Facturas")
        bar_set.append([12, 8, 15, 6, 10])
        bar_set.setColor(QColor("#A0BF6E"))
        
        # Serie de barras
        series = QBarSeries()
        series.append(bar_set)
        
        # Gráfico
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Facturas por Cliente")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        
        # Categorías (clientes)
        categories = ["Cliente A", "Cliente B", "Cliente C", "Cliente D", "Cliente E"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        # Eje Y
        axis_y = QValueAxis()
        axis_y.setRange(0, 20)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Vista
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout = QVBoxLayout(self)
        layout.addWidget(chart_view)
```

### 3. Gráfico Circular (Estado de Facturas)

```python
from PySide6.QtCharts import QPieSeries, QPieSlice

class InvoiceStatusPieChart(QWidget):
    def __init__(self):
        super().__init__()
        
        # Serie de datos
        series = QPieSeries()
        
        # Añadir slices
        paid = series.append("Pagadas", 45)
        pending = series.append("Pendientes", 25)
        overdue = series.append("Vencidas", 10)
        draft = series.append("Borradores", 20)
        
        # Colores corporativos
        paid.setBrush(QColor("#34C759"))      # Verde
        pending.setBrush(QColor("#FF9F0A"))   # Naranja
        overdue.setBrush(QColor("#FF3B30"))   # Rojo
        draft.setBrush(QColor("#86868B"))     # Gris
        
        # Destacar slice más grande
        paid.setLabelVisible(True)
        paid.setExploded(True)
        paid.setExplodeDistanceFactor(0.1)
        
        # Gráfico
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Estado de Facturas")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignRight)
        
        # Vista
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout = QVBoxLayout(self)
        layout.addWidget(chart_view)
```

### 4. Gráfico de Área (Tendencia de Ingresos)

```python
from PySide6.QtCharts import QAreaSeries, QLineSeries

class RevenueTrendChart(QWidget):
    def __init__(self):
        super().__init__()
        
        # Línea superior
        upper = QLineSeries()
        # Línea inferior (baseline)
        lower = QLineSeries()
        
        for i in range(12):
            upper.append(i, 1000 + i * 200 + (i % 3) * 100)
            lower.append(i, 0)
        
        # Serie de área
        series = QAreaSeries(upper, lower)
        series.setName("Ingresos")
        
        # Color corporativo con transparencia
        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, 1))
        gradient.setColorAt(0.0, QColor(160, 191, 110, 180))
        gradient.setColorAt(1.0, QColor(160, 191, 110, 20))
        gradient.setCoordinateMode(QGradient.ObjectBoundingMode)
        series.setBrush(gradient)
        
        # Gráfico
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Tendencia de Ingresos")
        chart.setAnimationOptions(QChart.AllAnimations)
        
        # Ejes
        axis_x = QValueAxis()
        axis_x.setRange(0, 12)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 4000)
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)
        
        # Vista
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        layout = QVBoxLayout(self)
        layout.addWidget(chart_view)
```

### 5. Dashboard Completo con Múltiples Gráficos

```python
class DashboardWithCharts(QWidget):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        
        # Row 1: Cards estadísticas (ya existentes)
        stats_row = QHBoxLayout()
        stats_row.addWidget(self.create_stat_card("Total Facturado", "12,450€"))
        stats_row.addWidget(self.create_stat_card("Facturas Pendientes", "8"))
        stats_row.addWidget(self.create_stat_card("Este Mes", "3,200€"))
        main_layout.addLayout(stats_row)
        
        # Row 2: Gráficos principales
        charts_row = QHBoxLayout()
        
        # Gráfico de línea (66% ancho)
        line_chart_container = QFrame()
        line_chart_container.setProperty("class", "StatCard")
        line_layout = QVBoxLayout(line_chart_container)
        line_layout.addWidget(QLabel("Facturación Mensual"))
        line_layout.addWidget(RevenueChart())
        charts_row.addWidget(line_chart_container, 2)
        
        # Gráfico circular (33% ancho)
        pie_chart_container = QFrame()
        pie_chart_container.setProperty("class", "StatCard")
        pie_layout = QVBoxLayout(pie_chart_container)
        pie_layout.addWidget(QLabel("Estado Facturas"))
        pie_layout.addWidget(InvoiceStatusPieChart())
        charts_row.addWidget(pie_chart_container, 1)
        
        main_layout.addLayout(charts_row)
        
        # Row 3: Gráfico de barras
        bar_chart_container = QFrame()
        bar_chart_container.setProperty("class", "StatCard")
        bar_layout = QVBoxLayout(bar_chart_container)
        bar_layout.addWidget(QLabel("Top 5 Clientes"))
        bar_layout.addWidget(ClientBarChart())
        main_layout.addWidget(bar_chart_container)
```

---

## 🔗 Integración Completa en FactuNabo

```python
# main.py (añadir imports)
import qtawesome as qta
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QPieSeries

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurar UI existente...
        self.setup_navigation_with_icons()
        self.setup_buttons_with_icons()
        
        # Añadir dashboard con gráficos
        self.dashboard_page = self.create_dashboard_with_charts()
    
    def setup_navigation_with_icons(self):
        """Añadir íconos a navegación"""
        nav_items = [
            ("Dashboard", "fa5s.chart-line"),
            ("Facturas", "fa5s.file-invoice"),
            ("Histórico", "fa5s.history"),
            ("Configuración", "fa5s.cog")
        ]
        
        for text, icon_name in nav_items:
            item = QListWidgetItem(text)
            item.setIcon(qta.icon(icon_name, color='#1D1D1F'))
            self.nav_list.addItem(item)
    
    def setup_buttons_with_icons(self):
        """Añadir íconos a botones"""
        # Botón enviar
        if hasattr(self, 'send_btn'):
            self.send_btn.setIcon(qta.icon('fa5s.paper-plane', color='white'))
        
        # Botón guardar
        if hasattr(self, 'save_btn'):
            self.save_btn.setIcon(qta.icon('fa5s.save', color='white'))
    
    def create_dashboard_with_charts(self):
        """Crear dashboard con gráficos"""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        
        # Título
        title = QLabel("Dashboard de Facturación")
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)
        
        # Cards + Gráficos
        layout.addWidget(DashboardWithCharts())
        
        return dashboard
```

---

## 📝 requirements.txt Actualizado

```txt
# Existentes
PySide6==6.10.0
pandas==2.2.3
openpyxl==3.1.5

# Nuevas bibliotecas modernas
qtawesome>=1.2.0
PySide6-Charts>=6.10.0
```

---

## 🎯 Resultado Final

Con estas bibliotecas obtendrás:

1. ✅ **Íconos vectoriales HD** en todos los botones y navegación
2. ✅ **Gráficos profesionales** en dashboard
3. ✅ **Animaciones** en íconos (spinner, pulse)
4. ✅ **Verde corporativo** mantenido en todo
5. ✅ **Sin refactoring** del código existente
6. ✅ **Tamaño pequeño** (~5MB adicional)

¿Quieres que implemente estos cambios en el código?
