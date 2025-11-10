# FactuNabo

Programa moderno para emitir y gestionar facturas con interfaz estilo **iOS 26** (Apple Design).

## ✨ Características iOS 26

La aplicación implementa los principios de diseño más recientes de iOS 26:

### 🎨 Diseño Visual
- **Minimalismo extremo**: Interfaz limpia sin elementos innecesarios
- **Colores suaves**: Paleta de colores pasteles oficial de iOS 26
  - Azul primario: `#007AFF` (iOS Blue)
  - Verde: `#34C759` (Success)
  - Naranja: `#FF9F0A` (Warning actualizado a iOS 26)
  - Rojo: `#FF3B30` (Error)
- **Esquinas ultra-redondeadas**: Bordes de 14-20px para mayor suavidad
- **Efecto vidrio**: Backgrounds translúcidos con blur (glassmorphism)
- **Sombras sutiles**: Sombras con alpha muy bajo (25-35) para profundidad sutil

### 🔤 Tipografía
- Fuente similar a **SF Pro Display/Text** de Apple
- Tamaños optimizados para legibilidad
- Pesos de fuente variados (500-600) para jerarquía visual

### 📐 Espaciado
- Padding generoso en componentes (14-24px)
- Márgenes amplios entre elementos
- Altura de botones de 48-50px (guías de accesibilidad Apple)

### 🎭 Animaciones
- Transiciones suaves de 200ms
- Easing curves de tipo `OutCubic`
- Efectos de elevación en hover (sombras animadas)
- Animaciones fluidas en navegación

### 🌓 Modo Oscuro
- Soporte completo para tema oscuro
- Negro puro `#000000` de fondo (OLED friendly)
- Contraste optimizado para visión nocturna

## 🚀 Funcionalidades

- 📄 **Gestión de facturas**: Crear, visualizar y gestionar facturas
- 📊 **Dashboard**: Métricas y estadísticas en tiempo real
- 📜 **Histórico**: Registro completo de envíos
- 🔐 **Login seguro**: Sistema de autenticación
- 💾 **Persistencia**: Base de datos SQLite
- 📁 **Importación**: Soporte para archivos Excel (.xlsm)

## 📋 Requisitos

- Python 3.8 o superior
- Windows 10/11 (para efectos Acrylic/Mica opcionales)

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/jjafergar/FactuNabo.git
cd FactuNabo
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 💻 Uso

Ejecuta la aplicación:

```bash
python main.py
```

## 🎨 Paleta de Colores iOS 26

| Color | Hex | Uso |
|-------|-----|-----|
| Azul iOS | `#007AFF` | Botones primarios, elementos seleccionados |
| Verde | `#34C759` | Éxito, confirmaciones |
| Naranja | `#FF9F0A` | Advertencias |
| Rojo | `#FF3B30` | Errores, acciones destructivas |
| Fondo claro | `#F5F5F7` | Background principal |
| Texto primario | `#1D1D1F` | Texto principal |
| Texto secundario | `#86868B` | Texto de apoyo |

## 📁 Estructura

```
FactuNabo/
├── main.py                 # Aplicación principal con UI iOS 26
├── styles.qss             # Estilos CSS modernos
├── worker.py              # Procesamiento asíncrono
├── macro_adapter.py       # Adaptador para Excel
├── login_dialog.py        # Diálogo de login
├── modern_dialogs.py      # Diálogos modernos
├── pdf_downloader.py      # Descarga de PDFs
├── requirements.txt       # Dependencias
├── resources/             # Recursos (iconos, logos)
└── Plantillas Facturas/   # Plantillas de facturas
```

## 🛠️ Tecnologías

- **PySide6**: Framework Qt para interfaces modernas
- **SQLite**: Base de datos embebida
- **Pandas**: Procesamiento de datos
- **OpenPyXL**: Manejo de archivos Excel

## 📝 Licencia

Proyecto de código abierto.
