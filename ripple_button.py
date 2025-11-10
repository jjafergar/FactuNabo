"""
RippleButton - Button with Material Design ripple effect
Enhanced version of AnimatedButton with ripple effect
"""

from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer, QPointF
from PySide6.QtGui import QPainter, QColor, QPainterPath, QMouseEvent
import math


class RippleButton(QPushButton):
    """
    Enhanced button with ripple effect and shadow animations
    Combina el AnimatedButton existente con ripple effect
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setProperty("class", "AnimatedButton")
        
        # Ripple state
        self.ripples = []
        self.ripple_color = QColor(255, 255, 255, 80)  # White ripple on green
        
        # Shadow animation (existing AnimatedButton logic)
        self._shadow = QGraphicsDropShadowEffect(self)
        self._shadow.setBlurRadius(24)
        color = QColor(0, 0, 0, 35)
        self._shadow.setColor(color)
        self._shadow.setOffset(0, 6)
        self.setGraphicsEffect(self._shadow)
        
        # Animaciones de sombra
        self._anim_blur = QPropertyAnimation(self._shadow, b"blurRadius")
        self._anim_blur.setDuration(200)
        self._anim_blur.setEasingCurve(QEasingCurve.OutCubic)
        
        self._anim_offset = QPropertyAnimation(self._shadow, b"yOffset")
        self._anim_offset.setDuration(200)
        self._anim_offset.setEasingCurve(QEasingCurve.OutCubic)
        
        # Timer for ripple animation
        self.ripple_timer = QTimer(self)
        self.ripple_timer.timeout.connect(self._animate_ripples)
        self.ripple_timer.setInterval(16)  # ~60 FPS
    
    def _animate_hover_in(self):
        """Shadow hover animation"""
        self._anim_blur.stop()
        self._anim_blur.setStartValue(self._shadow.blurRadius())
        self._anim_blur.setEndValue(32)
        self._anim_blur.start()
        
        self._anim_offset.stop()
        self._anim_offset.setStartValue(self._shadow.yOffset())
        self._anim_offset.setEndValue(8)
        self._anim_offset.start()
    
    def _animate_hover_out(self):
        """Shadow normal animation"""
        self._anim_blur.stop()
        self._anim_blur.setStartValue(self._shadow.blurRadius())
        self._anim_blur.setEndValue(24)
        self._anim_blur.start()
        
        self._anim_offset.stop()
        self._anim_offset.setStartValue(self._shadow.yOffset())
        self._anim_offset.setEndValue(6)
        self._anim_offset.start()
    
    def enterEvent(self, event):
        """Mouse enter - expand shadow"""
        self._animate_hover_in()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Mouse leave - restore shadow"""
        self._animate_hover_out()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Mouse press - create ripple and contract shadow"""
        if event.button() == Qt.LeftButton:
            # Start ripple effect
            self._start_ripple(event.position())
            
            # Contract shadow (existing AnimatedButton logic)
            self._anim_blur.stop()
            self._anim_blur.setStartValue(self._shadow.blurRadius())
            self._anim_blur.setEndValue(10)
            self._anim_blur.start()
            
            self._anim_offset.stop()
            self._anim_offset.setStartValue(self._shadow.yOffset())
            self._anim_offset.setEndValue(2)
            self._anim_offset.start()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Mouse release - restore hover state"""
        if event.button() == Qt.LeftButton:
            # Restore hover shadow
            self._animate_hover_in()
        
        super().mouseReleaseEvent(event)
    
    def _start_ripple(self, pos):
        """Start a new ripple animation"""
        # Calculate max radius to cover entire button
        max_radius = self._calculate_max_radius(pos)
        
        ripple = {
            'center': pos,
            'radius': 0.0,
            'max_radius': max_radius,
            'opacity': 1.0,
            'speed': max_radius / 25.0  # Complete in ~400ms at 60fps
        }
        
        self.ripples.append(ripple)
        
        if not self.ripple_timer.isActive():
            self.ripple_timer.start()
    
    def _calculate_max_radius(self, pos):
        """Calculate maximum radius to cover button from click point"""
        corners = [
            QPointF(0, 0),
            QPointF(self.width(), 0),
            QPointF(0, self.height()),
            QPointF(self.width(), self.height())
        ]
        
        max_dist = 0.0
        for corner in corners:
            dx = corner.x() - pos.x()
            dy = corner.y() - pos.y()
            dist = math.sqrt(dx * dx + dy * dy)
            max_dist = max(max_dist, dist)
        
        return max_dist
    
    def _animate_ripples(self):
        """Animate all active ripples"""
        if not self.ripples:
            self.ripple_timer.stop()
            return
        
        ripples_to_remove = []
        
        for ripple in self.ripples:
            # Expand radius
            ripple['radius'] += ripple['speed']
            
            # Fade out opacity
            progress = ripple['radius'] / ripple['max_radius']
            ripple['opacity'] = max(0.0, 1.0 - progress)
            
            # Mark for removal if complete
            if ripple['radius'] >= ripple['max_radius']:
                ripples_to_remove.append(ripple)
        
        # Remove completed ripples
        for ripple in ripples_to_remove:
            self.ripples.remove(ripple)
        
        # Trigger repaint
        self.update()
    
    def paintEvent(self, event):
        """Paint button with ripple effects"""
        # First paint normal button
        super().paintEvent(event)
        
        # Then paint ripples on top
        if self.ripples:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Create clipping path with button's border radius
            path = QPainterPath()
            path.addRoundedRect(0, 0, self.width(), self.height(), 12, 12)
            painter.setClipPath(path)
            
            # Paint each ripple
            for ripple in self.ripples:
                color = QColor(self.ripple_color)
                color.setAlphaF(ripple['opacity'])
                
                painter.setBrush(color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(
                    ripple['center'],
                    ripple['radius'],
                    ripple['radius']
                )
            
            painter.end()
