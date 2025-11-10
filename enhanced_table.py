"""
Enhanced Table Widget with Animated Effects
Custom QTableWidget with slide-in highlight bar on hover
"""

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QStyledItemDelegate
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from PySide6.QtGui import QPainter, QColor, QLinearGradient, QPen


class AnimatedTableDelegate(QStyledItemDelegate):
    """
    Custom delegate for animated table row hover effects
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hover_row = -1
        self.hover_progress = 0.0
        
    def paint(self, painter, option, index):
        """Custom paint with animated highlight"""
        # Paint default item first
        super().paint(painter, option, index)
        
        # Add animated highlight if this is the hover row
        if index.row() == self.hover_row and self.hover_progress > 0:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Calculate slide-in position
            rect = option.rect
            bar_width = int(rect.width() * self.hover_progress)
            
            # Draw gradient highlight bar from left
            gradient = QLinearGradient(rect.left(), rect.top(), rect.left() + bar_width, rect.top())
            gradient.setColorAt(0, QColor(160, 191, 110, 40))  # Corporate green
            gradient.setColorAt(1, QColor(160, 191, 110, 10))
            
            highlight_rect = QRect(rect.left(), rect.top(), bar_width, rect.height())
            painter.fillRect(highlight_rect, gradient)
            
            painter.restore()
    
    def set_hover_row(self, row, animate=True):
        """Set the currently hovered row"""
        if row == self.hover_row:
            return
        
        self.hover_row = row
        
        if animate and row >= 0:
            # Animate progress from 0 to 1
            self._animate_in()
        else:
            self.hover_progress = 0.0
    
    def _animate_in(self):
        """Animate highlight bar sliding in"""
        # Use a timer to animate (since QStyledItemDelegate isn't a QObject with properties)
        # We'll manually update progress
        self.hover_progress = 0.0
        
        def update_progress():
            self.hover_progress += 0.05
            if self.hover_progress >= 1.0:
                self.hover_progress = 1.0
                timer.stop()
            
            # Trigger repaint
            if hasattr(self.parent(), 'viewport'):
                self.parent().viewport().update()
        
        timer = QTimer()
        timer.timeout.connect(update_progress)
        timer.start(16)  # ~60 FPS
        
        # Keep reference to prevent garbage collection
        self._hover_timer = timer


class EnhancedTable(QTableWidget):
    """
    Enhanced table widget with animated hover effects
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set custom delegate for animations
        self.animated_delegate = AnimatedTableDelegate(self)
        self.setItemDelegate(self.animated_delegate)
        
        # Enable mouse tracking for hover
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        
        # Track hover state
        self.current_hover_row = -1
    
    def mouseMoveEvent(self, event):
        """Track mouse movement for hover effect"""
        # Get row at mouse position
        item = self.itemAt(event.position().toPoint())
        if item:
            row = item.row()
            if row != self.current_hover_row:
                self.current_hover_row = row
                self.animated_delegate.set_hover_row(row, animate=True)
        
        super().mouseMoveEvent(event)
    
    def leaveEvent(self, event):
        """Reset hover when mouse leaves"""
        self.current_hover_row = -1
        self.animated_delegate.set_hover_row(-1, animate=False)
        super().leaveEvent(event)


class PulsingProgressBar:
    """
    Add pulsing shimmer effect to progress bars
    """
    
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar
        self.shimmer_pos = 0.0
        self.running = False
        
    def start_shimmer(self):
        """Start shimmer animation"""
        if self.running:
            return
        
        self.running = True
        self.timer = QTimer()
        self.timer.timeout.connect(self._animate_shimmer)
        self.timer.start(30)  # ~33 FPS
    
    def stop_shimmer(self):
        """Stop shimmer animation"""
        self.running = False
        if hasattr(self, 'timer'):
            self.timer.stop()
    
    def _animate_shimmer(self):
        """Animate shimmer overlay"""
        self.shimmer_pos += 0.02
        if self.shimmer_pos > 1.3:
            self.shimmer_pos = -0.3
        
        # Update progress bar style with gradient
        # This is a simplified approach - full implementation would use custom painting
        value = self.progress_bar.value()
        if value > 0 and value < 100:
            self.progress_bar.update()


class SmootherProgressBar:
    """
    Enhanced progress bar with smooth value transitions
    """
    
    def __init__(self, progress_bar):
        self.progress_bar = progress_bar
        self.target_value = 0
        self.current_anim = None
    
    def set_value_animated(self, value, duration=300):
        """Set progress value with smooth animation"""
        # Stop any existing animation
        if self.current_anim and self.current_anim.state() == QPropertyAnimation.Running:
            self.current_anim.stop()
        
        # Create new animation
        self.current_anim = QPropertyAnimation(self.progress_bar, b"value")
        self.current_anim.setDuration(duration)
        self.current_anim.setStartValue(self.progress_bar.value())
        self.current_anim.setEndValue(value)
        self.current_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.current_anim.start()
    
    def increment_animated(self, amount, duration=200):
        """Increment progress smoothly"""
        new_value = min(100, self.progress_bar.value() + amount)
        self.set_value_animated(new_value, duration)


class TableRowHighlight:
    """
    Alternative table row highlight with fade effect
    """
    
    def __init__(self, table):
        self.table = table
        self.table.setMouseTracking(True)
        self.table.viewport().setMouseTracking(True)
        
        self.current_row = -1
        self.highlight_opacity = 0.0
        
        # Connect events
        self.table.entered.connect(self._on_cell_entered)
    
    def _on_cell_entered(self, index):
        """Handle cell entered event"""
        if index.row() != self.current_row:
            self.current_row = index.row()
            self._animate_highlight_in()
    
    def _animate_highlight_in(self):
        """Fade in row highlight"""
        # This would require custom painting or stylesheet manipulation
        # Simplified version using stylesheet
        self.table.selectRow(self.current_row)
